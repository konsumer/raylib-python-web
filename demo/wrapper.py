class Color:
    def __init__(self, r: int, g: int, b: int, a: int):
        self._size: int = 4
        self._address: int = _mod._malloc(self._size)
        self._r: int = r
        _mod.HEAPU8[self._address + 0] = self._r
        self._g: int = g
        _mod.HEAPU8[self._address + 1] = self._g
        self._b: int = b
        _mod.HEAPU8[self._address + 2] = self._b
        self._a: int = a
        _mod.HEAPU8[self._address + 3] = self._a

    @property
    def r(self):
        return _mod.HEAPU8[self._address + 0]

    @r.setter
    def r(self, value):
        self._r = value
        _mod.HEAPU8[self._address + 0] = self._r

    @property
    def g(self):
        return _mod.HEAPU8[self._address + 1]

    @g.setter
    def g(self, value):
        self._g = value
        _mod.HEAPU8[self._address + 1] = self._g

    @property
    def b(self):
        return _mod.HEAPU8[self._address + 2]

    @b.setter
    def b(self, value):
        self._b = value
        _mod.HEAPU8[self._address + 2] = self._b

    @property
    def a(self):
        return _mod.HEAPU8[self._address + 3]

    @a.setter
    def a(self, value):
        self._a = value
        _mod.HEAPU8[self._address + 3] = self._a

    def __del__(self):
        _mod.free(self._address)


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
    _mod.ccall('DrawText', 'void', ['string', 'i32', 'i32', 'f32', 'pointer'], [text, x, y, fontSize, color._address])
