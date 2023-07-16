from __future__ import annotations
from ctype_token import *

END_OF_FILE = '\0'

specifier_cases: dict[CTypeTokenKind, CTypeKind] = {
    CTypeTokenKind.VOID: CTypeKind.Void,

    # char kinds
    CTypeTokenKind.CHAR: CTypeKind.I8,
    CTypeTokenKind.SIGNED + CTypeTokenKind.CHAR: CTypeKind.I8,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.CHAR: CTypeKind.I8,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.CHAR: CTypeKind.I8,

    # short kinds
    CTypeKind.I16: CTypeKind.I16,
    CTypeTokenKind.SHORT + CTypeTokenKind.INT: CTypeKind.I16,
    CTypeTokenKind.SIGNED + CTypeTokenKind.SHORT: CTypeKind.I16,
    CTypeTokenKind.SIGNED + CTypeTokenKind.SHORT + CTypeTokenKind.INT: CTypeKind.I16,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.SHORT: CTypeKind.I16,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.SHORT + CTypeTokenKind.INT: CTypeKind.I16,

    # int X64WIN kinds
    CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.SIGNED: CTypeKind.I32,
    CTypeTokenKind.SIGNED + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.SIGNED + CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.SIGNED + CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,

    # long kinds
    CTypeTokenKind.LONG + CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.LONG + CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.SIGNED + CTypeTokenKind.LONG + CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.SIGNED + CTypeTokenKind.LONG + CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.LONG + CTypeTokenKind.LONG: CTypeKind.I32,
    CTypeTokenKind.UNSIGNED + CTypeTokenKind.LONG + CTypeTokenKind.LONG + CTypeTokenKind.INT: CTypeKind.I32,

    # float and double
    CTypeTokenKind.FLOAT: CTypeKind.Float,
    CTypeTokenKind.DOUBLE: CTypeKind.Double,
    # CTypeTokenKind.Long + CTypeTokenKind.Double: CTypeKind.LongDouble,
}


class CType:
    def __init__(self, kind: CTypeKind,
                 of: CType | None = None,
                 struct_token: CTypeToken | None = None,
                 pointer_level: int = 0,
                 array_size: int = 0):
        self.kind = kind
        self.of = of
        self.struct_token = struct_token
        self.pointer_level = pointer_level
        self.array_size = array_size


class Parser:
    def __init__(self):
        self.token_stream: list[CTypeToken] = []
        self.token_stream.append(CTypeToken(CTypeTokenKind.END, "\0"))
        self.index: int = 0
        self.current_token: CTypeToken = self.token_stream[self.index]

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

    def is_token_type_specifier(self) -> bool:
        return self.is_token_kind(
            [CTypeTokenKind.VOID,
             CTypeTokenKind.CHAR,
             CTypeTokenKind.SHORT,
             CTypeTokenKind.INT,
             CTypeTokenKind.LONG,
             CTypeTokenKind.FLOAT,
             CTypeTokenKind.DOUBLE,
             CTypeTokenKind.SIGNED,
             CTypeTokenKind.UNSIGNED,
             CTypeTokenKind.IDENTIFIER])

    def is_token_type_qualifier(self) -> bool:
        return self.is_token_kind(CTypeTokenKind.CONST)

    def peek_token_kind(self) -> CTypeTokenKind:
        kind: CTypeTokenKind = self.current_token.kind

        self.peek_token()  # peek token

        return kind

    def peek_specifier_qualifier_list(self) -> CType:
        """
        parse a specifier qualifier list
        specifier_qualifier_list
            : type_specifier specifier_qualifier_list
            | type_specifier
            | type_qualifier specifier_qualifier_list
            | type_qualifier
            ;
        :return: a specifier type node
        """

        # the idea is form https://github.com/sgraham/dyibicc/blob/main/src/parse.c#L359
        specifier_counter: CTypeTokenKind = CTypeTokenKind(0)
        ctype: CType = CType(CTypeKind.Void)

        while self.is_token_type_specifier() or self.is_token_type_qualifier():
            # handel qualifiers (aka jump over them)
            if self.is_token_type_qualifier():
                self.peek_token()  # peek qualifier token
                continue

            # handle struct identifier name
            # when parsing those specifiers the specifier count should be 0
            if self.is_token_kind(CTypeTokenKind.IDENTIFIER):
                if specifier_counter != 0:
                    raise SyntaxError("Invalid specifier in that current contex")

                token: CTypeToken = self.current_token

                self.peek_token()  # peek struct identifier name

                return CType(CTypeKind.Struct, struct_token=token)

            current_specifier_kind: CTypeTokenKind = self.peek_token_kind()
            if current_specifier_kind == current_specifier_kind.UNSIGNED or current_specifier_kind == current_specifier_kind.SIGNED:
                specifier_counter |= current_specifier_kind
            else:
                specifier_counter += current_specifier_kind

            specifier_type: CTypeKind = specifier_cases.get(specifier_counter)

            if specifier_type is None:
                raise SyntaxError("Invalid specifier in that current contex")
            else:
                ctype = CType(specifier_type)

        return ctype

    def parse_token_stream_to_ctype(self, token_stream: list[CTypeToken]) -> CType:
        self.token_stream = token_stream
        self.index = 0
        self.current_token = self.token_stream[self.index]

        ctype: CType = self.peek_specifier_qualifier_list()

        return ctype

from ctype_lexer import *
lexer = Lexer()
lexer.lex_string_to_token_stream("const unsigned char")
parser = Parser()
parser.parse_token_stream_to_ctype(lexer.token_stream)