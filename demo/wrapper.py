# Generic array-like collection that uses wasm as memory-back
class WasmArray:
    def __init__(self, itemSize, length, address=None):
        self._length = length
        self._itemSize = itemSize
        self._size = self._itemSize * self._length
        if address is not None:
            self._address:int = address
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


class Color:
    _size: int = 4
    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 0, frozen=False, address=None):
        self._frozen = frozen
        if address is not None:
            self._address:int = address
        else:
            self._address: int = _mod._malloc(self._size)
            _mod.mem.setUint8(self._address + 0, r, True)
            _mod.mem.setUint8(self._address + 1, g, True)
            _mod.mem.setUint8(self._address + 2, b, True)
            _mod.mem.setUint8(self._address + 3, a, True)

    # this seems to bug things out.
    # def __del__(self):
    #     _mod._free(self._address)

    def __str__(self):
        return "Color(r:%d, g:%d, b:%d, a:%d) %s" % (self.r, self.g, self.b, self.a, hex(self._address))

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
    _size: int = 16
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0, frozen=False, address=None):
        self._frozen = frozen
        if address is not None:
            self._address:int = address
        else:
            self._address: int = _mod._malloc(self._size)
            _mod.mem.setFloat32(self._address + 0, x, True)
            _mod.mem.setFloat32(self._address + 4, y, True)
            _mod.mem.setFloat32(self._address + 8, width, True)
            _mod.mem.setFloat32(self._address + 12, height, True)

    # this seems to bug things out.
    # def __del__(self):
    #     _mod._free(self._address)

    def __str__(self):
        return "Rectangle(x:%f, y:%f, width:%f, height:%f) %s" % (
            self.x,
            self.y,
            self.width,
            self.height,
            hex(self._address)
        )

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

class Texture:
    _size:int = 20
    def __init__(self, tid: int = 0, width: int = 0, height: int = 0, mipmaps: int = 0, tformat: int = 0, frozen=False, address=None):
        self._frozen = frozen
        if address is not None:
            self._address:int = address
        else:
            self._address: int = _mod._malloc(self._size)
            _mod.mem.setInt32(self._address + 0, tid, True)
            _mod.mem.setInt32(self._address + 4, width, True)
            _mod.mem.setInt32(self._address + 8, height, True)
            _mod.mem.setInt32(self._address + 12, mipmaps, True)
            _mod.mem.setInt32(self._address + 16, tformat, True)

    # this seems to bug things out.
    # def __del__(self):
    #     _mod._free(self._address)

    def __str__(self):
        return "Texture(tid:%d, width:%d, height:%d, mipmaps: %d, tformat: %d) %s" % (
            self.tid,
            self.width,
            self.height,
            self.mipmaps,
            self.tformat,
            hex(self._address)
        )

    @property
    def tid(self):
        return _mod.mem.getUint32(self._address + 0, True)

    @tid.setter
    def tid(self, value):
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
    def tformat(self):
        return _mod.mem.getInt32(self._address + 16, True)

    @tformat.setter
    def tformat(self, value):
        if not self._frozen:
            _mod.mem.setInt32(self._address + 16, value, True)

class Font:
    _size:int = 40
    def __init__(self, baseSize: int = 0, glyphCount: int = 0, glyphPadding: int = 0, texture=None, recs=None, glyphs=None, frozen=False, address=None):
        self._frozen = frozen
        if address is not None:
            self._address:int = address
        else:
            self._address: int = _mod._malloc(self._size)
            _mod.mem.setInt32(self._address + 0, baseSize, True)
            _mod.mem.setInt32(self._address + 4, glyphCount, True)
            _mod.mem.setInt32(self._address + 8, glyphPadding, True)
            if texture is not None:
                struct_clone(texture, self._address + 12)
            if recs is not None:
                _mod.mem.setInt32(self._address + 32, recs._address, True)
            if glyphs is not None:
                _mod.mem.setInt32(self._address + 36, glyphs._address, True)

    # this seems to bug things out.
    # def __del__(self):
    #     _mod._free(self._address)

    def __str__(self):
        return "Font(baseSize:%d, glyphCount:%d, glyphPadding:%d, texture:%s, recs:%s, glyphs:%s) %s" % (
            self.baseSize,
            self.glyphCount,
            self.glyphPadding,
            str(self.texture),
            str(self.recs),
            str(self.glyphs),
            hex(self._address)
        )

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
        return Texture(address=self._address + 12)

    @texture.setter
    def texture(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 12)

    @property
    def recs(self):
        # TODO: where does recs.length come from?
        length=10
        return StructArray(Rectangle, length, address=self._address + 32)

    @recs.setter
    def recs(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 32)

    @property
    def glyphs(self):
        glyphCount = _mod.mem.getInt32(self._address + 4, True)
        return StructArray(GlyphInfo, glyphCount, address=self._address + 36)

    @glyphs.setter
    def glyphs(self, value):
        if not self._frozen:
            struct_clone(value, self._address + 36)


# TODO: these need to be filled in for everything to work right

class Image:
    _size:int = 20
    def __init__(self, data:int=0, width:int=0, height:int=0, mipmaps:int=0, format:int=0, frozen=False, address=None):
        pass

"""
// Image, pixel data stored in CPU memory (RAM)
typedef struct Image {
    void *data;             // Image raw data
    int width;              // Image base width
    int height;             // Image base height
    int mipmaps;            // Mipmap levels, 1 by default
    int format;             // Data format (PixelFormat type)
} Image;
"""

class GlyphInfo:
    _size:int = 52
    def __init__(self, value:int=0, offsetX:int=0, offsetY:int=0, advanceX:int=0, image:Image=None, frozen=False, address=None):
        pass

"""
// GlyphInfo, font characters glyphs info
typedef struct GlyphInfo {
    int value;              // Character value (Unicode)
    int offsetX;            // Character offset X when drawing
    int offsetY;            // Character offset Y when drawing
    int advanceX;           // Character advance position X
    Image image;            // Character image data
} GlyphInfo;
"""


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
        a = _mod._malloc(source._size)
    _mod._memcpy(a, source._address, source._size)
    out = source.__class__(address = a)
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

def DrawTextBoxedSelectable(font, text, rec, fontSize, spacing, wordWrap, tint, selectStart, selectLength, selectTint, selectBackTint):
    sp = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, sp, len(text) + 1)
    _mod._DrawTextBoxedSelectable(font._address, sp, rec._address, fontSize, spacing, wordWrap, tint._address, selectStart, selectLength, selectTint._address, selectBackTint._address)
    _mod._free(sp)

def DrawTextBoxed(font, text, rec, fontSize, spacing, wordWrap, tint):
    sp = _mod._malloc(len(text) + 1)
    _mod.stringToUTF8(text, sp, len(text) + 1)
    _mod._DrawTextBoxed(font._address, sp, rec._address, fontSize, spacing, wordWrap, tint._address)
    _mod._free(sp)

