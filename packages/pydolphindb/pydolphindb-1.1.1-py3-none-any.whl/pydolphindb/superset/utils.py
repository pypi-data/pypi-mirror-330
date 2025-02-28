import pandas as pd
import dolphindb.settings as keys
import numpy as np
import sqlparse


def mutator_temporary_pandas(data: pd.Timestamp, elem_type: int):
    if data is None:
        return None
    if elem_type in [keys.DT_NANOTIME, keys.DT_NANOTIMESTAMP]:
        return data
    if elem_type in [keys.DT_TIME, keys.DT_MINUTE, keys.DT_SECOND]:
        return data.to_pydatetime()
    return data.to_pydatetime()


def mutator_temporary_numpy(data: np.datetime64, elem_type: int):
    if data is None:
        return None
    if data.dtype == np.dtype("datetime64[ns]"):
        return pd.Timestamp(data)
    if elem_type in [keys.DT_TIME, keys.DT_MINUTE, keys.DT_SECOND]:
        return data.tolist()
    return data.tolist()


def mutator_array(data: list, elem_type: int):
    if keys.getCategory(elem_type) != keys.DATA_CATEGORY.TEMPORAL:
        return data
    return [mutator_temporary_numpy(x, elem_type) for x in data]


def _extract_select_columns(sql_parsed):
    select_token = None
    select_seen = False
    p_id = -1

    for id, token in enumerate(sql_parsed.tokens):
        if select_seen:
            if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == "FROM":
                break
            if not token.ttype:
                p_id = id
                select_token = token
        elif token.ttype is sqlparse.tokens.DML and token.value.upper() == "SELECT":
            select_seen = True

    return p_id, select_token


def _extract_groupby_columns(sql_parsed):
    groupby_token = None
    groupby_seen = False
    p_id = -1

    for id, token in enumerate(sql_parsed.tokens):
        if groupby_seen:
            if p_id != -1:
                break
            if not token.ttype:
                p_id = id
                groupby_token = token
        elif token.ttype is sqlparse.tokens.Keyword and token.value.upper() == "GROUP BY":
            groupby_seen = True

    return p_id, groupby_token


def _extract_alias(token: sqlparse.sql.Identifier):
    kw_idx, kw = token.token_next_by(m=(sqlparse.tokens.Keyword, 'AS'))
    if kw is not None:
        v = token._get_first_name(kw_idx + 1, keywords=True)
        if v != "_":
            return v
        v = token._get_first_name(kw_idx + 3, keywords=True)
        return f'_"{v}"'

    _, ws = token.token_next_by(t=sqlparse.tokens.Whitespace)
    if len(token.tokens) > 2 and ws is not None:
        return token._get_first_name(reverse=True)


def _check_equal(a, b):
    # a(b) as c  //  a(b)
    if not isinstance(a, sqlparse.sql.Identifier):
        return False
    if not isinstance(b, sqlparse.sql.Function):
        return False
    if str(a.tokens[0]) == str(b):
        return True
    return False


def reformat_sql(sql_parsed: sqlparse.sql.Statement):
    select_id, select_token = _extract_select_columns(sql_parsed)

    if select_id == -1:
        return str(sql_parsed)

    groupby_id, groupby_token = _extract_groupby_columns(sql_parsed)

    if groupby_id == -1:
        return str(sql_parsed)

    if isinstance(select_token, sqlparse.sql.Identifier):
        if isinstance(groupby_token, sqlparse.sql.Function):
            # SELECT a(b) as c GROUP BY a(b)
            if _check_equal(select_token, groupby_token):
                alias = _extract_alias(select_token)
                sql_parsed.tokens[groupby_id] = select_token
                sql_parsed.tokens[select_id] = sqlparse.sql.Token(None, alias)
        elif isinstance(groupby_token, sqlparse.sql.IdentifierList):
            # SELECT a(b) as c GROUP BY a(b), d
            for id, token in enumerate(groupby_token):
                if isinstance(token, sqlparse.sql.Function):
                    if _check_equal(select_token, token):
                        alias = _extract_alias(select_token)
                        groupby_token.tokens[id] = select_token
                        sql_parsed.tokens[select_id] = sqlparse.sql.Token(None, alias)
    elif isinstance(select_token, sqlparse.sql.IdentifierList):
        for id_select, token in enumerate(select_token):
            if token.ttype:
                continue
            if isinstance(groupby_token, sqlparse.sql.Function):
                # SELECT a(b) as c, d GROUP BY a(b)
                if _check_equal(token, groupby_token):
                    alias = _extract_alias(token)
                    sql_parsed.tokens[groupby_id] = token
                    select_token.tokens[id_select] = sqlparse.sql.Token(None, alias)
            elif isinstance(groupby_token, sqlparse.sql.IdentifierList):
                # SELECT a(b) as c, d GROUP BY a(b), e
                for id_group, token_group in enumerate(groupby_token):
                    if isinstance(token_group, sqlparse.sql.Function):
                        if _check_equal(token, token_group):
                            alias = _extract_alias(token)
                            groupby_token.tokens[id_group] = token
                            select_token.tokens[id_select] = sqlparse.sql.Token(None, alias)

    return str(sql_parsed)