
import logging
import re
from typing import Tuple

import dolphindb.settings as keys

logger = logging.getLogger("pydolphindb_console_logger")
logger.setLevel(logging.INFO)


DECIMAL_SCALE_PATTERN = r"^DECIMAL(\d+)\((\d+)\)$"


def parse_decimal_typestr(type_str: str):
    bit_type_map = {
        32: keys.DT_DECIMAL32,
        64: keys.DT_DECIMAL64,
        128: keys.DT_DECIMAL128,
    }
    match = re.match(DECIMAL_SCALE_PATTERN, type_str)
    if match:
        bit_num = int(match.group(1))
        scale = int(match.group(2))
        return bit_type_map[bit_num], scale
    return keys.DT_VOID, None


_code2str = {
    keys.DT_VOID: "VOID",
    keys.DT_BOOL: "BOOL",
    keys.DT_CHAR: "CHAR",
    keys.DT_SHORT: "SHORT",
    keys.DT_INT: "INT",
    keys.DT_LONG: "LONG",
    keys.DT_DATE: "DATE",
    keys.DT_MONTH: "MONTH",
    keys.DT_TIME: "TIME",
    keys.DT_MINUTE: "MINUTE",
    keys.DT_SECOND: "SECOND",
    keys.DT_DATETIME: "DATETIME",
    keys.DT_TIMESTAMP: "TIMESTAMP",
    keys.DT_NANOTIME: "NANOTIME",
    keys.DT_NANOTIMESTAMP: "NANOTIMESTAMP",
    keys.DT_DATEHOUR: "DATEHOUR",
    keys.DT_FLOAT: "FLOAT",
    keys.DT_DOUBLE: "DOUBLE",
    keys.DT_SYMBOL: "SYMBOL",
    keys.DT_STRING: "STRING",
    keys.DT_IPADDR: "IPADDR",
    keys.DT_INT128: "INT128",
    keys.DT_BLOB: "BLOB",
    keys.DT_DECIMAL32: "DECIMAL32",
    keys.DT_DECIMAL64: "DECIMAL64",
    keys.DT_DECIMAL128: "DECIMAL128",
}


def generate_typestr(type_code: int, exparam: int = None):
    if type_code >= keys.ARRAY_TYPE_BASE:
        return generate_typestr(type_code - keys.ARRAY_TYPE_BASE, exparam)
    if type_code in [keys.DT_DECIMAL32, keys.DT_DECIMAL64, keys.DT_DECIMAL128]:
        if exparam:
            return f"{_code2str[type_code]}({exparam})"
        return f"{_code2str[type_code]}"
    return _code2str[type_code]


_str2code = {
    "VOID": keys.DT_VOID,
    "BOOL": keys.DT_BOOL,
    "CHAR": keys.DT_CHAR,
    "SHORT": keys.DT_SHORT,
    "INT": keys.DT_INT,
    "LONG": keys.DT_LONG,
    "DATE": keys.DT_DATE,
    "MONTH": keys.DT_MONTH,
    "TIME": keys.DT_TIME,
    "MINUTE": keys.DT_MINUTE,
    "SECOND": keys.DT_SECOND,
    "DATETIME": keys.DT_DATETIME,
    "TIMESTAMP": keys.DT_TIMESTAMP,
    "NANOTIME": keys.DT_NANOTIME,
    "NANOTIMESTAMP": keys.DT_NANOTIMESTAMP,
    "DATEHOUR": keys.DT_DATEHOUR,
    "FLOAT": keys.DT_FLOAT,
    "DOUBLE": keys.DT_DOUBLE,
    "SYMBOL": keys.DT_SYMBOL,
    "STRING": keys.DT_STRING,
    "IPADDR": keys.DT_IPADDR,
    "INT128": keys.DT_INT128,
    "BLOB": keys.DT_BLOB,
    "DECIMAL32": keys.DT_DECIMAL32,
    "DECIMAL64": keys.DT_DECIMAL64,
    "DECIMAL128": keys.DT_DECIMAL128,
}


def parse_typestr(type_str: str) -> Tuple[int, int]:
    if type_str.endswith("[]"):
        elem_code, exparam = parse_typestr(type_str[:-2])
        return elem_code + keys.ARRAY_TYPE_BASE, exparam
    if type_str in _str2code.keys():
        return _str2code[type_str], None
    return parse_decimal_typestr(type_str)
