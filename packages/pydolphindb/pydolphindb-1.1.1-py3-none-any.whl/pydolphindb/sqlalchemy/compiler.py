import re
from sqlalchemy.sql import compiler
from sqlalchemy import exc
from sqlalchemy import sql
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy import Column
from sqlalchemy.sql import operators
from sqlalchemy.sql import elements, functions

from . import types as ddbtypes
from ..helper import logger

DEFAULT_SCHEMA = "__shared_table"

BIND_PARAMS = re.compile(r"(?<![:\w\$\x5c]):([\w\$]+)(?![:\w\$])", re.UNICODE)
BIND_PARAMS_ESC = re.compile(r"\x5c(:[\w\$]*)(?![:\w\$])", re.UNICODE)


RE_DATETIME_PATTERN = r"'(?P<Y>\d{4})-(?P<M>\d{2})-(?P<D>\d{2}) (?P<H>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}).(?P<ms>\d{6})'"


def _datetime_replace(matched):
    matched_dict = matched.groupdict()
    Y_ = matched_dict["Y"]
    M_ = matched_dict["M"]
    D_ = matched_dict["D"]
    H_ = matched_dict["H"]
    m_ = matched_dict["m"]
    s_ = matched_dict["s"]
    ms_ = matched_dict["ms"]
    return "{}.{}.{}T{}:{}:{}.{}".format(Y_, M_, D_, H_, m_, s_, ms_)


RE_JOIN_AS = r"as (?P<name>\w*)__"


def _join_as_replace(matched):
    matched_dict = matched.groupdict()
    name_ = matched_dict["name"]
    if name_ == "mme_inner":
        return "as {}__".format(name_)
    else:
        return "as {}".format(name_)


RE_JOIN_ON = r"(?P<name1>\w*) = (?P<name2>\w*)__"


def _join_on_replace(matched):
    matched_dict = matched.groupdict()
    name1_ = matched_dict["name1"]
    name2_ = matched_dict["name2"]
    if name1_ == name2_:
        return "{}".format(name1_)
    else:
        return "{} = {}__".format(name1_, name2_)


OPERATORS = {
    # binary
    operators.and_: " && ",  # sqlparse will detect "and"/"AND" and add '\n' to sql string    refine link:sqlparse.__init__.format -> ReindentFilter._next_token
    operators.or_: " || ",
    operators.add: " + ",
    operators.mul: " * ",
    operators.sub: " - ",
    operators.div: " / ",
    operators.mod: " % ",
    operators.truediv: " / ",
    operators.neg: "-",
    operators.lt: " < ",
    operators.le: " <= ",
    operators.ne: " != ",
    operators.gt: " > ",
    operators.ge: " >= ",
    operators.eq: " = ",
    operators.is_distinct_from: " IS DISTINCT FROM ",
    operators.isnot_distinct_from: " IS NOT DISTINCT FROM ",
    operators.concat_op: " || ",
    operators.match_op: " MATCH ",
    operators.notmatch_op: " NOT MATCH ",
    operators.in_op: " in ",
    operators.notin_op: " not in ",
    operators.comma_op: ", ",
    operators.from_: " from ",
    operators.as_: " as ",
    operators.is_: " IS ",
    operators.isnot: " IS NOT ",
    operators.collate: " COLLATE ",
    # unary
    operators.exists: "EXISTS ",
    operators.distinct_op: "DISTINCT ",
    operators.inv: "NOT ",
    operators.any_op: "ANY ",
    operators.all_op: "ALL ",
    # modifiers
    operators.desc_op: " desc",
    operators.asc_op: " asc",
    operators.nullsfirst_op: " NULLS FIRST",
    operators.nullslast_op: " NULLS LAST",
}


FUNCTIONS = {
    functions.coalesce: "coalesce",
    functions.current_date: "CURRENT_DATE",
    functions.current_time: "CURRENT_TIME",
    functions.current_timestamp: "CURRENT_TIMESTAMP",
    functions.current_user: "CURRENT_USER",
    functions.localtime: "LOCALTIME",
    functions.localtimestamp: "LOCALTIMESTAMP",
    functions.random: "random",
    functions.sysdate: "sysdate",
    functions.session_user: "SESSION_USER",
    functions.user: "USER",
    functions.cube: "CUBE",
    functions.rollup: "ROLLUP",
    functions.grouping_sets: "GROUPING SETS",
}


