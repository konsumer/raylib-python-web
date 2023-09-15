from ctype_lexer import *
from ctype_parser import *


def function_member_to_python_type_hint(member: CType):
    match member.kind:
        case CTypeKind.Void:
            return ""
        case CTypeKind.Pointer:  # TODO: char * -> str and not char * -> int
            return "int"
        case CTypeKind.I8 | CTypeKind.UI8 | \
             CTypeKind.I16 | CTypeKind.UI16 | \
             CTypeKind.I32 | CTypeKind.UI32 | \
             CTypeKind.I64 | CTypeKind.UI64:
            return "int"
        case CTypeKind.Double | CTypeKind.Float:
            return "float"
        case CTypeKind.Array:
            match member.of.kind:
                case CTypeKind.I8:
                    return "CharArray"
                case CTypeKind.UI8:
                    return "UCharArray"
                case CTypeKind.I16:
                    return "Int16Array"
                case CTypeKind.UI16:
                    return "UInt16Array"
                case CTypeKind.I32:
                    return "Int32Array"
                case CTypeKind.UI32:
                    return "UInt32Array"
                case CTypeKind.Float:
                    return "FloatArray"
                case CTypeKind.Double:
                    return "DoubleArray"
                case CTypeKind.Struct:
                    return "StructArray"
                case _:
                    assert False, "array type is not implemented"
        case CTypeKind.Struct:
            return member.struct_token.string


def generate_function_code(function_data):
    string = ""
    end_function = ""

    lexer = Lexer()
    parser = Parser()

    parameters_ctype_index_list = []
    string += f"def {function_data['name']}("

    for param in function_data['params']:
        lexer.lex_string_to_token_stream(param["type"])
        ctype = parser.parse_token_stream_to_ctype(lexer.token_stream)
        parameters_ctype_index_list.append(ctype)

        string += function_data['name']
        string += f": {function_member_to_python_type_hint(ctype)}, "

    if len(function_data['params']) != 0:
        string = string[0:-2]
