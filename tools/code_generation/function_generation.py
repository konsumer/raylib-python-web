from ctype_lexer import *
from ctype_parser import *
import re


def underscore(_string: str) -> str:
    _string = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', _string)
    _string = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', _string)
    _string = _string.replace("-", "_")
    return _string.lower()


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
    start_function = ""
    end_function = ""
    function_header = ""
    function_body = ""

    lexer = Lexer()
    parser = Parser()

    parameters_ctype_index_list = []
    # function header
    # ----------------------------------------------------------------------------
    function_header += f"def {function_data['name']}("

    params = function_data.get('params', [])
    for param in params:
        if param["type"] == "void":
            continue
        elif param["type"] == "...":  # no support for variadic functions
            return ""
        elif param["type"] in ["AudioCallback", "TraceLogCallback", "LoadFileDataCallback", "SaveFileDataCallback", "LoadFileTextCallback", "SaveFileTextCallback"]:  # no support for those structs yet
            return ""

        lexer.lex_string_to_token_stream(param["type"])
        ctype = parser.parse_token_stream_to_ctype(lexer.token_stream)
        parameters_ctype_index_list.append(ctype)

        function_header += param['name']
        if param['type'] == "const char *":
            function_header += f": str, "
        else:
            function_header += f": {function_member_to_python_type_hint(ctype)}, "

    if len(params) != 0:
        function_header = function_header[0:-2]

    function_header += ")"

    is_return_type_struct = False
    return_ctype = CType(CTypeKind.Void)

    if function_data["returnType"] != "void":
        lexer.lex_string_to_token_stream(function_data["returnType"])
        return_ctype = parser.parse_token_stream_to_ctype(lexer.token_stream)

        function_header += f" -> {function_member_to_python_type_hint(return_ctype)}:\n"
    else:
        function_header += ":\n"
    # ----------------------------------------------------------------------------

    # function start
    # ----------------------------------------------------------------------------
    # create return struct instance
    if function_data["returnType"] != "void" and return_ctype.kind == CTypeKind.Struct:
        is_return_type_struct = True
        start_function += f"    {function_data['returnType']}_ = {function_data['returnType']}()\n"

    # add string-pointer interface
    for i, param in enumerate(params):
        if param['type'] == "const char *":
            start_function += f"    {param['name']}_ = _mod._malloc(len({param['name']}) + 1)\n"
            start_function += f"    _mod.stringToUTF8({param['name']}, {param['name']}_, len({param['name']}) + 1)\n"
    # ----------------------------------------------------------------------------

    # function body
    # ----------------------------------------------------------------------------
    # add function description
    function_body += f"    \"\"\"{function_data['description']}\"\"\"\n" if function_data['description'] != "" else ""

    # add start _mod._function
    # if function return type that is not a struct (and not void) we need to create a return instance
    if function_data["returnType"] != "void" and return_ctype.kind != CTypeKind.Struct:
        function_body += f"    return_interface = _mod._{function_data['name']}("
    else:
        function_body += f"    _mod._{function_data['name']}("

    # add return struct interface as first parameter (if needed)
    if function_data["returnType"] != "void" and return_ctype.kind == CTypeKind.Struct:
        function_body += f"{function_data['returnType']}_._address, "

    for i, param in enumerate(params):
        if param['type'] == "const char *":
            function_body += f"{param['name']}_, "
        elif parameters_ctype_index_list[i].kind == CTypeKind.Struct:
            function_body += f"{param['name']}._address, "
        else:
            function_body += f"{param['name']}, "

    if len(params) != 0 or is_return_type_struct:
        function_body = function_body[0:-2]

    function_body += ")\n"
    # ----------------------------------------------------------------------------

    # function end
    # ----------------------------------------------------------------------------
    # deallocate string-pointer interface
    for i, param in enumerate(params):
        if param['type'] == "const char *":
            end_function += f"    _mod._free({param['name']}_)\n"

    # if function return type that is not a struct (and not void) we need to return return_instance
    if function_data["returnType"] != "void" and return_ctype.kind != CTypeKind.Struct:
        end_function += f"    return return_interface\n"
    elif function_data["returnType"] != "void" and return_ctype.kind == CTypeKind.Struct:
        end_function += f"    return {function_data['returnType']}_\n"
    else:
        pass  # there should be no return statement

    return function_header + start_function + function_body + end_function
