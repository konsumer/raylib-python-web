from __future__ import annotations
from ctype_token import *

END_OF_FILE = '\0'

specifier_cases: dict[CTypeTokenKind, CTypeKind] = {
    CTypeTokenKind.Void: CTypeKind.Void,

    # char kinds
    CTypeTokenKind.Char: CTypeKind.I8,
    CTypeTokenKind.Signed + CTypeTokenKind.Char: CTypeKind.I8,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Char: CTypeKind.I8,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Char: CTypeKind.I8,

    # short kinds
    CTypeKind.I16: CTypeKind.I16,
    CTypeTokenKind.Short + CTypeTokenKind.Int: CTypeKind.I16,
    CTypeTokenKind.Signed + CTypeTokenKind.Short: CTypeKind.I16,
    CTypeTokenKind.Signed + CTypeTokenKind.Short + CTypeTokenKind.Int: CTypeKind.I16,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Short: CTypeKind.I16,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Short + CTypeTokenKind.Int: CTypeKind.I16,

    # int X64WIN kinds
    CTypeTokenKind.Int: CTypeKind.I32,
    CTypeTokenKind.Signed: CTypeKind.I32,
    CTypeTokenKind.Signed + CTypeTokenKind.Int: CTypeKind.I32,
    CTypeTokenKind.Long: CTypeKind.I32,
    CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.I32,
    CTypeTokenKind.Signed + CTypeTokenKind.Long: CTypeKind.I32,
    CTypeTokenKind.Signed + CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.I32,
    CTypeTokenKind.Unsigned: CTypeKind.UInt,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Int: CTypeKind.UInt,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Long: CTypeKind.I32,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.I32,

    # long kinds
    CTypeTokenKind.Long + CTypeTokenKind.Long: CTypeKind.Long,
    CTypeTokenKind.Long + CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.Long,
    CTypeTokenKind.Signed + CTypeTokenKind.Long + CTypeTokenKind.Long: CTypeKind.Long,
    CTypeTokenKind.Signed + CTypeTokenKind.Long + CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.Long,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Long + CTypeTokenKind.Long: CTypeKind.ULong,
    CTypeTokenKind.Unsigned + CTypeTokenKind.Long + CTypeTokenKind.Long + CTypeTokenKind.Int: CTypeKind.ULong,

    # float and double
    CTypeTokenKind.Float: CTypeKind.Float,
    CTypeTokenKind.Double: CTypeKind.Double,
    # CTypeTokenKind.Long + CTypeTokenKind.Double: CTypeKind.LongDouble,
}


class CType:
    def __init__(self, kind: CTypeKind, of: CType | CTypeToken, pointer_level: int = 0, array_size: int = 0):
        pass


class Parser:
    def __init__(self):
        self.token_stream: list[CTypeToken] = []
        self.index: int = 0
        self.current_token: CTypeToken = self.tokens[self.index]

    def peek_token(self) -> None:
        self.index += 1
        self.current_token = self.token_stream[self.index]

    def drop_token(self) -> None:
        self.index -= 1
        self.current_token = self.token_stream[self.index]

    def is_token_kind(self, kind: list[CTypeTokenKind] | CTypeTokenKind) -> bool:
        if isinstance(kind, CTypeTokenKind):
            return self.current_token.kind == kind
        else:
            return self.current_token.kind in kind

    def parse_token_stream_to_ctype(self, token_stream: list[CTypeToken]) -> CType:
        self.token_stream = token_stream
        self.index = 0
        self.current_token = self.tokens[self.index]
