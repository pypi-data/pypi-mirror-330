import sqlalchemy.engine.base as sql_base
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy.dialects.mysql.base import MySQLCompiler
from sqlalchemy.engine import default, reflection, URL
from sqlalchemy.sql.compiler import SQLCompiler

from .compiler import (DDBDDLCompiler,
                       DolphinDBCompiler, DolphinDBTypeCompiler, DolphinDBIdentifierPreparer
                       )
from . import types as ddbtypes
from . import compiler as ddbcompiler
from ..helper import logger
from ..helper import parse_typestr, generate_typestr

import dolphindb.settings as keys

ischema_names = {
    "VOID": ddbtypes.VOID,
    "BOOL": ddbtypes.BOOL,
    "CHAR": ddbtypes.CHAR,
    "SHORT": ddbtypes.SHORT,
    "INT": ddbtypes.INT,
    "LONG": ddbtypes.LONG,
    "DATE": ddbtypes.DATE,
    "MONTH": ddbtypes.MONTH,
    "TIME": ddbtypes.TIME,
    "MINUTE": ddbtypes.MINUTE,
    "SECOND": ddbtypes.SECOND,
    "DATETIME": ddbtypes.DATETIME,
    "TIMESTAMP": ddbtypes.TIMESTAMP,
    "NANOTIME": ddbtypes.NANOTIME,
    "NANOTIMESTAMP": ddbtypes.NANOTIMESTAMP,
    "DATEHOUR": ddbtypes.DATEHOUR,
    "FLOAT": ddbtypes.FLOAT,
    "DOUBLE": ddbtypes.DOUBLE,
    "SYMBOL": ddbtypes.SYMBOL,
    "STRING": ddbtypes.STRING,
    "UUID": ddbtypes.UUID,
    "IPADDR": ddbtypes.IPADDR,
    "INT128": ddbtypes.INT128,
    "BLOB": ddbtypes.BLOB,
    "DECIMAL32": ddbtypes.DECIMAL32,
    "DECIMAL64": ddbtypes.DECIMAL64,
    "DECIMAL128": ddbtypes.DECIMAL128,
}

colspecs = {}


