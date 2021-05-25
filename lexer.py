class TokenType(object):
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    COMMA = "COMMA"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    STRING = "STRING"
    NUMBER = "NUMBER"
    EOF = "EOF"

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(NUMBER, 3)
            Token(LBRACE, "{")
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid Character")

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """Peek at the next character in the input"""
        if self.pos + 1 > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos + 1]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        if self.current_char == "-":
            self.advance()
            result += "-"
        if self.current_char is None or not self.current_char.isdigit():
            self.error()
        elif self.current_char == "0" and self.peek() is not None and self.peek().isdigit():
            self.error()
        elif self.current_char == "0":
            self.advance()
            result += "0"
        else:
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        return result

    def fraction(self):
        result = ""
        result += "."
        self.advance()
        if self.current_char is None or not self.current_char.isdigit():
            self.error()
        result += self.current_char
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def exponent(self):
        result = ""
        result += self.current_char
        self.advance()
        if self.current_char == "-" or self.current_char == "+":
            result += self.current_char
            self.advance()
        if self.current_char is None or not self.current_char.isdigit():
            self.error()
        result += self.current_char
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def number(self):
        isFloat = False
        result = ""
        result += self.integer()
        if self.current_char == ".":
            isFloat = True
            result += self.fraction()
        if self.current_char == "e" or self.current_char == "E":
            isFloat = True
            result += self.exponent()
        if isFloat:
            return float(result)
        return int(result)

    def escape(self):
        hexdigits = "0123456789abcdefABCDEF"
        result = ""
        result += "\\"
        self.advance()
        if not self.current_char in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u'):
            self.error()
        elif self.current_char == "u":
            result += "u"
            self.advance()
            for _ in range(0, 4):
                if not self.current_char in hexdigits:
                    self.error()
                result += self.current_char
                self.advance()
        else:
            result += self.current_char
            self.advance()
        return result
        

    def string(self):
        result = ""
        self.advance()
        while self.current_char is not None and not self.current_char == '"':
            if self.current_char == "\\":
                result += self.escape()
            else:
                result += self.current_char
                self.advance()
        if not self.current_char == '"':
            self.error()
        self.advance()
        return result

    def _check_expect(self, expected):
        for i in range(0, len(expected)):
            if not self.current_char == expected[i]:
                self.error()
            self.advance()

    def true(self):
        self._check_expect("true")
        return True

    def false(self):
        self._check_expect("false")
        return False
    
    def null(self):
        self._check_expect("null")
        return None

    def get_next_token(self):
        """Lexical analyzer

        This method splits the input into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '"':
                return Token(TokenType.STRING, self.string())

            if self.current_char == "t":
                return Token(TokenType.TRUE, self.true())
            
            if self.current_char == "f":
                return Token(TokenType.FALSE, self.false())

            if self.current_char == "n":
                return Token(TokenType.NULL, self.null())

            if self.current_char == "-" or self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            
            if self.current_char == "[":
                self.advance()
                return Token(TokenType.LBRACKET, "[")

            if self.current_char == "]":
                self.advance()
                return Token(TokenType.RBRACKET, "]")

            if self.current_char == "{":
                self.advance()
                return Token(TokenType.LBRACE, "{")

            if self.current_char == "}":
                self.advance()
                return Token(TokenType.RBRACE, "}")
            
            if self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA, ",")
            
            if self.current_char == ":":
                self.advance()
                return Token(TokenType.COLON, ":")
            
            self.error()

        return Token(TokenType.EOF, None)