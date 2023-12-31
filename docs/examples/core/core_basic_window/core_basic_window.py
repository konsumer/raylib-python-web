"""

raylib [core] example - Basic Window

"""

# Declaration / Initialization
# ------------------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# Web main entry point
# ------------------------------------------------------------------------------------
def init():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - basic window")

    # TODO: Load resources / Initialize variables at this point

    set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# Web main loop
# ------------------------------------------------------------------------------------
def update():
    # Update
    # ----------------------------------------------------------------------------------
    # TODO: Update variables / Implement example logic at this point
    # ----------------------------------------------------------------------------------

    # Draw
    # ----------------------------------------------------------------------------------
    begin_drawing()

    clear_background(RED)
    draw_text("Congrats! You created your first python window!", 150, 200, 20, LIGHTGRAY)

    end_drawing()
    # ----------------------------------------------------------------------------------
