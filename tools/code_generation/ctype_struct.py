from __future__ import annotations
from ctype_lexer import *
from ctype_parser import *
import json
from pathlib import Path

END_OF_FILE = '\0'

# first step, build all the structs as objects and link then together (if needed)

# struct_name-size par
struct_name_size_pars: list[tuple[str, int]] = []


def get_struct_name_size_par_by_name(name: str) -> tuple[str, int]:
    for par in struct_name_size_pars:
        if name == par[0]:
            return par
    return None


def get_ctype_size(ctype: CType) -> int:
    """return CType object size in bytes"""
    size = 0
    match ctype.kind:
        case CTypeKind.Void:
            raise SyntaxError("void type shouldn't be checked for size")
        case CTypeKind.I8 | CTypeKind.UI8:
            size += 1
        case CTypeKind.I16 | CTypeKind.UI16:
            size += 2
        case CTypeKind.Pointer | CTypeKind.I32 | CTypeKind.UI32 | CTypeKind.Float:
            size += 4
        case CTypeKind.I64 | CTypeKind.UI64 | CTypeKind.Double:
            size += 8
        case CTypeKind.Array:
            multiplayer: int = ctype.array_size
            size += multiplayer * get_ctype_size(ctype.of)
        case CTypeKind.Struct:
            size += get_struct_name_size_par_by_name(ctype.struct_token.string)[1]

    return size


class CTypeStruct:
    def __init__(self, name: str, members: list[CType]):
        self.name = name
        self.members = members
        self.size = 0  # the size of the struct in bytes

    def calculate_size(self):
        for member in self.members:
            self.size += get_ctype_size(member)


def parse_struct_json_to_CTypeStruct(struct_json) -> CTypeStruct:
    members: list[CType] = []
    lexer = Lexer()
    parser = Parser()

    for field in struct_json["fields"]:
        lexer.lex_string_to_token_stream(field["type"])
        ctype = parser.parse_token_stream_to_ctype(lexer.token_stream)

        members.append(ctype)

    return CTypeStruct(struct_json["name"], members)
