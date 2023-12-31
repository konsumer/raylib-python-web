from __future__ import annotations
import array_generation
import ctype_struct
import struct_generation
import enum_generation
import define_generation
import function_generation
import color_generation
import json
from pathlib import Path

RAYLIB_PYTHON_WEB_FOLDER_PATH = Path(__file__).parent.parent.parent
print(RAYLIB_PYTHON_WEB_FOLDER_PATH)
JSON_API_FOLDER_PATH = RAYLIB_PYTHON_WEB_FOLDER_PATH / "tools/api"
WASMRAYPY_FOLDER_PATH = RAYLIB_PYTHON_WEB_FOLDER_PATH / "docs"

wrapped_defines_names = []

wrapped_colors_names = []

wrapped_enums_names = []

wrapped_structures_names = []
wrapped_structures_names_stub = []

wrapped_aliases_names = []

wrapped_functions_names = []


# -----------------------------------------


def generate_file(file_path: Path) -> None:
    if Path(file_path).exists():
        with open(Path(file_path), "w"):  # if the file exists we clean it
            pass
    else:
        print(f"the {file_path} doesn't exist, regenerating a new one")
        with open(file_path, "x"):
            pass


def add_text_to_file(file_path: Path, _string: str) -> None:
    with open(Path(file_path), "a") as file:
        file.write(_string)


# -----------------------------------------

def generate_wasm_array_classes_code() -> str:
    _string = ""
    _string += array_generation.wasm_array_string + '\n'
    _string += array_generation.struct_array_string + '\n'

    for primitive_array_metadata in array_generation.primitive_array_classes_metadata:
        _string += array_generation.generate_primitive_array_class(primitive_array_metadata) + '\n'

    return _string


def generate_structs_aliases_code(structs_api, aliases_api) -> str:
    _string = ""
    for struct_api in structs_api:
        if struct_api['name'] in wrapped_structures_names:
            continue
        wrapped_enums_names.append(struct_api['name'])
        _string += struct_generation.generate_struct_code(struct_api)

        struct_aliases = struct_generation.does_struct_name_has_alias(struct_api['name'], aliases_api)
        for alias_api in struct_aliases:
            if alias_api['name'] in wrapped_aliases_names:
                continue
            wrapped_aliases_names.append(alias_api['name'])
            _string += struct_generation.generate_struct_alias_code(alias_api) + '\n'
            struct_ = ctype_struct.parse_struct_json_to_CTypeStruct(struct_api)
            struct_.calculate_size()
            struct_generation.struct_name_size_pars.append((alias_api['name'], struct_.size))

    return _string


def generate_enums_code(enums_api) -> str:
    _string = ""
    for enum_api in enums_api:
        if enum_api['name'] in wrapped_enums_names:
            continue
        wrapped_enums_names.append(enum_api['name'])
        _string += enum_generation.generate_enum_code(enum_api) + '\n'

    return _string


def generate_defines_code(defines_api) -> str:
    _string = ""
    for define_api in defines_api:
        if define_api['name'] in wrapped_defines_names:
            continue
        wrapped_enums_names.append(define_api['name'])
        _string += define_generation.generate_define_code(define_api)

    return _string


def generate_functions_code(functions_api) -> str:
    _string = ""
    for function_api in functions_api:
        if function_api['name'] in wrapped_functions_names:
            continue
        wrapped_functions_names.append(function_api['name'])
        function_string = function_generation.generate_function_code(function_api)
        _string += function_string + '\n\n' if function_string != "" else ""

    return _string


def generate_colors_code(defines_api) -> str:
    _string = ""
    for defines_api in defines_api:
        if defines_api['name'] in wrapped_colors_names:
            continue
        color_string = color_generation.generate_color_code(defines_api)
        if color_string != "":
            wrapped_functions_names.append(defines_api['name'])
            _string += color_string + '\n'

    return _string + '\n'


# -----------------------------------------
"""# load config data
with open(Path(JSON_API_FOLDER_PATH / 'config.json')) as reader:
    config_api = json.load(reader)

config_api_defines = config_api['defines']
config_api_structs = config_api['structs']
config_api_aliases = config_api['aliases']
config_api_enums = config_api['enums']
config_api_functions = config_api['functions']"""

# load rlgl data
with open(Path(JSON_API_FOLDER_PATH / 'rlgl.json')) as reader:
    rlgl_api = json.load(reader)

rlgl_api_defines = rlgl_api['defines']
rlgl_api_structs = rlgl_api['structs']
rlgl_api_aliases = rlgl_api['aliases']
rlgl_api_enums = rlgl_api['enums']
rlgl_api_functions = rlgl_api['functions']

# load raylib data
with open(Path(JSON_API_FOLDER_PATH / 'raylib.json')) as reader:
    raylib_api = json.load(reader)

raylib_api_defines = raylib_api['defines']
raylib_api_structs = raylib_api['structs']
raylib_api_aliases = raylib_api['aliases']
raylib_api_enums = raylib_api['enums']
raylib_api_functions = raylib_api['functions']

# load raymath data
with open(Path(JSON_API_FOLDER_PATH / 'raymath.json')) as reader:
    raymath_api = json.load(reader)

raymath_api_defines = raymath_api['defines']
raymath_api_structs = raymath_api['structs']
raymath_api_aliases = raymath_api['aliases']
raymath_api_enums = raymath_api['enums']
raymath_api_functions = raymath_api['functions']

# load raygui data
with open(Path(JSON_API_FOLDER_PATH / 'raygui.json')) as reader:
    raygui_api = json.load(reader)

raygui_api_defines = raygui_api['defines']
raygui_api_structs = raygui_api['structs']
raygui_api_aliases = raygui_api['aliases']
raygui_api_enums = raygui_api['enums']
raygui_api_functions = raygui_api['functions']

# -----------------------------------------
# generate all the files for wasmraypy
generate_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt')
other_text = """
import enum

# helper to copy a struct
# newColor = struct_clone(RAYWHITE)
# newColor._frozen = false
# newColor.a = 127


def struct_clone(source, a):
    if not a:
        a = _mod._malloc(source._size)
    _mod._memcpy(a, source._address, source._size)
    out = source.__class__(address=a)
    return out
"""
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt', other_text)
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt', generate_wasm_array_classes_code())
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt',
                 generate_structs_aliases_code(raylib_api_structs, raylib_api_aliases))
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt',
                 generate_enums_code(raylib_api_enums))
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt',
                 generate_defines_code(raylib_api_defines))
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt',
                 generate_functions_code(raylib_api_functions))
add_text_to_file(WASMRAYPY_FOLDER_PATH / 'wasmraypy.txt',
                 generate_colors_code(raylib_api_defines))
