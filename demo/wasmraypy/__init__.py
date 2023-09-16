
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


RAYLIB_VERSION_MAJOR: int = 4
RAYLIB_VERSION_MINOR: int = 6
RAYLIB_VERSION_PATCH: int = 0
RAYLIB_VERSION: str = "4.6-dev"
PI: float = 3.141592653589793
DEG2RAD: float = (PI/180.0)
RAD2DEG: float = (180.0/PI)
def InitWindow(width: int, height: int, title: str):
    title_ = _mod._malloc(len(title) + 1)
    _mod.stringToUTF8(title, title_, len(title) + 1)
    _mod._InitWindow(width, height, title_)
    _mod._free(title_)


def WindowShouldClose() -> int:
    return_interface = _mod._WindowShouldClose()
    return return_interface


def CloseWindow():
    _mod._CloseWindow()


def IsWindowReady() -> int:
    return_interface = _mod._IsWindowReady()
    return return_interface


def IsWindowFullscreen() -> int:
    return_interface = _mod._IsWindowFullscreen()
    return return_interface


def IsWindowHidden() -> int:
    return_interface = _mod._IsWindowHidden()
    return return_interface


def IsWindowMinimized() -> int:
    return_interface = _mod._IsWindowMinimized()
    return return_interface


def IsWindowMaximized() -> int:
    return_interface = _mod._IsWindowMaximized()
    return return_interface


def IsWindowFocused() -> int:
    return_interface = _mod._IsWindowFocused()
    return return_interface


def IsWindowResized() -> int:
    return_interface = _mod._IsWindowResized()
    return return_interface


def IsWindowState(flag: int) -> int:
    return_interface = _mod._IsWindowState(flag)
    return return_interface


def SetWindowState(flags: int):
    _mod._SetWindowState(flags)


def ClearWindowState(flags: int):
    _mod._ClearWindowState(flags)


def ToggleFullscreen():
    _mod._ToggleFullscreen()


def MaximizeWindow():
    _mod._MaximizeWindow()


def MinimizeWindow():
    _mod._MinimizeWindow()


def RestoreWindow():
    _mod._RestoreWindow()


def SetWindowIcon(image: Image):
    _mod._SetWindowIcon(image._address)


def SetWindowIcons(images: int, count: int):
    _mod._SetWindowIcons(images, count)


def SetWindowTitle(title: str):
    title_ = _mod._malloc(len(title) + 1)
    _mod.stringToUTF8(title, title_, len(title) + 1)
    _mod._SetWindowTitle(title_)
    _mod._free(title_)


def SetWindowPosition(x: int, y: int):
    _mod._SetWindowPosition(x, y)


def SetWindowMonitor(monitor: int):
    _mod._SetWindowMonitor(monitor)


def SetWindowMinSize(width: int, height: int):
    _mod._SetWindowMinSize(width, height)


def SetWindowSize(width: int, height: int):
    _mod._SetWindowSize(width, height)


def SetWindowOpacity(opacity: float):
    _mod._SetWindowOpacity(opacity)


def SetWindowFocused():
    _mod._SetWindowFocused()


def GetWindowHandle() -> int:
    return_interface = _mod._GetWindowHandle()
    return return_interface


def GetScreenWidth() -> int:
    return_interface = _mod._GetScreenWidth()
    return return_interface


def GetScreenHeight() -> int:
    return_interface = _mod._GetScreenHeight()
    return return_interface


def GetRenderWidth() -> int:
    return_interface = _mod._GetRenderWidth()
    return return_interface


def GetRenderHeight() -> int:
    return_interface = _mod._GetRenderHeight()
    return return_interface


def GetMonitorCount() -> int:
    return_interface = _mod._GetMonitorCount()
    return return_interface


def GetCurrentMonitor() -> int:
    return_interface = _mod._GetCurrentMonitor()
    return return_interface


def GetMonitorPosition(monitor: int) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetMonitorPosition(Vector2_._address, monitor)
    return Vector2_


def GetMonitorWidth(monitor: int) -> int:
    return_interface = _mod._GetMonitorWidth(monitor)
    return return_interface


def GetMonitorHeight(monitor: int) -> int:
    return_interface = _mod._GetMonitorHeight(monitor)
    return return_interface


def GetMonitorPhysicalWidth(monitor: int) -> int:
    return_interface = _mod._GetMonitorPhysicalWidth(monitor)
    return return_interface


def GetMonitorPhysicalHeight(monitor: int) -> int:
    return_interface = _mod._GetMonitorPhysicalHeight(monitor)
    return return_interface


def GetMonitorRefreshRate(monitor: int) -> int:
    return_interface = _mod._GetMonitorRefreshRate(monitor)
    return return_interface


def GetWindowPosition() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetWindowPosition(Vector2_._address)
    return Vector2_


def GetWindowScaleDPI() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetWindowScaleDPI(Vector2_._address)
    return Vector2_


def GetMonitorName(monitor: int) -> int:
    return_interface = _mod._GetMonitorName(monitor)
    return return_interface


def SetClipboardText(text: str):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._SetClipboardText(text_)
    _mod._free(text_)


def GetClipboardText() -> int:
    return_interface = _mod._GetClipboardText()
    return return_interface


def EnableEventWaiting():
    _mod._EnableEventWaiting()


def DisableEventWaiting():
    _mod._DisableEventWaiting()


def SwapScreenBuffer():
    _mod._SwapScreenBuffer()


def PollInputEvents():
    _mod._PollInputEvents()


def WaitTime(seconds: float):
    _mod._WaitTime(seconds)


def ShowCursor():
    _mod._ShowCursor()


def HideCursor():
    _mod._HideCursor()


def IsCursorHidden() -> int:
    return_interface = _mod._IsCursorHidden()
    return return_interface


def EnableCursor():
    _mod._EnableCursor()


def DisableCursor():
    _mod._DisableCursor()


def IsCursorOnScreen() -> int:
    return_interface = _mod._IsCursorOnScreen()
    return return_interface


def ClearBackground(color: Color):
    _mod._ClearBackground(color._address)


def BeginDrawing():
    _mod._BeginDrawing()


def EndDrawing():
    _mod._EndDrawing()


def BeginMode2D(camera: Camera2D):
    _mod._BeginMode2D(camera._address)


def EndMode2D():
    _mod._EndMode2D()


def BeginMode3D(camera: Camera3D):
    _mod._BeginMode3D(camera._address)


def EndMode3D():
    _mod._EndMode3D()


def BeginTextureMode(target: RenderTexture2D):
    _mod._BeginTextureMode(target._address)


def EndTextureMode():
    _mod._EndTextureMode()


def BeginShaderMode(shader: Shader):
    _mod._BeginShaderMode(shader._address)


def EndShaderMode():
    _mod._EndShaderMode()


def BeginBlendMode(mode: int):
    _mod._BeginBlendMode(mode)


def EndBlendMode():
    _mod._EndBlendMode()


def BeginScissorMode(x: int, y: int, width: int, height: int):
    _mod._BeginScissorMode(x, y, width, height)


def EndScissorMode():
    _mod._EndScissorMode()


def BeginVrStereoMode(config: VrStereoConfig):
    _mod._BeginVrStereoMode(config._address)


def EndVrStereoMode():
    _mod._EndVrStereoMode()


def LoadVrStereoConfig(device: VrDeviceInfo) -> VrStereoConfig:
    VrStereoConfig_ = VrStereoConfig()
    _mod._LoadVrStereoConfig(VrStereoConfig_._address, device._address)
    return VrStereoConfig_


def UnloadVrStereoConfig(config: VrStereoConfig):
    _mod._UnloadVrStereoConfig(config._address)


def LoadShader(vsFileName: str, fsFileName: str) -> Shader:
    Shader_ = Shader()
    vsFileName_ = _mod._malloc(len(vsFileName) + 1)
    _mod.stringToUTF8(vsFileName, vsFileName_, len(vsFileName) + 1)
    fsFileName_ = _mod._malloc(len(fsFileName) + 1)
    _mod.stringToUTF8(fsFileName, fsFileName_, len(fsFileName) + 1)
    _mod._LoadShader(Shader_._address, vsFileName_, fsFileName_)
    _mod._free(vsFileName_)
    _mod._free(fsFileName_)
    return Shader_


def LoadShaderFromMemory(vsCode: str, fsCode: str) -> Shader:
    Shader_ = Shader()
    vsCode_ = _mod._malloc(len(vsCode) + 1)
    _mod.stringToUTF8(vsCode, vsCode_, len(vsCode) + 1)
    fsCode_ = _mod._malloc(len(fsCode) + 1)
    _mod.stringToUTF8(fsCode, fsCode_, len(fsCode) + 1)
    _mod._LoadShaderFromMemory(Shader_._address, vsCode_, fsCode_)
    _mod._free(vsCode_)
    _mod._free(fsCode_)
    return Shader_


def IsShaderReady(shader: Shader) -> int:
    return_interface = _mod._IsShaderReady(shader._address)
    return return_interface


def GetShaderLocation(shader: Shader, uniformName: str) -> int:
    uniformName_ = _mod._malloc(len(uniformName) + 1)
    _mod.stringToUTF8(uniformName, uniformName_, len(uniformName) + 1)
    return_interface = _mod._GetShaderLocation(shader._address, uniformName_)
    _mod._free(uniformName_)
    return return_interface


def GetShaderLocationAttrib(shader: Shader, attribName: str) -> int:
    attribName_ = _mod._malloc(len(attribName) + 1)
    _mod.stringToUTF8(attribName, attribName_, len(attribName) + 1)
    return_interface = _mod._GetShaderLocationAttrib(shader._address, attribName_)
    _mod._free(attribName_)
    return return_interface


def SetShaderValue(shader: Shader, locIndex: int, value: int, uniformType: int):
    _mod._SetShaderValue(shader._address, locIndex, value, uniformType)


def SetShaderValueV(shader: Shader, locIndex: int, value: int, uniformType: int, count: int):
    _mod._SetShaderValueV(shader._address, locIndex, value, uniformType, count)


def SetShaderValueMatrix(shader: Shader, locIndex: int, mat: Matrix):
    _mod._SetShaderValueMatrix(shader._address, locIndex, mat._address)


def SetShaderValueTexture(shader: Shader, locIndex: int, texture: Texture2D):
    _mod._SetShaderValueTexture(shader._address, locIndex, texture._address)


