from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from enum import *

RAYLIB_PYTHON_WEB_FOLDER_PATH = Path(__file__).parent.parent
JSON_API_FOLDER_PATH = RAYLIB_PYTHON_WEB_FOLDER_PATH / "tools/api"
WASMRAYPY_FOLDER_PATH = RAYLIB_PYTHON_WEB_FOLDER_PATH / "demo/wasmraypy"

wrapped_defines_names = []

wrapped_colors_names = []

wrapped_enums_names = []

wrapped_structures_names = []
wrapped_structures_names_stub = []

wrapped_aliases_names = []

wrapped_functions_names_stub = []


# -----------------------------------------

class CTypeKind(Enum):
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    Float = auto()
    Double = auto()
    Array = auto()
    Pointer = auto()
    Struct = auto()

class CType:
    def __init__(self, kind: CTypeKind, of: CType, pointer_level: int = 0, array_sizee: int = 0):
        pass


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

def generate_structs_aliases_code(structs_api, aliases_api, for_stub: bool = False) -> str:
    _string = ""
    if not for_stub:
        _wrapped_structures_names = wrapped_structures_names
    else:
        _wrapped_structures_names = wrapped_structures_names_stub
    for struct in structs_api:
        if struct['name'] not in _wrapped_structures_names:
            struct_string_logic = generate_struct_code(struct, for_stub)
            if struct_string_logic != "":
                _wrapped_structures_names.append(struct['name'])
                struct_string_logic += "\n"

            _string += struct_string_logic

            for alias in aliases_api:
                if struct['name'] == alias['type']:
                    if alias['name'] not in _wrapped_structures_names:
                        alias_string_logic = ""
                        alias_string_logic += generate_alias_code(alias['name'], struct['name'])
                        if alias_string_logic != "":
                            _wrapped_structures_names.append(alias['name'])
                        alias_string_logic += "\n\n"

                        _string += alias_string_logic

    return _string


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
generate_file(WASMRAYPY_FOLDER_PATH / 'structures/__init__.py')
