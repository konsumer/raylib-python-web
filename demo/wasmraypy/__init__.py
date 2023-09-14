
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

class WasmArray:
    """Generic array-like collection that uses wasm as memory-back"""
    
    def __init__(self, item_size: int, length: int, address: int = 0):
        self._length = length
        self._item_size = item_size
        self._size = self._item_size * self._length
        if address != 0:
            self._address: int = address
            self._to_free: bool = False
        else:
            self._address: int = _mod._malloc(self._size)
            self._to_free: bool = True

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

    def __len__(self):
        return self._length

    def __str__(self):
        out = "WasmArray["
        out += ', '.join([str(self[i]) for i in range(self._length)])
        out += "] " + hex(self._address)
        return out


class StructArray(WasmArray):
    """an array of structs"""
    def __init__(self, stype, length, address: int = 0):
        super(StructArray, self).__init__(stype._size, length, address)
        self._stype = stype

    def __getitem__(self, item):
        return self._stype(address=(self._address + (self._item_size * item)))

    def __setitem__(self, item, value):
        struct_clone(value, self._address + (self._item_size * item))
    
class CharArray(WasmArray):
    def __init__(self, length, address: int = 0):
        super(CharArray, self).__init__(1, length, address)

    def __getitem__(self, item):
        return _mod.mem.getInt8(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt8(self._address + (item * self._item_size), value, True)


class UCharArray(WasmArray):
    def __init__(self, length, address: int = 0):
        super(UCharArray, self).__init__(1, length, address)

    def __getitem__(self, item):
        return _mod.mem.getUint8(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint8(self._address + (item * self._item_size), value, True)


class Int16Array(WasmArray):
    def __init__(self, length, address: int = 0):
        super(Int16Array, self).__init__(2, length, address)

    def __getitem__(self, item):
        return _mod.mem.getInt16(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt16(self._address + (item * self._item_size), value, True)


class UInt16Array(WasmArray):
    def __init__(self, length, address: int = 0):
        super(UInt16Array, self).__init__(2, length, address)

    def __getitem__(self, item):
        return _mod.mem.getUint16(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint16(self._address + (item * self._item_size), value, True)


class Int32Array(WasmArray):
    def __init__(self, length, address: int = 0):
        super(Int32Array, self).__init__(4, length, address)

    def __getitem__(self, item):
        return _mod.mem.getInt32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt32(self._address + (item * self._item_size), value, True)


class UInt32Array(WasmArray):
    def __init__(self, length, address: int = 0):
        super(UInt32Array, self).__init__(4, length, address)

    def __getitem__(self, item):
        return _mod.mem.getUint32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint32(self._address + (item * self._item_size), value, True)


class FloatArray(WasmArray):
    def __init__(self, length, address: int = 0):
        super(FloatArray, self).__init__(4, length, address)

    def __getitem__(self, item):
        return _mod.mem.getFloat32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setFloat32(self._address + (item * self._item_size), value, True)


class DoubleArray(WasmArray):
    def __init__(self, length, address: int = 0):
        super(DoubleArray, self).__init__(8, length, address)

    def __getitem__(self, item):
        return _mod.mem.getFloat64(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setFloat64(self._address + (item * self._item_size), value, True)


class Vector2:
    """Vector2, 2 components"""

    _size: int = 8

    def __init__(self, x: float = 0.0, y: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(8)
            self._to_free = True
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0, True)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value, True)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4, True)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value, True)

    def __str__(self):
        return f"Vector2(address={self._address}, {self.x}, {self.y})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Vector3:
    """Vector3, 3 components"""

    _size: int = 12

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(12)
            self._to_free = True
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, z)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0, True)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value, True)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4, True)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value, True)

    @property
    def z(self):
        return _mod.mem.getFloat32(self._address + 8, True)

    @z.setter
    def z(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value, True)

    def __str__(self):
        return f"Vector3(address={self._address}, {self.x}, {self.y}, {self.z})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Vector4:
    """Vector4, 4 components"""

    _size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(16)
            self._to_free = True
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, z)
            _mod.mem.setFloat32(self._address + 12, w)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0, True)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value, True)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4, True)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value, True)

    @property
    def z(self):
        return _mod.mem.getFloat32(self._address + 8, True)

    @z.setter
    def z(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value, True)

    @property
    def w(self):
        return _mod.mem.getFloat32(self._address + 12, True)

    @w.setter
    def w(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value, True)

    def __str__(self):
        return f"Vector4(address={self._address}, {self.x}, {self.y}, {self.z}, {self.w})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

Quaternion = Vector4