def UnloadShader(shader: Shader):
    _mod._UnloadShader(shader._address)


def GetMouseRay(mousePosition: Vector2, camera: Camera) -> Ray:
    Ray_ = Ray()
    _mod._GetMouseRay(Ray_._address, mousePosition._address, camera._address)
    return Ray_


def GetCameraMatrix(camera: Camera) -> Matrix:
    Matrix_ = Matrix()
    _mod._GetCameraMatrix(Matrix_._address, camera._address)
    return Matrix_


def GetCameraMatrix2D(camera: Camera2D) -> Matrix:
    Matrix_ = Matrix()
    _mod._GetCameraMatrix2D(Matrix_._address, camera._address)
    return Matrix_


def GetWorldToScreen(position: Vector3, camera: Camera) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetWorldToScreen(Vector2_._address, position._address, camera._address)
    return Vector2_


def GetScreenToWorld2D(position: Vector2, camera: Camera2D) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetScreenToWorld2D(Vector2_._address, position._address, camera._address)
    return Vector2_


def GetWorldToScreenEx(position: Vector3, camera: Camera, width: int, height: int) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetWorldToScreenEx(Vector2_._address, position._address, camera._address, width, height)
    return Vector2_


def GetWorldToScreen2D(position: Vector2, camera: Camera2D) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetWorldToScreen2D(Vector2_._address, position._address, camera._address)
    return Vector2_


def SetTargetFPS(fps: int):
    _mod._SetTargetFPS(fps)


def GetFPS() -> int:
    return_interface = _mod._GetFPS()
    return return_interface


def GetFrameTime() -> float:
    return_interface = _mod._GetFrameTime()
    return return_interface


def GetTime() -> float:
    return_interface = _mod._GetTime()
    return return_interface


def GetRandomValue(min: int, max: int) -> int:
    return_interface = _mod._GetRandomValue(min, max)
    return return_interface


def SetRandomSeed(seed: int):
    _mod._SetRandomSeed(seed)


def TakeScreenshot(fileName: str):
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._TakeScreenshot(fileName_)
    _mod._free(fileName_)


def SetConfigFlags(flags: int):
    _mod._SetConfigFlags(flags)


def SetTraceLogLevel(logLevel: int):
    _mod._SetTraceLogLevel(logLevel)


def MemAlloc(size: int) -> int:
    return_interface = _mod._MemAlloc(size)
    return return_interface


def MemRealloc(ptr: int, size: int) -> int:
    return_interface = _mod._MemRealloc(ptr, size)
    return return_interface


def MemFree(ptr: int):
    _mod._MemFree(ptr)


def OpenURL(url: str):
    url_ = _mod._malloc(len(url) + 1)
    _mod.stringToUTF8(url, url_, len(url) + 1)
    _mod._OpenURL(url_)
    _mod._free(url_)


def LoadFileData(fileName: str, bytesRead: int) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._LoadFileData(fileName_, bytesRead)
    _mod._free(fileName_)
    return return_interface


def UnloadFileData(data: int):
    _mod._UnloadFileData(data)


def SaveFileData(fileName: str, data: int, bytesToWrite: int) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._SaveFileData(fileName_, data, bytesToWrite)
    _mod._free(fileName_)
    return return_interface


