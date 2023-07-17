from __future__ import annotations
from ctype_lexer import *
from ctype_parser import *
import json
from pathlib import Path

END_OF_FILE = '\0'

# first step, build all the structs as objects and link then together (if needed)

general_structs: list[CTypeStruct] = []


def get_general_struct_by_name(name: str) -> CTypeStruct:
    for struct in general_structs:
        if name == struct.name:
            return struct
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
            size += get_general_struct_by_name(ctype.struct_token.string).size

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


RAYLIB_PYTHON_WEB_FOLDER_PATH = Path(__file__).parent.parent.parent
JSON_API_FOLDER_PATH = RAYLIB_PYTHON_WEB_FOLDER_PATH / "tools/api"

with open(Path(JSON_API_FOLDER_PATH / 'raylib.json')) as reader:
    raylib_api = json.load(reader)

raylib_api_defines = raylib_api['defines']
raylib_api_structs = raylib_api['structs']
raylib_api_aliases = raylib_api['aliases']
raylib_api_enums = raylib_api['enums']
raylib_api_functions = raylib_api['functions']

for struct_api in raylib_api_structs:
    # get struct aliases
    aliases = []
    for alias_api in raylib_api_aliases:
        if alias_api["type"] == struct_api["name"]:
            aliases.append(alias_api)
    out = parse_struct_json_to_CTypeStruct(struct_api)
    out.calculate_size()

    general_structs.append(out)
    if len(aliases) != 0:
        for alias in aliases:
            alias_struct = CTypeStruct(alias["name"], out.members)
            alias_struct.size = out.size
            general_structs.append(alias_struct)

"""for struct in general_structs:
    print(struct.name, struct.size)"""