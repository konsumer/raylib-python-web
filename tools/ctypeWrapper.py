from __future__ import annotations
from enum import *


class CTypeTokenKind(Enum):
    COMMENT = auto()  # // ... \n or /* ... */

    # Keywords
    CHAR = auto()  # char
    CONST = auto()  # const
    DOUBLE = auto()  # double
    ENUM = auto()  # enum
    FLOAT = auto()  # float
    INT = auto()  # int
    LONG = auto()  # long
    SHORT = auto()  # short
    SIGNED = auto()  # signed
    UNSIGNED = auto()  # unsigned
    VOID = auto()  # void

    # struct identifier name
    IDENTIFIER = auto()

    END = auto()  # End Of Tokens stream token


class CTypeKind(Enum):
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    Float = auto()
    Double = auto()
    Array = auto()
    Pointer = auto()
    Struct = auto()


class CTypeToken:
    def __init__(self, kind: CTypeKind, string: str = ""):
        self.kind = kind
        self.string = string


class CType:
    def __init__(self, kind: CTypeKind, of: CType | CTypeToken, pointer_level: int = 0, array_size: int = 0):
        pass


class Lexer:
    def __init__(self):
        self.string = ""
        self.char = ""
        self.index = 0
        self.token_stream: list[CTypeToken] = list()

    def peek_char(self):
        if self.is_char('\n'):
            self.current_line += 1

        self.index += 1
        self.current_char = self.file_string[self.index]

    def lex_string_to_token_stream(self, string: str) -> list[CTypeToken]:
        # setup lexer
        self.string = string
        self.string += "\0"
        self.index = 0
        self.char = self.string[self.index]
        self.token_stream.clear()


class Parser:
    @staticmethod
    def parse_string_to_ctype() -> CType:
        pass
