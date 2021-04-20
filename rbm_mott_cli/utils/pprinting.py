
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import json
import datetime


def pprint_and_color(obj):

    obj = _try_string_to_json(obj)

    if isinstance(obj, dict):
        return _pprint_and_color_json_obj(obj)
    elif isinstance(obj, str):
        return obj
    return _pprint_and_color_json_obj(obj)


def _pprint_json_obj(j):
    return json.dumps(j, indent=4, ensure_ascii=False, default=_my_converter)


def _pprint_and_color_json_obj(j):
    return highlight(_pprint_json_obj(j), JsonLexer(), TerminalFormatter())


def _try_string_to_json(myjson):
    if not isinstance(myjson, str):
        return myjson
    try:
        return json.loads(myjson)
    except ValueError as e:
        return myjson
    except TypeError as e:
        return myjson


def _my_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()