from enum import *


class CTypeTokenKind(IntFlag):
    # Keywords
    CHAR = 1 << 0  # char
    CONST = 1 << 2  # const
    DOUBLE = 1 << 4  # double
    FLOAT = 1 << 6  # float
    INT = 1 << 8  # int
    LONG = 1 << 10  # long
    SHORT = 1 << 12  # short
    SIGNED = 1 << 14  # signed
    UNSIGNED = 1 << 16  # unsigned
    VOID = 1 << 18  # void

    # Separators
    ASTERISK = 1 << 19  # *
    OPENING_PARENTHESIS = 1 << 20  # [
    CLOSING_PARENTHESIS = 1 << 21  # ]

    # Numbers
    INTEGER_LITERAL = 1 << 22

    # struct identifier name
    IDENTIFIER = 1 << 23

    END = 1 << 24  # End Of Tokens stream token


string_to_separator: dict[str, CTypeTokenKind] = {
    '*': CTypeTokenKind.ASTERISK,
    '[': CTypeTokenKind.OPENING_PARENTHESIS,
    ']': CTypeTokenKind.CLOSING_PARENTHESIS,
}

string_to_keyword: dict[str, CTypeTokenKind] = {
    "char": CTypeTokenKind.CHAR,
    "const": CTypeTokenKind.CONST,
    "double": CTypeTokenKind.DOUBLE,
    "float": CTypeTokenKind.FLOAT,
    "int": CTypeTokenKind.INT,
    "long": CTypeTokenKind.LONG,
    "short": CTypeTokenKind.SHORT,
    "signed": CTypeTokenKind.SIGNED,
    "unsigned": CTypeTokenKind.UNSIGNED,
    "void": CTypeTokenKind.VOID,
}


class CTypeKind(Enum):
    Void = auto()
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
    def __init__(self, kind: CTypeTokenKind, string: str = ""):
        self.kind = kind
        self.string = string
