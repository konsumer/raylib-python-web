from enum import *
from ctype_struct import *
import json


class HeapKind(Enum):
    Int8 = auto()
    Int16 = auto()
    Int32 = auto()
    # Int64 = auto() not implemented TODO: implement 64 bit ints heap code generation
    UInt8 = auto()
    UInt16 = auto()
    UInt32 = auto()
    # UInt64 = auto() not implemented TODO: implement 64 bit ints heap code generation
    Float32 = auto()
    Float64 = auto()
    NOT_HEAPED_KIND = auto()  # used when we want to get a member, but it is a struct or an array


def struct_member_heap_kind(member: CType) -> HeapKind:
    match member.kind:
        case CTypeKind.Void:
            raise SyntaxError("void type shouldn't be checked for size")
        case CTypeKind.Pointer:
            return HeapKind.UInt8
        case CTypeKind.I8:
            return HeapKind.Int8
        case CTypeKind.UI8:
            return HeapKind.UInt8
        case CTypeKind.I16:
            return HeapKind.Int16
        case CTypeKind.UI16:
            return HeapKind.UInt16
        case CTypeKind.I32:
            return HeapKind.Int32
        case CTypeKind.UI32:
            return HeapKind.UInt32
        case CTypeKind.Float:
            return HeapKind.Float32
        case CTypeKind.I64:
            assert False, "not implemented yet"
        case CTypeKind.UI64:
            assert False, "not implemented yet"
        case CTypeKind.Double:
            return HeapKind.Float64
        case CTypeKind.Array:
            return HeapKind.NOT_HEAPED_KIND
        case CTypeKind.Struct:
            return HeapKind.NOT_HEAPED_KIND


def struct_member_to_python_type_hint(member: CType):
    match member.kind:
        case CTypeKind.Void:
            raise SyntaxError("void type shouldn't be checked")
        case CTypeKind.Pointer:
            return ""  # TODO: we can do better
        case CTypeKind.I8 | CTypeKind.UI8 | \
             CTypeKind.I16 | CTypeKind.UI16 | \
             CTypeKind.I32 | CTypeKind.UI32 | \
             CTypeKind.I64 | CTypeKind.UI64:
            return "int"
        case CTypeKind.Double | CTypeKind.Float:
            return "float"
        case CTypeKind.Array:
            return ""  # TODO: we can do better
        case CTypeKind.Struct:
            return member.struct_token.string


def generate_struct_code(struct_api) -> str:
    string: str = ""
    struct_: CTypeStruct = parse_struct_json_to_CTypeStruct(struct_api)
    struct_.calculate_size()

    string += f"class {struct_api['name']}:\n"
    string += f"    \"\"\"{struct_api['description']}\"\"\"\n\n"
    # add size member variable
    string += f"    size: int = {struct_.size}\n\n"

    # add init method
    string += f"    def __init__("
    for member_ctype, member_json in zip(struct_.members, struct_api['fields']):
        string += f"{member_json['name']}"
        type_hint: str = struct_member_to_python_type_hint(member_ctype)
        if type_hint != "":
            string += f": {type_hint}"

        string += ", "

    # remove the last ", "
    string: str = string[0:-2]
    string += f"):\n"

    return string

for struct_api in raylib_api_structs:
    struct_string = generate_struct_code(struct_api)
    print(struct_string)
    print()