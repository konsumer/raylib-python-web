from ctype_token import *

END_OF_FILE = '\0'


class Lexer:
    def __init__(self):
        self.string = ""
        self.current_char = ""
        self.index = 0
        self.token_stream: list[CTypeToken] = list()

    def peek_char(self):
        self.index += 1
        self.current_char = self.string[self.index]

    def drop_char(self):
        self.index -= 1
        self.current_char = self.string[self.index]

    def is_char(self, string: str) -> bool:
        return self.current_char in string

    def is_char_whitespace(self) -> bool:
        return self.current_char in "\n\t\r "

    def is_char_numeric(self) -> bool:
        return self.current_char.isnumeric()

    def is_char_identifier_starter(self) -> bool:
        return self.current_char.isalpha() or self.is_char('_')

    def is_char_identifier(self) -> bool:
        return self.current_char.isalnum() or self.is_char('_')

    def is_char_separator(self) -> bool:
        return self.is_char("*[]")

    def peek_integer(self):
        str_: str = self.current_char
        self.peek_char()  # peek first char

        while not self.is_char(END_OF_FILE) and self.is_char_numeric():
            str_ += self.current_char
            self.peek_char()  # peek numeric char

        return CTypeToken(CTypeTokenKind.INTEGER_LITERAL, str_)

    def peek_identifier(self):
        str_: str = self.current_char

        self.peek_char()  # peek first char

        while not self.is_char(END_OF_FILE):
            if not self.is_char_identifier():
                break

            str_ += self.current_char
            self.peek_char()  # peek identifier char

        return CTypeToken(CTypeTokenKind.IDENTIFIER, str_)

    def peek_separator(self) -> CTypeToken:
        index_: int = self.index
        str_: str = self.current_char

        self.peek_char()  # peek first char

        while not self.is_char(END_OF_FILE) and self.is_char_separator():
            str_ += self.current_char
            self.peek_char()

            if str_ not in string_to_separator.keys():
                str_ = str_[0:-1]
                self.drop_char()  # drop the last char
                break

        return CTypeToken(string_to_separator[str_], str_)

    def lex_string_to_token_stream(self, string: str) -> list[CTypeToken]:
        # setup lexer
        self.string = string
        self.string += END_OF_FILE
        self.index = 0
        self.current_char = self.string[self.index]
        self.token_stream.clear()

        while not self.is_char(END_OF_FILE):
            if self.is_char_whitespace():
                self.peek_char()
            elif self.is_char_numeric():
                token: CTypeToken = self.peek_integer()
                self.token_stream.append(token)
            elif self.is_char_identifier_starter():
                token: CTypeToken = self.peek_identifier()
                if token.string in string_to_keyword.keys():
                    keyword_kind: CTypeTokenKind = string_to_keyword[token.string]
                    token.kind = keyword_kind
                self.token_stream.append(token)
            elif self.is_char_separator():
                token: CTypeToken = self.peek_separator()
                self.token_stream.append(token)
            else:
                if self.is_char(END_OF_FILE):
                    break
                raise SyntaxError(f"Unexpected character: {self.current_char}, file index: {self.index}")

        self.token_stream.append(CTypeToken(CTypeTokenKind.END, '\0'))

        return self.token_stream


lexer = Lexer()
stream = lexer.lex_string_to_token_stream("const long long[10]**")

print("")