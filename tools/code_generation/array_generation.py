wasm_array_string: str = \
    """
class WasmArray:
    \"\"\"Generic array-like collection that uses wasm as memory-back\"\"\"
    
    def __init__(self, item_size: int, length: int, address: int = 0, to_alloc: bool = True):
        self._length = length
        self._item_size = item_size
        self._size = self._item_size * self._length
        self._to_alloc = to_alloc
        if not to_alloc:
            self._address: int = address
        else:
            self._address: int = _mod._malloc(self._size)

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)

    def __len__(self):
        return self._length

    def __str__(self):
        out = "WasmArray["
        out += ', '.join([str(self[i]) for i in range(self._length)])
        out += "] " + hex(self._address)
        return out
    """

struct_array_string: str = \
    """
class StructArray(WasmArray):
    \"\"\"an array of structs\"\"\"
    def __init__(self, stype, length, address: int = 0, to_alloc: bool = True):
        super(StructArray, self).__init__(stype.size, length, address, to_alloc)
        self._stype = stype

    def __getitem__(self, item):
        return self._stype(address=(self._address + (self._item_size * item)), to_alloc=False)

    def __setitem__(self, item, value):
        struct_clone(value, self._address + (self._item_size * item))
    """


def generate_primitive_array_class(metadata: tuple[str, str, int]) -> str:
    string = ""
    string += f"class {metadata[0]}(WasmArray):\n"

    # add __init__ method
    string += f"    def __init__(self, length, address: int = 0, to_alloc: bool = True):\n"
    string += f"        super({metadata[0]}, self).__init__({metadata[2]}, length, address, to_alloc)\n\n"

    # add __getitem__
    string += f"    def __getitem__(self, item):\n"
    string += f"        return _mod.mem.get{metadata[1]}(self._address + (item * self._item_size), True)\n\n"

    # add __setitem__
    string += f"    def __setitem__(self, item, value):\n"
    string += f"        _mod.mem.set{metadata[1]}(self._address + (item * self._item_size), value, True)\n\n"

    return string


# first str in tuple(str, str, int) is for the name of the array class.
# second str in tuple(str, str, int) is for the string that will use to get/set the memory from wasm,
# for example Int16 or Float32...
# first int in tuple(str, str, int) is for the size in bytes of an item.
primitive_array_classes_metadata: list[tuple[str, str, int]] = [
    ("CharArray", "Int8", 1),
    ("UCharArray", "Uint8", 1),
    ("Int16Array", "Int16", 2),
    ("UInt16Array", "Uint16", 2),
    ("Int32Array", "Int32", 4),
    ("UInt32Array", "Uint32", 4),
    # ("Int64Array", "Int16"), not implemented
    # ("UInt64Array", "Uint16"), not implemented
    ("FloatArray", "Float32", 4),
    ("DoubleArray", "Float64", 8),
]

print(wasm_array_string)
print(struct_array_string)
for primitive_array_metadata in primitive_array_classes_metadata:
    print(generate_primitive_array_class(primitive_array_metadata))
