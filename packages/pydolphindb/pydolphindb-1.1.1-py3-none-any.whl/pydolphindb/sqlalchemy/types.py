import sqlalchemy.types as sqltypes

from ..helper import parse_typestr, generate_typestr
# import uuid
# import ipaddress
# import pandas as pd
# from . import custom_python_type as cpt


class VOID(sqltypes.NullType):
    __visit_name__ = "VOID"


class BOOL(sqltypes.BOOLEAN):
    __visit_name__ = "BOOL"


# TODO: NEED TO CHECK: like CHAR or INTEGER ?
class CHAR(sqltypes.INTEGER):
    __visit_name__ = "CHAR"

    def bind_processor(self, dialect):
        def process(value):
            if isinstance(value, str):
                return ord(value)
            elif isinstance(value, int):
                return value
            return None

        return process


class SHORT(sqltypes.Integer):
    __visit_name__ = "SHORT"


class INT(sqltypes.Integer):
    __visit_name__ = "INT"


class LONG(sqltypes.Integer):
    __visit_name__ = "LONG"


class DATE(sqltypes.DATE):
    __visit_name__ = "DATE"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class MONTH(sqltypes.DATE):
    __visit_name__ = "MONTH"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class TIME(sqltypes.TIME):
    __visit_name__ = "TIME"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class MINUTE(sqltypes.TIME):
    __visit_name__ = "MINUTE"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class SECOND(sqltypes.TIME):
    __visit_name__ = "SECOND"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class DATETIME(sqltypes.DATETIME):
    __visit_name__ = "DATETIME"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class TIMESTAMP(sqltypes.TIMESTAMP):
    __visit_name__ = "TIMESTAMP"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class NANOTIME(sqltypes.TIME):
    __visit_name__ = "NANOTIME"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class NANOTIMESTAMP(sqltypes.TIMESTAMP):
    __visit_name__ = "NANOTIMESTAMP"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class DATEHOUR(sqltypes.DATETIME):
    __visit_name__ = "DATEHOUR"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class FLOAT(sqltypes.FLOAT):
    __visit_name__ = "FLOAT"

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = str(float(value))
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class DOUBLE(sqltypes.FLOAT):
    __visit_name__ = "DOUBLE"

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = str(float(value))
            return value

        return process

    def coerce_compared_value(self, op, value):
        return self


class STRING(sqltypes.String):
    __visit_name__ = "STRING"

    def literal_processor(self, dialect):
        def process(value):
            # use double quotation marks but not signle quotation marks
            if value is not None:
                value = f'"{value}"'
            return value

        return process


class SYMBOL(STRING):
    __visit_name__ = "SYMBOL"


class UUID(sqltypes.BINARY):
    __visit_name__ = "UUID"

    def __init__(self):
        super().__init__(16)

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = f'uuid("{value}")'
            return value

        return process

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process


class IPADDR(sqltypes.BINARY):
    __visit_name__ = "IPADDR"

    def __init__(self):
        super().__init__(16)

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = f'ipaddr("{value}")'
            return value

        return process

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process


class INT128(sqltypes.BINARY):
    __visit_name__ = "INT128"

    def __init__(self):
        super().__init__(16)

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = f'int128("{value}")'
            return value

        return process

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process


class BLOB(sqltypes.LargeBinary):
    __visit_name__ = "BLOB"

    def literal_processor(self, dialect):
        def process(value):
            if value is not None:
                value = f'blob("{value}")'
            return value

        return process

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value.hex()

        return process


class DECIMAL32(sqltypes.DECIMAL):
    __visit_name__ = "DECIMAL32"

    def __init__(self, scale=None, decimal_return_scale=None, asdecimal=True):
        super().__init__(9, scale, decimal_return_scale, asdecimal)


class DECIMAL64(sqltypes.DECIMAL):
    __visit_name__ = "DECIMAL64"

    def __init__(self, scale=None, decimal_return_scale=None, asdecimal=True):
        super().__init__(18, scale, decimal_return_scale, asdecimal)


class DECIMAL128(sqltypes.DECIMAL):
    __visit_name__ = "DECIMAL128"

    def __init__(self, scale=None, decimal_return_scale=None, asdecimal=True):
        super().__init__(38, scale, decimal_return_scale, asdecimal)


class ARRAY(sqltypes.ARRAY):
    def __init__(self, item_type, as_tuple=False, dimensions=None, zero_indexes=False):
        super().__init__(item_type, as_tuple, dimensions, zero_indexes)

    def _proc_array(self, arr, itemproc, dim, collection):
        if dim is None:
            arr = list(arr)
        if (
            dim == 1
            or dim is None
            and (
                # this has to be (list, tuple), or at least
                # not hasattr('__iter__'), since Py3K strings
                # etc. have __iter__
                not arr
                or not isinstance(arr[0], (list, tuple))
            )
        ):
            if itemproc:
                return collection(itemproc(x) for x in arr)
            else:
                return collection(arr)
        else:
            return collection(
                self._proc_array(
                    x,
                    itemproc,
                    dim - 1 if dim is not None else None,
                    collection,
                )
                for x in arr
            )

    def bind_processor(self, dialect):
        item_proc = self.item_type.dialect_impl(dialect).bind_precessor(
            dialect
        )

        def process(value):
            if value is None:
                return value
            else:
                return self._proc_array(
                    value, item_proc, self.dimensions, list
                )

        return process

    def result_processor(self, dialect, coltype):
        item_proc = self.item_type.dialect_impl(dialect).result_processor(
            dialect
        )

        def process(value):
            if value is None:
                return value
            else:
                return self._proc_array(
                    value,
                    item_proc,
                    self.dimensions,
                    tuple if self.as_tuple else list,
                )

        return process