# this is extract map for time
# such as:
#       select([extract('year', Orders.order_date)]).select_from(Orders)
# =>
#       SELECT year(orders.order_date) AS year_1 FROM orders
# TODO: NEED TO CHECK
EXTRACT_MAP = {
    "month": "month",
    "day": "day",
    "year": "year",
    "second": "second",
    "hour": "hour",
    "doy": "doy",
    "minute": "minute",
    "quarter": "quarter",
    "dow": "dow",
    "week": "week",
    "epoch": "epoch",
    "milliseconds": "milliseconds",
    "microseconds": "microseconds",
    "timezone_hour": "timezone_hour",       # unsupport
    "timezone_minute": "timezone_minute",   # unsupport
}

# compound query keyword:
# - UNION
# - UNION ALL
# - EXCEPT              // unsupport
# - EXCEPT ALL          // unsupport
# - INTERSECT           // unsupport
# - INTERSECT ALL       // unsupport
COMPOUND_KEYWORDS = sql.compiler.SQLCompiler.extract_map.copy()


class DolphinDBCompiler(sql.compiler.SQLCompiler):

    # override from Base: SQLCompiler
    extract_map = EXTRACT_MAP
    compound_keywords = COMPOUND_KEYWORDS

    returning = None
    returning_precedes_values = False

    ansi_bind_rules = True              # TODO: NEED TO CHECK: whether support ? = ?

    _textual_ordered_columns = False    # TODO: NEED TO CHECK: need to support text-select ?
    _ad_hoc_textual = False
    _loose_column_name_matching = False

    _ordered_columns = True

    OPERATORS = OPERATORS

    # default_from: default

    # visit_grouping: default [GROUP BY] (use custom op)
    def group_by_clause(self, select: sql.Select, **kw):
        group_by = self._generate_delimited_list(
            select._group_by_clauses, OPERATORS[operators.comma_op], **kw
        )
        if group_by:
            return " GROUP BY " + group_by
        else:
            return ""

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is None:
            if select._offset_clause is not None:
                text += "\n LIMIT " + self.process(select._offset_clause, **kw) + ", 9223372036854775807"
                return text
        if select._offset_clause is None:
            if select._limit_clause is not None:
                text += "\n LIMIT " + self.process(select._limit_clause, **kw)
                return text
        text += "\n LIMIT " + self.process(select._offset_clause, **kw) + ", " + self.process(select._limit_clause, **kw)
        return text
    # visit_select_statement_grouping: default
    # visit_label_reference: FIXME: default ?
    # visit_textual_label_reference: FIXME: default ?

    # visit_label
    def visit_label(
        self,
        label,
        add_to_result_map=None,
        within_label_clause=False,
        within_columns_clause=False,
        render_label_as_label=None,
        result_map_targets=(),
        **kw
    ):
        logger.debug("visit label label.name: ", label.name)
        # only render labels within the columns clause
        # or ORDER BY clause of a select.
        render_label_with_as = within_columns_clause and not within_label_clause
        render_label_only = render_label_as_label is label

        label_name = ""
        if render_label_only or render_label_with_as:
            if isinstance(label.name, elements._truncated_label):
                label_name = self._truncated_identifier("colident", label.name)
            else:
                label_name = label.name

        if label_name.find("(") != -1 and label_name.find(")") != -1:
            label_name = label_name.replace("(", '_"')
            label_name = label_name.replace(")", '"')

        if render_label_with_as:
            index = label.element.name.find('(')
            if label_name == "__timestamp":
                # special case about Time-series Table
                if index != -1:
                    label_name = label.element.name[:index] + "_" + label.element.col.name
                else:
                    label_name = label.element.name
            elif index != -1:
                # process time_grain function's label_name. for example: date(a) => date_a
                time_grain = label.element.name[:index]
                if time_grain in ["second", "minute", "hour", "date", "weekBegin", "month", "quarterBegin", "year"]:
                    label_name = time_grain + "_" + label.name
            if add_to_result_map is not None:
                add_to_result_map(
                    label_name,
                    label.name,
                    (label, label_name) + label._alt_names + result_map_targets,
                    label.type,
                )
            l = (
                label.element._compiler_dispatch(
                    self,
                    within_columns_clause=True,
                    within_label_clause=True,
                    **kw
                )
                + OPERATORS[operators.as_]
                + self.preparer.format_label(label, label_name)
            )
            logger.debug("visit label result render_label_with_as: ", l)
            return l
        elif render_label_only:
            l = self.preparer.format_label(label, label_name)
            logger.debug("visit label result render_label_only: ", l)
            return l
        else:
            l = label.element._compiler_dispatch(
                self, within_columns_clause=False, **kw
            )
            logger.debug("visit label result other: ", l)
            return l
    # visit_lambda_element: default

    # visit_column
    def visit_column(
        self,
        column: Column,
        add_to_result_map=None,
        include_table=True,
        result_map_targets=(),
        **kwargs
    ):
        logger.debug("visit Column column.name: ", column.name)
        name = orig_name = column.name
        if name is None:
            name = self._fallback_column_name(column)

        is_literal = column.is_literal
        if not is_literal and isinstance(name, elements._truncated_label):
            name = self._truncated_identifier("colident", name)

        if add_to_result_map is not None:
            targets = (column, name, column.key) + result_map_targets
            if column._tq_label:
                targets += (column._tq_label,)

            add_to_result_map(name, orig_name, targets, column.type)

        if is_literal:
            if name == "COUNT(*)":
                name = "count(*)"
            # note we are not currently accommodating for
            # literal_column(quoted_name('ident', True)) here
            name = self.escape_literal_column(name)
        else:
            name = self.preparer.quote(name)
        table = column.table
        if table is None or not include_table or not table.named_with_column:
            return name
        else:
            effective_schema = self.preparer.schema_for_object(table)

            # TODO: check behaviour when schema is DEFAULT_SECHMA(shared_table)
            if effective_schema and effective_schema != DEFAULT_SCHEMA:
                schema_prefix = (
                    self.preparer.quote_schema(effective_schema) + "."
                )
            else:
                schema_prefix = ""
            tablename = table.name
            if isinstance(tablename, elements._truncated_label):
                tablename = self._truncated_identifier("alias", tablename)

            return schema_prefix + self.preparer.quote(tablename) + "." + name

    # visit_collation: FIXME: default ?
    # visit_fromclause: default
    # visit_index: default
    # visit_typeclause: default
    # visit_textclause: default
    # visit_textual_select: default
    # visit_null: default
    # visit_true: default
    # visit_false: default
    # visit_tuple: default
    # visit_clauselist
    # TODO: for OPERATORS changes
    def visit_clauselist(self, clauselist: elements.ClauseList, **kw):
        logger.debug("visit clauseList clauselist.operator: ", clauselist.operator)
        sep = clauselist.operator
        if sep is None:
            sep = " "
        else:
            sep = OPERATORS[clauselist.operator]

        return self._generate_delimited_list(clauselist.clauses, sep, **kw)
    # visit_case
    # visit_type_coerce

    # visit_cast
    def visit_cast(self, cast, **kwargs):
        logger.debug("visit cast")
        return "cast(%s, %s)" % (
            cast.clause._compiler_dispatch(self, **kwargs),
            cast.typeclause._compiler_dispatch(self, **kwargs),
        )
    # visit_over
    # visit_withingroup
    # visit_funcfilter
    # visit_extract
    # visit_scalar_function_column

    # visit_function TODO: check support `WITH ORDINALITY` or not ?
    def visit_function(self, func: functions.Function, add_to_result_map=None, **kwargs):
        logger.debug("visit function func.name: ", func.name)
        if add_to_result_map is not None:
            add_to_result_map(func.name, func.name, (), func.type)

        disp = getattr(self, "visit_%s_func" % func.name, None)
        if disp:
            text = disp(func, **kwargs)
        else:
            name = FUNCTIONS.get(func._deannotate().__class__, None)
            if name:
                if func._has_args:
                    name += "%{expr}s"
            else:
                name = func.name
                name = (
                    self.preparer.quote(name)
                    if self.preparer._requires_quotes_illegal_chars(name)
                    or isinstance(name, elements.quoted_name)
                    else name
                )
                name = name + "%(expr)s"
            text = ".".join(
                [
                    (
                        self.preparer.quote(tok)
                        if self.preparer._requires_quotes_illegal_chars(tok)
                        or isinstance(name, elements.quoted_name)
                        else tok
                    )
                    for tok in func.packagenames
                ]
                + [name]
            ) % {'expr': self.function_argspec(func, **kwargs)}

        # TODO: NOT SUPPORT [WITH ORDINALITY] clause
        # if func._with_ordinality:
        #     text += " WITH ORDINALITY"
        return text

    # use count, because sqlalchemy will use lower case count when visit_function
    def visit_count_func(self, func: functions.Function, **kw):
        logger.debug("visit_count_func func: ", func)
        ret = "count" + self.function_argspec(func, **kw)
        if ret[:15] == "count(distinct(":
            return ("nunique(" + ret[15:])[:-1]
        else:
            return ret

    def visit_AVG_func(self, func: functions.Function, **kw):
        return "avg" + self.function_argspec(func, **kw)

    def visit_distinct_op_unary_operator(self, unary, operator, **kw):
        return "distinct(" + self.visit_label(unary.element) + ")"

    def visit_unary(
        self, unary, add_to_result_map=None, result_map_targets=(), **kw
    ):
        logger.debug("visit unary unary.operator: ", unary.operator, ", kw:", kw)

        if add_to_result_map is not None:
            result_map_targets += (unary,)
            kw["add_to_result_map"] = add_to_result_map
            kw["result_map_targets"] = result_map_targets

        if unary.operator:
            if unary.modifier:
                raise exc.CompileError(
                    "Unary expression does not support operator "
                    "and modifier simultaneously"
                )
            disp = self._get_operator_dispatch(
                unary.operator, "unary", "operator"
            )
            if disp:
                return disp(unary, unary.operator, **kw)
            else:
                return self._generate_generic_unary_operator(
                    unary, OPERATORS[unary.operator], **kw
                )
        elif unary.modifier:
            disp = self._get_operator_dispatch(
                unary.modifier, "unary", "modifier"
            )
            if disp:
                return disp(unary, unary.modifier, **kw)
            else:
                return self._generate_generic_unary_modifier(
                    unary, OPERATORS[unary.modifier], **kw
                )
        else:
            raise exc.CompileError(
                "Unary expression has no operator or modifier"
            )

    # TODO: AVG
    # TODO: count DISTINCT ?
    # TODO: __timestamp ?

    # visit_next_value_func
    # visit_sequence
    # visit_compound_select
    # visit_unary
    # visit_is_true_unary_operator
    # visit_is_false_unary_operator
    # visit_not_match_op_binary
    # visit_not_in_op_binary
    # visit_empty_set_op_expr
    # visit_empty_set_expr
    # visit_binary
    # visit_function_as_comparison_op_binary
    # visit_mod_binary
    # visit_custom_op_binary
    # visit_custom_op_unary_operator
    # visit_custom_op_unary_modifier
    # visit_contains_op_binary
    # visit_not_contains_op_binary
    # visit_startswith_op_binary
    # visit_not_startswith_op_binary
    # visit_endswith_op_binary
    # visit_not_endswith_op_binary
    # visit_like_op_binary
    # visit_not_like_op_binary
    # visit_ilike_op_binary
    # visit_not_ilike_op_binary
    # visit_between_op_binary
    # visit_not_between_op_binary
    # visit_regexp_match_op_binary
    # visit_not_regexp_match_op_binary
    # visit_regexp_replace_op_binary
    # visit_bindparam
    # visit_cte
    # visit_table_valued_alias
    # visit_table_valued_column
    # visit_alias
    # visit_subquery
    # visit_lateral
    # visit_tablesample
    # visit_values
    # visit_select: default

    # visit_table
    def visit_table(
        self,
        table,
        asfrom=False,
        iscrud=False,
        ashint=False,
        fromhints=None,
        use_schema=True,
        from_linter=None,
        **kwargs
    ):
        logger.debug("visit table table.fullname: ", table.fullname)
        if from_linter:
            from_linter.froms[table] = table.fullname

        if asfrom or ashint:
            effective_schema = self.preparer.schema_for_object(table)

            # shared_table no need prefix
            if use_schema and effective_schema and effective_schema != DEFAULT_SCHEMA:
                ret = (
                    self.preparer.quote_schema(effective_schema)
                    + "."
                    + self.preparer.quote(table.name)
                )
            else:
                ret = self.preparer.quote(table.name)
            if fromhints and table in fromhints:
                ret = self.format_from_hint_text(
                    ret, table, fromhints[table], iscrud
                )
            return ret
        else:
            return ""


    def visit_textclause(self, textclause, add_to_result_map=None, **kw):
        logger.debug("visit_textclause")
        def do_bindparam(m):
            name = m.group(1)
            if name in textclause._bindparams:
                return self.process(textclause._bindparams[name], **kw)
            else:
                return self.bindparam_string(name, **kw)

        if not self.stack:
            self.isplaintext = True

        if add_to_result_map:
            # text() object is present in the columns clause of a
            # select().   Add a no-name entry to the result map so that
            # row[text()] produces a result
            add_to_result_map(None, None, (textclause,), sqltypes.NULLTYPE)

        # un-escape any \:params
        ret = BIND_PARAMS_ESC.sub(
            lambda m: m.group(1),
            BIND_PARAMS.sub(
                do_bindparam, self.post_process_text(textclause.text)
            ),
        )
        if "_\"" + DEFAULT_SCHEMA + "\"." in ret:
            ret = ret.replace("_\"" + DEFAULT_SCHEMA + "\".", "")
        return ret








    # visit_join
    # visit_insert
    # visit_update
    # visit_delete
    # visit_savepoint
    # visit_rollback_to_savepoint
    # visit_release_savepoint


