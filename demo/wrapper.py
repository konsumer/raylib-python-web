# Generic array-like collection that uses wasm as memory-back
class WasmArray:
    def __init__(self, itemSize, length, address=None):
        self._length = length
        self._itemSize = itemSize
        self._size = self._itemSize * self._length
        if address is not None:
            self._address: int = address
        else:
            self._address: int = _mod._malloc(self._size)

    # this seems to bug things out.
    # def __del__(self):
    #     _mod._free(self._address)
    def __len__(self):
        return self._length

    def __str__(self):
        out = "WasmArray["
        out += ', '.join([str(self[i]) for i in range(self._length)])
        out += "] " + hex(self._address)
        return out


# an array of structs
class StructArray(WasmArray):
    def __init__(self, stype, length, address=None):
        super(StructArray, self).__init__(stype._size, length, address)
        self._stype = stype

    def __getitem__(self, item):
        return self._stype(address=(self._address + (self._itemSize * item)))

    def __setitem__(self, item, value):
        struct_clone(value, self._address + (self._itemSize * item))


# int* used as an array of i32's
class IntArray(WasmArray):
    def __init__(self, length, address=None):
        super(IntArray, self).__init__(4, length, address)

    def __getitem__(self, item):
        return _mod.mem.getInt32(self._address + (item * self._itemSize), True)

    def __setitem__(self, item, value):
        _mod.mem.setInt32(self._address + (item * self._itemSize), value, True)


# float* used as an array of floats
class FloatArray(WasmArray):
    def __init__(self, length, address=None):
        super(FloatArray, self).__init__(4, length, address)

    def __getitem__(self, item):
        return _mod.mem.getFloat32(self._address + 0, True)

    def __setitem__(self, item, value):
        _mod.mem.setFloat32(self._address + (item * self._itemSize), value, True)


# char* used as an array of bytes
class ByteArray(WasmArray):
    def __init__(self, length, address=None):
        super(ByteArray, self).__init__(1, length, address)

    def __getitem__(self, item):
        return _mod.mem.getUint8(self._address + (item * self._itemSize), True)

    def __setitem__(self, item, value):
        _mod.mem.setUint8(self._address + (item * self._itemSize), value, True)


class Vector2:
    """Vector2, 2 components"""

    size: int = 8

    def __init__(self, x: float = 0.0, y: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(8)
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value)


class Vector3:
    """Vector3, 3 components"""

    size: int = 12

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(12)
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, z)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value)

    @property
    def z(self):
        return _mod.mem.getFloat32(self._address + 8)

    @z.setter
    def z(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value)


class Vector4:
    """Vector4, 4 components"""

    size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0, address: int = 0,
                 frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(16)
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, z)
            _mod.mem.setFloat32(self._address + 12, w)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value)

    @property
    def z(self):
        return _mod.mem.getFloat32(self._address + 8)

    @z.setter
    def z(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value)

    @property
    def w(self):
        return _mod.mem.getFloat32(self._address + 12)

    @w.setter
    def w(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value)


Quaternion = Vector4


