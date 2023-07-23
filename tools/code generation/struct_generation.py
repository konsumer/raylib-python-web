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


def heap_kind_to_wasm_heap_string(kind: HeapKind):
    match kind:
        case HeapKind.NOT_HEAPED_KIND:
            raise SyntaxError("not heap size doesn't have an heap string")
        case HeapKind.Int8:
            return "HEAP8"
        case HeapKind.UInt8:
            return "HEAPU8"
        case HeapKind.Int16:
            return "HEAP16"
        case HeapKind.UInt16:
            return "HEAPU16"
        case HeapKind.Int32:
            return "HEAP32"
        case HeapKind.UInt32:
            return "HEAPU32"
        case HeapKind.Float32:
            return "HEAPF32"
        case HeapKind.Float64:
            return "HEAPF32"


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
            return "int"
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


def emscripten_XXXType_string_for_ctype_kind(kind: CTypeKind, get: bool = True) -> str:
    string_ = "get" if get else "set"
    match kind:
        case CTypeKind.Void:
            return ""
        case CTypeKind.Pointer:
            string_ += "Uint32"
        case CTypeKind.I8:
            string_ += "Int8"
        case CTypeKind.UI8:
            string_ += "Uint8"
        case CTypeKind.I16:
            string_ += "Int16"
        case CTypeKind.UI16:
            string_ += "Uint16"
        case CTypeKind.I32:
            string_ += "Int32"
        case CTypeKind.UI32:
            string_ += "Uint32"
        case CTypeKind.I64:
            assert False, "not implemented yet"
        case CTypeKind.UI64:
            assert False, "not implemented yet"
        case CTypeKind.Float:
            string_ += "Float32"
        case CTypeKind.Double:
            string_ += "Float64"
        case CTypeKind.Array:
            return ""
        case CTypeKind.Struct:
            return ""
    return string_


def default_attribute_string_from_ctype_kind(kind: CTypeKind) -> str:
    match kind:
        case CTypeKind.Void:
            return ""
        case CTypeKind.Pointer | \
             CTypeKind.I8 | CTypeKind.UI8 | \
             CTypeKind.I16 | CTypeKind.UI16 | \
             CTypeKind.I32 | CTypeKind.UI32 | \
             CTypeKind.I64 | CTypeKind.UI64:
            return "0"
        case CTypeKind.Double | CTypeKind.Float:
            return "0.0"
        case CTypeKind.Array:
            return ""  # TODO: we can do better
        case CTypeKind.Struct:
            return "None"


def emscripten_Value_type_string_from_ctype_kind(kind: CTypeKind) -> str:
    match kind:
        case CTypeKind.Void:
            return ""
        case CTypeKind.Pointer:
            return "*"
        case CTypeKind.I8 | CTypeKind.UI8:
            return "i8"
        case CTypeKind.I16 | CTypeKind.UI16:
            return "i16"
        case CTypeKind.I32 | CTypeKind.UI32:
            return "i32"
        case CTypeKind.Float:
            return "float"
        case CTypeKind.I64:
            assert False, "not implemented yet"
        case CTypeKind.UI64:
            assert False, "not implemented yet"
        case CTypeKind.Double:
            return "double"
        case CTypeKind.Array:
            return ""
        case CTypeKind.Struct:
            return ""


def generate_struct_code(struct_api) -> str:
    string: str = ""
    struct_: CTypeStruct = parse_struct_json_to_CTypeStruct(struct_api)
    struct_.calculate_size()

    string += f"class {struct_api['name']}:\n"
    string += f"    \"\"\"{struct_api['description']}\"\"\"\n\n"
    # add size member variable
    string += f"    size: int = {struct_.size}\n\n"

    # add init method
    string += f"    def __init__(self, "
    for member_ctype, member_json in zip(struct_.members, struct_api['fields']):
        if member_ctype.kind == CTypeKind.Array:
            return ""  # TODO: implement struct code generation for structs that has members of array type

        string += f"{member_json['name']}"
        type_hint: str = struct_member_to_python_type_hint(member_ctype)
        if type_hint != "":
            string += f": {type_hint}"
            string += f" = {default_attribute_string_from_ctype_kind(member_ctype.kind)}"

        string += ", "

    # added frozen and address arguments
    string += f"address: int = 0, "
    string += f"frozen: bool = False"
    string += f"):\n"

    # add frozen self
    string += f"        self._frozen = frozen\n"
    # malloc code of class
    string += f"        if address != 0:\n"
    string += f"            self._address = address\n"
    string += f"        else:\n"
    string += f"            self._address = _mod._malloc({struct_.size})\n"

    # set self values
    offset: int = 0
    for member_ctype, member_json in zip(struct_.members, struct_api['fields']):
        if member_ctype.kind == CTypeKind.Array:
            return ""  # TODO: implement struct code generation for structs that has members of array type

        if member_ctype.kind != CTypeKind.Struct:
            string += f"            _mod.mem.{emscripten_XXXType_string_for_ctype_kind(member_ctype.kind, False)}" \
                      f"(self._address + {offset}, {member_json['name']})\n"
        else:
            string += f"            if {member_json['name']} is not None: \n"
            string += f"                struct_clone({member_json['name']}, self._address + {offset})\n"
        offset += get_ctype_size(member_ctype)

    string += '\n'

    # add setters and getters
    offset = 0
    for member_ctype, member_json in zip(struct_.members, struct_api['fields']):
        if member_ctype.kind == CTypeKind.Array:
            return ""  # TODO: implement struct code generation for structs that has members of array type

        if member_ctype.kind != CTypeKind.Struct:
            # getter
            string += f"    @property\n"
            string += f"    def {member_json['name']}(self):\n"
            string += f"        return _mod.mem.{emscripten_XXXType_string_for_ctype_kind(member_ctype.kind, True)}" \
                      f"(self._address + {offset}, True)\n\n"

            # setter
            string += f"    @{member_json['name']}.setter\n"
            string += f"    def {member_json['name']}(self, value):\n"
            string += f"        if not self._frozen:\n"
            string += f"            _mod.mem.{emscripten_XXXType_string_for_ctype_kind(member_ctype.kind, False)}" \
                      f"(self._address + {offset}, value, True)\n\n"
        else:
            type_hint: str = struct_member_to_python_type_hint(member_ctype)
            # getter
            string += f"    @property\n"
            string += f"    def {member_json['name']}(self):\n"
            string += f"        return {type_hint}(address=self._address + {offset})\n\n"

            # setter
            string += f"    @{member_json['name']}.setter\n"
            string += f"    def {member_json['name']}(self, value):\n"
            string += f"        if not self._frozen:\n"
            string += f"            struct_clone(value, self._address + {offset})\n\n"

        offset += get_ctype_size(member_ctype)

    return string


def does_struct_name_has_alias(name: str) -> list[dict]:
    for alias in raylib_api_aliases:
        if alias['type'] == name:
            yield alias


def generate_struct_alias_code(alias_api) -> str:
    return f"{alias_api['name']} = {alias_api['type']}\n"


for struct_api in raylib_api_structs:
    struct_string = generate_struct_code(struct_api)
    print(struct_string)

    struct_aliases = does_struct_name_has_alias(struct_api['name'])
    for alias in struct_aliases:
        alias_string = generate_struct_alias_code(alias)
        print(alias_string)
