import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value"])

TOKEN_SPEC = [
    ("COMMENT_MULTI", r"--\[\[.*?\]\]", re.DOTALL),
    ("COMMENT_SINGLE", r"#.*"),
    ("NUMBER", r"[+-]?\d+(\.\d+)?([eE][+-]?\d+)?"),
    ("STRING", r'@".*?"'),
    ("CONST_EVAL", r"\|[_a-zA-Z]+\|"),
    ("NAME", r"[_a-zA-Z]+"),
    ("COLON", r":"),
    ("ARROW", r"=>"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("ARRAY_START", r"'"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA", r","),
    ("WHITESPACE", r"\s+"),
]

TOKEN_REGEX = "|".join(f"(?P<{name}>{regex})" for name, regex, *_ in TOKEN_SPEC)
TOKEN_FLAGS = re.DOTALL | re.MULTILINE


def tokenize(text):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, text, TOKEN_FLAGS):
        kind = match.lastgroup
        value = match.group()
        if kind in ("WHITESPACE", "COMMENT_SINGLE", "COMMENT_MULTI"):
            continue
        tokens.append(Token(kind, value))
    return tokens