class DolphinDBDialect(default.DefaultDialect):
    name = "dolphindb"
    driver = "pydolphindb"

    statement_compiler = DolphinDBCompiler              # SQL query
    ddl_compiler = DDBDDLCompiler                   # DDL support
    preparer = DolphinDBIdentifierPreparer                # catalog
    type_compiler = DolphinDBTypeCompiler

    global_schema_name = ddbcompiler.DEFAULT_SCHEMA              # global_schema_name

    supports_alter = False                          # ALTER TABLE clause
    supports_sane_rowcount = False                  # row count in INSERT / UPDATE / DELETE clause
    supports_sane_multi_rowcount = False
    preexecute_autoincrement_sequences = False      # not support autoincrement
    implicit_returning = False                      # about INSERT with RETURNING

    supports_views = False
    supports_default_values = False
    supports_sequences = False                      # CREATE SEQUENCES
    sequences_optional = False

    colspecs = colspecs

    supports_native_enum = False                    # ENUM
    supports_native_boolean = True
    supports_native_decimal = True
    supports_statement_cache = True                 # execute cache

    ischema_names = ischema_names

    supports_empty_insert = False
    """dialect supports INSERT () VALUES ()"""

    _backslash_escapes = None

    supports_simple_order_by_label = True           # needed by SQLCompiler.visit_label_reference

    @classmethod
    def dbapi(cls):
        return __import__("pydolphindb")

    def __init__(self, **kwargs):
        default.DefaultDialect.__init__(self, **kwargs)

    def create_connect_args(self, url: URL):
        opts: dict = url.translate_connect_args()
        if "database" in opts:
            catalog = opts.pop("database")
            opts["catalog"] = catalog
        opts["sqlStd"] = keys.SqlStd.MySQL
        return [[], opts]

    def _extract_scale_and_precision_from_decimal(self, decimal_str):
        start = decimal_str.find('(') + 1
        end = decimal_str.find(')')
        scale = int(decimal_str[start:end])
        if 'DECIMAL32' in decimal_str:
            decimal_str = 'DECIMAL32'
            precision = 9
        elif 'DECIMAL64' in decimal_str:
            decimal_str = 'DECIMAL64'
            precision = 18
        elif 'DECIMAL128' in decimal_str:
            decimal_str = 'DECIMAL128'
            precision = 38
        return int(scale), precision, decimal_str

    def _get_column_info(self, name: str, type_int: int, exparam: int = None, comment: str = None):
        if type_int >= keys.ARRAY_TYPE_BASE:
            # array vector column
            is_array = True
            elem_type_int = type_int - keys.ARRAY_TYPE_BASE
        else:
            # vector column
            is_array = False
            elem_type_int = type_int
        col_type = self.ischema_names.get(generate_typestr(elem_type_int))
        if col_type is None:
            util.warn(
                "Did not recognize type '%s' of column '%s'" % (generate_typestr(type_int, exparam), name)
            )
            col_type = sqltypes.NULLTYPE
        elif elem_type_int in [keys.DT_DECIMAL32, keys.DT_DECIMAL64, keys.DT_DECIMAL128]:
            col_type = col_type(scale=exparam)
        else:
            col_type = col_type()

        if is_array:
            col_type = ddbtypes.ARRAY(col_type)

        default_value = None

        col_d = {
            'name': name,
            'type': col_type,
            'nullable': True,
            'default': default_value,
            'comment': comment,
        }
        return col_d

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        # Query to extract the details of all the fields of the given table
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.global_schema_name

        if current_schema == self.global_schema_name:
            tbl_query = f"""
                schema({table_name})['colDefs']
            """
        else:
            tbl_query = f"""
                schema({schema}.{table_name})['colDefs']
            """

        result = connection.execute(tbl_query)
        cols = []
        while True:
            row = result.fetchone()
            if row is None:
                break
            name = row['name']
            type_int = row['typeInt']
            if row.has_key('extra'):
                exparam = row['extra']
            else:
                exparam = None
            comment = row['comment']
            col_d = self._get_column_info(
                name=name,
                type_int=type_int,
                exparam=exparam,
                comment=comment,
            )
            cols.append(col_d)
        return cols

    # UNSUPPORT: get_pk_constraint
    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return []

    # UNSUPPORT: get_foreign_keys
    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.global_schema_name

        if current_schema == self.global_schema_name:
            script = """
                SELECT name FROM objs(shared=true) WHERE shared=true AND form=`TABLE
            """
        else:
            script = f"""
                dbUrl = (EXEC dbUrl FROM getSchemaByCatalog(getCurrentCatalog()) WHERE schema=`{schema})[0];
                SELECT tableName FROM listTables(dbUrl)
            """
        cursor = connection.execute(script)
        ans = [r[0] for r in cursor]
        return ans

    # UNSUPPORT: get_temp_table_names
    # UNSUPPORT: get_view_names
    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        return []

    # UNSUPPORT: get_sequence_names
    # UNSUPPORT: get_temp_view_names
    # UNSUPPORT: get_view_definition
    # UNSUPPORT: get_indexes
    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []
    # UNSUPPORT: get_unique_constraints
    # UNSUPPORT: get_check_constraints
    # UNSUPPORT: get_table_comment

    def has_table(self, connection, table_name, schema=None, **kw):
        """Return ``True`` if the given table exists"""
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.global_schema_name

        if current_schema == self.global_schema_name:
            tbl_query = f"""
                size(SELECT name FROM objs(shared=true) WHERE shared=true AND name=`{table_name}) >= 1
            """
        else:
            tbl_query = f"""
                dbUrl = (EXEC dbUrl FROM getSchemaByCatalog(getCurrentCatalog()) WHERE schema=`{schema})[0];
                existsTable(dbUrl, `{table_name})
            """
        result = connection.connection.run(tbl_query)
        return result

    # UNSUPPORT: has_index
    # UNSUPPORT: has_sequence

    # get server version
    # LEVEL 1
    # def _get_server_version_info(self, connection: sql_base.Connection):
    #     cursor = connection.execute("version()")
    #     logger.debug("dir cursor: ", dir(cursor))
    #     ans = cursor.scalar()
    #     logger.debug("ans: ", ans)
    #     return ans

    # def _get_default_schema_name(self, connection):
    #     return "shared_table"

    def do_execute(self, cursor, statement, parameters, context=None):
        statement = statement.replace("?", "%s")
        return super().do_execute(cursor, statement, parameters, context)

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        catalog = connection.connection.run("getCurrentCatalog()")
        if not catalog:
            return [self.global_schema_name]
        cursor = connection.execute("""
            SELECT schema FROM getSchemaByCatalog(getCurrentCatalog()) ORDER BY schema ASC
        """)
        return [self.global_schema_name] + [r[0] for r in cursor]
