from lexer import tokenize


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.constants = {}

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type):
        token = self.current()
        if not token or token.type != token_type:
            raise ParserError(f"Ожидался {token_type}, получено {token}")
        self.pos += 1
        return token

    def parse(self):
        result = {}
        while self.current():
            name = self.consume("NAME").value
            self.consume("COLON")
            value = self.parse_value()
            self.constants[name] = value
            result[name] = value
        return result

    def parse_value(self):
        token = self.current()

        if token.type == "NUMBER":
            self.pos += 1
            return float(token.value)

        if token.type == "STRING":
            self.pos += 1
            return token.value[2:-1]  # убрать @"..."

        if token.type == "CONST_EVAL":
            self.pos += 1
            name = token.value.strip("|")
            if name not in self.constants:
                raise ParserError(f"Неизвестная константа {name}")
            return self.constants[name]

        if token.type == "ARRAY_START":
            return self.parse_array()

        if token.type == "LBRACE":
            return self.parse_dict()

        raise ParserError(f"Неожиданное значение {token}")

    def parse_array(self):
        self.consume("ARRAY_START")
        self.consume("LPAREN")
        values = []
        while self.current().type != "RPAREN":
            values.append(self.parse_value())
        self.consume("RPAREN")
        return values

    def parse_dict(self):
        self.consume("LBRACE")
        d = {}
        while self.current().type != "RBRACE":
            key = self.consume("NAME").value
            self.consume("ARROW")
            value = self.parse_value()
            d[key] = value

            if self.current() and self.current().type == "COMMA":
                self.consume("COMMA")
        self.consume("RBRACE")
        return d


def parse_text(text):
    tokens = tokenize(text)
    return Parser(tokens).parse()
