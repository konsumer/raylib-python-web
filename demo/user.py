def init():
    InitWindow(800, 450)

    # test struct
    print(RAYWHITE)
    r = Rectangle()
    r.height = 150
    r.width = 150
    print(r)

    # test StructArray
    # this should copy values into array
    colors = StructArray(Color, 4)
    colors[0] = RED
    colors[1] = BLUE
    colors[2] = GREEN
    colors[3] = BLACK
    print("colors.len (%d == 4?)" % len(colors))
    print(colors)

    # test fonts
    font = GetFontDefault()
    print(font)


def update():
    BeginDrawing()
    ClearBackground(RAYWHITE)
    DrawText("Congrats! You created your first python window!", 150, 200, 20, LIGHTGRAY)
    DrawFPS(10, 10)
    EndDrawing()
