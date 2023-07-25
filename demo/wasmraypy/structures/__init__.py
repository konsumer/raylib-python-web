from ..utils import struct_clone


class WasmArray:
    """Generic array-like collection that uses wasm as memory-back"""
    
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



class StructArray(WasmArray):
    """an array of structs"""
    def __init__(self, stype, length, address: int = 0, to_alloc: bool = True):
        super(StructArray, self).__init__(stype.size, length, address, to_alloc)
        self._stype = stype

    def __getitem__(self, item):
        return self._stype(address=(self._address + (self._item_size * item)), to_alloc=False)

    def __setitem__(self, item, value):
        struct_clone(value, self._address + (self._item_size * item))
    

class CharArray(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(CharArray, self).__init__(1, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getInt8(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt8(self._address + (item * self._item_size), value, True)



class UCharArray(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(UCharArray, self).__init__(1, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getUint8(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint8(self._address + (item * self._item_size), value, True)



class Int16Array(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(Int16Array, self).__init__(2, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getInt16(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt16(self._address + (item * self._item_size), value, True)



class UInt16Array(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(UInt16Array, self).__init__(2, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getUint16(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint16(self._address + (item * self._item_size), value, True)



class Int32Array(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(Int32Array, self).__init__(4, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getInt32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt32(self._address + (item * self._item_size), value, True)



class UInt32Array(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(UInt32Array, self).__init__(4, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getUint32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint32(self._address + (item * self._item_size), value, True)



class FloatArray(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(FloatArray, self).__init__(4, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getFloat32(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setFloat32(self._address + (item * self._item_size), value, True)



class DoubleArray(WasmArray):
    def __init__(self, length, address: int = 0, to_alloc: bool = True):
        super(DoubleArray, self).__init__(8, length, address, to_alloc)

    def __getitem__(self, item):
        return _mod.mem.getFloat64(self._address + (item * self._item_size), True)

    def __setitem__(self, item, value):
        _mod.mem.setFloat64(self._address + (item * self._item_size), value, True)



class Vector2:
    """Vector2, 2 components"""

    size: int = 8

    def __init__(self, x: float = 0.0, y: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(8)
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
        if self._to_alloc:
            _mod._free(self._address)


class Vector3:
    """Vector3, 3 components"""

    size: int = 12

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(12)
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
        if self._to_alloc:
            _mod._free(self._address)


class Vector4:
    """Vector4, 4 components"""

    size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(16)
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
        if self._to_alloc:
            _mod._free(self._address)


Quaternion = Vector4

class Matrix:
    """Matrix, 4x4 components, column major, OpenGL style, right-handed"""

    size: int = 64

    def __init__(self, m0: float = 0.0, m4: float = 0.0, m8: float = 0.0, m12: float = 0.0, m1: float = 0.0, m5: float = 0.0, m9: float = 0.0, m13: float = 0.0, m2: float = 0.0, m6: float = 0.0, m10: float = 0.0, m14: float = 0.0, m3: float = 0.0, m7: float = 0.0, m11: float = 0.0, m15: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(64)
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
        if self._to_alloc:
            _mod._free(self._address)


class Color:
    """Color, 4 components, R8G8B8A8 (32bit)"""

    size: int = 4

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(4)
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
        if self._to_alloc:
            _mod._free(self._address)


class Rectangle:
    """Rectangle, 4 components"""

    size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(16)
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
        if self._to_alloc:
            _mod._free(self._address)


class Image:
    """Image, pixel data stored in CPU memory (RAM)"""

    size: int = 20

    def __init__(self, data: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(20)
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
        if self._to_alloc:
            _mod._free(self._address)


class Texture:
    """Texture, tex data stored in GPU memory (VRAM)"""

    size: int = 20

    def __init__(self, id: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(20)
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
        if self._to_alloc:
            _mod._free(self._address)


Texture2D = Texture

TextureCubemap = Texture

class RenderTexture:
    """RenderTexture, fbo for texture rendering"""

    size: int = 44

    def __init__(self, id: int = 0, texture: Texture = None, depth: Texture = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(44)
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
        return Texture(address=self._address + 4, to_alloc=False)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 4)

    @property
    def depth(self):
        return Texture(address=self._address + 24, to_alloc=False)

    @depth.setter
    def depth(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 24)

    def __str__(self):
        return f"RenderTexture(address={self._address}, {self.id}, {self.texture}, {self.depth})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


RenderTexture2D = RenderTexture

class NPatchInfo:
    """NPatchInfo, n-patch layout info"""

    size: int = 36

    def __init__(self, source: Rectangle = None, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0, layout: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(36)
            if source is not None:
                struct_clone(source, self._address + 0)
            _mod.mem.setInt32(self._address + 16, left)
            _mod.mem.setInt32(self._address + 20, top)
            _mod.mem.setInt32(self._address + 24, right)
            _mod.mem.setInt32(self._address + 28, bottom)
            _mod.mem.setInt32(self._address + 32, layout)

    @property
    def source(self):
        return Rectangle(address=self._address + 0, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class GlyphInfo:
    """GlyphInfo, font characters glyphs info"""

    size: int = 36

    def __init__(self, value: int = 0, offsetX: int = 0, offsetY: int = 0, advanceX: int = 0, image: Image = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(36)
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
        return Image(address=self._address + 16, to_alloc=False)

    @image.setter
    def image(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 16)

    def __str__(self):
        return f"GlyphInfo(address={self._address}, {self.value}, {self.offsetX}, {self.offsetY}, {self.advanceX}, {self.image})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class Font:
    """Font, font texture and GlyphInfo array data"""

    size: int = 40

    def __init__(self, baseSize: int = 0, glyphCount: int = 0, glyphPadding: int = 0, texture: Texture2D = None, recs: int = 0, glyphs: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(40)
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
        return Texture2D(address=self._address + 12, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class Camera3D:
    """Camera, defines position/orientation in 3d space"""

    size: int = 44

    def __init__(self, position: Vector3 = None, target: Vector3 = None, up: Vector3 = None, fovy: float = 0.0, projection: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(44)
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
        return Vector3(address=self._address + 0, to_alloc=False)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector3(address=self._address + 12, to_alloc=False)

    @target.setter
    def target(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def up(self):
        return Vector3(address=self._address + 24, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


Camera = Camera3D

class Camera2D:
    """Camera2D, defines position/orientation in 2d space"""

    size: int = 24

    def __init__(self, offset: Vector2 = None, target: Vector2 = None, rotation: float = 0.0, zoom: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if offset is not None:
                struct_clone(offset, self._address + 0)
            if target is not None:
                struct_clone(target, self._address + 8)
            _mod.mem.setFloat32(self._address + 16, rotation)
            _mod.mem.setFloat32(self._address + 20, zoom)

    @property
    def offset(self):
        return Vector2(address=self._address + 0, to_alloc=False)

    @offset.setter
    def offset(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector2(address=self._address + 8, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class Mesh:
    """Mesh, vertex data and vao/vbo"""

    size: int = 60

    def __init__(self, vertexCount: int = 0, triangleCount: int = 0, vertices: int = 0, texcoords: int = 0, texcoords2: int = 0, normals: int = 0, tangents: int = 0, colors: int = 0, indices: int = 0, animVertices: int = 0, animNormals: int = 0, boneIds: int = 0, boneWeights: int = 0, vaoId: int = 0, vboId: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(60)
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
        if self._to_alloc:
            _mod._free(self._address)


class Shader:
    """Shader"""

    size: int = 8

    def __init__(self, id: int = 0, locs: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(8)
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
        if self._to_alloc:
            _mod._free(self._address)


class MaterialMap:
    """MaterialMap"""

    size: int = 28

    def __init__(self, texture: Texture2D = None, color: Color = None, value: float = 0.0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(28)
            if texture is not None:
                struct_clone(texture, self._address + 0)
            if color is not None:
                struct_clone(color, self._address + 20)
            _mod.mem.setFloat32(self._address + 24, value)

    @property
    def texture(self):
        return Texture2D(address=self._address + 0, to_alloc=False)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def color(self):
        return Color(address=self._address + 20, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class Material:
    """Material, includes shader and maps"""

    size: int = 28

    def __init__(self, shader: Shader = None, maps: int = 0, params: FloatArray = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(28)
            if shader is not None:
                struct_clone(shader, self._address + 0)
            _mod.mem.setUint32(self._address + 8, maps)
            if params is not None:
                struct_clone(params, self._address + 12)

    @property
    def shader(self):
        return Shader(address=self._address + 0, to_alloc=False)

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
        return FloatArray(address=self._address + 12, to_alloc=False)

    @params.setter
    def params(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"Material(address={self._address}, {self.shader}, {self.maps}, {self.params})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class Transform:
    """Transform, vertex transformation data"""

    size: int = 40

    def __init__(self, translation: Vector3 = None, rotation: Quaternion = None, scale: Vector3 = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(40)
            if translation is not None:
                struct_clone(translation, self._address + 0)
            if rotation is not None:
                struct_clone(rotation, self._address + 12)
            if scale is not None:
                struct_clone(scale, self._address + 28)

    @property
    def translation(self):
        return Vector3(address=self._address + 0, to_alloc=False)

    @translation.setter
    def translation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def rotation(self):
        return Quaternion(address=self._address + 12, to_alloc=False)

    @rotation.setter
    def rotation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def scale(self):
        return Vector3(address=self._address + 28, to_alloc=False)

    @scale.setter
    def scale(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 28)

    def __str__(self):
        return f"Transform(address={self._address}, {self.translation}, {self.rotation}, {self.scale})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class BoneInfo:
    """Bone, skeletal animation bone"""

    size: int = 36

    def __init__(self, name: CharArray = None, parent: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(36)
            if name is not None:
                struct_clone(name, self._address + 0)
            _mod.mem.setInt32(self._address + 32, parent)

    @property
    def name(self):
        return CharArray(address=self._address + 0, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class Model:
    """Model, meshes, materials and animation data"""

    size: int = 96

    def __init__(self, transform: Matrix = None, meshCount: int = 0, materialCount: int = 0, meshes: int = 0, materials: int = 0, meshMaterial: int = 0, boneCount: int = 0, bones: int = 0, bindPose: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(96)
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
        return Matrix(address=self._address + 0, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class ModelAnimation:
    """ModelAnimation"""

    size: int = 48

    def __init__(self, boneCount: int = 0, frameCount: int = 0, bones: int = 0, framePoses: int = 0, name: CharArray = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(48)
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
        return CharArray(address=self._address + 16, to_alloc=False)

    @name.setter
    def name(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 16)

    def __str__(self):
        return f"ModelAnimation(address={self._address}, {self.boneCount}, {self.frameCount}, {self.bones}, {self.framePoses}, {self.name})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class Ray:
    """Ray, ray for raycasting"""

    size: int = 24

    def __init__(self, position: Vector3 = None, direction: Vector3 = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if position is not None:
                struct_clone(position, self._address + 0)
            if direction is not None:
                struct_clone(direction, self._address + 12)

    @property
    def position(self):
        return Vector3(address=self._address + 0, to_alloc=False)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def direction(self):
        return Vector3(address=self._address + 12, to_alloc=False)

    @direction.setter
    def direction(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"Ray(address={self._address}, {self.position}, {self.direction})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class RayCollision:
    """RayCollision, ray hit information"""

    size: int = 29

    def __init__(self, hit: int = 0, distance: float = 0.0, point: Vector3 = None, normal: Vector3 = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(29)
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
        return Vector3(address=self._address + 5, to_alloc=False)

    @point.setter
    def point(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 5)

    @property
    def normal(self):
        return Vector3(address=self._address + 17, to_alloc=False)

    @normal.setter
    def normal(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 17)

    def __str__(self):
        return f"RayCollision(address={self._address}, {self.hit}, {self.distance}, {self.point}, {self.normal})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class BoundingBox:
    """BoundingBox"""

    size: int = 24

    def __init__(self, min: Vector3 = None, max: Vector3 = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if min is not None:
                struct_clone(min, self._address + 0)
            if max is not None:
                struct_clone(max, self._address + 12)

    @property
    def min(self):
        return Vector3(address=self._address + 0, to_alloc=False)

    @min.setter
    def min(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def max(self):
        return Vector3(address=self._address + 12, to_alloc=False)

    @max.setter
    def max(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    def __str__(self):
        return f"BoundingBox(address={self._address}, {self.min}, {self.max})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class Wave:
    """Wave, audio wave data"""

    size: int = 20

    def __init__(self, frameCount: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0, data: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(20)
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
        if self._to_alloc:
            _mod._free(self._address)


class AudioStream:
    """AudioStream, custom audio stream"""

    size: int = 20

    def __init__(self, buffer: int = 0, processor: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(20)
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
        if self._to_alloc:
            _mod._free(self._address)


class Sound:
    """Sound"""

    size: int = 24

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if stream is not None:
                struct_clone(stream, self._address + 0)
            _mod.mem.setUint32(self._address + 20, frameCount)

    @property
    def stream(self):
        return AudioStream(address=self._address + 0, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class Music:
    """Music, audio stream, anything longer than ~10 seconds should be streamed"""

    size: int = 33

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, looping: int = 0, ctxType: int = 0, ctxData: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(33)
            if stream is not None:
                struct_clone(stream, self._address + 0)
            _mod.mem.setUint32(self._address + 20, frameCount)
            _mod.mem.setInt8(self._address + 24, looping)
            _mod.mem.setInt32(self._address + 25, ctxType)
            _mod.mem.setUint32(self._address + 29, ctxData)

    @property
    def stream(self):
        return AudioStream(address=self._address + 0, to_alloc=False)

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
        if self._to_alloc:
            _mod._free(self._address)


class VrDeviceInfo:
    """VrDeviceInfo, Head-Mounted-Display device parameters"""

    size: int = 64

    def __init__(self, hResolution: int = 0, vResolution: int = 0, hScreenSize: float = 0.0, vScreenSize: float = 0.0, vScreenCenter: float = 0.0, eyeToScreenDistance: float = 0.0, lensSeparationDistance: float = 0.0, interpupillaryDistance: float = 0.0, lensDistortionValues: FloatArray = None, chromaAbCorrection: FloatArray = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(64)
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
        return FloatArray(address=self._address + 32, to_alloc=False)

    @lensDistortionValues.setter
    def lensDistortionValues(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 32)

    @property
    def chromaAbCorrection(self):
        return FloatArray(address=self._address + 48, to_alloc=False)

    @chromaAbCorrection.setter
    def chromaAbCorrection(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 48)

    def __str__(self):
        return f"VrDeviceInfo(address={self._address}, {self.hResolution}, {self.vResolution}, {self.hScreenSize}, {self.vScreenSize}, {self.vScreenCenter}, {self.eyeToScreenDistance}, {self.lensSeparationDistance}, {self.interpupillaryDistance}, {self.lensDistortionValues}, {self.chromaAbCorrection})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class VrStereoConfig:
    """VrStereoConfig, VR stereo rendering configuration for simulator"""

    size: int = 304

    def __init__(self, projection: StructArray = None, viewOffset: StructArray = None, leftLensCenter: FloatArray = None, rightLensCenter: FloatArray = None, leftScreenCenter: FloatArray = None, rightScreenCenter: FloatArray = None, scale: FloatArray = None, scaleIn: FloatArray = None, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(304)
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
        return StructArray(Matrix, address=self._address + 0, to_alloc=False)

    @projection.setter
    def projection(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def viewOffset(self):
        return StructArray(Matrix, address=self._address + 128, to_alloc=False)

    @viewOffset.setter
    def viewOffset(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 128)

    @property
    def leftLensCenter(self):
        return FloatArray(address=self._address + 256, to_alloc=False)

    @leftLensCenter.setter
    def leftLensCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 256)

    @property
    def rightLensCenter(self):
        return FloatArray(address=self._address + 264, to_alloc=False)

    @rightLensCenter.setter
    def rightLensCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 264)

    @property
    def leftScreenCenter(self):
        return FloatArray(address=self._address + 272, to_alloc=False)

    @leftScreenCenter.setter
    def leftScreenCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 272)

    @property
    def rightScreenCenter(self):
        return FloatArray(address=self._address + 280, to_alloc=False)

    @rightScreenCenter.setter
    def rightScreenCenter(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 280)

    @property
    def scale(self):
        return FloatArray(address=self._address + 288, to_alloc=False)

    @scale.setter
    def scale(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 288)

    @property
    def scaleIn(self):
        return FloatArray(address=self._address + 296, to_alloc=False)

    @scaleIn.setter
    def scaleIn(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 296)

    def __str__(self):
        return f"VrStereoConfig(address={self._address}, {self.projection}, {self.viewOffset}, {self.leftLensCenter}, {self.rightLensCenter}, {self.leftScreenCenter}, {self.rightScreenCenter}, {self.scale}, {self.scaleIn})"

    def __del__(self):
        if self._to_alloc:
            _mod._free(self._address)


class FilePathList:
    """File path list"""

    size: int = 12

    def __init__(self, capacity: int = 0, count: int = 0, paths: int = 0, address: int = 0, to_alloc: bool = True, frozen: bool = False):
        self._to_alloc = to_alloc
        self._frozen = frozen
        if not to_alloc:
            self._address = address
        else:
            self._address = _mod._malloc(12)
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
        if self._to_alloc:
            _mod._free(self._address)


