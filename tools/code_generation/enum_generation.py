def generate_enum_code(enum_data):
    _string = ""
    _string += f"class {enum_data['name']}(enum.IntEnum):\n"
    if enum_data['description'] != '':
        _string += f"    \"\"\"{enum_data['description']}\"\"\"\n"

    for value in enum_data['values']:
        _string += f"    {value['name']}: int"
        _string += f" = {value['value']}"
        if value['description'] != '':
            _string += f"  # {value['description']}"
        _string += "\n"

    _string += "\n"

    return _string
