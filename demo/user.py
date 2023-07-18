def init():
  InitWindow(800, 450)

  # test StructArray
  colors = StructArray(Color, 4)
  print("colors.len (4)", len(colors))
  # this should copy values into array
  colors[0] = RED
  colors[1] = BLUE
  colors[2] = GREEN
  colors[3] = BLACK
  print("BLACK: (%d, %d, %d, %d)" % (colors[3].r, colors[3].g, colors[3].b, colors[3].a))
  
  # test fonts
  font = GetFontDefault()
  print("glyphCount (224) ", font.glyphCount)

def update():
  BeginDrawing()
  ClearBackground(RAYWHITE)
  DrawText("Congrats! You created your first python window!", 150, 200, 20, LIGHTGRAY)
  DrawFPS(10, 10)
  EndDrawing()