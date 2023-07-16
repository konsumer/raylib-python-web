from enum import *


class CTypeTokenKind(Enum):
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

    # Separators
    ASTERISK = auto()  # *
    OPENING_PARENTHESIS = auto()  # [
    CLOSING_PARENTHESIS = auto()  # ]

    # Numbers
    INTEGER_LITERAL = auto()

    # struct identifier name
    IDENTIFIER = auto()

    END = auto()  # End Of Tokens stream token


string_to_separator: dict[str, CTypeTokenKind] = {
    '*': CTypeTokenKind.ASTERISK,
    '[': CTypeTokenKind.OPENING_PARENTHESIS,
    ']': CTypeTokenKind.CLOSING_PARENTHESIS,
}

string_to_keyword: dict[str, CTypeTokenKind] = {
    "char": CTypeTokenKind.CHAR,
    "const": CTypeTokenKind.CONST,
    "double": CTypeTokenKind.DOUBLE,
    "enum": CTypeTokenKind.ENUM,
    "float": CTypeTokenKind.FLOAT,
    "int": CTypeTokenKind.INT,
    "long": CTypeTokenKind.LONG,
    "short": CTypeTokenKind.SHORT,
    "signed": CTypeTokenKind.SIGNED,
    "unsigned": CTypeTokenKind.UNSIGNED,
    "void": CTypeTokenKind.VOID,
}


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
