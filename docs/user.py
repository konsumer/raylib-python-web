font = None
colors = None


def init():
    global font, colors
    init_window(800, 450, "dfgdfg")

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
    font = get_font_default()
    print(font)


def update():
    begin_drawing()
    clear_background(RAYWHITE)
    draw_text("Congrats! You created your first python window!", 150, 200, 20, LIGHTGRAY)
    draw_fps(10, 10)
    end_drawing()
