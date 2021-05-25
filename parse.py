from lexer import Lexer, TokenType

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def array(self):
        if self.current_token.type == TokenType.LBRACKET:
            result = []
            self.eat(TokenType.LBRACKET)
            if not self.current_token.type == TokenType.RBRACKET:
                result.append(self.value())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    result.append(self.value())
            self.eat(TokenType.RBRACKET)
        elif self.current_token.type == TokenType.LBRACE:
            result = self.object()
        return result

    def object(self):
        result = {}
        self.eat(TokenType.LBRACE) 
        if not self.current_token.type == TokenType.RBRACE:
            pair = self.pair()
            result.update({pair[0]: pair[1]})
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                pair = self.pair()
                result.update({pair[0]: pair[1]})
        self.eat(TokenType.RBRACE)
        return result

    def pair(self):
        key = self.current_token.value
        self.eat(TokenType.STRING)
        self.eat(TokenType.COLON)
        value = self.value()
        return [key, value]
    
    def value(self):
        if self.current_token.type in (TokenType.STRING, TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE, TokenType.NULL):
            result = self.current_token.value
            self.eat(self.current_token.type)
        elif self.current_token.type in (TokenType.LBRACE, TokenType.LBRACKET):
            result = self.array()
        else:
            self.error()
        return result

    def parse(self):
        if self.current_token.type == TokenType.EOF:
            return None
        result = self.array()
        if self.current_token.type != TokenType.EOF:
            self.error()

        return result
        