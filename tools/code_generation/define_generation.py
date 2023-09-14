def generate_define_code(define_data) -> str:
    temp = ""

    if not define_data['type'] in ["FLOAT_MATH", "FLOAT", "DOUBLE", "STRING", "INT"]:
        return ""

    elif define_data['type'] == "FLOAT_MATH":
        temp += f"{define_data['name']}: float"
        temp += f" = {define_data['value'].replace('f', '')}"
        temp += f"{('  # ' + define_data['description']) if define_data['description'] != '' else ''}"

    elif define_data['type'] == "INT":
        temp += f"{define_data['name']}: int"
        temp += f" = {define_data['value']}"
        temp += f"{('  # ' + define_data['description']) if define_data['description'] != '' else ''}"

    elif define_data['type'] in ["DOUBLE", "FLOAT"]:
        temp += f"{define_data['name']}: float"
        temp += f" = {define_data['value']}"
        temp += f"{('  # ' + define_data['description']) if define_data['description'] != '' else ''}"

    elif define_data['type'] == "STRING":
        temp += f"{define_data['name']}: str"
        temp += f" = \"{define_data['value']}\""
        temp += f"{('  # ' + define_data['description']) if define_data['description'] != '' else ''}"

    return temp + '\n'
