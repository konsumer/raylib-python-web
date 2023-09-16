def generate_color_code(color_data):
    if color_data['type'] == "COLOR":
        ints_array_string = color_data['value'].split('{')[1].split('}')[0].replace(' ', '').split(',')
        temp = f"{color_data['name']}: Color"
        temp += f" = Color({ints_array_string[0]}, {ints_array_string[1]}, {ints_array_string[2]}, {ints_array_string[3]}, frozen=True)"
        temp += f"{('  # ' + color_data['description']) if color_data['description'] != '' else ''}"
        return temp
    else:
        return ""
