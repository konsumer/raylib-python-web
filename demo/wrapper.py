class Color:
    def __init__(self, r: int, g: int, b: int, a: int):
        self._size: int = 4
        self._address: int = _mod._malloc(self._size)
        _mod.HEAPU8[self._address + 0] = r or 0
        _mod.HEAPU8[self._address + 1] = g or 0
        _mod.HEAPU8[self._address + 2] = b or 0
        _mod.HEAPU8[self._address + 3] = a or 0

    def __del__(self):
        _mod._free(self._address)

    @property
    def r(self):
        return _mod.HEAPU8[self._address + 0]

    @r.setter
    def r(self, value):
        _mod.HEAPU8[self._address + 0] = value

    @property
    def g(self):
        return _mod.HEAPU8[self._address + 1]

    @g.setter
    def g(self, value):
        _mod.HEAPU8[self._address + 1] = value

    @property
    def b(self):
        return _mod.HEAPU8[self._address + 2]

    @b.setter
    def b(self, value):
        _mod.HEAPU8[self._address + 2] = value

    @property
    def a(self):
        return _mod.HEAPU8[self._address + 3]

    @a.setter
    def a(self, value):
        _mod.HEAPU8[self._address + 3] = value


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self._size: int = 16
        self._address: int = _mod._malloc(self._size)
        _mod.HEAPF32[self._address + 0] = x or 0
        _mod.HEAPF32[self._address + 4] = y or 0
        _mod.HEAPF32[self._address + 8] = width or 0
        _mod.HEAPF32[self._address + 12] = height or 0

    def __del__(self):
        _mod._free(self._address)

    @property
    def x(self):
        return _mod.HEAPF32[self._address + 0]

    @x.setter
    def x(self, value):
        _mod.HEAPF32[self._address + 0] = value

    @property
    def y(self):
        return _mod.HEAPF32[self._address + 4]

    @y.setter
    def y(self, value):
        _mod.HEAPF32[self._address + 4] = value

    @property
    def width(self):
        return _mod.HEAPF32[self._address + 8]

    @width.setter
    def width(self, value):
        _mod.HEAPF32[self._address + 8] = value

    @property
    def height(self):
        return _mod.HEAPF32[self._address + 12]

    @width.setter
    def height(self, value):
        _mod.HEAPF32[self._address + 12] = value



LIGHTGRAY = Color(200, 200, 200, 255)  # Light Gray
GRAY = Color(130, 130, 130, 255)  # Gray
DARKGRAY = Color(80, 80, 80, 255)  # Dark Gray
YELLOW = Color(253, 249, 0, 255)  # Yellow
GOLD = Color(255, 203, 0, 255)  # Gold
ORANGE = Color(255, 161, 0, 255)  # Orange
PINK = Color(255, 109, 194, 255)  # Pink
RED = Color(230, 41, 55, 255)  # Red
MAROON = Color(190, 33, 55, 255)  # Maroon
GREEN = Color(0, 228, 48, 255)  # Green
LIME = Color(0, 158, 47, 255)  # Lime
DARKGREEN = Color(0, 117, 44, 255)  # Dark Green
SKYBLUE = Color(102, 191, 255, 255)  # Sky Blue
BLUE = Color(0, 121, 241, 255)  # Blue
DARKBLUE = Color(0, 82, 172, 255)  # Dark Blue
PURPLE = Color(200, 122, 255, 255)  # Purple
VIOLET = Color(135, 60, 190, 255)  # Violet
DARKPURPLE = Color(112, 31, 126, 255)  # Dark Purple
BEIGE = Color(211, 176, 131, 255)  # Beige
BROWN = Color(127, 106, 79, 255)  # Brown
DARKBROWN = Color(76, 63, 47, 255)  # Dark Brown
WHITE = Color(255, 255, 255, 255)  # White
BLACK = Color(0, 0, 0, 255)  # Black
BLANK = Color(0, 0, 0, 0)  # Blank (Transparent)
MAGENTA = Color(255, 0, 255, 255)  # Magenta
RAYWHITE = Color(245, 245, 245, 255)  # My own White (raylib logo)


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