class DolphinDBTypeCompiler(compiler.TypeCompiler):
    def visit_VOID(self, type_: ddbtypes.VOID, **kw):
        return "VOID"

    def visit_BOOL(self, type_: ddbtypes.BOOL, **kw):
        return "BOOL"

    def visit_CHAR(self, type_: ddbtypes.CHAR, **kw):
        return "CHAR"

    def visit_SHORT(self, type_: ddbtypes.SHORT, **kw):
        return "SHORT"

    def visit_INT(self, type_: ddbtypes.INT, **kw):
        return "INT"

    def visit_LONG(self, type_: ddbtypes.LONG, **kw):
        return "LONG"

    def visit_DATE(self, type_: ddbtypes.DATE, **kw):
        return "DATE"

    def visit_MONTH(self, type_: ddbtypes.MONTH, **kw):
        return "MONTH"

    def visit_TIME(self, type_: ddbtypes.TIME, **kw):
        return "TIME"

    def visit_MINUTE(self, type_: ddbtypes.MINUTE, **kw):
        return "MINUTE"

    def visit_SECOND(self, type_: ddbtypes.SECOND, **kw):
        return "SECOND"

    def visit_DATETIME(self, type_: ddbtypes.DATETIME, **kw):
        return "DATETIME"

    def visit_TIMESTAMP(self, type_: ddbtypes.TIMESTAMP, **kw):
        return "TIMESTAMP"

    def visit_NANOTIME(self, type_: ddbtypes.NANOTIME, **kw):
        return "NANOTIME"

    def visit_NANOTIMESTAMP(self, type_: ddbtypes.NANOTIMESTAMP, **kw):
        return "NANOTIMESTAMP"

    def visit_DATEHOUR(self, type_: ddbtypes.DATEHOUR, **kw):
        return "DATEHOUR"

    def visit_FLOAT(self, type_: ddbtypes.FLOAT, **kw):
        return "FLOAT"

    def visit_DOUBLE(self, type_: ddbtypes.DOUBLE, **kw):
        return "DOUBLE"

    def visit_SYMBOL(self, type_: ddbtypes.SYMBOL, **kw):
        return "SYMBOL"

    def visit_STRING(self, type_: ddbtypes.STRING, **kw):
        return "STRING"

    def visit_UUID(self, type_: ddbtypes.UUID, **kw):
        return "UUID"

    def visit_IPADDR(self, type_: ddbtypes.IPADDR, **kw):
        return "IPADDR"

    def visit_INT128(self, type_: ddbtypes.INT128, **kw):
        return "INT128"

    def visit_BLOB(self, type_: ddbtypes.BLOB, **kw):
        return "BLOB"

    def visit_DECIMAL32(self, type_: ddbtypes.DECIMAL32, **kw):
        return f"DECIMAL32({type_.scale})"

    def visit_DECIMAL64(self, type_: ddbtypes.DECIMAL64, **kw):
        return f"DECIMAL64({type_.scale})"

    def visit_DECIMAL128(self, type_: ddbtypes.DECIMAL128, **kw):
        return f"DECIMAL128({type_.scale})"

    def visit_ARRAY(self, type_: ddbtypes.ARRAY, **kw):
        elem_str = self.process(type_.item_type)
        return elem_str + "[]"