class Matrix:
    """Matrix, 4x4 components, column major, OpenGL style, right-handed"""

    size: int = 64

    def __init__(self, m0: float = 0.0, m4: float = 0.0, m8: float = 0.0, m12: float = 0.0, m1: float = 0.0,
                 m5: float = 0.0, m9: float = 0.0, m13: float = 0.0, m2: float = 0.0, m6: float = 0.0, m10: float = 0.0,
                 m14: float = 0.0, m3: float = 0.0, m7: float = 0.0, m11: float = 0.0, m15: float = 0.0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getFloat32(self._address + 0)

    @m0.setter
    def m0(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value)

    @property
    def m4(self):
        return _mod.mem.getFloat32(self._address + 4)

    @m4.setter
    def m4(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value)

    @property
    def m8(self):
        return _mod.mem.getFloat32(self._address + 8)

    @m8.setter
    def m8(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value)

    @property
    def m12(self):
        return _mod.mem.getFloat32(self._address + 12)

    @m12.setter
    def m12(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value)

    @property
    def m1(self):
        return _mod.mem.getFloat32(self._address + 16)

    @m1.setter
    def m1(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 16, value)

    @property
    def m5(self):
        return _mod.mem.getFloat32(self._address + 20)

    @m5.setter
    def m5(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 20, value)

    @property
    def m9(self):
        return _mod.mem.getFloat32(self._address + 24)

    @m9.setter
    def m9(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 24, value)

    @property
    def m13(self):
        return _mod.mem.getFloat32(self._address + 28)

    @m13.setter
    def m13(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 28, value)

    @property
    def m2(self):
        return _mod.mem.getFloat32(self._address + 32)

    @m2.setter
    def m2(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 32, value)

    @property
    def m6(self):
        return _mod.mem.getFloat32(self._address + 36)

    @m6.setter
    def m6(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 36, value)

    @property
    def m10(self):
        return _mod.mem.getFloat32(self._address + 40)

    @m10.setter
    def m10(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 40, value)

    @property
    def m14(self):
        return _mod.mem.getFloat32(self._address + 44)

    @m14.setter
    def m14(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 44, value)

    @property
    def m3(self):
        return _mod.mem.getFloat32(self._address + 48)

    @m3.setter
    def m3(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 48, value)

    @property
    def m7(self):
        return _mod.mem.getFloat32(self._address + 52)

    @m7.setter
    def m7(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 52, value)

    @property
    def m11(self):
        return _mod.mem.getFloat32(self._address + 56)

    @m11.setter
    def m11(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 56, value)

    @property
    def m15(self):
        return _mod.mem.getFloat32(self._address + 60)

    @m15.setter
    def m15(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 60, value)


class Color:
    """Color, 4 components, R8G8B8A8 (32bit)"""

    size: int = 4

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(4)
            _mod.mem.setUint8(self._address + 0, r)
            _mod.mem.setUint8(self._address + 1, g)
            _mod.mem.setUint8(self._address + 2, b)
            _mod.mem.setUint8(self._address + 3, a)

    @property
    def r(self):
        return _mod.mem.getUint8(self._address + 0)

    @r.setter
    def r(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 0, value)

    @property
    def g(self):
        return _mod.mem.getUint8(self._address + 1)

    @g.setter
    def g(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 1, value)

    @property
    def b(self):
        return _mod.mem.getUint8(self._address + 2)

    @b.setter
    def b(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 2, value)

    @property
    def a(self):
        return _mod.mem.getUint8(self._address + 3)

    @a.setter
    def a(self, value):
        if not self._frozen:
            _mod.mem.setUint8(self._address + 3, value)


class Rectangle:
    """Rectangle, 4 components"""

    size: int = 16

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0, address: int = 0,
                 frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(16)
            _mod.mem.setFloat32(self._address + 0, x)
            _mod.mem.setFloat32(self._address + 4, y)
            _mod.mem.setFloat32(self._address + 8, width)
            _mod.mem.setFloat32(self._address + 12, height)

    @property
    def x(self):
        return _mod.mem.getFloat32(self._address + 0)

    @x.setter
    def x(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 0, value)

    @property
    def y(self):
        return _mod.mem.getFloat32(self._address + 4)

    @y.setter
    def y(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 4, value)

    @property
    def width(self):
        return _mod.mem.getFloat32(self._address + 8)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 8, value)

    @property
    def height(self):
        return _mod.mem.getFloat32(self._address + 12)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 12, value)


class Image:
    """Image, pixel data stored in CPU memory (RAM)"""

    size: int = 20

    def __init__(self, data: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getUint32(self._address + 0)

    @data.setter
    def data(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def width(self):
        return _mod.mem.getInt32(self._address + 4)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value)

    @property
    def height(self):
        return _mod.mem.getInt32(self._address + 8)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value)

    @property
    def mipmaps(self):
        return _mod.mem.getInt32(self._address + 12)

    @mipmaps.setter
    def mipmaps(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value)

    @property
    def format(self):
        return _mod.mem.getInt32(self._address + 16)

    @format.setter
    def format(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value)


