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
            return HeapKind.UInt32
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
            return ""
        case CTypeKind.Pointer:
            return f"\"{struct_member_to_python_type_hint(member.of)}*\""
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
        if member_ctype.kind == CTypeKind.Array:
            return ""  # TODO: implement struct code generation for structs that has members of array type

        string += f"{member_json['name']}"
        type_hint: str = struct_member_to_python_type_hint(member_ctype)
        if type_hint != "":
            string += f": {type_hint}"

        string += ", "

    # remove the last ", "
    string: str = string[0:-2]
    string += f"):\n"

    # malloc code of class
    string += f"        self._address = _mod._malloc({struct_.size})\n"

    # set self values
    offset: int = 0
    for member_ctype, member_json in zip(struct_.members, struct_api['fields']):
        if member_ctype.kind == CTypeKind.Array:
            return ""  # TODO: implement struct code generation for structs that has members of array type

        if member_ctype.kind != CTypeKind.Struct:
            string += f"        self._{member_json['name']} = {member_json['name']}\n"
            heap_kind: CTypeKind = struct_member_heap_kind(member_ctype)
            match heap_kind:
                case CTypeKind.Void:
                    raise SyntaxError("void type shouldn't be checked for size")
                case HeapKind.Int8:
                    string += f"        _mod.HEAP8[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.UInt8:
                    string += f"        _mod.HEAPU8[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.Int16:
                    string += f"        _mod.HEAP16[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.UInt16:
                    string += f"        _mod.HEAPU16[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.Int32:
                    string += f"        _mod.HEAP32[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.UInt32:
                    string += f"        _mod.HEAPU32[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.Float32:
                    string += f"        _mod.HEAPF32[self._address + {offset}] = {member_json['name']}\n"
                case HeapKind.Float64:
                    string += f"        _mod.HEAPF32[self._address + {offset}] = {member_json['name']}\n"
        else:
            string += f"        self._{member_json['name']} = {member_json['name']}\n"


        offset += get_ctype_size(member_ctype)

    return string


for struct_api in raylib_api_structs:
    struct_string = generate_struct_code(struct_api)
    print(struct_string)
    print()