class Matrix:
    """Matrix, 4x4 components, column major, OpenGL style, right-handed"""

    _size: int = 64

    def __init__(self, m0: float = 0.0, m4: float = 0.0, m8: float = 0.0, m12: float = 0.0, m1: float = 0.0, m5: float = 0.0, m9: float = 0.0, m13: float = 0.0, m2: float = 0.0, m6: float = 0.0, m10: float = 0.0, m14: float = 0.0, m3: float = 0.0, m7: float = 0.0, m11: float = 0.0, m15: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(64)
            self._to_free = True
            _mod.mem.setFloat32(self._address + 0, m0)
            _mod.mem.setFloat32(self._address + 4, m4)
            _mod.mem.setFloat32(self._address + 8, m8)
            _mod.mem.setFloat32(self._address + 12, m12)
            _mod.mem.setFloat32(self._address + 16, m1)
            _mod.mem.setFloat32(self._address + 20, m5)
            _mod.mem.setFloat32(self._address + 24, m9)
            _mod.mem.setFloat32(self._address + 28, m13)
            _mod.mem.setFloat32(self._address + 32, m2)
            _mod.mem.setFloat32(self._address + 36, m6)
            _mod.mem.setFloat32(self._address + 40, m10)
            _mod.mem.setFloat32(self._address + 44, m14)
            _mod.mem.setFloat32(self._address + 48, m3)
            _mod.mem.setFloat32(self._address + 52, m7)
            _mod.mem.setFloat32(self._address + 56, m11)
            _mod.mem.setFloat32(self._address + 60, m15)

    @property
    def m0(self):
        return _mod.mem.getFloat32(self._address + 0, True)

    @m0.setter
    def m0(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value, True)

    @property
    def m4(self):
        return _mod.mem.getFloat32(self._address + 4, True)

    @m4.setter
    def m4(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value, True)

    @property
    def m8(self):
        return _mod.mem.getFloat32(self._address + 8, True)

    @m8.setter
    def m8(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value, True)

    @property
    def m12(self):
        return _mod.mem.getFloat32(self._address + 12, True)

    @m12.setter
    def m12(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value, True)

    @property
    def m1(self):
        return _mod.mem.getFloat32(self._address + 16, True)

    @m1.setter
    def m1(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 16, value, True)

    @property
    def m5(self):
        return _mod.mem.getFloat32(self._address + 20, True)

    @m5.setter
    def m5(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 20, value, True)

    @property
    def m9(self):
        return _mod.mem.getFloat32(self._address + 24, True)

    @m9.setter
    def m9(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 24, value, True)

    @property
    def m13(self):
        return _mod.mem.getFloat32(self._address + 28, True)

    @m13.setter
    def m13(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 28, value, True)

    @property
    def m2(self):
        return _mod.mem.getFloat32(self._address + 32, True)

    @m2.setter
    def m2(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 32, value, True)

    @property
    def m6(self):
        return _mod.mem.getFloat32(self._address + 36, True)

    @m6.setter
    def m6(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 36, value, True)

    @property
    def m10(self):
        return _mod.mem.getFloat32(self._address + 40, True)

    @m10.setter
    def m10(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 40, value, True)

    @property
    def m14(self):
        return _mod.mem.getFloat32(self._address + 44, True)

    @m14.setter
    def m14(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 44, value, True)

    @property
    def m3(self):
        return _mod.mem.getFloat32(self._address + 48, True)

    @m3.setter
    def m3(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 48, value, True)

    @property
    def m7(self):
        return _mod.mem.getFloat32(self._address + 52, True)

    @m7.setter
    def m7(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 52, value, True)

    @property
    def m11(self):
        return _mod.mem.getFloat32(self._address + 56, True)

    @m11.setter
    def m11(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 56, value, True)

    @property
    def m15(self):
        return _mod.mem.getFloat32(self._address + 60, True)

    @m15.setter
    def m15(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 60, value, True)

    def __str__(self):
        return f"Matrix(address={self._address}, {self.m0}, {self.m4}, {self.m8}, {self.m12}, {self.m1}, {self.m5}, {self.m9}, {self.m13}, {self.m2}, {self.m6}, {self.m10}, {self.m14}, {self.m3}, {self.m7}, {self.m11}, {self.m15})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Color:
    """Color, 4 components, R8G8B8A8 (32bit)"""

    _size: int = 4

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(4)
            self._to_free = True
            _mod.mem.setUint8(self._address + 0, r)
            _mod.mem.setUint8(self._address + 1, g)
            _mod.mem.setUint8(self._address + 2, b)
            _mod.mem.setUint8(self._address + 3, a)

    @property
    def r(self):
        return _mod.mem.getUint8(self._address + 0, True)

    @r.setter
    def r(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 0, value, True)

    @property
    def g(self):
        return _mod.mem.getUint8(self._address + 1, True)

    @g.setter
    def g(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 1, value, True)

    @property
    def b(self):
        return _mod.mem.getUint8(self._address + 2, True)

    @b.setter
    def b(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 2, value, True)

    @property
    def a(self):
        return _mod.mem.getUint8(self._address + 3, True)

    @a.setter
    def a(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 3, value, True)

    def __str__(self):
        return f"Color(address={self._address}, {self.r}, {self.g}, {self.b}, {self.a})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Rectangle:
    """Rectangle, 4 components"""

    _size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(16)
            self._to_free = True
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, width)
            _mod.mem.setFloat32(self._address + 12, height)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0, True)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value, True)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4, True)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value, True)

    @property
    def width(self):
        return _mod.mem.getFloat32(self._address + 8, True)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value, True)

    @property
    def height(self):
        return _mod.mem.getFloat32(self._address + 12, True)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value, True)

    def __str__(self):
        return f"Rectangle(address={self._address}, {self.x}, {self.y}, {self.width}, {self.height})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Image:
    """Image, pixel data stored in CPU memory (RAM)"""

    _size: int = 20

    def __init__(self, data: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(20)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, data)
            _mod.mem.setInt32(self._address + 4, width)
            _mod.mem.setInt32(self._address + 8, height)
            _mod.mem.setInt32(self._address + 12, mipmaps)
            _mod.mem.setInt32(self._address + 16, format)

    @property
    def data(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @data.setter
    def data(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def width(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def height(self):
        return _mod.mem.getInt32(self._address + 8, True)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value, True)

    @property
    def mipmaps(self):
        return _mod.mem.getInt32(self._address + 12, True)

    @mipmaps.setter
    def mipmaps(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value, True)

    @property
    def format(self):
        return _mod.mem.getInt32(self._address + 16, True)

    @format.setter
    def format(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value, True)

    def __str__(self):
        return f"Image(address={self._address}, {self.data}, {self.width}, {self.height}, {self.mipmaps}, {self.format})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Texture:
    """Texture, tex data stored in GPU memory (VRAM)"""

    _size: int = 20

    def __init__(self, id: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(20)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, id)
            _mod.mem.setInt32(self._address + 4, width)
            _mod.mem.setInt32(self._address + 8, height)
            _mod.mem.setInt32(self._address + 12, mipmaps)
            _mod.mem.setInt32(self._address + 16, format)

    @property
    def id(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def width(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def height(self):
        return _mod.mem.getInt32(self._address + 8, True)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value, True)

    @property
    def mipmaps(self):
        return _mod.mem.getInt32(self._address + 12, True)

    @mipmaps.setter
    def mipmaps(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value, True)

    @property
    def format(self):
        return _mod.mem.getInt32(self._address + 16, True)

    @format.setter
    def format(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value, True)

    def __str__(self):
        return f"Texture(address={self._address}, {self.id}, {self.width}, {self.height}, {self.mipmaps}, {self.format})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

Texture2D = Texture

TextureCubemap = Texture

class RenderTexture:
    """RenderTexture, fbo for texture rendering"""

    _size: int = 44

    def __init__(self, id: int = 0, texture: Texture = None, depth: Texture = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(44)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, id)
            if texture is not None:
                struct_clone(texture, self._address + 4)
            if depth is not None:
                struct_clone(depth, self._address + 24)

    @property
    def id(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def texture(self):
        return Texture(0, address=self._address + 4)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 4)

    @property
    def depth(self):
        return Texture(0, address=self._address + 24)

    @depth.setter
    def depth(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 24)

    def __str__(self):
        return f"RenderTexture(address={self._address}, {self.id}, {self.texture}, {self.depth})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

RenderTexture2D = RenderTexture

class NPatchInfo:
    """NPatchInfo, n-patch layout info"""

    _size: int = 36

    def __init__(self, source: Rectangle = None, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0, layout: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(36)
            self._to_free = True
            if source is not None:
                struct_clone(source, self._address + 0)
            _mod.mem.setInt32(self._address + 16, left)
            _mod.mem.setInt32(self._address + 20, top)
            _mod.mem.setInt32(self._address + 24, right)
            _mod.mem.setInt32(self._address + 28, bottom)
            _mod.mem.setInt32(self._address + 32, layout)

    @property
    def source(self):
        return Rectangle(0, address=self._address + 0)

    @source.setter
    def source(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def left(self):
        return _mod.mem.getInt32(self._address + 16, True)

    @left.setter
    def left(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value, True)

    @property
    def top(self):
        return _mod.mem.getInt32(self._address + 20, True)

    @top.setter
    def top(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 20, value, True)

    @property
    def right(self):
        return _mod.mem.getInt32(self._address + 24, True)

    @right.setter
    def right(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 24, value, True)

    @property
    def bottom(self):
        return _mod.mem.getInt32(self._address + 28, True)

    @bottom.setter
    def bottom(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 28, value, True)

    @property
    def layout(self):
        return _mod.mem.getInt32(self._address + 32, True)

    @layout.setter
    def layout(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 32, value, True)

    def __str__(self):
        return f"NPatchInfo(address={self._address}, {self.source}, {self.left}, {self.top}, {self.right}, {self.bottom}, {self.layout})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class GlyphInfo:
    """GlyphInfo, font characters glyphs info"""

    _size: int = 36

    def __init__(self, value: int = 0, offsetX: int = 0, offsetY: int = 0, advanceX: int = 0, image: Image = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(36)
            self._to_free = True
            _mod.mem.setInt32(self._address + 0, value)
            _mod.mem.setInt32(self._address + 4, offsetX)
            _mod.mem.setInt32(self._address + 8, offsetY)
            _mod.mem.setInt32(self._address + 12, advanceX)
            if image is not None:
                struct_clone(image, self._address + 16)

    @property
    def value(self):
        return _mod.mem.getInt32(self._address + 0, True)

    @value.setter
    def value(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value, True)

    @property
    def offsetX(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @offsetX.setter
    def offsetX(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def offsetY(self):
        return _mod.mem.getInt32(self._address + 8, True)

    @offsetY.setter
    def offsetY(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value, True)

    @property
    def advanceX(self):
        return _mod.mem.getInt32(self._address + 12, True)

    @advanceX.setter
    def advanceX(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value, True)

    @property
    def image(self):
        return Image(0, address=self._address + 16)

    @image.setter
    def image(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 16)

    def __str__(self):
        return f"GlyphInfo(address={self._address}, {self.value}, {self.offsetX}, {self.offsetY}, {self.advanceX}, {self.image})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Font:
    """Font, font texture and GlyphInfo array data"""

    _size: int = 40

    def __init__(self, baseSize: int = 0, glyphCount: int = 0, glyphPadding: int = 0, texture: Texture2D = None, recs: int = 0, glyphs: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(40)
            self._to_free = True
            _mod.mem.setInt32(self._address + 0, baseSize)
            _mod.mem.setInt32(self._address + 4, glyphCount)
            _mod.mem.setInt32(self._address + 8, glyphPadding)
            if texture is not None:
                struct_clone(texture, self._address + 12)
            _mod.mem.setUint32(self._address + 32, recs)
            _mod.mem.setUint32(self._address + 36, glyphs)

    @property
    def baseSize(self):
        return _mod.mem.getInt32(self._address + 0, True)

    @baseSize.setter
    def baseSize(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value, True)

    @property
    def glyphCount(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @glyphCount.setter
    def glyphCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def glyphPadding(self):
        return _mod.mem.getInt32(self._address + 8, True)

    @glyphPadding.setter
    def glyphPadding(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value, True)

    @property
    def texture(self):
        return Texture2D(0, address=self._address + 12)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def recs(self):
        return _mod.mem.getUint32(self._address + 32, True)

    @recs.setter
    def recs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 32, value, True)

    @property
    def glyphs(self):
        return _mod.mem.getUint32(self._address + 36, True)

    @glyphs.setter
    def glyphs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 36, value, True)

    def __str__(self):
        return f"Font(address={self._address}, {self.baseSize}, {self.glyphCount}, {self.glyphPadding}, {self.texture}, {self.recs}, {self.glyphs})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Camera3D:
    """Camera, defines position/orientation in 3d space"""

    _size: int = 44

    def __init__(self, position: Vector3 = None, target: Vector3 = None, up: Vector3 = None, fovy: float = 0.0, projection: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(44)
            self._to_free = True
            if position is not None:
                struct_clone(position, self._address + 0)
            if target is not None:
                struct_clone(target, self._address + 12)
            if up is not None:
                struct_clone(up, self._address + 24)
            _mod.mem.setFloat32(self._address + 36, fovy)
            _mod.mem.setInt32(self._address + 40, projection)

    @property
    def position(self):
        return Vector3(0, address=self._address + 0)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector3(0, address=self._address + 12)

    @target.setter
    def target(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def up(self):
        return Vector3(0, address=self._address + 24)

    @up.setter
    def up(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 24)

    @property
    def fovy(self):
        return _mod.mem.getFloat32(self._address + 36, True)

    @fovy.setter
    def fovy(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 36, value, True)

    @property
    def projection(self):
        return _mod.mem.getInt32(self._address + 40, True)

    @projection.setter
    def projection(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 40, value, True)

    def __str__(self):
        return f"Camera3D(address={self._address}, {self.position}, {self.target}, {self.up}, {self.fovy}, {self.projection})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

Camera = Camera3D

class Camera2D:
    """Camera2D, defines position/orientation in 2d space"""

    _size: int = 24

    def __init__(self, offset: Vector2 = None, target: Vector2 = None, rotation: float = 0.0, zoom: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(24)
            self._to_free = True
            if offset is not None:
                struct_clone(offset, self._address + 0)
            if target is not None:
                struct_clone(target, self._address + 8)
            _mod.mem.setFloat32(self._address + 16, rotation)
            _mod.mem.setFloat32(self._address + 20, zoom)

    @property
    def offset(self):
        return Vector2(0, address=self._address + 0)

    @offset.setter
    def offset(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector2(0, address=self._address + 8)

    @target.setter
    def target(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 8)

    @property
    def rotation(self):
        return _mod.mem.getFloat32(self._address + 16, True)

    @rotation.setter
    def rotation(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 16, value, True)

    @property
    def zoom(self):
        return _mod.mem.getFloat32(self._address + 20, True)

    @zoom.setter
    def zoom(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 20, value, True)

    def __str__(self):
        return f"Camera2D(address={self._address}, {self.offset}, {self.target}, {self.rotation}, {self.zoom})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Mesh:
    """Mesh, vertex data and vao/vbo"""

    _size: int = 60

    def __init__(self, vertexCount: int = 0, triangleCount: int = 0, vertices: int = 0, texcoords: int = 0, texcoords2: int = 0, normals: int = 0, tangents: int = 0, colors: int = 0, indices: int = 0, animVertices: int = 0, animNormals: int = 0, boneIds: int = 0, boneWeights: int = 0, vaoId: int = 0, vboId: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(60)
            self._to_free = True
            _mod.mem.setInt32(self._address + 0, vertexCount)
            _mod.mem.setInt32(self._address + 4, triangleCount)
            _mod.mem.setUint32(self._address + 8, vertices)
            _mod.mem.setUint32(self._address + 12, texcoords)
            _mod.mem.setUint32(self._address + 16, texcoords2)
            _mod.mem.setUint32(self._address + 20, normals)
            _mod.mem.setUint32(self._address + 24, tangents)
            _mod.mem.setUint32(self._address + 28, colors)
            _mod.mem.setUint32(self._address + 32, indices)
            _mod.mem.setUint32(self._address + 36, animVertices)
            _mod.mem.setUint32(self._address + 40, animNormals)
            _mod.mem.setUint32(self._address + 44, boneIds)
            _mod.mem.setUint32(self._address + 48, boneWeights)
            _mod.mem.setUint32(self._address + 52, vaoId)
            _mod.mem.setUint32(self._address + 56, vboId)

    @property
    def vertexCount(self):
        return _mod.mem.getInt32(self._address + 0, True)

    @vertexCount.setter
    def vertexCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value, True)

    @property
    def triangleCount(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @triangleCount.setter
    def triangleCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def vertices(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @vertices.setter
    def vertices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    @property
    def texcoords(self):
        return _mod.mem.getUint32(self._address + 12, True)

    @texcoords.setter
    def texcoords(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value, True)

    @property
    def texcoords2(self):
        return _mod.mem.getUint32(self._address + 16, True)

    @texcoords2.setter
    def texcoords2(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value, True)

    @property
    def normals(self):
        return _mod.mem.getUint32(self._address + 20, True)

    @normals.setter
    def normals(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value, True)

    @property
    def tangents(self):
        return _mod.mem.getUint32(self._address + 24, True)

    @tangents.setter
    def tangents(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 24, value, True)

    @property
    def colors(self):
        return _mod.mem.getUint32(self._address + 28, True)

    @colors.setter
    def colors(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 28, value, True)

    @property
    def indices(self):
        return _mod.mem.getUint32(self._address + 32, True)

    @indices.setter
    def indices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 32, value, True)

    @property
    def animVertices(self):
        return _mod.mem.getUint32(self._address + 36, True)

    @animVertices.setter
    def animVertices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 36, value, True)

    @property
    def animNormals(self):
        return _mod.mem.getUint32(self._address + 40, True)

    @animNormals.setter
    def animNormals(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 40, value, True)

    @property
    def boneIds(self):
        return _mod.mem.getUint32(self._address + 44, True)

    @boneIds.setter
    def boneIds(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 44, value, True)

    @property
    def boneWeights(self):
        return _mod.mem.getUint32(self._address + 48, True)

    @boneWeights.setter
    def boneWeights(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 48, value, True)

    @property
    def vaoId(self):
        return _mod.mem.getUint32(self._address + 52, True)

    @vaoId.setter
    def vaoId(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 52, value, True)

    @property
    def vboId(self):
        return _mod.mem.getUint32(self._address + 56, True)

    @vboId.setter
    def vboId(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 56, value, True)

    def __str__(self):
        return f"Mesh(address={self._address}, {self.vertexCount}, {self.triangleCount}, {self.vertices}, {self.texcoords}, {self.texcoords2}, {self.normals}, {self.tangents}, {self.colors}, {self.indices}, {self.animVertices}, {self.animNormals}, {self.boneIds}, {self.boneWeights}, {self.vaoId}, {self.vboId})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Shader:
    """Shader"""

    _size: int = 8

    def __init__(self, id: int = 0, locs: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(8)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, id)
            _mod.mem.setUint32(self._address + 4, locs)

    @property
    def id(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def locs(self):
        return _mod.mem.getUint32(self._address + 4, True)

    @locs.setter
    def locs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value, True)

    def __str__(self):
        return f"Shader(address={self._address}, {self.id}, {self.locs})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class MaterialMap:
    """MaterialMap"""

    _size: int = 28

    def __init__(self, texture: Texture2D = None, color: Color = None, value: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(28)
            self._to_free = True
            if texture is not None:
                struct_clone(texture, self._address + 0)
            if color is not None:
                struct_clone(color, self._address + 20)
            _mod.mem.setFloat32(self._address + 24, value)

    @property
    def texture(self):
        return Texture2D(0, address=self._address + 0)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def color(self):
        return Color(0, address=self._address + 20)

    @color.setter
    def color(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 20)

    @property
    def value(self):
        return _mod.mem.getFloat32(self._address + 24, True)

    @value.setter
    def value(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 24, value, True)

    def __str__(self):
        return f"MaterialMap(address={self._address}, {self.texture}, {self.color}, {self.value})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Material:
    """Material, includes shader and maps"""

    _size: int = 28

    def __init__(self, shader: Shader = None, maps: int = 0, params: FloatArray = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(28)
            self._to_free = True
            if shader is not None:
                struct_clone(shader, self._address + 0)
            _mod.mem.setUint32(self._address + 8, maps)
            if params is not None:
                struct_clone(params, self._address + 12)

    @property
    def shader(self):
        return Shader(0, address=self._address + 0)

    @shader.setter
    def shader(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def maps(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @maps.setter
    def maps(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    @property
    def params(self):
        return FloatArray(4, address=self._address + 12)

    @params.setter
    def params(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"Material(address={self._address}, {self.shader}, {self.maps}, {self.params})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Transform:
    """Transform, vertex transformation data"""

    _size: int = 40

    def __init__(self, translation: Vector3 = None, rotation: Quaternion = None, scale: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(40)
            self._to_free = True
            if translation is not None:
                struct_clone(translation, self._address + 0)
            if rotation is not None:
                struct_clone(rotation, self._address + 12)
            if scale is not None:
                struct_clone(scale, self._address + 28)

    @property
    def translation(self):
        return Vector3(0, address=self._address + 0)

    @translation.setter
    def translation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def rotation(self):
        return Quaternion(0, address=self._address + 12)

    @rotation.setter
    def rotation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def scale(self):
        return Vector3(0, address=self._address + 28)

    @scale.setter
    def scale(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 28)

    def __str__(self):
        return f"Transform(address={self._address}, {self.translation}, {self.rotation}, {self.scale})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class BoneInfo:
    """Bone, skeletal animation bone"""

    _size: int = 36

    def __init__(self, name: CharArray = None, parent: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(36)
            self._to_free = True
            if name is not None:
                struct_clone(name, self._address + 0)
            _mod.mem.setInt32(self._address + 32, parent)

    @property
    def name(self):
        return CharArray(32, address=self._address + 0)

    @name.setter
    def name(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def parent(self):
        return _mod.mem.getInt32(self._address + 32, True)

    @parent.setter
    def parent(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 32, value, True)

    def __str__(self):
        return f"BoneInfo(address={self._address}, {self.name}, {self.parent})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Model:
    """Model, meshes, materials and animation data"""

    _size: int = 96

    def __init__(self, transform: Matrix = None, meshCount: int = 0, materialCount: int = 0, meshes: int = 0, materials: int = 0, meshMaterial: int = 0, boneCount: int = 0, bones: int = 0, bindPose: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(96)
            self._to_free = True
            if transform is not None:
                struct_clone(transform, self._address + 0)
            _mod.mem.setInt32(self._address + 64, meshCount)
            _mod.mem.setInt32(self._address + 68, materialCount)
            _mod.mem.setUint32(self._address + 72, meshes)
            _mod.mem.setUint32(self._address + 76, materials)
            _mod.mem.setUint32(self._address + 80, meshMaterial)
            _mod.mem.setInt32(self._address + 84, boneCount)
            _mod.mem.setUint32(self._address + 88, bones)
            _mod.mem.setUint32(self._address + 92, bindPose)

    @property
    def transform(self):
        return Matrix(0, address=self._address + 0)

    @transform.setter
    def transform(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def meshCount(self):
        return _mod.mem.getInt32(self._address + 64, True)

    @meshCount.setter
    def meshCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 64, value, True)

    @property
    def materialCount(self):
        return _mod.mem.getInt32(self._address + 68, True)

    @materialCount.setter
    def materialCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 68, value, True)

    @property
    def meshes(self):
        return _mod.mem.getUint32(self._address + 72, True)

    @meshes.setter
    def meshes(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 72, value, True)

    @property
    def materials(self):
        return _mod.mem.getUint32(self._address + 76, True)

    @materials.setter
    def materials(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 76, value, True)

    @property
    def meshMaterial(self):
        return _mod.mem.getUint32(self._address + 80, True)

    @meshMaterial.setter
    def meshMaterial(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 80, value, True)

    @property
    def boneCount(self):
        return _mod.mem.getInt32(self._address + 84, True)

    @boneCount.setter
    def boneCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 84, value, True)

    @property
    def bones(self):
        return _mod.mem.getUint32(self._address + 88, True)

    @bones.setter
    def bones(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 88, value, True)

    @property
    def bindPose(self):
        return _mod.mem.getUint32(self._address + 92, True)

    @bindPose.setter
    def bindPose(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 92, value, True)

    def __str__(self):
        return f"Model(address={self._address}, {self.transform}, {self.meshCount}, {self.materialCount}, {self.meshes}, {self.materials}, {self.meshMaterial}, {self.boneCount}, {self.bones}, {self.bindPose})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class ModelAnimation:
    """ModelAnimation"""

    _size: int = 48

    def __init__(self, boneCount: int = 0, frameCount: int = 0, bones: int = 0, framePoses: int = 0, name: CharArray = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(48)
            self._to_free = True
            _mod.mem.setInt32(self._address + 0, boneCount)
            _mod.mem.setInt32(self._address + 4, frameCount)
            _mod.mem.setUint32(self._address + 8, bones)
            _mod.mem.setUint32(self._address + 12, framePoses)
            if name is not None:
                struct_clone(name, self._address + 16)

    @property
    def boneCount(self):
        return _mod.mem.getInt32(self._address + 0, True)

    @boneCount.setter
    def boneCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value, True)

    @property
    def frameCount(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def bones(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @bones.setter
    def bones(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    @property
    def framePoses(self):
        return _mod.mem.getUint32(self._address + 12, True)

    @framePoses.setter
    def framePoses(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value, True)

    @property
    def name(self):
        return CharArray(32, address=self._address + 16)

    @name.setter
    def name(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 16)

    def __str__(self):
        return f"ModelAnimation(address={self._address}, {self.boneCount}, {self.frameCount}, {self.bones}, {self.framePoses}, {self.name})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Ray:
    """Ray, ray for raycasting"""

    _size: int = 24

    def __init__(self, position: Vector3 = None, direction: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(24)
            self._to_free = True
            if position is not None:
                struct_clone(position, self._address + 0)
            if direction is not None:
                struct_clone(direction, self._address + 12)

    @property
    def position(self):
        return Vector3(0, address=self._address + 0)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def direction(self):
        return Vector3(0, address=self._address + 12)

    @direction.setter
    def direction(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"Ray(address={self._address}, {self.position}, {self.direction})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class RayCollision:
    """RayCollision, ray hit information"""

    _size: int = 29

    def __init__(self, hit: int = 0, distance: float = 0.0, point: Vector3 = None, normal: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(29)
            self._to_free = True
            _mod.mem.setInt8(self._address + 0, hit)
            _mod.mem.setFloat32(self._address + 1, distance)
            if point is not None:
                struct_clone(point, self._address + 5)
            if normal is not None:
                struct_clone(normal, self._address + 17)

    @property
    def hit(self):
        return _mod.mem.getInt8(self._address + 0, True)

    @hit.setter
    def hit(self, value):
        if not self._frozen:
            _mod.mem.setInt8(self._address + 0, value, True)

    @property
    def distance(self):
        return _mod.mem.getFloat32(self._address + 1, True)

    @distance.setter
    def distance(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 1, value, True)

    @property
    def point(self):
        return Vector3(0, address=self._address + 5)

    @point.setter
    def point(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 5)

    @property
    def normal(self):
        return Vector3(0, address=self._address + 17)

    @normal.setter
    def normal(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 17)

    def __str__(self):
        return f"RayCollision(address={self._address}, {self.hit}, {self.distance}, {self.point}, {self.normal})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class BoundingBox:
    """BoundingBox"""

    _size: int = 24

    def __init__(self, min: Vector3 = None, max: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(24)
            self._to_free = True
            if min is not None:
                struct_clone(min, self._address + 0)
            if max is not None:
                struct_clone(max, self._address + 12)

    @property
    def min(self):
        return Vector3(0, address=self._address + 0)

    @min.setter
    def min(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def max(self):
        return Vector3(0, address=self._address + 12)

    @max.setter
    def max(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"BoundingBox(address={self._address}, {self.min}, {self.max})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Wave:
    """Wave, audio wave data"""

    _size: int = 20

    def __init__(self, frameCount: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0, data: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(20)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, frameCount)
            _mod.mem.setUint32(self._address + 4, sampleRate)
            _mod.mem.setUint32(self._address + 8, sampleSize)
            _mod.mem.setUint32(self._address + 12, channels)
            _mod.mem.setUint32(self._address + 16, data)

    @property
    def frameCount(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def sampleRate(self):
        return _mod.mem.getUint32(self._address + 4, True)

    @sampleRate.setter
    def sampleRate(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value, True)

    @property
    def sampleSize(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @sampleSize.setter
    def sampleSize(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    @property
    def channels(self):
        return _mod.mem.getUint32(self._address + 12, True)

    @channels.setter
    def channels(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value, True)

    @property
    def data(self):
        return _mod.mem.getUint32(self._address + 16, True)

    @data.setter
    def data(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value, True)

    def __str__(self):
        return f"Wave(address={self._address}, {self.frameCount}, {self.sampleRate}, {self.sampleSize}, {self.channels}, {self.data})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class AudioStream:
    """AudioStream, custom audio stream"""

    _size: int = 20

    def __init__(self, buffer: int = 0, processor: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(20)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, buffer)
            _mod.mem.setUint32(self._address + 4, processor)
            _mod.mem.setUint32(self._address + 8, sampleRate)
            _mod.mem.setUint32(self._address + 12, sampleSize)
            _mod.mem.setUint32(self._address + 16, channels)

    @property
    def buffer(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @buffer.setter
    def buffer(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def processor(self):
        return _mod.mem.getUint32(self._address + 4, True)

    @processor.setter
    def processor(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value, True)

    @property
    def sampleRate(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @sampleRate.setter
    def sampleRate(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    @property
    def sampleSize(self):
        return _mod.mem.getUint32(self._address + 12, True)

    @sampleSize.setter
    def sampleSize(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value, True)

    @property
    def channels(self):
        return _mod.mem.getUint32(self._address + 16, True)

    @channels.setter
    def channels(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value, True)

    def __str__(self):
        return f"AudioStream(address={self._address}, {self.buffer}, {self.processor}, {self.sampleRate}, {self.sampleSize}, {self.channels})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Sound:
    """Sound"""

    _size: int = 24

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(24)
            self._to_free = True
            if stream is not None:
                struct_clone(stream, self._address + 0)
            _mod.mem.setUint32(self._address + 20, frameCount)

    @property
    def stream(self):
        return AudioStream(0, address=self._address + 0)

    @stream.setter
    def stream(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def frameCount(self):
        return _mod.mem.getUint32(self._address + 20, True)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value, True)

    def __str__(self):
        return f"Sound(address={self._address}, {self.stream}, {self.frameCount})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class Music:
    """Music, audio stream, anything longer than ~10 seconds should be streamed"""

    _size: int = 33

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, looping: int = 0, ctxType: int = 0, ctxData: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(33)
            self._to_free = True
            if stream is not None:
                struct_clone(stream, self._address + 0)
            _mod.mem.setUint32(self._address + 20, frameCount)
            _mod.mem.setInt8(self._address + 24, looping)
            _mod.mem.setInt32(self._address + 25, ctxType)
            _mod.mem.setUint32(self._address + 29, ctxData)

    @property
    def stream(self):
        return AudioStream(0, address=self._address + 0)

    @stream.setter
    def stream(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def frameCount(self):
        return _mod.mem.getUint32(self._address + 20, True)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value, True)

    @property
    def looping(self):
        return _mod.mem.getInt8(self._address + 24, True)

    @looping.setter
    def looping(self, value):
        if not self._frozen:
            _mod.mem.setInt8(self._address + 24, value, True)

    @property
    def ctxType(self):
        return _mod.mem.getInt32(self._address + 25, True)

    @ctxType.setter
    def ctxType(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 25, value, True)

    @property
    def ctxData(self):
        return _mod.mem.getUint32(self._address + 29, True)

    @ctxData.setter
    def ctxData(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 29, value, True)

    def __str__(self):
        return f"Music(address={self._address}, {self.stream}, {self.frameCount}, {self.looping}, {self.ctxType}, {self.ctxData})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class VrDeviceInfo:
    """VrDeviceInfo, Head-Mounted-Display device parameters"""

    _size: int = 64

    def __init__(self, hResolution: int = 0, vResolution: int = 0, hScreenSize: float = 0.0, vScreenSize: float = 0.0, vScreenCenter: float = 0.0, eyeToScreenDistance: float = 0.0, lensSeparationDistance: float = 0.0, interpupillaryDistance: float = 0.0, lensDistortionValues: FloatArray = None, chromaAbCorrection: FloatArray = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(64)
            self._to_free = True
            _mod.mem.setInt32(self._address + 0, hResolution)
            _mod.mem.setInt32(self._address + 4, vResolution)
            _mod.mem.setFloat32(self._address + 8, hScreenSize)
            _mod.mem.setFloat32(self._address + 12, vScreenSize)
            _mod.mem.setFloat32(self._address + 16, vScreenCenter)
            _mod.mem.setFloat32(self._address + 20, eyeToScreenDistance)
            _mod.mem.setFloat32(self._address + 24, lensSeparationDistance)
            _mod.mem.setFloat32(self._address + 28, interpupillaryDistance)
            if lensDistortionValues is not None:
                struct_clone(lensDistortionValues, self._address + 32)
            if chromaAbCorrection is not None:
                struct_clone(chromaAbCorrection, self._address + 48)

    @property
    def hResolution(self):
        return _mod.mem.getInt32(self._address + 0, True)

    @hResolution.setter
    def hResolution(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value, True)

    @property
    def vResolution(self):
        return _mod.mem.getInt32(self._address + 4, True)

    @vResolution.setter
    def vResolution(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value, True)

    @property
    def hScreenSize(self):
        return _mod.mem.getFloat32(self._address + 8, True)

    @hScreenSize.setter
    def hScreenSize(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value, True)

    @property
    def vScreenSize(self):
        return _mod.mem.getFloat32(self._address + 12, True)

    @vScreenSize.setter
    def vScreenSize(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value, True)

    @property
    def vScreenCenter(self):
        return _mod.mem.getFloat32(self._address + 16, True)

    @vScreenCenter.setter
    def vScreenCenter(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 16, value, True)

    @property
    def eyeToScreenDistance(self):
        return _mod.mem.getFloat32(self._address + 20, True)

    @eyeToScreenDistance.setter
    def eyeToScreenDistance(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 20, value, True)

    @property
    def lensSeparationDistance(self):
        return _mod.mem.getFloat32(self._address + 24, True)

    @lensSeparationDistance.setter
    def lensSeparationDistance(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 24, value, True)

    @property
    def interpupillaryDistance(self):
        return _mod.mem.getFloat32(self._address + 28, True)

    @interpupillaryDistance.setter
    def interpupillaryDistance(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 28, value, True)

    @property
    def lensDistortionValues(self):
        return FloatArray(4, address=self._address + 32)

    @lensDistortionValues.setter
    def lensDistortionValues(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 32)

    @property
    def chromaAbCorrection(self):
        return FloatArray(4, address=self._address + 48)

    @chromaAbCorrection.setter
    def chromaAbCorrection(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 48)

    def __str__(self):
        return f"VrDeviceInfo(address={self._address}, {self.hResolution}, {self.vResolution}, {self.hScreenSize}, {self.vScreenSize}, {self.vScreenCenter}, {self.eyeToScreenDistance}, {self.lensSeparationDistance}, {self.interpupillaryDistance}, {self.lensDistortionValues}, {self.chromaAbCorrection})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class VrStereoConfig:
    """VrStereoConfig, VR stereo rendering configuration for simulator"""

    _size: int = 304

    def __init__(self, projection: StructArray = None, viewOffset: StructArray = None, leftLensCenter: FloatArray = None, rightLensCenter: FloatArray = None, leftScreenCenter: FloatArray = None, rightScreenCenter: FloatArray = None, scale: FloatArray = None, scaleIn: FloatArray = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(304)
            self._to_free = True
            if projection is not None:
                struct_clone(projection, self._address + 0)
            if viewOffset is not None:
                struct_clone(viewOffset, self._address + 128)
            if leftLensCenter is not None:
                struct_clone(leftLensCenter, self._address + 256)
            if rightLensCenter is not None:
                struct_clone(rightLensCenter, self._address + 264)
            if leftScreenCenter is not None:
                struct_clone(leftScreenCenter, self._address + 272)
            if rightScreenCenter is not None:
                struct_clone(rightScreenCenter, self._address + 280)
            if scale is not None:
                struct_clone(scale, self._address + 288)
            if scaleIn is not None:
                struct_clone(scaleIn, self._address + 296)

    @property
    def projection(self):
        return StructArray(Matrix, 2, address=self._address + 0)

    @projection.setter
    def projection(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def viewOffset(self):
        return StructArray(Matrix, 2, address=self._address + 128)

    @viewOffset.setter
    def viewOffset(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 128)

    @property
    def leftLensCenter(self):
        return FloatArray(2, address=self._address + 256)

    @leftLensCenter.setter
    def leftLensCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 256)

    @property
    def rightLensCenter(self):
        return FloatArray(2, address=self._address + 264)

    @rightLensCenter.setter
    def rightLensCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 264)

    @property
    def leftScreenCenter(self):
        return FloatArray(2, address=self._address + 272)

    @leftScreenCenter.setter
    def leftScreenCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 272)

    @property
    def rightScreenCenter(self):
        return FloatArray(2, address=self._address + 280)

    @rightScreenCenter.setter
    def rightScreenCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 280)

    @property
    def scale(self):
        return FloatArray(2, address=self._address + 288)

    @scale.setter
    def scale(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 288)

    @property
    def scaleIn(self):
        return FloatArray(2, address=self._address + 296)

    @scaleIn.setter
    def scaleIn(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 296)

    def __str__(self):
        return f"VrStereoConfig(address={self._address}, {self.projection}, {self.viewOffset}, {self.leftLensCenter}, {self.rightLensCenter}, {self.leftScreenCenter}, {self.rightScreenCenter}, {self.scale}, {self.scaleIn})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class FilePathList:
    """File path list"""

    _size: int = 12

    def __init__(self, capacity: int = 0, count: int = 0, paths: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
            self._to_free = False
        else:
            self._address = _mod._malloc(12)
            self._to_free = True
            _mod.mem.setUint32(self._address + 0, capacity)
            _mod.mem.setUint32(self._address + 4, count)
            _mod.mem.setUint32(self._address + 8, paths)

    @property
    def capacity(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @capacity.setter
    def capacity(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value, True)

    @property
    def count(self):
        return _mod.mem.getUint32(self._address + 4, True)

    @count.setter
    def count(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value, True)

    @property
    def paths(self):
        return _mod.mem.getUint32(self._address + 8, True)

    @paths.setter
    def paths(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value, True)

    def __str__(self):
        return f"FilePathList(address={self._address}, {self.capacity}, {self.count}, {self.paths})"

    def __del__(self):
        if self._to_free:
            _mod._free(self._address)

class ConfigFlags(enum.IntEnum):
    """System/Window config flags"""
    FLAG_VSYNC_HINT: int = 64  # Set to try enabling V-Sync on GPU
    FLAG_FULLSCREEN_MODE: int = 2  # Set to run program in fullscreen
    FLAG_WINDOW_RESIZABLE: int = 4  # Set to allow resizable window
    FLAG_WINDOW_UNDECORATED: int = 8  # Set to disable window decoration (frame and buttons)
    FLAG_WINDOW_HIDDEN: int = 128  # Set to hide window
    FLAG_WINDOW_MINIMIZED: int = 512  # Set to minimize window (iconify)
    FLAG_WINDOW_MAXIMIZED: int = 1024  # Set to maximize window (expanded to monitor)
    FLAG_WINDOW_UNFOCUSED: int = 2048  # Set to window non focused
    FLAG_WINDOW_TOPMOST: int = 4096  # Set to window always on top
    FLAG_WINDOW_ALWAYS_RUN: int = 256  # Set to allow windows running while minimized
    FLAG_WINDOW_TRANSPARENT: int = 16  # Set to allow transparent framebuffer
    FLAG_WINDOW_HIGHDPI: int = 8192  # Set to support HighDPI
    FLAG_WINDOW_MOUSE_PASSTHROUGH: int = 16384  # Set to support mouse passthrough, only supported when FLAG_WINDOW_UNDECORATED
    FLAG_MSAA_4X_HINT: int = 32  # Set to try enabling MSAA 4X
    FLAG_INTERLACED_HINT: int = 65536  # Set to try enabling interlaced video format (for V3D)


class TraceLogLevel(enum.IntEnum):
    """Trace log level"""
    LOG_ALL: int = 0  # Display all logs
    LOG_TRACE: int = 1  # Trace logging, intended for internal use only
    LOG_DEBUG: int = 2  # Debug logging, used for internal debugging, it should be disabled on release builds
    LOG_INFO: int = 3  # Info logging, used for program execution info
    LOG_WARNING: int = 4  # Warning logging, used on recoverable failures
    LOG_ERROR: int = 5  # Error logging, used on unrecoverable failures
    LOG_FATAL: int = 6  # Fatal logging, used to abort program: exit(EXIT_FAILURE)
    LOG_NONE: int = 7  # Disable logging


class KeyboardKey(enum.IntEnum):
    """Keyboard keys (US keyboard layout)"""
    KEY_NULL: int = 0  # Key: NULL, used for no key pressed
    KEY_APOSTROPHE: int = 39  # Key: '
    KEY_COMMA: int = 44  # Key: ,
    KEY_MINUS: int = 45  # Key: -
    KEY_PERIOD: int = 46  # Key: .
    KEY_SLASH: int = 47  # Key: /
    KEY_ZERO: int = 48  # Key: 0
    KEY_ONE: int = 49  # Key: 1
    KEY_TWO: int = 50  # Key: 2
    KEY_THREE: int = 51  # Key: 3
    KEY_FOUR: int = 52  # Key: 4
    KEY_FIVE: int = 53  # Key: 5
    KEY_SIX: int = 54  # Key: 6
    KEY_SEVEN: int = 55  # Key: 7
    KEY_EIGHT: int = 56  # Key: 8
    KEY_NINE: int = 57  # Key: 9
    KEY_SEMICOLON: int = 59  # Key: ;
    KEY_EQUAL: int = 61  # Key: =
    KEY_A: int = 65  # Key: A | a
    KEY_B: int = 66  # Key: B | b
    KEY_C: int = 67  # Key: C | c
    KEY_D: int = 68  # Key: D | d
    KEY_E: int = 69  # Key: E | e
    KEY_F: int = 70  # Key: F | f
    KEY_G: int = 71  # Key: G | g
    KEY_H: int = 72  # Key: H | h
    KEY_I: int = 73  # Key: I | i
    KEY_J: int = 74  # Key: J | j
    KEY_K: int = 75  # Key: K | k
    KEY_L: int = 76  # Key: L | l
    KEY_M: int = 77  # Key: M | m
    KEY_N: int = 78  # Key: N | n
    KEY_O: int = 79  # Key: O | o
    KEY_P: int = 80  # Key: P | p
    KEY_Q: int = 81  # Key: Q | q
    KEY_R: int = 82  # Key: R | r
    KEY_S: int = 83  # Key: S | s
    KEY_T: int = 84  # Key: T | t
    KEY_U: int = 85  # Key: U | u
    KEY_V: int = 86  # Key: V | v
    KEY_W: int = 87  # Key: W | w
    KEY_X: int = 88  # Key: X | x
    KEY_Y: int = 89  # Key: Y | y
    KEY_Z: int = 90  # Key: Z | z
    KEY_LEFT_BRACKET: int = 91  # Key: [
    KEY_BACKSLASH: int = 92  # Key: '\'
    KEY_RIGHT_BRACKET: int = 93  # Key: ]
    KEY_GRAVE: int = 96  # Key: `
    KEY_SPACE: int = 32  # Key: Space
    KEY_ESCAPE: int = 256  # Key: Esc
    KEY_ENTER: int = 257  # Key: Enter
    KEY_TAB: int = 258  # Key: Tab
    KEY_BACKSPACE: int = 259  # Key: Backspace
    KEY_INSERT: int = 260  # Key: Ins
    KEY_DELETE: int = 261  # Key: Del
    KEY_RIGHT: int = 262  # Key: Cursor right
    KEY_LEFT: int = 263  # Key: Cursor left
    KEY_DOWN: int = 264  # Key: Cursor down
    KEY_UP: int = 265  # Key: Cursor up
    KEY_PAGE_UP: int = 266  # Key: Page up
    KEY_PAGE_DOWN: int = 267  # Key: Page down
    KEY_HOME: int = 268  # Key: Home
    KEY_END: int = 269  # Key: End
    KEY_CAPS_LOCK: int = 280  # Key: Caps lock
    KEY_SCROLL_LOCK: int = 281  # Key: Scroll down
    KEY_NUM_LOCK: int = 282  # Key: Num lock
    KEY_PRINT_SCREEN: int = 283  # Key: Print screen
    KEY_PAUSE: int = 284  # Key: Pause
    KEY_F1: int = 290  # Key: F1
    KEY_F2: int = 291  # Key: F2
    KEY_F3: int = 292  # Key: F3
    KEY_F4: int = 293  # Key: F4
    KEY_F5: int = 294  # Key: F5
    KEY_F6: int = 295  # Key: F6
    KEY_F7: int = 296  # Key: F7
    KEY_F8: int = 297  # Key: F8
    KEY_F9: int = 298  # Key: F9
    KEY_F10: int = 299  # Key: F10
    KEY_F11: int = 300  # Key: F11
    KEY_F12: int = 301  # Key: F12
    KEY_LEFT_SHIFT: int = 340  # Key: Shift left
    KEY_LEFT_CONTROL: int = 341  # Key: Control left
    KEY_LEFT_ALT: int = 342  # Key: Alt left
    KEY_LEFT_SUPER: int = 343  # Key: Super left
    KEY_RIGHT_SHIFT: int = 344  # Key: Shift right
    KEY_RIGHT_CONTROL: int = 345  # Key: Control right
    KEY_RIGHT_ALT: int = 346  # Key: Alt right
    KEY_RIGHT_SUPER: int = 347  # Key: Super right
    KEY_KB_MENU: int = 348  # Key: KB menu
    KEY_KP_0: int = 320  # Key: Keypad 0
    KEY_KP_1: int = 321  # Key: Keypad 1
    KEY_KP_2: int = 322  # Key: Keypad 2
    KEY_KP_3: int = 323  # Key: Keypad 3
    KEY_KP_4: int = 324  # Key: Keypad 4
    KEY_KP_5: int = 325  # Key: Keypad 5
    KEY_KP_6: int = 326  # Key: Keypad 6
    KEY_KP_7: int = 327  # Key: Keypad 7
    KEY_KP_8: int = 328  # Key: Keypad 8
    KEY_KP_9: int = 329  # Key: Keypad 9
    KEY_KP_DECIMAL: int = 330  # Key: Keypad .
    KEY_KP_DIVIDE: int = 331  # Key: Keypad /
    KEY_KP_MULTIPLY: int = 332  # Key: Keypad *
    KEY_KP_SUBTRACT: int = 333  # Key: Keypad -
    KEY_KP_ADD: int = 334  # Key: Keypad +
    KEY_KP_ENTER: int = 335  # Key: Keypad Enter
    KEY_KP_EQUAL: int = 336  # Key: Keypad =
    KEY_BACK: int = 4  # Key: Android back button
    KEY_MENU: int = 82  # Key: Android menu button
    KEY_VOLUME_UP: int = 24  # Key: Android volume up button
    KEY_VOLUME_DOWN: int = 25  # Key: Android volume down button


class MouseButton(enum.IntEnum):
    """Mouse buttons"""
    MOUSE_BUTTON_LEFT: int = 0  # Mouse button left
    MOUSE_BUTTON_RIGHT: int = 1  # Mouse button right
    MOUSE_BUTTON_MIDDLE: int = 2  # Mouse button middle (pressed wheel)
    MOUSE_BUTTON_SIDE: int = 3  # Mouse button side (advanced mouse device)
    MOUSE_BUTTON_EXTRA: int = 4  # Mouse button extra (advanced mouse device)
    MOUSE_BUTTON_FORWARD: int = 5  # Mouse button forward (advanced mouse device)
    MOUSE_BUTTON_BACK: int = 6  # Mouse button back (advanced mouse device)


class MouseCursor(enum.IntEnum):
    """Mouse cursor"""
    MOUSE_CURSOR_DEFAULT: int = 0  # Default pointer shape
    MOUSE_CURSOR_ARROW: int = 1  # Arrow shape
    MOUSE_CURSOR_IBEAM: int = 2  # Text writing cursor shape
    MOUSE_CURSOR_CROSSHAIR: int = 3  # Cross shape
    MOUSE_CURSOR_POINTING_HAND: int = 4  # Pointing hand cursor
    MOUSE_CURSOR_RESIZE_EW: int = 5  # Horizontal resize/move arrow shape
    MOUSE_CURSOR_RESIZE_NS: int = 6  # Vertical resize/move arrow shape
    MOUSE_CURSOR_RESIZE_NWSE: int = 7  # Top-left to bottom-right diagonal resize/move arrow shape
    MOUSE_CURSOR_RESIZE_NESW: int = 8  # The top-right to bottom-left diagonal resize/move arrow shape
    MOUSE_CURSOR_RESIZE_ALL: int = 9  # The omnidirectional resize/move cursor shape
    MOUSE_CURSOR_NOT_ALLOWED: int = 10  # The operation-not-allowed shape


class GamepadButton(enum.IntEnum):
    """Gamepad buttons"""
    GAMEPAD_BUTTON_UNKNOWN: int = 0  # Unknown button, just for error checking
    GAMEPAD_BUTTON_LEFT_FACE_UP: int = 1  # Gamepad left DPAD up button
    GAMEPAD_BUTTON_LEFT_FACE_RIGHT: int = 2  # Gamepad left DPAD right button
    GAMEPAD_BUTTON_LEFT_FACE_DOWN: int = 3  # Gamepad left DPAD down button
    GAMEPAD_BUTTON_LEFT_FACE_LEFT: int = 4  # Gamepad left DPAD left button
    GAMEPAD_BUTTON_RIGHT_FACE_UP: int = 5  # Gamepad right button up (i.e. PS3: Triangle, Xbox: Y)
    GAMEPAD_BUTTON_RIGHT_FACE_RIGHT: int = 6  # Gamepad right button right (i.e. PS3: Square, Xbox: X)
    GAMEPAD_BUTTON_RIGHT_FACE_DOWN: int = 7  # Gamepad right button down (i.e. PS3: Cross, Xbox: A)
    GAMEPAD_BUTTON_RIGHT_FACE_LEFT: int = 8  # Gamepad right button left (i.e. PS3: Circle, Xbox: B)
    GAMEPAD_BUTTON_LEFT_TRIGGER_1: int = 9  # Gamepad top/back trigger left (first), it could be a trailing button
    GAMEPAD_BUTTON_LEFT_TRIGGER_2: int = 10  # Gamepad top/back trigger left (second), it could be a trailing button
    GAMEPAD_BUTTON_RIGHT_TRIGGER_1: int = 11  # Gamepad top/back trigger right (one), it could be a trailing button
    GAMEPAD_BUTTON_RIGHT_TRIGGER_2: int = 12  # Gamepad top/back trigger right (second), it could be a trailing button
    GAMEPAD_BUTTON_MIDDLE_LEFT: int = 13  # Gamepad center buttons, left one (i.e. PS3: Select)
    GAMEPAD_BUTTON_MIDDLE: int = 14  # Gamepad center buttons, middle one (i.e. PS3: PS, Xbox: XBOX)
    GAMEPAD_BUTTON_MIDDLE_RIGHT: int = 15  # Gamepad center buttons, right one (i.e. PS3: Start)
    GAMEPAD_BUTTON_LEFT_THUMB: int = 16  # Gamepad joystick pressed button left
    GAMEPAD_BUTTON_RIGHT_THUMB: int = 17  # Gamepad joystick pressed button right


class GamepadAxis(enum.IntEnum):
    """Gamepad axis"""
    GAMEPAD_AXIS_LEFT_X: int = 0  # Gamepad left stick X axis
    GAMEPAD_AXIS_LEFT_Y: int = 1  # Gamepad left stick Y axis
    GAMEPAD_AXIS_RIGHT_X: int = 2  # Gamepad right stick X axis
    GAMEPAD_AXIS_RIGHT_Y: int = 3  # Gamepad right stick Y axis
    GAMEPAD_AXIS_LEFT_TRIGGER: int = 4  # Gamepad back trigger left, pressure level: [1..-1]
    GAMEPAD_AXIS_RIGHT_TRIGGER: int = 5  # Gamepad back trigger right, pressure level: [1..-1]


class MaterialMapIndex(enum.IntEnum):
    """Material map index"""
    MATERIAL_MAP_ALBEDO: int = 0  # Albedo material (same as: MATERIAL_MAP_DIFFUSE)
    MATERIAL_MAP_METALNESS: int = 1  # Metalness material (same as: MATERIAL_MAP_SPECULAR)
    MATERIAL_MAP_NORMAL: int = 2  # Normal material
    MATERIAL_MAP_ROUGHNESS: int = 3  # Roughness material
    MATERIAL_MAP_OCCLUSION: int = 4  # Ambient occlusion material
    MATERIAL_MAP_EMISSION: int = 5  # Emission material
    MATERIAL_MAP_HEIGHT: int = 6  # Heightmap material
    MATERIAL_MAP_CUBEMAP: int = 7  # Cubemap material (NOTE: Uses GL_TEXTURE_CUBE_MAP)
    MATERIAL_MAP_IRRADIANCE: int = 8  # Irradiance material (NOTE: Uses GL_TEXTURE_CUBE_MAP)
    MATERIAL_MAP_PREFILTER: int = 9  # Prefilter material (NOTE: Uses GL_TEXTURE_CUBE_MAP)
    MATERIAL_MAP_BRDF: int = 10  # Brdf material


class ShaderLocationIndex(enum.IntEnum):
    """Shader location index"""
    SHADER_LOC_VERTEX_POSITION: int = 0  # Shader location: vertex attribute: position
    SHADER_LOC_VERTEX_TEXCOORD01: int = 1  # Shader location: vertex attribute: texcoord01
    SHADER_LOC_VERTEX_TEXCOORD02: int = 2  # Shader location: vertex attribute: texcoord02
    SHADER_LOC_VERTEX_NORMAL: int = 3  # Shader location: vertex attribute: normal
    SHADER_LOC_VERTEX_TANGENT: int = 4  # Shader location: vertex attribute: tangent
    SHADER_LOC_VERTEX_COLOR: int = 5  # Shader location: vertex attribute: color
    SHADER_LOC_MATRIX_MVP: int = 6  # Shader location: matrix uniform: model-view-projection
    SHADER_LOC_MATRIX_VIEW: int = 7  # Shader location: matrix uniform: view (camera transform)
    SHADER_LOC_MATRIX_PROJECTION: int = 8  # Shader location: matrix uniform: projection
    SHADER_LOC_MATRIX_MODEL: int = 9  # Shader location: matrix uniform: model (transform)
    SHADER_LOC_MATRIX_NORMAL: int = 10  # Shader location: matrix uniform: normal
    SHADER_LOC_VECTOR_VIEW: int = 11  # Shader location: vector uniform: view
    SHADER_LOC_COLOR_DIFFUSE: int = 12  # Shader location: vector uniform: diffuse color
    SHADER_LOC_COLOR_SPECULAR: int = 13  # Shader location: vector uniform: specular color
    SHADER_LOC_COLOR_AMBIENT: int = 14  # Shader location: vector uniform: ambient color
    SHADER_LOC_MAP_ALBEDO: int = 15  # Shader location: sampler2d texture: albedo (same as: SHADER_LOC_MAP_DIFFUSE)
    SHADER_LOC_MAP_METALNESS: int = 16  # Shader location: sampler2d texture: metalness (same as: SHADER_LOC_MAP_SPECULAR)
    SHADER_LOC_MAP_NORMAL: int = 17  # Shader location: sampler2d texture: normal
    SHADER_LOC_MAP_ROUGHNESS: int = 18  # Shader location: sampler2d texture: roughness
    SHADER_LOC_MAP_OCCLUSION: int = 19  # Shader location: sampler2d texture: occlusion
    SHADER_LOC_MAP_EMISSION: int = 20  # Shader location: sampler2d texture: emission
    SHADER_LOC_MAP_HEIGHT: int = 21  # Shader location: sampler2d texture: height
    SHADER_LOC_MAP_CUBEMAP: int = 22  # Shader location: samplerCube texture: cubemap
    SHADER_LOC_MAP_IRRADIANCE: int = 23  # Shader location: samplerCube texture: irradiance
    SHADER_LOC_MAP_PREFILTER: int = 24  # Shader location: samplerCube texture: prefilter
    SHADER_LOC_MAP_BRDF: int = 25  # Shader location: sampler2d texture: brdf


class ShaderUniformDataType(enum.IntEnum):
    """Shader uniform data type"""
    SHADER_UNIFORM_FLOAT: int = 0  # Shader uniform type: float
    SHADER_UNIFORM_VEC2: int = 1  # Shader uniform type: vec2 (2 float)
    SHADER_UNIFORM_VEC3: int = 2  # Shader uniform type: vec3 (3 float)
    SHADER_UNIFORM_VEC4: int = 3  # Shader uniform type: vec4 (4 float)
    SHADER_UNIFORM_INT: int = 4  # Shader uniform type: int
    SHADER_UNIFORM_IVEC2: int = 5  # Shader uniform type: ivec2 (2 int)
    SHADER_UNIFORM_IVEC3: int = 6  # Shader uniform type: ivec3 (3 int)
    SHADER_UNIFORM_IVEC4: int = 7  # Shader uniform type: ivec4 (4 int)
    SHADER_UNIFORM_SAMPLER2D: int = 8  # Shader uniform type: sampler2d


class ShaderAttributeDataType(enum.IntEnum):
    """Shader attribute data types"""
    SHADER_ATTRIB_FLOAT: int = 0  # Shader attribute type: float
    SHADER_ATTRIB_VEC2: int = 1  # Shader attribute type: vec2 (2 float)
    SHADER_ATTRIB_VEC3: int = 2  # Shader attribute type: vec3 (3 float)
    SHADER_ATTRIB_VEC4: int = 3  # Shader attribute type: vec4 (4 float)


class PixelFormat(enum.IntEnum):
    """Pixel formats"""
    PIXELFORMAT_UNCOMPRESSED_GRAYSCALE: int = 1  # 8 bit per pixel (no alpha)
    PIXELFORMAT_UNCOMPRESSED_GRAY_ALPHA: int = 2  # 8*2 bpp (2 channels)
    PIXELFORMAT_UNCOMPRESSED_R5G6B5: int = 3  # 16 bpp
    PIXELFORMAT_UNCOMPRESSED_R8G8B8: int = 4  # 24 bpp
    PIXELFORMAT_UNCOMPRESSED_R5G5B5A1: int = 5  # 16 bpp (1 bit alpha)
    PIXELFORMAT_UNCOMPRESSED_R4G4B4A4: int = 6  # 16 bpp (4 bit alpha)
    PIXELFORMAT_UNCOMPRESSED_R8G8B8A8: int = 7  # 32 bpp
    PIXELFORMAT_UNCOMPRESSED_R32: int = 8  # 32 bpp (1 channel - float)
    PIXELFORMAT_UNCOMPRESSED_R32G32B32: int = 9  # 32*3 bpp (3 channels - float)
    PIXELFORMAT_UNCOMPRESSED_R32G32B32A32: int = 10  # 32*4 bpp (4 channels - float)
    PIXELFORMAT_COMPRESSED_DXT1_RGB: int = 11  # 4 bpp (no alpha)
    PIXELFORMAT_COMPRESSED_DXT1_RGBA: int = 12  # 4 bpp (1 bit alpha)
    PIXELFORMAT_COMPRESSED_DXT3_RGBA: int = 13  # 8 bpp
    PIXELFORMAT_COMPRESSED_DXT5_RGBA: int = 14  # 8 bpp
    PIXELFORMAT_COMPRESSED_ETC1_RGB: int = 15  # 4 bpp
    PIXELFORMAT_COMPRESSED_ETC2_RGB: int = 16  # 4 bpp
    PIXELFORMAT_COMPRESSED_ETC2_EAC_RGBA: int = 17  # 8 bpp
    PIXELFORMAT_COMPRESSED_PVRT_RGB: int = 18  # 4 bpp
    PIXELFORMAT_COMPRESSED_PVRT_RGBA: int = 19  # 4 bpp
    PIXELFORMAT_COMPRESSED_ASTC_4x4_RGBA: int = 20  # 8 bpp
    PIXELFORMAT_COMPRESSED_ASTC_8x8_RGBA: int = 21  # 2 bpp


class TextureFilter(enum.IntEnum):
    """Texture parameters: filter mode"""
    TEXTURE_FILTER_POINT: int = 0  # No filter, just pixel approximation
    TEXTURE_FILTER_BILINEAR: int = 1  # Linear filtering
    TEXTURE_FILTER_TRILINEAR: int = 2  # Trilinear filtering (linear with mipmaps)
    TEXTURE_FILTER_ANISOTROPIC_4X: int = 3  # Anisotropic filtering 4x
    TEXTURE_FILTER_ANISOTROPIC_8X: int = 4  # Anisotropic filtering 8x
    TEXTURE_FILTER_ANISOTROPIC_16X: int = 5  # Anisotropic filtering 16x


class TextureWrap(enum.IntEnum):
    """Texture parameters: wrap mode"""
    TEXTURE_WRAP_REPEAT: int = 0  # Repeats texture in tiled mode
    TEXTURE_WRAP_CLAMP: int = 1  # Clamps texture to edge pixel in tiled mode
    TEXTURE_WRAP_MIRROR_REPEAT: int = 2  # Mirrors and repeats the texture in tiled mode
    TEXTURE_WRAP_MIRROR_CLAMP: int = 3  # Mirrors and clamps to border the texture in tiled mode


class CubemapLayout(enum.IntEnum):
    """Cubemap layouts"""
    CUBEMAP_LAYOUT_AUTO_DETECT: int = 0  # Automatically detect layout type
    CUBEMAP_LAYOUT_LINE_VERTICAL: int = 1  # Layout is defined by a vertical line with faces
    CUBEMAP_LAYOUT_LINE_HORIZONTAL: int = 2  # Layout is defined by a horizontal line with faces
    CUBEMAP_LAYOUT_CROSS_THREE_BY_FOUR: int = 3  # Layout is defined by a 3x4 cross with cubemap faces
    CUBEMAP_LAYOUT_CROSS_FOUR_BY_THREE: int = 4  # Layout is defined by a 4x3 cross with cubemap faces
    CUBEMAP_LAYOUT_PANORAMA: int = 5  # Layout is defined by a panorama image (equirrectangular map)


class FontType(enum.IntEnum):
    """Font type, defines generation method"""
    FONT_DEFAULT: int = 0  # Default font generation, anti-aliased
    FONT_BITMAP: int = 1  # Bitmap font generation, no anti-aliasing
    FONT_SDF: int = 2  # SDF font generation, requires external shader


class BlendMode(enum.IntEnum):
    """Color blending modes (pre-defined)"""
    BLEND_ALPHA: int = 0  # Blend textures considering alpha (default)
    BLEND_ADDITIVE: int = 1  # Blend textures adding colors
    BLEND_MULTIPLIED: int = 2  # Blend textures multiplying colors
    BLEND_ADD_COLORS: int = 3  # Blend textures adding colors (alternative)
    BLEND_SUBTRACT_COLORS: int = 4  # Blend textures subtracting colors (alternative)
    BLEND_ALPHA_PREMULTIPLY: int = 5  # Blend premultiplied textures considering alpha
    BLEND_CUSTOM: int = 6  # Blend textures using custom src/dst factors (use rlSetBlendFactors())
    BLEND_CUSTOM_SEPARATE: int = 7  # Blend textures using custom rgb/alpha separate src/dst factors (use rlSetBlendFactorsSeparate())


class Gesture(enum.IntEnum):
    """Gesture"""
    GESTURE_NONE: int = 0  # No gesture
    GESTURE_TAP: int = 1  # Tap gesture
    GESTURE_DOUBLETAP: int = 2  # Double tap gesture
    GESTURE_HOLD: int = 4  # Hold gesture
    GESTURE_DRAG: int = 8  # Drag gesture
    GESTURE_SWIPE_RIGHT: int = 16  # Swipe right gesture
    GESTURE_SWIPE_LEFT: int = 32  # Swipe left gesture
    GESTURE_SWIPE_UP: int = 64  # Swipe up gesture
    GESTURE_SWIPE_DOWN: int = 128  # Swipe down gesture
    GESTURE_PINCH_IN: int = 256  # Pinch in gesture
    GESTURE_PINCH_OUT: int = 512  # Pinch out gesture


class CameraMode(enum.IntEnum):
    """Camera system modes"""
    CAMERA_CUSTOM: int = 0  # Custom camera
    CAMERA_FREE: int = 1  # Free camera
    CAMERA_ORBITAL: int = 2  # Orbital camera
    CAMERA_FIRST_PERSON: int = 3  # First person camera
    CAMERA_THIRD_PERSON: int = 4  # Third person camera


class CameraProjection(enum.IntEnum):
    """Camera projection"""
    CAMERA_PERSPECTIVE: int = 0  # Perspective projection
    CAMERA_ORTHOGRAPHIC: int = 1  # Orthographic projection


class NPatchLayout(enum.IntEnum):
    """N-patch layout"""
    NPATCH_NINE_PATCH: int = 0  # Npatch layout: 3x3 tiles
    NPATCH_THREE_PATCH_VERTICAL: int = 1  # Npatch layout: 1x3 tiles
    NPATCH_THREE_PATCH_HORIZONTAL: int = 2  # Npatch layout: 3x1 tiles



LIGHTGRAY = Color(200, 200, 200, 255, frozen=True)  # Light Gray
GRAY = Color(130, 130, 130, 255, frozen=True)  # Gray
DARKGRAY = Color(80, 80, 80, 255, frozen=True)  # Dark Gray
YELLOW = Color(253, 249, 0, 255, frozen=True)  # Yellow
GOLD = Color(255, 203, 0, 255, frozen=True)  # Gold
ORANGE = Color(255, 161, 0, 255, frozen=True)  # Orange
PINK = Color(255, 109, 194, 255, frozen=True)  # Pink
RED = Color(230, 41, 55, 255, frozen=True)  # Red
MAROON = Color(190, 33, 55, 255, frozen=True)  # Maroon
GREEN = Color(0, 228, 48, 255, frozen=True)  # Green
LIME = Color(0, 158, 47, 255, frozen=True)  # Lime
DARKGREEN = Color(0, 117, 44, 255, frozen=True)  # Dark Green
SKYBLUE = Color(102, 191, 255, 255, frozen=True)  # Sky Blue
BLUE = Color(0, 121, 241, 255, frozen=True)  # Blue
DARKBLUE = Color(0, 82, 172, 255, frozen=True)  # Dark Blue
PURPLE = Color(200, 122, 255, 255, frozen=True)  # Purple
VIOLET = Color(135, 60, 190, 255, frozen=True)  # Violet
DARKPURPLE = Color(112, 31, 126, 255, frozen=True)  # Dark Purple
BEIGE = Color(211, 176, 131, 255, frozen=True)  # Beige
BROWN = Color(127, 106, 79, 255, frozen=True)  # Brown
DARKBROWN = Color(76, 63, 47, 255, frozen=True)  # Dark Brown
WHITE = Color(255, 255, 255, 255, frozen=True)  # White
BLACK = Color(0, 0, 0, 255, frozen=True)  # Black
BLANK = Color(0, 0, 0, 0, frozen=True)  # Blank (Transparent)
MAGENTA = Color(255, 0, 255, 255, frozen=True)  # Magenta
RAYWHITE = Color(245, 245, 245, 255, frozen=True)  # My own White (raylib logo)


def GetFontDefault():
    a = _mod._malloc(Font._size)
    _mod._GetFontDefault(a)
    return Font(address=a)


def ClearBackground(color):
    _mod._ClearBackground(color._address)


def DrawText(text, x, y, fontSize, color):
    sp = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, sp, len(text) + 1)
    _mod._DrawText(sp, x, y, fontSize, color._address)
    _mod._free(sp)


def BeginDrawing():
    _mod._BeginDrawing()


def EndDrawing():
    _mod._EndDrawing()


def DrawFPS(x, y):
    _mod._DrawFPS(x, y)


def InitWindow(width, height):
    _mod._InitWindow(width, height)


def DrawTextBoxedSelectable(font, text, rec, fontSize, spacing, wordWrap, tint, selectStart, selectLength, selectTint,
                            selectBackTint):
    sp = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, sp, len(text) + 1)
    _mod._DrawTextBoxedSelectable(font._address, sp, rec._address, fontSize, spacing, wordWrap, tint._address,
                                  selectStart, selectLength, selectTint._address, selectBackTint._address)
    _mod._free(sp)


def DrawTextBoxed(font, text, rec, fontSize, spacing, wordWrap, tint):
    sp = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, sp, len(text) + 1)
    _mod._DrawTextBoxed(font._address, sp, rec._address, fontSize, spacing, wordWrap, tint._address)
    _mod._free(sp)
    
    