class Texture:
    """Texture, tex data stored in GPU memory (VRAM)"""

    size: int = 20

    def __init__(self, id: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, format: int = 0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getUint32(self._address + 0)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def width(self):
        return _mod.mem.getInt32(self._address + 4)

    @width.setter
    def width(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value)

    @property
    def height(self):
        return _mod.mem.getInt32(self._address + 8)

    @height.setter
    def height(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value)

    @property
    def mipmaps(self):
        return _mod.mem.getInt32(self._address + 12)

    @mipmaps.setter
    def mipmaps(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value)

    @property
    def format(self):
        return _mod.mem.getInt32(self._address + 16)

    @format.setter
    def format(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value)


Texture2D = Texture

TextureCubemap = Texture


class RenderTexture:
    """RenderTexture, fbo for texture rendering"""

    size: int = 44

    def __init__(self, id: int = 0, texture: Texture = None, depth: Texture = None, address: int = 0,
                 frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getUint32(self._address + 0)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def texture(self):
        return Texture(address=self._address + 4)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 4)

    @property
    def depth(self):
        return Texture(address=self._address + 24)

    @depth.setter
    def depth(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 24)


RenderTexture2D = RenderTexture


class NPatchInfo:
    """NPatchInfo, n-patch layout info"""

    size: int = 36

    def __init__(self, source: Rectangle = None, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0,
                 layout: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Rectangle(address=self._address + 0)

    @source.setter
    def source(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def left(self):
        return _mod.mem.getInt32(self._address + 16)

    @left.setter
    def left(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value)

    @property
    def top(self):
        return _mod.mem.getInt32(self._address + 20)

    @top.setter
    def top(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 20, value)

    @property
    def right(self):
        return _mod.mem.getInt32(self._address + 24)

    @right.setter
    def right(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 24, value)

    @property
    def bottom(self):
        return _mod.mem.getInt32(self._address + 28)

    @bottom.setter
    def bottom(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 28, value)

    @property
    def layout(self):
        return _mod.mem.getInt32(self._address + 32)

    @layout.setter
    def layout(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 32, value)


class GlyphInfo:
    """GlyphInfo, font characters glyphs info"""

    size: int = 36

    def __init__(self, value: int = 0, offsetX: int = 0, offsetY: int = 0, advanceX: int = 0, image: Image = None,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getInt32(self._address + 0)

    @value.setter
    def value(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value)

    @property
    def offsetX(self):
        return _mod.mem.getInt32(self._address + 4)

    @offsetX.setter
    def offsetX(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value)

    @property
    def offsetY(self):
        return _mod.mem.getInt32(self._address + 8)

    @offsetY.setter
    def offsetY(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value)

    @property
    def advanceX(self):
        return _mod.mem.getInt32(self._address + 12)

    @advanceX.setter
    def advanceX(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 12, value)

    @property
    def image(self):
        return Image(address=self._address + 16)

    @image.setter
    def image(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 16)


class Font:
    """Font, font texture and GlyphInfo array data"""

    size: int = 40

    def __init__(self, baseSize: int = 0, glyphCount: int = 0, glyphPadding: int = 0, texture: Texture2D = None,
                 recs: int = 0, glyphs: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getInt32(self._address + 0)

    @baseSize.setter
    def baseSize(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value)

    @property
    def glyphCount(self):
        return _mod.mem.getInt32(self._address + 4)

    @glyphCount.setter
    def glyphCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value)

    @property
    def glyphPadding(self):
        return _mod.mem.getInt32(self._address + 8)

    @glyphPadding.setter
    def glyphPadding(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 8, value)

    @property
    def texture(self):
        return Texture2D(address=self._address + 12)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def recs(self):
        return _mod.mem.getUint32(self._address + 32)

    @recs.setter
    def recs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 32, value)

    @property
    def glyphs(self):
        return _mod.mem.getUint32(self._address + 36)

    @glyphs.setter
    def glyphs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 36, value)


class Camera3D:
    """Camera, defines position/orientation in 3d space"""

    size: int = 44

    def __init__(self, position: Vector3 = None, target: Vector3 = None, up: Vector3 = None, fovy: float = 0.0,
                 projection: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Vector3(address=self._address + 0)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector3(address=self._address + 12)

    @target.setter
    def target(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def up(self):
        return Vector3(address=self._address + 24)

    @up.setter
    def up(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 24)

    @property
    def fovy(self):
        return _mod.mem.getFloat32(self._address + 36)

    @fovy.setter
    def fovy(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 36, value)

    @property
    def projection(self):
        return _mod.mem.getInt32(self._address + 40)

    @projection.setter
    def projection(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 40, value)


Camera = Camera3D


class Camera2D:
    """Camera2D, defines position/orientation in 2d space"""

    size: int = 24

    def __init__(self, offset: Vector2 = None, target: Vector2 = None, rotation: float = 0.0, zoom: float = 0.0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Vector2(address=self._address + 0)

    @offset.setter
    def offset(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def target(self):
        return Vector2(address=self._address + 8)

    @target.setter
    def target(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 8)

    @property
    def rotation(self):
        return _mod.mem.getFloat32(self._address + 16)

    @rotation.setter
    def rotation(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 16, value)

    @property
    def zoom(self):
        return _mod.mem.getFloat32(self._address + 20)

    @zoom.setter
    def zoom(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 20, value)


class Mesh:
    """Mesh, vertex data and vao/vbo"""

    size: int = 60

    def __init__(self, vertexCount: int = 0, triangleCount: int = 0, vertices: int = 0, texcoords: int = 0,
                 texcoords2: int = 0, normals: int = 0, tangents: int = 0, colors: int = 0, indices: int = 0,
                 animVertices: int = 0, animNormals: int = 0, boneIds: int = 0, boneWeights: int = 0, vaoId: int = 0,
                 vboId: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getInt32(self._address + 0)

    @vertexCount.setter
    def vertexCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 0, value)

    @property
    def triangleCount(self):
        return _mod.mem.getInt32(self._address + 4)

    @triangleCount.setter
    def triangleCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 4, value)

    @property
    def vertices(self):
        return _mod.mem.getUint32(self._address + 8)

    @vertices.setter
    def vertices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value)

    @property
    def texcoords(self):
        return _mod.mem.getUint32(self._address + 12)

    @texcoords.setter
    def texcoords(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value)

    @property
    def texcoords2(self):
        return _mod.mem.getUint32(self._address + 16)

    @texcoords2.setter
    def texcoords2(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value)

    @property
    def normals(self):
        return _mod.mem.getUint32(self._address + 20)

    @normals.setter
    def normals(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value)

    @property
    def tangents(self):
        return _mod.mem.getUint32(self._address + 24)

    @tangents.setter
    def tangents(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 24, value)

    @property
    def colors(self):
        return _mod.mem.getUint32(self._address + 28)

    @colors.setter
    def colors(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 28, value)

    @property
    def indices(self):
        return _mod.mem.getUint32(self._address + 32)

    @indices.setter
    def indices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 32, value)

    @property
    def animVertices(self):
        return _mod.mem.getUint32(self._address + 36)

    @animVertices.setter
    def animVertices(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 36, value)

    @property
    def animNormals(self):
        return _mod.mem.getUint32(self._address + 40)

    @animNormals.setter
    def animNormals(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 40, value)

    @property
    def boneIds(self):
        return _mod.mem.getUint32(self._address + 44)

    @boneIds.setter
    def boneIds(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 44, value)

    @property
    def boneWeights(self):
        return _mod.mem.getUint32(self._address + 48)

    @boneWeights.setter
    def boneWeights(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 48, value)

    @property
    def vaoId(self):
        return _mod.mem.getUint32(self._address + 52)

    @vaoId.setter
    def vaoId(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 52, value)

    @property
    def vboId(self):
        return _mod.mem.getUint32(self._address + 56)

    @vboId.setter
    def vboId(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 56, value)


class Shader:
    """Shader"""

    size: int = 8

    def __init__(self, id: int = 0, locs: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(8)
            _mod.mem.setUint32(self._address + 0, id)
            _mod.mem.setUint32(self._address + 4, locs)

    @property
    def id(self):
        return _mod.mem.getUint32(self._address + 0)

    @id.setter
    def id(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def locs(self):
        return _mod.mem.getUint32(self._address + 4)

    @locs.setter
    def locs(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value)


class MaterialMap:
    """MaterialMap"""

    size: int = 28

    def __init__(self, texture: Texture2D = None, color: Color = None, value: float = 0.0, address: int = 0,
                 frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Texture2D(address=self._address + 0)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def color(self):
        return Color(address=self._address + 20)

    @color.setter
    def color(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 20)

    @property
    def value(self):
        return _mod.mem.getFloat32(self._address + 24)

    @value.setter
    def value(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 24, value)


class Transform:
    """Transform, vertex transformation data"""

    size: int = 40

    def __init__(self, translation: Vector3 = None, rotation: Quaternion = None, scale: Vector3 = None,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Vector3(address=self._address + 0)

    @translation.setter
    def translation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def rotation(self):
        return Quaternion(address=self._address + 12)

    @rotation.setter
    def rotation(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def scale(self):
        return Vector3(address=self._address + 28)

    @scale.setter
    def scale(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 28)


class Model:
    """Model, meshes, materials and animation data"""

    size: int = 96

    def __init__(self, transform: Matrix = None, meshCount: int = 0, materialCount: int = 0, meshes: int = 0,
                 materials: int = 0, meshMaterial: int = 0, boneCount: int = 0, bones: int = 0, bindPose: int = 0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return Matrix(address=self._address + 0)

    @transform.setter
    def transform(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def meshCount(self):
        return _mod.mem.getInt32(self._address + 64)

    @meshCount.setter
    def meshCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 64, value)

    @property
    def materialCount(self):
        return _mod.mem.getInt32(self._address + 68)

    @materialCount.setter
    def materialCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 68, value)

    @property
    def meshes(self):
        return _mod.mem.getUint32(self._address + 72)

    @meshes.setter
    def meshes(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 72, value)

    @property
    def materials(self):
        return _mod.mem.getUint32(self._address + 76)

    @materials.setter
    def materials(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 76, value)

    @property
    def meshMaterial(self):
        return _mod.mem.getUint32(self._address + 80)

    @meshMaterial.setter
    def meshMaterial(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 80, value)

    @property
    def boneCount(self):
        return _mod.mem.getInt32(self._address + 84)

    @boneCount.setter
    def boneCount(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 84, value)

    @property
    def bones(self):
        return _mod.mem.getUint32(self._address + 88)

    @bones.setter
    def bones(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 88, value)

    @property
    def bindPose(self):
        return _mod.mem.getUint32(self._address + 92)

    @bindPose.setter
    def bindPose(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 92, value)


class Ray:
    """Ray, ray for raycasting"""

    size: int = 24

    def __init__(self, position: Vector3 = None, direction: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if position is not None:
                struct_clone(position, self._address + 0)
            if direction is not None:
                struct_clone(direction, self._address + 12)

    @property
    def position(self):
        return Vector3(address=self._address + 0)

    @position.setter
    def position(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def direction(self):
        return Vector3(address=self._address + 12)

    @direction.setter
    def direction(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)


class RayCollision:
    """RayCollision, ray hit information"""

    size: int = 29

    def __init__(self, hit: int = 0, distance: float = 0.0, point: Vector3 = None, normal: Vector3 = None,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getInt8(self._address + 0)

    @hit.setter
    def hit(self, value):
        if not self._frozen:
            _mod.mem.setInt8(self._address + 0, value)

    @property
    def distance(self):
        return _mod.mem.getFloat32(self._address + 1)

    @distance.setter
    def distance(self, value):
        if not self._frozen:
            _mod.mem.setFloat32(self._address + 1, value)

    @property
    def point(self):
        return Vector3(address=self._address + 5)

    @point.setter
    def point(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 5)

    @property
    def normal(self):
        return Vector3(address=self._address + 17)

    @normal.setter
    def normal(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 17)


class BoundingBox:
    """BoundingBox"""

    size: int = 24

    def __init__(self, min: Vector3 = None, max: Vector3 = None, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if min is not None:
                struct_clone(min, self._address + 0)
            if max is not None:
                struct_clone(max, self._address + 12)

    @property
    def min(self):
        return Vector3(address=self._address + 0)

    @min.setter
    def min(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def max(self):
        return Vector3(address=self._address + 12)

    @max.setter
    def max(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)


class Wave:
    """Wave, audio wave data"""

    size: int = 20

    def __init__(self, frameCount: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0, data: int = 0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getUint32(self._address + 0)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def sampleRate(self):
        return _mod.mem.getUint32(self._address + 4)

    @sampleRate.setter
    def sampleRate(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value)

    @property
    def sampleSize(self):
        return _mod.mem.getUint32(self._address + 8)

    @sampleSize.setter
    def sampleSize(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value)

    @property
    def channels(self):
        return _mod.mem.getUint32(self._address + 12)

    @channels.setter
    def channels(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value)

    @property
    def data(self):
        return _mod.mem.getUint32(self._address + 16)

    @data.setter
    def data(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value)


class AudioStream:
    """AudioStream, custom audio stream"""

    size: int = 20

    def __init__(self, buffer: int = 0, processor: int = 0, sampleRate: int = 0, sampleSize: int = 0, channels: int = 0,
                 address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return _mod.mem.getUint32(self._address + 0)

    @buffer.setter
    def buffer(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def processor(self):
        return _mod.mem.getUint32(self._address + 4)

    @processor.setter
    def processor(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value)

    @property
    def sampleRate(self):
        return _mod.mem.getUint32(self._address + 8)

    @sampleRate.setter
    def sampleRate(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value)

    @property
    def sampleSize(self):
        return _mod.mem.getUint32(self._address + 12)

    @sampleSize.setter
    def sampleSize(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 12, value)

    @property
    def channels(self):
        return _mod.mem.getUint32(self._address + 16)

    @channels.setter
    def channels(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 16, value)


class Sound:
    """Sound"""

    size: int = 24

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(24)
            if stream is not None:
                struct_clone(stream, self._address + 0)
            _mod.mem.setUint32(self._address + 20, frameCount)

    @property
    def stream(self):
        return AudioStream(address=self._address + 0)

    @stream.setter
    def stream(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def frameCount(self):
        return _mod.mem.getUint32(self._address + 20)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value)


class Music:
    """Music, audio stream, anything longer than ~10 seconds should be streamed"""

    size: int = 33

    def __init__(self, stream: AudioStream = None, frameCount: int = 0, looping: int = 0, ctxType: int = 0,
                 ctxData: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
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
        return AudioStream(address=self._address + 0)

    @stream.setter
    def stream(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 0)

    @property
    def frameCount(self):
        return _mod.mem.getUint32(self._address + 20)

    @frameCount.setter
    def frameCount(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 20, value)

    @property
    def looping(self):
        return _mod.mem.getInt8(self._address + 24)

    @looping.setter
    def looping(self, value):
        if not self._frozen:
            _mod.mem.setInt8(self._address + 24, value)

    @property
    def ctxType(self):
        return _mod.mem.getInt32(self._address + 25)

    @ctxType.setter
    def ctxType(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 25, value)

    @property
    def ctxData(self):
        return _mod.mem.getUint32(self._address + 29)

    @ctxData.setter
    def ctxData(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 29, value)


class FilePathList:
    """File path list"""

    size: int = 12

    def __init__(self, capacity: int = 0, count: int = 0, paths: int = 0, address: int = 0, frozen: bool = False):
        self._frozen = frozen
        if address != 0:
            self._address = address
        else:
            self._address = _mod._malloc(12)
            _mod.mem.setUint32(self._address + 0, capacity)
            _mod.mem.setUint32(self._address + 4, count)
            _mod.mem.setUint32(self._address + 8, paths)

    @property
    def capacity(self):
        return _mod.mem.getUint32(self._address + 0)

    @capacity.setter
    def capacity(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 0, value)

    @property
    def count(self):
        return _mod.mem.getUint32(self._address + 4)

    @count.setter
    def count(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 4, value)

    @property
    def paths(self):
        return _mod.mem.getUint32(self._address + 8)

    @paths.setter
    def paths(self, value):
        if not self._frozen:
            _mod.mem.setUint32(self._address + 8, value)


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


# helper to copy a struct
# newColor = struct_clone(RAYWHITE)
# newColor._frozen = false
# newColor.a = 127
def struct_clone(source, a):
    if not a:
        a = _mod._malloc(source.size)
    _mod._memcpy(a, source._address, source.size)
    out = source.__class__(address=a)
    return out


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
