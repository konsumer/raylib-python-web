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
    BOOL = 1 << 14  # bool
    SIGNED = 1 << 16  # signed
    UNSIGNED = 1 << 18  # unsigned
    VOID = 1 << 20  # void

    # Separators
    ASTERISK = 1 << 21  # *
    OPENING_BRACKETS = 1 << 22  # [
    CLOSING_BRACKETS = 1 << 23  # ]

    # Numbers
    INTEGER_LITERAL = 1 << 24

    # struct identifier name
    IDENTIFIER = 1 << 25

    END = 1 << 26  # End Of Tokens stream token


string_to_separator: dict[str, CTypeTokenKind] = {
    '*': CTypeTokenKind.ASTERISK,
    '[': CTypeTokenKind.OPENING_BRACKETS,
    ']': CTypeTokenKind.CLOSING_BRACKETS,
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
