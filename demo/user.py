# I put this up here, so it doesn't try to deallocate the original colors
colors = StructArray(Color, 4)

def init():
  InitWindow(800, 450)

  # test StructArray
  # this should copy values into array
  colors[0] = RED
  colors[1] = BLUE
  colors[2] = GREEN
  colors[3] = BLACK
  print("colors.len (%d == 4?)" % len(colors))
  print("RED: (%d, %d, %d, %d)" % (colors[0].r, colors[0].g, colors[0].b, colors[0].a)) # this one is wrong for some reason
  print("BLUE: (%d, %d, %d, %d)" % (colors[1].r, colors[1].g, colors[1].b, colors[1].a))
  print("GREEN: (%d, %d, %d, %d)" % (colors[2].r, colors[2].g, colors[2].b, colors[2].a))
  print("BLACK: (%d, %d, %d, %d)" % (colors[3].r, colors[3].g, colors[3].b, colors[3].a))

  # test fonts
  font = GetFontDefault()
  print('Font: size: %d, address: %d' % ( font._size, font._address ))
  print("baseSize (%d == 10?) " % font.baseSize)
  print("glyphCount (%d == 224?) " % font.glyphCount)
  print("glyphPadding (%d == 0?) " % font.glyphPadding)

def update():
  BeginDrawing()
  ClearBackground(RAYWHITE)
  DrawText("Congrats! You created your first python window!", 150, 200, 20, LIGHTGRAY)
  DrawFPS(10, 10)
  EndDrawing()