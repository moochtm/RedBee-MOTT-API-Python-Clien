
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import json


def pprint_json_obj(j):
    json_str = json.dumps(j, indent=4, ensure_ascii=False)
    return json_str


def pprint_and_color_json_obj(j):
    json_str = json.dumps(j, indent=4, ensure_ascii=False)
    json_str_colored = highlight(json_str, JsonLexer(), TerminalFormatter())
    return json_str_colored