def ExportDataAsCode(data: int, size: int, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportDataAsCode(data, size, fileName_)
    _mod._free(fileName_)
    return return_interface


def LoadFileText(fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._LoadFileText(fileName_)
    _mod._free(fileName_)
    return return_interface


def UnloadFileText(text: int):
    _mod._UnloadFileText(text)


def SaveFileText(fileName: str, text: int) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._SaveFileText(fileName_, text)
    _mod._free(fileName_)
    return return_interface


def FileExists(fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._FileExists(fileName_)
    _mod._free(fileName_)
    return return_interface


def DirectoryExists(dirPath: str) -> int:
    dirPath_ = _mod._malloc(len(dirPath) + 1)
    _mod.stringToUTF8(dirPath, dirPath_, len(dirPath) + 1)
    return_interface = _mod._DirectoryExists(dirPath_)
    _mod._free(dirPath_)
    return return_interface


def IsFileExtension(fileName: str, ext: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    ext_ = _mod._malloc(len(ext) + 1)
    _mod.stringToUTF8(ext, ext_, len(ext) + 1)
    return_interface = _mod._IsFileExtension(fileName_, ext_)
    _mod._free(fileName_)
    _mod._free(ext_)
    return return_interface


def GetFileLength(fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._GetFileLength(fileName_)
    _mod._free(fileName_)
    return return_interface


def GetFileExtension(fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._GetFileExtension(fileName_)
    _mod._free(fileName_)
    return return_interface


def GetFileName(filePath: str) -> int:
    filePath_ = _mod._malloc(len(filePath) + 1)
    _mod.stringToUTF8(filePath, filePath_, len(filePath) + 1)
    return_interface = _mod._GetFileName(filePath_)
    _mod._free(filePath_)
    return return_interface


def GetFileNameWithoutExt(filePath: str) -> int:
    filePath_ = _mod._malloc(len(filePath) + 1)
    _mod.stringToUTF8(filePath, filePath_, len(filePath) + 1)
    return_interface = _mod._GetFileNameWithoutExt(filePath_)
    _mod._free(filePath_)
    return return_interface


def GetDirectoryPath(filePath: str) -> int:
    filePath_ = _mod._malloc(len(filePath) + 1)
    _mod.stringToUTF8(filePath, filePath_, len(filePath) + 1)
    return_interface = _mod._GetDirectoryPath(filePath_)
    _mod._free(filePath_)
    return return_interface


def GetPrevDirectoryPath(dirPath: str) -> int:
    dirPath_ = _mod._malloc(len(dirPath) + 1)
    _mod.stringToUTF8(dirPath, dirPath_, len(dirPath) + 1)
    return_interface = _mod._GetPrevDirectoryPath(dirPath_)
    _mod._free(dirPath_)
    return return_interface


def GetWorkingDirectory() -> int:
    return_interface = _mod._GetWorkingDirectory()
    return return_interface


def GetApplicationDirectory() -> int:
    return_interface = _mod._GetApplicationDirectory()
    return return_interface


def ChangeDirectory(dir: str) -> int:
    dir_ = _mod._malloc(len(dir) + 1)
    _mod.stringToUTF8(dir, dir_, len(dir) + 1)
    return_interface = _mod._ChangeDirectory(dir_)
    _mod._free(dir_)
    return return_interface


def IsPathFile(path: str) -> int:
    path_ = _mod._malloc(len(path) + 1)
    _mod.stringToUTF8(path, path_, len(path) + 1)
    return_interface = _mod._IsPathFile(path_)
    _mod._free(path_)
    return return_interface


def LoadDirectoryFiles(dirPath: str) -> FilePathList:
    FilePathList_ = FilePathList()
    dirPath_ = _mod._malloc(len(dirPath) + 1)
    _mod.stringToUTF8(dirPath, dirPath_, len(dirPath) + 1)
    _mod._LoadDirectoryFiles(FilePathList_._address, dirPath_)
    _mod._free(dirPath_)
    return FilePathList_


def LoadDirectoryFilesEx(basePath: str, filter: str, scanSubdirs: int) -> FilePathList:
    FilePathList_ = FilePathList()
    basePath_ = _mod._malloc(len(basePath) + 1)
    _mod.stringToUTF8(basePath, basePath_, len(basePath) + 1)
    filter_ = _mod._malloc(len(filter) + 1)
    _mod.stringToUTF8(filter, filter_, len(filter) + 1)
    _mod._LoadDirectoryFilesEx(FilePathList_._address, basePath_, filter_, scanSubdirs)
    _mod._free(basePath_)
    _mod._free(filter_)
    return FilePathList_


def UnloadDirectoryFiles(files: FilePathList):
    _mod._UnloadDirectoryFiles(files._address)


def IsFileDropped() -> int:
    return_interface = _mod._IsFileDropped()
    return return_interface


def LoadDroppedFiles() -> FilePathList:
    FilePathList_ = FilePathList()
    _mod._LoadDroppedFiles(FilePathList_._address)
    return FilePathList_


def UnloadDroppedFiles(files: FilePathList):
    _mod._UnloadDroppedFiles(files._address)


def GetFileModTime(fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._GetFileModTime(fileName_)
    _mod._free(fileName_)
    return return_interface


def CompressData(data: int, dataSize: int, compDataSize: int) -> int:
    return_interface = _mod._CompressData(data, dataSize, compDataSize)
    return return_interface


def DecompressData(compData: int, compDataSize: int, dataSize: int) -> int:
    return_interface = _mod._DecompressData(compData, compDataSize, dataSize)
    return return_interface


def EncodeDataBase64(data: int, dataSize: int, outputSize: int) -> int:
    return_interface = _mod._EncodeDataBase64(data, dataSize, outputSize)
    return return_interface


def DecodeDataBase64(data: int, outputSize: int) -> int:
    return_interface = _mod._DecodeDataBase64(data, outputSize)
    return return_interface


def IsKeyPressed(key: int) -> int:
    return_interface = _mod._IsKeyPressed(key)
    return return_interface


def IsKeyDown(key: int) -> int:
    return_interface = _mod._IsKeyDown(key)
    return return_interface


def IsKeyReleased(key: int) -> int:
    return_interface = _mod._IsKeyReleased(key)
    return return_interface


def IsKeyUp(key: int) -> int:
    return_interface = _mod._IsKeyUp(key)
    return return_interface


def SetExitKey(key: int):
    _mod._SetExitKey(key)


def GetKeyPressed() -> int:
    return_interface = _mod._GetKeyPressed()
    return return_interface


def GetCharPressed() -> int:
    return_interface = _mod._GetCharPressed()
    return return_interface


def IsGamepadAvailable(gamepad: int) -> int:
    return_interface = _mod._IsGamepadAvailable(gamepad)
    return return_interface


def GetGamepadName(gamepad: int) -> int:
    return_interface = _mod._GetGamepadName(gamepad)
    return return_interface


def IsGamepadButtonPressed(gamepad: int, button: int) -> int:
    return_interface = _mod._IsGamepadButtonPressed(gamepad, button)
    return return_interface


def IsGamepadButtonDown(gamepad: int, button: int) -> int:
    return_interface = _mod._IsGamepadButtonDown(gamepad, button)
    return return_interface


def IsGamepadButtonReleased(gamepad: int, button: int) -> int:
    return_interface = _mod._IsGamepadButtonReleased(gamepad, button)
    return return_interface


def IsGamepadButtonUp(gamepad: int, button: int) -> int:
    return_interface = _mod._IsGamepadButtonUp(gamepad, button)
    return return_interface


def GetGamepadButtonPressed() -> int:
    return_interface = _mod._GetGamepadButtonPressed()
    return return_interface


def GetGamepadAxisCount(gamepad: int) -> int:
    return_interface = _mod._GetGamepadAxisCount(gamepad)
    return return_interface


def GetGamepadAxisMovement(gamepad: int, axis: int) -> float:
    return_interface = _mod._GetGamepadAxisMovement(gamepad, axis)
    return return_interface


def SetGamepadMappings(mappings: str) -> int:
    mappings_ = _mod._malloc(len(mappings) + 1)
    _mod.stringToUTF8(mappings, mappings_, len(mappings) + 1)
    return_interface = _mod._SetGamepadMappings(mappings_)
    _mod._free(mappings_)
    return return_interface


def IsMouseButtonPressed(button: int) -> int:
    return_interface = _mod._IsMouseButtonPressed(button)
    return return_interface


def IsMouseButtonDown(button: int) -> int:
    return_interface = _mod._IsMouseButtonDown(button)
    return return_interface


def IsMouseButtonReleased(button: int) -> int:
    return_interface = _mod._IsMouseButtonReleased(button)
    return return_interface


def IsMouseButtonUp(button: int) -> int:
    return_interface = _mod._IsMouseButtonUp(button)
    return return_interface


def GetMouseX() -> int:
    return_interface = _mod._GetMouseX()
    return return_interface


def GetMouseY() -> int:
    return_interface = _mod._GetMouseY()
    return return_interface


def GetMousePosition() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetMousePosition(Vector2_._address)
    return Vector2_


def GetMouseDelta() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetMouseDelta(Vector2_._address)
    return Vector2_


def SetMousePosition(x: int, y: int):
    _mod._SetMousePosition(x, y)


def SetMouseOffset(offsetX: int, offsetY: int):
    _mod._SetMouseOffset(offsetX, offsetY)


def SetMouseScale(scaleX: float, scaleY: float):
    _mod._SetMouseScale(scaleX, scaleY)


def GetMouseWheelMove() -> float:
    return_interface = _mod._GetMouseWheelMove()
    return return_interface


def GetMouseWheelMoveV() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetMouseWheelMoveV(Vector2_._address)
    return Vector2_


def SetMouseCursor(cursor: int):
    _mod._SetMouseCursor(cursor)


def GetTouchX() -> int:
    return_interface = _mod._GetTouchX()
    return return_interface


def GetTouchY() -> int:
    return_interface = _mod._GetTouchY()
    return return_interface


def GetTouchPosition(index: int) -> Vector2:
    Vector2_ = Vector2()
    _mod._GetTouchPosition(Vector2_._address, index)
    return Vector2_


def GetTouchPointId(index: int) -> int:
    return_interface = _mod._GetTouchPointId(index)
    return return_interface


def GetTouchPointCount() -> int:
    return_interface = _mod._GetTouchPointCount()
    return return_interface


def SetGesturesEnabled(flags: int):
    _mod._SetGesturesEnabled(flags)


def IsGestureDetected(gesture: int) -> int:
    return_interface = _mod._IsGestureDetected(gesture)
    return return_interface


def GetGestureDetected() -> int:
    return_interface = _mod._GetGestureDetected()
    return return_interface


def GetGestureHoldDuration() -> float:
    return_interface = _mod._GetGestureHoldDuration()
    return return_interface


def GetGestureDragVector() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetGestureDragVector(Vector2_._address)
    return Vector2_


def GetGestureDragAngle() -> float:
    return_interface = _mod._GetGestureDragAngle()
    return return_interface


def GetGesturePinchVector() -> Vector2:
    Vector2_ = Vector2()
    _mod._GetGesturePinchVector(Vector2_._address)
    return Vector2_


def GetGesturePinchAngle() -> float:
    return_interface = _mod._GetGesturePinchAngle()
    return return_interface


def UpdateCamera(camera: int, mode: int):
    _mod._UpdateCamera(camera, mode)


def UpdateCameraPro(camera: int, movement: Vector3, rotation: Vector3, zoom: float):
    _mod._UpdateCameraPro(camera, movement._address, rotation._address, zoom)


def SetShapesTexture(texture: Texture2D, source: Rectangle):
    _mod._SetShapesTexture(texture._address, source._address)


def DrawPixel(posX: int, posY: int, color: Color):
    _mod._DrawPixel(posX, posY, color._address)


def DrawPixelV(position: Vector2, color: Color):
    _mod._DrawPixelV(position._address, color._address)


def DrawLine(startPosX: int, startPosY: int, endPosX: int, endPosY: int, color: Color):
    _mod._DrawLine(startPosX, startPosY, endPosX, endPosY, color._address)


def DrawLineV(startPos: Vector2, endPos: Vector2, color: Color):
    _mod._DrawLineV(startPos._address, endPos._address, color._address)


def DrawLineEx(startPos: Vector2, endPos: Vector2, thick: float, color: Color):
    _mod._DrawLineEx(startPos._address, endPos._address, thick, color._address)


def DrawLineBezier(startPos: Vector2, endPos: Vector2, thick: float, color: Color):
    _mod._DrawLineBezier(startPos._address, endPos._address, thick, color._address)


def DrawLineBezierQuad(startPos: Vector2, endPos: Vector2, controlPos: Vector2, thick: float, color: Color):
    _mod._DrawLineBezierQuad(startPos._address, endPos._address, controlPos._address, thick, color._address)


def DrawLineBezierCubic(startPos: Vector2, endPos: Vector2, startControlPos: Vector2, endControlPos: Vector2, thick: float, color: Color):
    _mod._DrawLineBezierCubic(startPos._address, endPos._address, startControlPos._address, endControlPos._address, thick, color._address)


def DrawLineStrip(points: int, pointCount: int, color: Color):
    _mod._DrawLineStrip(points, pointCount, color._address)


def DrawCircle(centerX: int, centerY: int, radius: float, color: Color):
    _mod._DrawCircle(centerX, centerY, radius, color._address)


def DrawCircleSector(center: Vector2, radius: float, startAngle: float, endAngle: float, segments: int, color: Color):
    _mod._DrawCircleSector(center._address, radius, startAngle, endAngle, segments, color._address)


def DrawCircleSectorLines(center: Vector2, radius: float, startAngle: float, endAngle: float, segments: int, color: Color):
    _mod._DrawCircleSectorLines(center._address, radius, startAngle, endAngle, segments, color._address)


def DrawCircleGradient(centerX: int, centerY: int, radius: float, color1: Color, color2: Color):
    _mod._DrawCircleGradient(centerX, centerY, radius, color1._address, color2._address)


def DrawCircleV(center: Vector2, radius: float, color: Color):
    _mod._DrawCircleV(center._address, radius, color._address)


def DrawCircleLines(centerX: int, centerY: int, radius: float, color: Color):
    _mod._DrawCircleLines(centerX, centerY, radius, color._address)


def DrawEllipse(centerX: int, centerY: int, radiusH: float, radiusV: float, color: Color):
    _mod._DrawEllipse(centerX, centerY, radiusH, radiusV, color._address)


def DrawEllipseLines(centerX: int, centerY: int, radiusH: float, radiusV: float, color: Color):
    _mod._DrawEllipseLines(centerX, centerY, radiusH, radiusV, color._address)


def DrawRing(center: Vector2, innerRadius: float, outerRadius: float, startAngle: float, endAngle: float, segments: int, color: Color):
    _mod._DrawRing(center._address, innerRadius, outerRadius, startAngle, endAngle, segments, color._address)


def DrawRingLines(center: Vector2, innerRadius: float, outerRadius: float, startAngle: float, endAngle: float, segments: int, color: Color):
    _mod._DrawRingLines(center._address, innerRadius, outerRadius, startAngle, endAngle, segments, color._address)


def DrawRectangle(posX: int, posY: int, width: int, height: int, color: Color):
    _mod._DrawRectangle(posX, posY, width, height, color._address)


def DrawRectangleV(position: Vector2, size: Vector2, color: Color):
    _mod._DrawRectangleV(position._address, size._address, color._address)


def DrawRectangleRec(rec: Rectangle, color: Color):
    _mod._DrawRectangleRec(rec._address, color._address)


def DrawRectanglePro(rec: Rectangle, origin: Vector2, rotation: float, color: Color):
    _mod._DrawRectanglePro(rec._address, origin._address, rotation, color._address)


def DrawRectangleGradientV(posX: int, posY: int, width: int, height: int, color1: Color, color2: Color):
    _mod._DrawRectangleGradientV(posX, posY, width, height, color1._address, color2._address)


def DrawRectangleGradientH(posX: int, posY: int, width: int, height: int, color1: Color, color2: Color):
    _mod._DrawRectangleGradientH(posX, posY, width, height, color1._address, color2._address)


def DrawRectangleGradientEx(rec: Rectangle, col1: Color, col2: Color, col3: Color, col4: Color):
    _mod._DrawRectangleGradientEx(rec._address, col1._address, col2._address, col3._address, col4._address)


def DrawRectangleLines(posX: int, posY: int, width: int, height: int, color: Color):
    _mod._DrawRectangleLines(posX, posY, width, height, color._address)


def DrawRectangleLinesEx(rec: Rectangle, lineThick: float, color: Color):
    _mod._DrawRectangleLinesEx(rec._address, lineThick, color._address)


def DrawRectangleRounded(rec: Rectangle, roundness: float, segments: int, color: Color):
    _mod._DrawRectangleRounded(rec._address, roundness, segments, color._address)


def DrawRectangleRoundedLines(rec: Rectangle, roundness: float, segments: int, lineThick: float, color: Color):
    _mod._DrawRectangleRoundedLines(rec._address, roundness, segments, lineThick, color._address)


def DrawTriangle(v1: Vector2, v2: Vector2, v3: Vector2, color: Color):
    _mod._DrawTriangle(v1._address, v2._address, v3._address, color._address)


def DrawTriangleLines(v1: Vector2, v2: Vector2, v3: Vector2, color: Color):
    _mod._DrawTriangleLines(v1._address, v2._address, v3._address, color._address)


def DrawTriangleFan(points: int, pointCount: int, color: Color):
    _mod._DrawTriangleFan(points, pointCount, color._address)


def DrawTriangleStrip(points: int, pointCount: int, color: Color):
    _mod._DrawTriangleStrip(points, pointCount, color._address)


def DrawPoly(center: Vector2, sides: int, radius: float, rotation: float, color: Color):
    _mod._DrawPoly(center._address, sides, radius, rotation, color._address)


def DrawPolyLines(center: Vector2, sides: int, radius: float, rotation: float, color: Color):
    _mod._DrawPolyLines(center._address, sides, radius, rotation, color._address)


def DrawPolyLinesEx(center: Vector2, sides: int, radius: float, rotation: float, lineThick: float, color: Color):
    _mod._DrawPolyLinesEx(center._address, sides, radius, rotation, lineThick, color._address)


def CheckCollisionRecs(rec1: Rectangle, rec2: Rectangle) -> int:
    return_interface = _mod._CheckCollisionRecs(rec1._address, rec2._address)
    return return_interface


def CheckCollisionCircles(center1: Vector2, radius1: float, center2: Vector2, radius2: float) -> int:
    return_interface = _mod._CheckCollisionCircles(center1._address, radius1, center2._address, radius2)
    return return_interface


def CheckCollisionCircleRec(center: Vector2, radius: float, rec: Rectangle) -> int:
    return_interface = _mod._CheckCollisionCircleRec(center._address, radius, rec._address)
    return return_interface


def CheckCollisionPointRec(point: Vector2, rec: Rectangle) -> int:
    return_interface = _mod._CheckCollisionPointRec(point._address, rec._address)
    return return_interface


def CheckCollisionPointCircle(point: Vector2, center: Vector2, radius: float) -> int:
    return_interface = _mod._CheckCollisionPointCircle(point._address, center._address, radius)
    return return_interface


def CheckCollisionPointTriangle(point: Vector2, p1: Vector2, p2: Vector2, p3: Vector2) -> int:
    return_interface = _mod._CheckCollisionPointTriangle(point._address, p1._address, p2._address, p3._address)
    return return_interface


def CheckCollisionPointPoly(point: Vector2, points: int, pointCount: int) -> int:
    return_interface = _mod._CheckCollisionPointPoly(point._address, points, pointCount)
    return return_interface


def CheckCollisionLines(startPos1: Vector2, endPos1: Vector2, startPos2: Vector2, endPos2: Vector2, collisionPoint: int) -> int:
    return_interface = _mod._CheckCollisionLines(startPos1._address, endPos1._address, startPos2._address, endPos2._address, collisionPoint)
    return return_interface


def CheckCollisionPointLine(point: Vector2, p1: Vector2, p2: Vector2, threshold: int) -> int:
    return_interface = _mod._CheckCollisionPointLine(point._address, p1._address, p2._address, threshold)
    return return_interface


def GetCollisionRec(rec1: Rectangle, rec2: Rectangle) -> Rectangle:
    Rectangle_ = Rectangle()
    _mod._GetCollisionRec(Rectangle_._address, rec1._address, rec2._address)
    return Rectangle_


def LoadImage(fileName: str) -> Image:
    Image_ = Image()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadImage(Image_._address, fileName_)
    _mod._free(fileName_)
    return Image_


def LoadImageRaw(fileName: str, width: int, height: int, format: int, headerSize: int) -> Image:
    Image_ = Image()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadImageRaw(Image_._address, fileName_, width, height, format, headerSize)
    _mod._free(fileName_)
    return Image_


def LoadImageAnim(fileName: str, frames: int) -> Image:
    Image_ = Image()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadImageAnim(Image_._address, fileName_, frames)
    _mod._free(fileName_)
    return Image_


def LoadImageFromMemory(fileType: str, fileData: int, dataSize: int) -> Image:
    Image_ = Image()
    fileType_ = _mod._malloc(len(fileType) + 1)
    _mod.stringToUTF8(fileType, fileType_, len(fileType) + 1)
    _mod._LoadImageFromMemory(Image_._address, fileType_, fileData, dataSize)
    _mod._free(fileType_)
    return Image_


def LoadImageFromTexture(texture: Texture2D) -> Image:
    Image_ = Image()
    _mod._LoadImageFromTexture(Image_._address, texture._address)
    return Image_


def LoadImageFromScreen() -> Image:
    Image_ = Image()
    _mod._LoadImageFromScreen(Image_._address)
    return Image_


def IsImageReady(image: Image) -> int:
    return_interface = _mod._IsImageReady(image._address)
    return return_interface


def UnloadImage(image: Image):
    _mod._UnloadImage(image._address)


def ExportImage(image: Image, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportImage(image._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def ExportImageToMemory(image: Image, fileType: str, fileSize: int) -> int:
    fileType_ = _mod._malloc(len(fileType) + 1)
    _mod.stringToUTF8(fileType, fileType_, len(fileType) + 1)
    return_interface = _mod._ExportImageToMemory(image._address, fileType_, fileSize)
    _mod._free(fileType_)
    return return_interface


def ExportImageAsCode(image: Image, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportImageAsCode(image._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def GenImageColor(width: int, height: int, color: Color) -> Image:
    Image_ = Image()
    _mod._GenImageColor(Image_._address, width, height, color._address)
    return Image_


def GenImageGradientLinear(width: int, height: int, direction: int, start: Color, end: Color) -> Image:
    Image_ = Image()
    _mod._GenImageGradientLinear(Image_._address, width, height, direction, start._address, end._address)
    return Image_


def GenImageGradientRadial(width: int, height: int, density: float, inner: Color, outer: Color) -> Image:
    Image_ = Image()
    _mod._GenImageGradientRadial(Image_._address, width, height, density, inner._address, outer._address)
    return Image_


def GenImageGradientSquare(width: int, height: int, density: float, inner: Color, outer: Color) -> Image:
    Image_ = Image()
    _mod._GenImageGradientSquare(Image_._address, width, height, density, inner._address, outer._address)
    return Image_


def GenImageChecked(width: int, height: int, checksX: int, checksY: int, col1: Color, col2: Color) -> Image:
    Image_ = Image()
    _mod._GenImageChecked(Image_._address, width, height, checksX, checksY, col1._address, col2._address)
    return Image_


def GenImageWhiteNoise(width: int, height: int, factor: float) -> Image:
    Image_ = Image()
    _mod._GenImageWhiteNoise(Image_._address, width, height, factor)
    return Image_


def GenImagePerlinNoise(width: int, height: int, offsetX: int, offsetY: int, scale: float) -> Image:
    Image_ = Image()
    _mod._GenImagePerlinNoise(Image_._address, width, height, offsetX, offsetY, scale)
    return Image_


def GenImageCellular(width: int, height: int, tileSize: int) -> Image:
    Image_ = Image()
    _mod._GenImageCellular(Image_._address, width, height, tileSize)
    return Image_


def GenImageText(width: int, height: int, text: str) -> Image:
    Image_ = Image()
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._GenImageText(Image_._address, width, height, text_)
    _mod._free(text_)
    return Image_


def ImageCopy(image: Image) -> Image:
    Image_ = Image()
    _mod._ImageCopy(Image_._address, image._address)
    return Image_


def ImageFromImage(image: Image, rec: Rectangle) -> Image:
    Image_ = Image()
    _mod._ImageFromImage(Image_._address, image._address, rec._address)
    return Image_


def ImageText(text: str, fontSize: int, color: Color) -> Image:
    Image_ = Image()
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._ImageText(Image_._address, text_, fontSize, color._address)
    _mod._free(text_)
    return Image_


def ImageTextEx(font: Font, text: str, fontSize: float, spacing: float, tint: Color) -> Image:
    Image_ = Image()
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._ImageTextEx(Image_._address, font._address, text_, fontSize, spacing, tint._address)
    _mod._free(text_)
    return Image_


def ImageFormat(image: int, newFormat: int):
    _mod._ImageFormat(image, newFormat)


def ImageToPOT(image: int, fill: Color):
    _mod._ImageToPOT(image, fill._address)


def ImageCrop(image: int, crop: Rectangle):
    _mod._ImageCrop(image, crop._address)


def ImageAlphaCrop(image: int, threshold: float):
    _mod._ImageAlphaCrop(image, threshold)


def ImageAlphaClear(image: int, color: Color, threshold: float):
    _mod._ImageAlphaClear(image, color._address, threshold)


def ImageAlphaMask(image: int, alphaMask: Image):
    _mod._ImageAlphaMask(image, alphaMask._address)


def ImageAlphaPremultiply(image: int):
    _mod._ImageAlphaPremultiply(image)


def ImageBlurGaussian(image: int, blurSize: int):
    _mod._ImageBlurGaussian(image, blurSize)


def ImageResize(image: int, newWidth: int, newHeight: int):
    _mod._ImageResize(image, newWidth, newHeight)


def ImageResizeNN(image: int, newWidth: int, newHeight: int):
    _mod._ImageResizeNN(image, newWidth, newHeight)


def ImageResizeCanvas(image: int, newWidth: int, newHeight: int, offsetX: int, offsetY: int, fill: Color):
    _mod._ImageResizeCanvas(image, newWidth, newHeight, offsetX, offsetY, fill._address)


def ImageMipmaps(image: int):
    _mod._ImageMipmaps(image)


def ImageDither(image: int, rBpp: int, gBpp: int, bBpp: int, aBpp: int):
    _mod._ImageDither(image, rBpp, gBpp, bBpp, aBpp)


def ImageFlipVertical(image: int):
    _mod._ImageFlipVertical(image)


def ImageFlipHorizontal(image: int):
    _mod._ImageFlipHorizontal(image)


def ImageRotate(image: int, degrees: int):
    _mod._ImageRotate(image, degrees)


def ImageRotateCW(image: int):
    _mod._ImageRotateCW(image)


def ImageRotateCCW(image: int):
    _mod._ImageRotateCCW(image)


def ImageColorTint(image: int, color: Color):
    _mod._ImageColorTint(image, color._address)


def ImageColorInvert(image: int):
    _mod._ImageColorInvert(image)


def ImageColorGrayscale(image: int):
    _mod._ImageColorGrayscale(image)


def ImageColorContrast(image: int, contrast: float):
    _mod._ImageColorContrast(image, contrast)


def ImageColorBrightness(image: int, brightness: int):
    _mod._ImageColorBrightness(image, brightness)


def ImageColorReplace(image: int, color: Color, replace: Color):
    _mod._ImageColorReplace(image, color._address, replace._address)


def LoadImageColors(image: Image) -> int:
    return_interface = _mod._LoadImageColors(image._address)
    return return_interface


def LoadImagePalette(image: Image, maxPaletteSize: int, colorCount: int) -> int:
    return_interface = _mod._LoadImagePalette(image._address, maxPaletteSize, colorCount)
    return return_interface


def UnloadImageColors(colors: int):
    _mod._UnloadImageColors(colors)


def UnloadImagePalette(colors: int):
    _mod._UnloadImagePalette(colors)


def GetImageAlphaBorder(image: Image, threshold: float) -> Rectangle:
    Rectangle_ = Rectangle()
    _mod._GetImageAlphaBorder(Rectangle_._address, image._address, threshold)
    return Rectangle_


def GetImageColor(image: Image, x: int, y: int) -> Color:
    Color_ = Color()
    _mod._GetImageColor(Color_._address, image._address, x, y)
    return Color_


def ImageClearBackground(dst: int, color: Color):
    _mod._ImageClearBackground(dst, color._address)


def ImageDrawPixel(dst: int, posX: int, posY: int, color: Color):
    _mod._ImageDrawPixel(dst, posX, posY, color._address)


def ImageDrawPixelV(dst: int, position: Vector2, color: Color):
    _mod._ImageDrawPixelV(dst, position._address, color._address)


def ImageDrawLine(dst: int, startPosX: int, startPosY: int, endPosX: int, endPosY: int, color: Color):
    _mod._ImageDrawLine(dst, startPosX, startPosY, endPosX, endPosY, color._address)


def ImageDrawLineV(dst: int, start: Vector2, end: Vector2, color: Color):
    _mod._ImageDrawLineV(dst, start._address, end._address, color._address)


def ImageDrawCircle(dst: int, centerX: int, centerY: int, radius: int, color: Color):
    _mod._ImageDrawCircle(dst, centerX, centerY, radius, color._address)


def ImageDrawCircleV(dst: int, center: Vector2, radius: int, color: Color):
    _mod._ImageDrawCircleV(dst, center._address, radius, color._address)


def ImageDrawCircleLines(dst: int, centerX: int, centerY: int, radius: int, color: Color):
    _mod._ImageDrawCircleLines(dst, centerX, centerY, radius, color._address)


def ImageDrawCircleLinesV(dst: int, center: Vector2, radius: int, color: Color):
    _mod._ImageDrawCircleLinesV(dst, center._address, radius, color._address)


def ImageDrawRectangle(dst: int, posX: int, posY: int, width: int, height: int, color: Color):
    _mod._ImageDrawRectangle(dst, posX, posY, width, height, color._address)


def ImageDrawRectangleV(dst: int, position: Vector2, size: Vector2, color: Color):
    _mod._ImageDrawRectangleV(dst, position._address, size._address, color._address)


def ImageDrawRectangleRec(dst: int, rec: Rectangle, color: Color):
    _mod._ImageDrawRectangleRec(dst, rec._address, color._address)


def ImageDrawRectangleLines(dst: int, rec: Rectangle, thick: int, color: Color):
    _mod._ImageDrawRectangleLines(dst, rec._address, thick, color._address)


def ImageDraw(dst: int, src: Image, srcRec: Rectangle, dstRec: Rectangle, tint: Color):
    _mod._ImageDraw(dst, src._address, srcRec._address, dstRec._address, tint._address)


def ImageDrawText(dst: int, text: str, posX: int, posY: int, fontSize: int, color: Color):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._ImageDrawText(dst, text_, posX, posY, fontSize, color._address)
    _mod._free(text_)


def ImageDrawTextEx(dst: int, font: Font, text: str, position: Vector2, fontSize: float, spacing: float, tint: Color):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._ImageDrawTextEx(dst, font._address, text_, position._address, fontSize, spacing, tint._address)
    _mod._free(text_)


def LoadTexture(fileName: str) -> Texture2D:
    Texture2D_ = Texture2D()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadTexture(Texture2D_._address, fileName_)
    _mod._free(fileName_)
    return Texture2D_


def LoadTextureFromImage(image: Image) -> Texture2D:
    Texture2D_ = Texture2D()
    _mod._LoadTextureFromImage(Texture2D_._address, image._address)
    return Texture2D_


def LoadTextureCubemap(image: Image, layout: int) -> TextureCubemap:
    TextureCubemap_ = TextureCubemap()
    _mod._LoadTextureCubemap(TextureCubemap_._address, image._address, layout)
    return TextureCubemap_


def LoadRenderTexture(width: int, height: int) -> RenderTexture2D:
    RenderTexture2D_ = RenderTexture2D()
    _mod._LoadRenderTexture(RenderTexture2D_._address, width, height)
    return RenderTexture2D_


def IsTextureReady(texture: Texture2D) -> int:
    return_interface = _mod._IsTextureReady(texture._address)
    return return_interface


def UnloadTexture(texture: Texture2D):
    _mod._UnloadTexture(texture._address)


def IsRenderTextureReady(target: RenderTexture2D) -> int:
    return_interface = _mod._IsRenderTextureReady(target._address)
    return return_interface


def UnloadRenderTexture(target: RenderTexture2D):
    _mod._UnloadRenderTexture(target._address)


def UpdateTexture(texture: Texture2D, pixels: int):
    _mod._UpdateTexture(texture._address, pixels)


def UpdateTextureRec(texture: Texture2D, rec: Rectangle, pixels: int):
    _mod._UpdateTextureRec(texture._address, rec._address, pixels)


def GenTextureMipmaps(texture: int):
    _mod._GenTextureMipmaps(texture)


def SetTextureFilter(texture: Texture2D, filter: int):
    _mod._SetTextureFilter(texture._address, filter)


def SetTextureWrap(texture: Texture2D, wrap: int):
    _mod._SetTextureWrap(texture._address, wrap)


def DrawTexture(texture: Texture2D, posX: int, posY: int, tint: Color):
    _mod._DrawTexture(texture._address, posX, posY, tint._address)


def DrawTextureV(texture: Texture2D, position: Vector2, tint: Color):
    _mod._DrawTextureV(texture._address, position._address, tint._address)


def DrawTextureEx(texture: Texture2D, position: Vector2, rotation: float, scale: float, tint: Color):
    _mod._DrawTextureEx(texture._address, position._address, rotation, scale, tint._address)


def DrawTextureRec(texture: Texture2D, source: Rectangle, position: Vector2, tint: Color):
    _mod._DrawTextureRec(texture._address, source._address, position._address, tint._address)


def DrawTexturePro(texture: Texture2D, source: Rectangle, dest: Rectangle, origin: Vector2, rotation: float, tint: Color):
    _mod._DrawTexturePro(texture._address, source._address, dest._address, origin._address, rotation, tint._address)


def DrawTextureNPatch(texture: Texture2D, nPatchInfo: NPatchInfo, dest: Rectangle, origin: Vector2, rotation: float, tint: Color):
    _mod._DrawTextureNPatch(texture._address, nPatchInfo._address, dest._address, origin._address, rotation, tint._address)


def Fade(color: Color, alpha: float) -> Color:
    Color_ = Color()
    _mod._Fade(Color_._address, color._address, alpha)
    return Color_


def ColorToInt(color: Color) -> int:
    return_interface = _mod._ColorToInt(color._address)
    return return_interface


def ColorNormalize(color: Color) -> Vector4:
    Vector4_ = Vector4()
    _mod._ColorNormalize(Vector4_._address, color._address)
    return Vector4_


def ColorFromNormalized(normalized: Vector4) -> Color:
    Color_ = Color()
    _mod._ColorFromNormalized(Color_._address, normalized._address)
    return Color_


def ColorToHSV(color: Color) -> Vector3:
    Vector3_ = Vector3()
    _mod._ColorToHSV(Vector3_._address, color._address)
    return Vector3_


def ColorFromHSV(hue: float, saturation: float, value: float) -> Color:
    Color_ = Color()
    _mod._ColorFromHSV(Color_._address, hue, saturation, value)
    return Color_


def ColorTint(color: Color, tint: Color) -> Color:
    Color_ = Color()
    _mod._ColorTint(Color_._address, color._address, tint._address)
    return Color_


def ColorBrightness(color: Color, factor: float) -> Color:
    Color_ = Color()
    _mod._ColorBrightness(Color_._address, color._address, factor)
    return Color_


def ColorContrast(color: Color, contrast: float) -> Color:
    Color_ = Color()
    _mod._ColorContrast(Color_._address, color._address, contrast)
    return Color_


def ColorAlpha(color: Color, alpha: float) -> Color:
    Color_ = Color()
    _mod._ColorAlpha(Color_._address, color._address, alpha)
    return Color_


def ColorAlphaBlend(dst: Color, src: Color, tint: Color) -> Color:
    Color_ = Color()
    _mod._ColorAlphaBlend(Color_._address, dst._address, src._address, tint._address)
    return Color_


def GetColor(hexValue: int) -> Color:
    Color_ = Color()
    _mod._GetColor(Color_._address, hexValue)
    return Color_


def GetPixelColor(srcPtr: int, format: int) -> Color:
    Color_ = Color()
    _mod._GetPixelColor(Color_._address, srcPtr, format)
    return Color_


def SetPixelColor(dstPtr: int, color: Color, format: int):
    _mod._SetPixelColor(dstPtr, color._address, format)


def GetPixelDataSize(width: int, height: int, format: int) -> int:
    return_interface = _mod._GetPixelDataSize(width, height, format)
    return return_interface


def GetFontDefault() -> Font:
    Font_ = Font()
    _mod._GetFontDefault(Font_._address)
    return Font_


def LoadFont(fileName: str) -> Font:
    Font_ = Font()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadFont(Font_._address, fileName_)
    _mod._free(fileName_)
    return Font_


def LoadFontEx(fileName: str, fontSize: int, fontChars: int, glyphCount: int) -> Font:
    Font_ = Font()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadFontEx(Font_._address, fileName_, fontSize, fontChars, glyphCount)
    _mod._free(fileName_)
    return Font_


def LoadFontFromImage(image: Image, key: Color, firstChar: int) -> Font:
    Font_ = Font()
    _mod._LoadFontFromImage(Font_._address, image._address, key._address, firstChar)
    return Font_


def LoadFontFromMemory(fileType: str, fileData: int, dataSize: int, fontSize: int, fontChars: int, glyphCount: int) -> Font:
    Font_ = Font()
    fileType_ = _mod._malloc(len(fileType) + 1)
    _mod.stringToUTF8(fileType, fileType_, len(fileType) + 1)
    _mod._LoadFontFromMemory(Font_._address, fileType_, fileData, dataSize, fontSize, fontChars, glyphCount)
    _mod._free(fileType_)
    return Font_


def IsFontReady(font: Font) -> int:
    return_interface = _mod._IsFontReady(font._address)
    return return_interface


def LoadFontData(fileData: int, dataSize: int, fontSize: int, fontChars: int, glyphCount: int, type: int) -> int:
    return_interface = _mod._LoadFontData(fileData, dataSize, fontSize, fontChars, glyphCount, type)
    return return_interface


def GenImageFontAtlas(chars: int, recs: int, glyphCount: int, fontSize: int, padding: int, packMethod: int) -> Image:
    Image_ = Image()
    _mod._GenImageFontAtlas(Image_._address, chars, recs, glyphCount, fontSize, padding, packMethod)
    return Image_


def UnloadFontData(chars: int, glyphCount: int):
    _mod._UnloadFontData(chars, glyphCount)


def UnloadFont(font: Font):
    _mod._UnloadFont(font._address)


def ExportFontAsCode(font: Font, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportFontAsCode(font._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def DrawFPS(posX: int, posY: int):
    _mod._DrawFPS(posX, posY)


def DrawText(text: str, posX: int, posY: int, fontSize: int, color: Color):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._DrawText(text_, posX, posY, fontSize, color._address)
    _mod._free(text_)


def DrawTextEx(font: Font, text: str, position: Vector2, fontSize: float, spacing: float, tint: Color):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._DrawTextEx(font._address, text_, position._address, fontSize, spacing, tint._address)
    _mod._free(text_)


def DrawTextPro(font: Font, text: str, position: Vector2, origin: Vector2, rotation: float, fontSize: float, spacing: float, tint: Color):
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._DrawTextPro(font._address, text_, position._address, origin._address, rotation, fontSize, spacing, tint._address)
    _mod._free(text_)


def DrawTextCodepoint(font: Font, codepoint: int, position: Vector2, fontSize: float, tint: Color):
    _mod._DrawTextCodepoint(font._address, codepoint, position._address, fontSize, tint._address)


def DrawTextCodepoints(font: Font, codepoints: int, count: int, position: Vector2, fontSize: float, spacing: float, tint: Color):
    _mod._DrawTextCodepoints(font._address, codepoints, count, position._address, fontSize, spacing, tint._address)


def SetTextLineSpacing(spacing: int):
    _mod._SetTextLineSpacing(spacing)


def MeasureText(text: str, fontSize: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._MeasureText(text_, fontSize)
    _mod._free(text_)
    return return_interface


def MeasureTextEx(font: Font, text: str, fontSize: float, spacing: float) -> Vector2:
    Vector2_ = Vector2()
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    _mod._MeasureTextEx(Vector2_._address, font._address, text_, fontSize, spacing)
    _mod._free(text_)
    return Vector2_


def GetGlyphIndex(font: Font, codepoint: int) -> int:
    return_interface = _mod._GetGlyphIndex(font._address, codepoint)
    return return_interface


def GetGlyphInfo(font: Font, codepoint: int) -> GlyphInfo:
    GlyphInfo_ = GlyphInfo()
    _mod._GetGlyphInfo(GlyphInfo_._address, font._address, codepoint)
    return GlyphInfo_


def GetGlyphAtlasRec(font: Font, codepoint: int) -> Rectangle:
    Rectangle_ = Rectangle()
    _mod._GetGlyphAtlasRec(Rectangle_._address, font._address, codepoint)
    return Rectangle_


def LoadUTF8(codepoints: int, length: int) -> int:
    return_interface = _mod._LoadUTF8(codepoints, length)
    return return_interface


def UnloadUTF8(text: int):
    _mod._UnloadUTF8(text)


def LoadCodepoints(text: str, count: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._LoadCodepoints(text_, count)
    _mod._free(text_)
    return return_interface


def UnloadCodepoints(codepoints: int):
    _mod._UnloadCodepoints(codepoints)


def GetCodepointCount(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._GetCodepointCount(text_)
    _mod._free(text_)
    return return_interface


def GetCodepoint(text: str, codepointSize: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._GetCodepoint(text_, codepointSize)
    _mod._free(text_)
    return return_interface


def GetCodepointNext(text: str, codepointSize: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._GetCodepointNext(text_, codepointSize)
    _mod._free(text_)
    return return_interface


def GetCodepointPrevious(text: str, codepointSize: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._GetCodepointPrevious(text_, codepointSize)
    _mod._free(text_)
    return return_interface


def CodepointToUTF8(codepoint: int, utf8Size: int) -> int:
    return_interface = _mod._CodepointToUTF8(codepoint, utf8Size)
    return return_interface


def TextCopy(dst: int, src: str) -> int:
    src_ = _mod._malloc(len(src) + 1)
    _mod.stringToUTF8(src, src_, len(src) + 1)
    return_interface = _mod._TextCopy(dst, src_)
    _mod._free(src_)
    return return_interface


def TextIsEqual(text1: str, text2: str) -> int:
    text1_ = _mod._malloc(len(text1) + 1)
    _mod.stringToUTF8(text1, text1_, len(text1) + 1)
    text2_ = _mod._malloc(len(text2) + 1)
    _mod.stringToUTF8(text2, text2_, len(text2) + 1)
    return_interface = _mod._TextIsEqual(text1_, text2_)
    _mod._free(text1_)
    _mod._free(text2_)
    return return_interface


def TextLength(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextLength(text_)
    _mod._free(text_)
    return return_interface


def TextSubtext(text: str, position: int, length: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextSubtext(text_, position, length)
    _mod._free(text_)
    return return_interface


def TextReplace(text: int, replace: str, by: str) -> int:
    replace_ = _mod._malloc(len(replace) + 1)
    _mod.stringToUTF8(replace, replace_, len(replace) + 1)
    by_ = _mod._malloc(len(by) + 1)
    _mod.stringToUTF8(by, by_, len(by) + 1)
    return_interface = _mod._TextReplace(text, replace_, by_)
    _mod._free(replace_)
    _mod._free(by_)
    return return_interface


def TextInsert(text: str, insert: str, position: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    insert_ = _mod._malloc(len(insert) + 1)
    _mod.stringToUTF8(insert, insert_, len(insert) + 1)
    return_interface = _mod._TextInsert(text_, insert_, position)
    _mod._free(text_)
    _mod._free(insert_)
    return return_interface


def TextJoin(textList: int, count: int, delimiter: str) -> int:
    delimiter_ = _mod._malloc(len(delimiter) + 1)
    _mod.stringToUTF8(delimiter, delimiter_, len(delimiter) + 1)
    return_interface = _mod._TextJoin(textList, count, delimiter_)
    _mod._free(delimiter_)
    return return_interface


def TextSplit(text: str, delimiter: int, count: int) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextSplit(text_, delimiter, count)
    _mod._free(text_)
    return return_interface


def TextAppend(text: int, append: str, position: int):
    append_ = _mod._malloc(len(append) + 1)
    _mod.stringToUTF8(append, append_, len(append) + 1)
    _mod._TextAppend(text, append_, position)
    _mod._free(append_)


def TextFindIndex(text: str, find: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    find_ = _mod._malloc(len(find) + 1)
    _mod.stringToUTF8(find, find_, len(find) + 1)
    return_interface = _mod._TextFindIndex(text_, find_)
    _mod._free(text_)
    _mod._free(find_)
    return return_interface


def TextToUpper(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextToUpper(text_)
    _mod._free(text_)
    return return_interface


def TextToLower(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextToLower(text_)
    _mod._free(text_)
    return return_interface


def TextToPascal(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextToPascal(text_)
    _mod._free(text_)
    return return_interface


def TextToInteger(text: str) -> int:
    text_ = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, text_, len(text) + 1)
    return_interface = _mod._TextToInteger(text_)
    _mod._free(text_)
    return return_interface


def DrawLine3D(startPos: Vector3, endPos: Vector3, color: Color):
    _mod._DrawLine3D(startPos._address, endPos._address, color._address)


def DrawPoint3D(position: Vector3, color: Color):
    _mod._DrawPoint3D(position._address, color._address)


def DrawCircle3D(center: Vector3, radius: float, rotationAxis: Vector3, rotationAngle: float, color: Color):
    _mod._DrawCircle3D(center._address, radius, rotationAxis._address, rotationAngle, color._address)


def DrawTriangle3D(v1: Vector3, v2: Vector3, v3: Vector3, color: Color):
    _mod._DrawTriangle3D(v1._address, v2._address, v3._address, color._address)


def DrawTriangleStrip3D(points: int, pointCount: int, color: Color):
    _mod._DrawTriangleStrip3D(points, pointCount, color._address)


def DrawCube(position: Vector3, width: float, height: float, length: float, color: Color):
    _mod._DrawCube(position._address, width, height, length, color._address)


def DrawCubeV(position: Vector3, size: Vector3, color: Color):
    _mod._DrawCubeV(position._address, size._address, color._address)


def DrawCubeWires(position: Vector3, width: float, height: float, length: float, color: Color):
    _mod._DrawCubeWires(position._address, width, height, length, color._address)


def DrawCubeWiresV(position: Vector3, size: Vector3, color: Color):
    _mod._DrawCubeWiresV(position._address, size._address, color._address)


def DrawSphere(centerPos: Vector3, radius: float, color: Color):
    _mod._DrawSphere(centerPos._address, radius, color._address)


def DrawSphereEx(centerPos: Vector3, radius: float, rings: int, slices: int, color: Color):
    _mod._DrawSphereEx(centerPos._address, radius, rings, slices, color._address)


def DrawSphereWires(centerPos: Vector3, radius: float, rings: int, slices: int, color: Color):
    _mod._DrawSphereWires(centerPos._address, radius, rings, slices, color._address)


def DrawCylinder(position: Vector3, radiusTop: float, radiusBottom: float, height: float, slices: int, color: Color):
    _mod._DrawCylinder(position._address, radiusTop, radiusBottom, height, slices, color._address)


def DrawCylinderEx(startPos: Vector3, endPos: Vector3, startRadius: float, endRadius: float, sides: int, color: Color):
    _mod._DrawCylinderEx(startPos._address, endPos._address, startRadius, endRadius, sides, color._address)


def DrawCylinderWires(position: Vector3, radiusTop: float, radiusBottom: float, height: float, slices: int, color: Color):
    _mod._DrawCylinderWires(position._address, radiusTop, radiusBottom, height, slices, color._address)


def DrawCylinderWiresEx(startPos: Vector3, endPos: Vector3, startRadius: float, endRadius: float, sides: int, color: Color):
    _mod._DrawCylinderWiresEx(startPos._address, endPos._address, startRadius, endRadius, sides, color._address)


def DrawCapsule(startPos: Vector3, endPos: Vector3, radius: float, slices: int, rings: int, color: Color):
    _mod._DrawCapsule(startPos._address, endPos._address, radius, slices, rings, color._address)


def DrawCapsuleWires(startPos: Vector3, endPos: Vector3, radius: float, slices: int, rings: int, color: Color):
    _mod._DrawCapsuleWires(startPos._address, endPos._address, radius, slices, rings, color._address)


def DrawPlane(centerPos: Vector3, size: Vector2, color: Color):
    _mod._DrawPlane(centerPos._address, size._address, color._address)


def DrawRay(ray: Ray, color: Color):
    _mod._DrawRay(ray._address, color._address)


def DrawGrid(slices: int, spacing: float):
    _mod._DrawGrid(slices, spacing)


def LoadModel(fileName: str) -> Model:
    Model_ = Model()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadModel(Model_._address, fileName_)
    _mod._free(fileName_)
    return Model_


def LoadModelFromMesh(mesh: Mesh) -> Model:
    Model_ = Model()
    _mod._LoadModelFromMesh(Model_._address, mesh._address)
    return Model_


def IsModelReady(model: Model) -> int:
    return_interface = _mod._IsModelReady(model._address)
    return return_interface


def UnloadModel(model: Model):
    _mod._UnloadModel(model._address)


def GetModelBoundingBox(model: Model) -> BoundingBox:
    BoundingBox_ = BoundingBox()
    _mod._GetModelBoundingBox(BoundingBox_._address, model._address)
    return BoundingBox_


def DrawModel(model: Model, position: Vector3, scale: float, tint: Color):
    _mod._DrawModel(model._address, position._address, scale, tint._address)


def DrawModelEx(model: Model, position: Vector3, rotationAxis: Vector3, rotationAngle: float, scale: Vector3, tint: Color):
    _mod._DrawModelEx(model._address, position._address, rotationAxis._address, rotationAngle, scale._address, tint._address)


def DrawModelWires(model: Model, position: Vector3, scale: float, tint: Color):
    _mod._DrawModelWires(model._address, position._address, scale, tint._address)


def DrawModelWiresEx(model: Model, position: Vector3, rotationAxis: Vector3, rotationAngle: float, scale: Vector3, tint: Color):
    _mod._DrawModelWiresEx(model._address, position._address, rotationAxis._address, rotationAngle, scale._address, tint._address)


def DrawBoundingBox(box: BoundingBox, color: Color):
    _mod._DrawBoundingBox(box._address, color._address)


def DrawBillboard(camera: Camera, texture: Texture2D, position: Vector3, size: float, tint: Color):
    _mod._DrawBillboard(camera._address, texture._address, position._address, size, tint._address)


def DrawBillboardRec(camera: Camera, texture: Texture2D, source: Rectangle, position: Vector3, size: Vector2, tint: Color):
    _mod._DrawBillboardRec(camera._address, texture._address, source._address, position._address, size._address, tint._address)


def DrawBillboardPro(camera: Camera, texture: Texture2D, source: Rectangle, position: Vector3, up: Vector3, size: Vector2, origin: Vector2, rotation: float, tint: Color):
    _mod._DrawBillboardPro(camera._address, texture._address, source._address, position._address, up._address, size._address, origin._address, rotation, tint._address)


def UploadMesh(mesh: int, dynamic: int):
    _mod._UploadMesh(mesh, dynamic)


def UpdateMeshBuffer(mesh: Mesh, index: int, data: int, dataSize: int, offset: int):
    _mod._UpdateMeshBuffer(mesh._address, index, data, dataSize, offset)


def UnloadMesh(mesh: Mesh):
    _mod._UnloadMesh(mesh._address)


def DrawMesh(mesh: Mesh, material: Material, transform: Matrix):
    _mod._DrawMesh(mesh._address, material._address, transform._address)


def DrawMeshInstanced(mesh: Mesh, material: Material, transforms: int, instances: int):
    _mod._DrawMeshInstanced(mesh._address, material._address, transforms, instances)


def ExportMesh(mesh: Mesh, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportMesh(mesh._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def GetMeshBoundingBox(mesh: Mesh) -> BoundingBox:
    BoundingBox_ = BoundingBox()
    _mod._GetMeshBoundingBox(BoundingBox_._address, mesh._address)
    return BoundingBox_


def GenMeshTangents(mesh: int):
    _mod._GenMeshTangents(mesh)


def GenMeshPoly(sides: int, radius: float) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshPoly(Mesh_._address, sides, radius)
    return Mesh_


def GenMeshPlane(width: float, length: float, resX: int, resZ: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshPlane(Mesh_._address, width, length, resX, resZ)
    return Mesh_


def GenMeshCube(width: float, height: float, length: float) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshCube(Mesh_._address, width, height, length)
    return Mesh_


def GenMeshSphere(radius: float, rings: int, slices: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshSphere(Mesh_._address, radius, rings, slices)
    return Mesh_


def GenMeshHemiSphere(radius: float, rings: int, slices: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshHemiSphere(Mesh_._address, radius, rings, slices)
    return Mesh_


def GenMeshCylinder(radius: float, height: float, slices: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshCylinder(Mesh_._address, radius, height, slices)
    return Mesh_


def GenMeshCone(radius: float, height: float, slices: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshCone(Mesh_._address, radius, height, slices)
    return Mesh_


def GenMeshTorus(radius: float, size: float, radSeg: int, sides: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshTorus(Mesh_._address, radius, size, radSeg, sides)
    return Mesh_


def GenMeshKnot(radius: float, size: float, radSeg: int, sides: int) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshKnot(Mesh_._address, radius, size, radSeg, sides)
    return Mesh_


def GenMeshHeightmap(heightmap: Image, size: Vector3) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshHeightmap(Mesh_._address, heightmap._address, size._address)
    return Mesh_


def GenMeshCubicmap(cubicmap: Image, cubeSize: Vector3) -> Mesh:
    Mesh_ = Mesh()
    _mod._GenMeshCubicmap(Mesh_._address, cubicmap._address, cubeSize._address)
    return Mesh_


def LoadMaterials(fileName: str, materialCount: int) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._LoadMaterials(fileName_, materialCount)
    _mod._free(fileName_)
    return return_interface


def LoadMaterialDefault() -> Material:
    Material_ = Material()
    _mod._LoadMaterialDefault(Material_._address)
    return Material_


def IsMaterialReady(material: Material) -> int:
    return_interface = _mod._IsMaterialReady(material._address)
    return return_interface


def UnloadMaterial(material: Material):
    _mod._UnloadMaterial(material._address)


def SetMaterialTexture(material: int, mapType: int, texture: Texture2D):
    _mod._SetMaterialTexture(material, mapType, texture._address)


def SetModelMeshMaterial(model: int, meshId: int, materialId: int):
    _mod._SetModelMeshMaterial(model, meshId, materialId)


def LoadModelAnimations(fileName: str, animCount: int) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._LoadModelAnimations(fileName_, animCount)
    _mod._free(fileName_)
    return return_interface


def UpdateModelAnimation(model: Model, anim: ModelAnimation, frame: int):
    _mod._UpdateModelAnimation(model._address, anim._address, frame)


def UnloadModelAnimation(anim: ModelAnimation):
    _mod._UnloadModelAnimation(anim._address)


def UnloadModelAnimations(animations: int, count: int):
    _mod._UnloadModelAnimations(animations, count)


def IsModelAnimationValid(model: Model, anim: ModelAnimation) -> int:
    return_interface = _mod._IsModelAnimationValid(model._address, anim._address)
    return return_interface


def CheckCollisionSpheres(center1: Vector3, radius1: float, center2: Vector3, radius2: float) -> int:
    return_interface = _mod._CheckCollisionSpheres(center1._address, radius1, center2._address, radius2)
    return return_interface


def CheckCollisionBoxes(box1: BoundingBox, box2: BoundingBox) -> int:
    return_interface = _mod._CheckCollisionBoxes(box1._address, box2._address)
    return return_interface


def CheckCollisionBoxSphere(box: BoundingBox, center: Vector3, radius: float) -> int:
    return_interface = _mod._CheckCollisionBoxSphere(box._address, center._address, radius)
    return return_interface


def GetRayCollisionSphere(ray: Ray, center: Vector3, radius: float) -> RayCollision:
    RayCollision_ = RayCollision()
    _mod._GetRayCollisionSphere(RayCollision_._address, ray._address, center._address, radius)
    return RayCollision_


def GetRayCollisionBox(ray: Ray, box: BoundingBox) -> RayCollision:
    RayCollision_ = RayCollision()
    _mod._GetRayCollisionBox(RayCollision_._address, ray._address, box._address)
    return RayCollision_


def GetRayCollisionMesh(ray: Ray, mesh: Mesh, transform: Matrix) -> RayCollision:
    RayCollision_ = RayCollision()
    _mod._GetRayCollisionMesh(RayCollision_._address, ray._address, mesh._address, transform._address)
    return RayCollision_


def GetRayCollisionTriangle(ray: Ray, p1: Vector3, p2: Vector3, p3: Vector3) -> RayCollision:
    RayCollision_ = RayCollision()
    _mod._GetRayCollisionTriangle(RayCollision_._address, ray._address, p1._address, p2._address, p3._address)
    return RayCollision_


def GetRayCollisionQuad(ray: Ray, p1: Vector3, p2: Vector3, p3: Vector3, p4: Vector3) -> RayCollision:
    RayCollision_ = RayCollision()
    _mod._GetRayCollisionQuad(RayCollision_._address, ray._address, p1._address, p2._address, p3._address, p4._address)
    return RayCollision_


def InitAudioDevice():
    _mod._InitAudioDevice()


def CloseAudioDevice():
    _mod._CloseAudioDevice()


def IsAudioDeviceReady() -> int:
    return_interface = _mod._IsAudioDeviceReady()
    return return_interface


def SetMasterVolume(volume: float):
    _mod._SetMasterVolume(volume)


def LoadWave(fileName: str) -> Wave:
    Wave_ = Wave()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadWave(Wave_._address, fileName_)
    _mod._free(fileName_)
    return Wave_


def LoadWaveFromMemory(fileType: str, fileData: int, dataSize: int) -> Wave:
    Wave_ = Wave()
    fileType_ = _mod._malloc(len(fileType) + 1)
    _mod.stringToUTF8(fileType, fileType_, len(fileType) + 1)
    _mod._LoadWaveFromMemory(Wave_._address, fileType_, fileData, dataSize)
    _mod._free(fileType_)
    return Wave_


def IsWaveReady(wave: Wave) -> int:
    return_interface = _mod._IsWaveReady(wave._address)
    return return_interface


def LoadSound(fileName: str) -> Sound:
    Sound_ = Sound()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadSound(Sound_._address, fileName_)
    _mod._free(fileName_)
    return Sound_


def LoadSoundFromWave(wave: Wave) -> Sound:
    Sound_ = Sound()
    _mod._LoadSoundFromWave(Sound_._address, wave._address)
    return Sound_


def IsSoundReady(sound: Sound) -> int:
    return_interface = _mod._IsSoundReady(sound._address)
    return return_interface


def UpdateSound(sound: Sound, data: int, sampleCount: int):
    _mod._UpdateSound(sound._address, data, sampleCount)


def UnloadWave(wave: Wave):
    _mod._UnloadWave(wave._address)


def UnloadSound(sound: Sound):
    _mod._UnloadSound(sound._address)


def ExportWave(wave: Wave, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportWave(wave._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def ExportWaveAsCode(wave: Wave, fileName: str) -> int:
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    return_interface = _mod._ExportWaveAsCode(wave._address, fileName_)
    _mod._free(fileName_)
    return return_interface


def PlaySound(sound: Sound):
    _mod._PlaySound(sound._address)


def StopSound(sound: Sound):
    _mod._StopSound(sound._address)


def PauseSound(sound: Sound):
    _mod._PauseSound(sound._address)


def ResumeSound(sound: Sound):
    _mod._ResumeSound(sound._address)


def IsSoundPlaying(sound: Sound) -> int:
    return_interface = _mod._IsSoundPlaying(sound._address)
    return return_interface


def SetSoundVolume(sound: Sound, volume: float):
    _mod._SetSoundVolume(sound._address, volume)


def SetSoundPitch(sound: Sound, pitch: float):
    _mod._SetSoundPitch(sound._address, pitch)


def SetSoundPan(sound: Sound, pan: float):
    _mod._SetSoundPan(sound._address, pan)


def WaveCopy(wave: Wave) -> Wave:
    Wave_ = Wave()
    _mod._WaveCopy(Wave_._address, wave._address)
    return Wave_


def WaveCrop(wave: int, initSample: int, finalSample: int):
    _mod._WaveCrop(wave, initSample, finalSample)


def WaveFormat(wave: int, sampleRate: int, sampleSize: int, channels: int):
    _mod._WaveFormat(wave, sampleRate, sampleSize, channels)


def LoadWaveSamples(wave: Wave) -> int:
    return_interface = _mod._LoadWaveSamples(wave._address)
    return return_interface


def UnloadWaveSamples(samples: int):
    _mod._UnloadWaveSamples(samples)


def LoadMusicStream(fileName: str) -> Music:
    Music_ = Music()
    fileName_ = _mod._malloc(len(fileName) + 1)
    _mod.stringToUTF8(fileName, fileName_, len(fileName) + 1)
    _mod._LoadMusicStream(Music_._address, fileName_)
    _mod._free(fileName_)
    return Music_


def LoadMusicStreamFromMemory(fileType: str, data: int, dataSize: int) -> Music:
    Music_ = Music()
    fileType_ = _mod._malloc(len(fileType) + 1)
    _mod.stringToUTF8(fileType, fileType_, len(fileType) + 1)
    _mod._LoadMusicStreamFromMemory(Music_._address, fileType_, data, dataSize)
    _mod._free(fileType_)
    return Music_


def IsMusicReady(music: Music) -> int:
    return_interface = _mod._IsMusicReady(music._address)
    return return_interface


def UnloadMusicStream(music: Music):
    _mod._UnloadMusicStream(music._address)


def PlayMusicStream(music: Music):
    _mod._PlayMusicStream(music._address)


def IsMusicStreamPlaying(music: Music) -> int:
    return_interface = _mod._IsMusicStreamPlaying(music._address)
    return return_interface


def UpdateMusicStream(music: Music):
    _mod._UpdateMusicStream(music._address)


def StopMusicStream(music: Music):
    _mod._StopMusicStream(music._address)


def PauseMusicStream(music: Music):
    _mod._PauseMusicStream(music._address)


def ResumeMusicStream(music: Music):
    _mod._ResumeMusicStream(music._address)


def SeekMusicStream(music: Music, position: float):
    _mod._SeekMusicStream(music._address, position)


def SetMusicVolume(music: Music, volume: float):
    _mod._SetMusicVolume(music._address, volume)


def SetMusicPitch(music: Music, pitch: float):
    _mod._SetMusicPitch(music._address, pitch)


def SetMusicPan(music: Music, pan: float):
    _mod._SetMusicPan(music._address, pan)


def GetMusicTimeLength(music: Music) -> float:
    return_interface = _mod._GetMusicTimeLength(music._address)
    return return_interface


def GetMusicTimePlayed(music: Music) -> float:
    return_interface = _mod._GetMusicTimePlayed(music._address)
    return return_interface


def LoadAudioStream(sampleRate: int, sampleSize: int, channels: int) -> AudioStream:
    AudioStream_ = AudioStream()
    _mod._LoadAudioStream(AudioStream_._address, sampleRate, sampleSize, channels)
    return AudioStream_


def IsAudioStreamReady(stream: AudioStream) -> int:
    return_interface = _mod._IsAudioStreamReady(stream._address)
    return return_interface


def UnloadAudioStream(stream: AudioStream):
    _mod._UnloadAudioStream(stream._address)


def UpdateAudioStream(stream: AudioStream, data: int, frameCount: int):
    _mod._UpdateAudioStream(stream._address, data, frameCount)


def IsAudioStreamProcessed(stream: AudioStream) -> int:
    return_interface = _mod._IsAudioStreamProcessed(stream._address)
    return return_interface


def PlayAudioStream(stream: AudioStream):
    _mod._PlayAudioStream(stream._address)


def PauseAudioStream(stream: AudioStream):
    _mod._PauseAudioStream(stream._address)


def ResumeAudioStream(stream: AudioStream):
    _mod._ResumeAudioStream(stream._address)


def IsAudioStreamPlaying(stream: AudioStream) -> int:
    return_interface = _mod._IsAudioStreamPlaying(stream._address)
    return return_interface


def StopAudioStream(stream: AudioStream):
    _mod._StopAudioStream(stream._address)


def SetAudioStreamVolume(stream: AudioStream, volume: float):
    _mod._SetAudioStreamVolume(stream._address, volume)


def SetAudioStreamPitch(stream: AudioStream, pitch: float):
    _mod._SetAudioStreamPitch(stream._address, pitch)


def SetAudioStreamPan(stream: AudioStream, pan: float):
    _mod._SetAudioStreamPan(stream._address, pan)


def SetAudioStreamBufferSizeDefault(size: int):
    _mod._SetAudioStreamBufferSizeDefault(size)


LIGHTGRAY: Color = Color(200, 200, 200, 255, frozen=True)  # Light Gray
GRAY: Color = Color(130, 130, 130, 255, frozen=True)  # Gray
DARKGRAY: Color = Color(80, 80, 80, 255, frozen=True)  # Dark Gray
YELLOW: Color = Color(253, 249, 0, 255, frozen=True)  # Yellow
GOLD: Color = Color(255, 203, 0, 255, frozen=True)  # Gold
ORANGE: Color = Color(255, 161, 0, 255, frozen=True)  # Orange
PINK: Color = Color(255, 109, 194, 255, frozen=True)  # Pink
RED: Color = Color(230, 41, 55, 255, frozen=True)  # Red
MAROON: Color = Color(190, 33, 55, 255, frozen=True)  # Maroon
GREEN: Color = Color(0, 228, 48, 255, frozen=True)  # Green
LIME: Color = Color(0, 158, 47, 255, frozen=True)  # Lime
DARKGREEN: Color = Color(0, 117, 44, 255, frozen=True)  # Dark Green
SKYBLUE: Color = Color(102, 191, 255, 255, frozen=True)  # Sky Blue
BLUE: Color = Color(0, 121, 241, 255, frozen=True)  # Blue
DARKBLUE: Color = Color(0, 82, 172, 255, frozen=True)  # Dark Blue
PURPLE: Color = Color(200, 122, 255, 255, frozen=True)  # Purple
VIOLET: Color = Color(135, 60, 190, 255, frozen=True)  # Violet
DARKPURPLE: Color = Color(112, 31, 126, 255, frozen=True)  # Dark Purple
BEIGE: Color = Color(211, 176, 131, 255, frozen=True)  # Beige
BROWN: Color = Color(127, 106, 79, 255, frozen=True)  # Brown
DARKBROWN: Color = Color(76, 63, 47, 255, frozen=True)  # Dark Brown
WHITE: Color = Color(255, 255, 255, 255, frozen=True)  # White
BLACK: Color = Color(0, 0, 0, 255, frozen=True)  # Black
BLANK: Color = Color(0, 0, 0, 0, frozen=True)  # Blank (Transparent)
MAGENTA: Color = Color(255, 0, 255, 255, frozen=True)  # Magenta
RAYWHITE: Color = Color(245, 245, 245, 255, frozen=True)  # My own White (raylib logo)

