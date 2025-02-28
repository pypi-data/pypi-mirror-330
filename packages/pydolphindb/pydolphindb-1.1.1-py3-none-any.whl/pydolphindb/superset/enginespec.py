from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING, Union, List, Tuple

import re
from . import utils
from ..sqlalchemy import types
from ..sqlalchemy.dialect import ischema_names
from ..sqlalchemy import custom_python_type
from superset.utils.core import GenericDataType
import sqlalchemy.types as sqltypes
import sqlparse

import dolphindb.settings as keys

if TYPE_CHECKING:
    from superset.connectors.sqla.models import TableColumn

from superset import app
with app.app_context():
    # Note:
    #       only can be import inside an app_context, otherwise they fail
    #       AttributeError: 'NoneType' object has no attribute 'user_model'
    from superset.db_engine_specs.base import BaseEngineSpec
    from superset.db_engine_specs.base import LimitMethod


class DolphinDBEngineSpec(BaseEngineSpec):
    engine = "dolphindb"
    engine_name = "DolphinDB"

    allows_alias_in_select = True

    sqlalchemy_uri_placeholder = (
        "dolphindb://user:password@host:port/catalog"
    )
    # Correspondence between string and sqla_type, generic_type
    column_type_mappings = (
        (
            re.compile(r"\w+\[\]$", re.IGNORECASE),
            types.ARRAY,
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^void$", re.IGNORECASE),
            types.VOID(),
            None,
        ),
        (
            re.compile(r"^bool$", re.IGNORECASE),
            types.BOOL(),
            GenericDataType.BOOLEAN,
        ),
        (
            re.compile(r"^char$", re.IGNORECASE),
            types.CHAR(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^short$", re.IGNORECASE),
            types.SHORT(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^int$", re.IGNORECASE),
            types.INT(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^long$", re.IGNORECASE),
            types.LONG(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^date$", re.IGNORECASE),
            types.DATE(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^month$", re.IGNORECASE),
            types.MONTH(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^time$", re.IGNORECASE),
            types.TIME(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^minute$", re.IGNORECASE),
            types.MINUTE(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^second$", re.IGNORECASE),
            types.SECOND(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^datetime$", re.IGNORECASE),
            types.DATETIME(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^timestamp$", re.IGNORECASE),
            types.TIMESTAMP(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^nanotime$", re.IGNORECASE),
            types.NANOTIME(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^nanotimestamp$", re.IGNORECASE),
            types.NANOTIMESTAMP(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^datehour$", re.IGNORECASE),
            types.DATEHOUR(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^float$", re.IGNORECASE),
            types.FLOAT(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^double$", re.IGNORECASE),
            types.DOUBLE(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^symbol$", re.IGNORECASE),
            types.SYMBOL(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^string$", re.IGNORECASE),
            types.STRING(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^uuid$", re.IGNORECASE),
            types.UUID(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^ipaddr$", re.IGNORECASE),
            types.IPADDR(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^int128$", re.IGNORECASE),
            types.INT128(),
            GenericDataType.STRING,  # TODO: numeric or string or None? (numeric has problem when filter)
        ),
        (
            re.compile(r"^blob$", re.IGNORECASE),
            types.BLOB(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^decimal32", re.IGNORECASE),
            types.DECIMAL32,
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^decimal64", re.IGNORECASE),
            types.DECIMAL64,
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^decimal128", re.IGNORECASE),
            types.DECIMAL128,
            GenericDataType.NUMERIC,
        ),
    )

    @classmethod
    def get_column_types(
        cls,
        column_type: str | None,
    ):
        """
        Return a sqlalchemy native column type and generic data type that corresponds
        to the column type defined in the data source (return None to use default type
        inferred by SQLAlchemy).

        :param column_type: Column type returned by inspector
        :return: SQLAlchemy and generic Superset column types
        """
        if not column_type:
            return None
        for regex, sqla_type, generic_type in (
            cls.column_type_mappings + cls._default_column_type_mappings
        ):
            match = regex.match(column_type)
            if not match:
                continue
            if callable(sqla_type):
                type_code, exparam = types.parse_typestr(column_type)
                if sqla_type is types.ARRAY:
                    # ARRAY
                    elem_type = ischema_names[types.generate_typestr(type_code - keys.ARRAY_TYPE_BASE)]
                    if type_code in [keys.DT_DECIMAL32_ARRAY, keys.DT_DECIMAL64_ARRAY, keys.DT_DECIMAL128_ARRAY]:
                        return sqla_type(elem_type(scale=exparam)), generic_type
                    return sqla_type(elem_type()), generic_type
                elif sqla_type in [types.DECIMAL32, types.DECIMAL64, types.DECIMAL128]:
                    # DECIMAL32, DECIMAL64, DECIMAL128
                    return sqla_type(scale=exparam), generic_type
            return sqla_type, generic_type
        return None

    # type mutators after fetch data
    column_type_mutators = {
        # TODO maybe need to add more type mutators, example: ipaddr, int128 (now is treated as string)
        types.DATE: lambda val: utils.mutator_temporary_pandas(val, keys.DT_DATE),
        types.MONTH: lambda val: utils.mutator_temporary_pandas(val, keys.DT_MONTH),
        types.TIME: lambda val: utils.mutator_temporary_pandas(val, keys.DT_TIME),  # time is microsecond level in python but millisecond level in dolphindb
        types.MINUTE: lambda val: utils.mutator_temporary_pandas(val, keys.DT_MINUTE),
        types.SECOND: lambda val: utils.mutator_temporary_pandas(val, keys.DT_SECOND),  # time is microsecond level in python but second is second level in dolphindb
        types.DATETIME: lambda val: utils.mutator_temporary_pandas(val, keys.DT_DATETIME),  # datetime is microsecond level in python but second level in dolphindb
        types.TIMESTAMP: lambda val: utils.mutator_temporary_pandas(val, keys.DT_TIMESTAMP),  # datetime is microsecond level in python but timestamp is millisecond level in dolphindb
        types.NANOTIME: lambda val: utils.mutator_temporary_pandas(val, keys.DT_NANOTIME),  # time is microsecond level in python but nanotime is nanosecond level in dolphindb
        types.NANOTIMESTAMP: lambda val: utils.mutator_temporary_pandas(val, keys.DT_NANOTIMESTAMP),  # datetime is microsecond level in python but nanotimestamp is nanosecond level in dolphindb
        types.DATEHOUR: lambda val: utils.mutator_temporary_pandas(val, keys.DT_DATEHOUR),
    }

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "second({col})",
        # "PT5S": "",
        # "PT30S": "",
        "PT1M": "minute({col})",
        # "PT5M": "",
        # "PT10M": "",
        # "PT30M": "",
        # "PT1H": "datehour({col})",
        # "PT6H": "",
        "P1D": "date({col})",
        "P1W": "weekBegin({col}, weekday=6)",  # Note: Week Start Sunday like engine mysql
        "P1M": "month({col})",
        "P3M": "quarterBegin({col})",
        # "P1Y": "month({col})",
        "1969-12-28T00:00:00Z/P1W": "weekBegin({col}, weekday=6)",
        "1969-12-29T00:00:00Z/P1W": "weekBegin({col}, weekday=0)",
        # "P1W/1970-01-03T00:00:00Z": "",
        # "P1W/1970-01-04T00:00:00Z": "",
    }

    # @classmethod
    # def column_datatype_to_string(
    #     cls, sqla_column_type: TypeEngine, dialect: Dialect
    # ) -> str:
    #     """
    #     Convert sqlalchemy column type to string representation.
    #     By default, removes collation and character encoding info to avoid
    #     unnecessarily long datatypes.

    #     :param sqla_column_type: SqlAlchemy column type
    #     :param dialect: Sqlalchemy dialect
    #     :return: Compiled column type
    #     """
    #     sqla_column_type = sqla_column_type.copy()
    #     if hasattr(sqla_column_type, "collation"):
    #         sqla_column_type.collation = None
    #     if hasattr(sqla_column_type, "charset"):
    #         sqla_column_type.charset = None
    #     return sqla_column_type.compile(dialect=dialect).upper()

    @classmethod
    def convert_dttm(
        cls, target_type: str, dttm: datetime, db_extra: dict[str, Any] | None = None
    ) -> str | None:
        """
        Convert a datetime object to a string representation suitable for filtering with time.

        Args:
            target_type (str): The target type to which the datetime should be converted.
            dttm (datetime): The datetime object to be converted.
            db_extra (dict[str, Any] | None, optional): Additional database-specific parameters. Defaults to None.

        Returns:
            str | None: The string representation of the datetime object in the appropriate format,
                        or None if the target type is not recognized.
        """
        sqla_type = cls.get_sqla_column_type(target_type)
        if isinstance(sqla_type, types.DATE):
            return f'date("{dttm.year:04d}.{dttm.month:02d}.{dttm.day:02d}")'
        elif isinstance(sqla_type, types.MONTH):
            return f'month("{dttm.year:04d}.{dttm.month:02d}")'
        elif isinstance(sqla_type, types.TIME):
            return f'time("{dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}.{dttm.microsecond:03d}")'
        elif isinstance(sqla_type, types.MINUTE):
            return f'minute("{dttm.hour:02d}:{dttm.minute:02d}")'
        elif isinstance(sqla_type, types.SECOND):
            return f'second("{dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}")'
        elif isinstance(sqla_type, types.DATETIME):
            return f'datetime("{dttm.year:04d}.{dttm.month:02d}.{dttm.day:02d} {dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}")'
        elif isinstance(sqla_type, types.TIMESTAMP):
            return f'timestamp("{dttm.year:04d}.{dttm.month:02d}.{dttm.day:02d} {dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}.{dttm.microsecond:06d}")'
        elif isinstance(sqla_type, types.NANOTIME):
            return f'nanotime("{dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}.{dttm.microsecond:06d}")'
        elif isinstance(sqla_type, types.NANOTIMESTAMP):
            return f'nanotimestamp("{dttm.year:04d}.{dttm.month:02d}.{dttm.day:02d} {dttm.hour:02d}:{dttm.minute:02d}:{dttm.second:02d}.{dttm.microsecond:06d}")'
        elif isinstance(sqla_type, types.DATEHOUR):
            return f'datehour("{dttm.year:04d}.{dttm.month:02d}.{dttm.day:02d} {dttm.hour:02d}")'
        return None

    @classmethod
    def get_datatype(cls, type_code: Union[int, str, Tuple[int, int]]):
        """
        Change column type code from cursor description to string representation.

        :param type_code: Type code from cursor description
        :return: String representation of type code
        """
        exparam = None
        if isinstance(type_code, list) or isinstance(type_code, tuple):
            type_code, exparam = type_code
        if isinstance(type_code, str):
            return type_code
        if isinstance(type_code, int):
            return types.generate_typestr(type_code, exparam)
        return None

    @classmethod
    def fetch_data(cls, cursor: Any, limit: Optional[int] = None) -> List[Tuple[Any, ...]]:
        """

        :param cursor: Cursor instance
        :param limit: Maximum number of rows to be returned by the cursor
        :return: Result of query
        """
        if cls.arraysize:
            cursor.arraysize = cls.arraysize
        try:
            if cls.limit_method == LimitMethod.FETCH_MANY and limit:
                return cursor.fetchmany(limit)
            data = cursor.fetchall()
            description = cursor.description or []
            # Create a mapping between column name and a mutator function to normalize
            # values with. The first two items in the description row are
            # the column name and type.
            column_mutators = dict()
            for row in description:
                func = cls.column_type_mutators.get(
                    type(cls.get_sqla_column_type(cls.get_datatype((row[1], row[5]))))
                )
                if func:
                    column_mutators[row[0]] = func
            if column_mutators:
                indexes = {row[0]: idx for idx, row in enumerate(description)}
                for row_idx, row in enumerate(data):
                    new_row = list(row)
                    for col, func in column_mutators.items():
                        # col: col name
                        # func: mutator
                        col_idx = indexes[col]
                        type_code = description[col_idx][1]
                        if type_code >= keys.ARRAY_TYPE_BASE:
                            new_row[col_idx] = utils.mutator_array(row[col_idx], type_code - keys.ARRAY_TYPE_BASE)
                        else:
                            new_row[col_idx] = func(row[col_idx])
                    data[row_idx] = tuple(new_row)

            return data
        except Exception as ex:
            raise cls.get_dbapi_mapped_exception(ex) from ex

    @classmethod
    def select_star(  # pylint: disable=too-many-arguments
        cls,
        database,
        table,
        engine,
        limit: int = 100,
        show_cols: bool = False,
        indent: bool = True,
        latest_partition=True,
        cols=None,
    ) -> str:
        return BaseEngineSpec.select_star(database, table, engine, limit, show_cols, False, latest_partition, cols)

    @classmethod
    def execute(  # pylint: disable=unused-argument
        cls,
        cursor: Any,
        query: str,
        database,
        **kwargs: Any,
    ) -> None:
        parsed = sqlparse.parse(query)
        sqls = [utils.reformat_sql(_) for _ in parsed]
        query = "".join(sqls)
        return super().execute(cursor, query, database, **kwargs)