LEGAL_CHARACTERS = re.compile(r"^[A-Z0-9_]+$", re.I)
ILLEGAL_INITIAL_CHARACTERS = {str(x) for x in range(0, 10)}.union(["_"])
RESERVED_WORDS = """def """.split()


class DolphinDBIdentifierPreparer(sql.compiler.IdentifierPreparer):
    reserved_words = RESERVED_WORDS
    legal_characters = LEGAL_CHARACTERS
    illegal_initial_characters = ILLEGAL_INITIAL_CHARACTERS

    def __init__(self, dialect):
        super().__init__(dialect, initial_quote='_"', final_quote='"')
        self.escape_to_quote = ""


    def quote_schema(self, schema, force=None):
        """Conditionally quote a schema name.


        The name is quoted if it is a reserved word, contains quote-necessary
        characters, or is an instance of :class:`.quoted_name` which includes
        ``quote`` set to ``True``.

        Subclasses can override this to provide database-dependent
        quoting behavior for schema names.

        :param schema: string schema name
        :param force: unused

            .. deprecated:: 0.9

                The :paramref:`.IdentifierPreparer.quote_schema.force`
                parameter is deprecated and will be removed in a future
                release.  This flag has no effect on the behavior of the
                :meth:`.IdentifierPreparer.quote` method; please refer to
                :class:`.quoted_name`.

        """
        if force is not None:
            # not using the util.deprecated_params() decorator in this
            # case because of the additional function call overhead on this
            # very performance-critical spot.
            util.warn_deprecated(
                "The IdentifierPreparer.quote_schema.force parameter is "
                "deprecated and will be removed in a future release.  This "
                "flag has no effect on the behavior of the "
                "IdentifierPreparer.quote method; please refer to "
                "quoted_name().",
                # deprecated 0.9. warning from 1.3
                version="0.9",
            )
        ret = schema
        # ret = self.quote(schema)
        return ret

class DDBDDLCompiler(sql.compiler.DDLCompiler):
    pass


# class DDBExecutionContext(default.DefaultExecutionContext):
#     def fire_sequence(self, seq, type_):
#         """Get the next value from the sequence using ``gen_id()``."""

#         return self._execute_scalar(
#             "SELECT gen_id(%s, 1) FROM rdb$database"
#             % self.identifier_preparer.format_sequence(seq),
#             type_,
#         )

# class DDBExecutionContext_kinterbasdb(DDBExecutionContext):
#     @property
#     def rowcount(self):
#         if self.execution_options.get(
#             "enable_rowcount", self.dialect.enable_rowcount
#         ):
#             return self.cursor.rowcount
#         else:
#             return -1
