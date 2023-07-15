import Module from './raylib.js'

export default async function setup (canvas) {
  const mod = await Module({ canvas })
  const pyodide = await loadPyodide()

  // this is a temp function until I figure out how structs will work
  // it creates a pointer to a color, then sets r/g/b/a
  const color = (r, g, b, a) => {
    const o = mod._malloc(4)
    mod.HEAP8[o + 0] = r
    mod.HEAP8[o + 1] = g
    mod.HEAP8[o + 2] = b
    mod.HEAP8[o + 3] = a
    return o
  }

  // here we do all the binding: this will be generated
  // most wasm functions can be exposed directly with _NAME
  pyodide.globals.set('_mod', mod)
  pyodide.globals.set('InitWindow', mod._InitWindow)
  pyodide.globals.set('BeginDrawing', mod._BeginDrawing)
  pyodide.globals.set('DrawFPS', mod._DrawFPS)
  pyodide.globals.set('EndDrawing', mod._EndDrawing)
  pyodide.globals.set('ClearBackground', mod._ClearBackground)

  // some have types that can be automatically converted (like the string here)
  pyodide.globals.set('DrawText', mod.cwrap('DrawText', 'void', ['string', 'i32', 'i32', 'f32', 'pointer']))

  // these are functions that are not in the api JSON
  pyodide.globals.set('DrawTextBoxedSelectable', mod.cwrap('DrawTextBoxedSelectable', 'void', ['pointer', 'string', 'pointer', 'f32', 'f32', 'bool', 'pointer', 'i32', 'pointer', 'pointer']))
  pyodide.globals.set('DrawTextBoxed', mod.cwrap('DrawTextBoxed', 'void', ['pointer', 'string', 'pointer', 'f32', 'f32', 'bool', 'pointer']))

  // since I am not sure how structs will work, this is just some initial stuff to make the demo work
  pyodide.globals.set('LIGHTGRAY', color(200, 200, 200, 255)) // Light Gray
  pyodide.globals.set('GRAY', color(130, 130, 130, 255)) // Gray
  pyodide.globals.set('DARKGRAY', color(80, 80, 80, 255)) // Dark Gray
  pyodide.globals.set('YELLOW', color(253, 249, 0, 255)) // Yellow
  pyodide.globals.set('GOLD', color(255, 203, 0, 255)) // Gold
  pyodide.globals.set('ORANGE', color(255, 161, 0, 255)) // Orange
  pyodide.globals.set('PINK', color(255, 109, 194, 255)) // Pink
  pyodide.globals.set('RED', color(230, 41, 55, 255)) // Red
  pyodide.globals.set('MAROON', color(190, 33, 55, 255)) // Maroon
  pyodide.globals.set('GREEN', color(0, 228, 48, 255)) // Green
  pyodide.globals.set('LIME', color(0, 158, 47, 255)) // Lime
  pyodide.globals.set('DARKGREEN', color(0, 117, 44, 255)) // Dark Green
  pyodide.globals.set('SKYBLUE', color(102, 191, 255, 255)) // Sky Blue
  pyodide.globals.set('BLUE', color(0, 121, 241, 255)) // Blue
  pyodide.globals.set('DARKBLUE', color(0, 82, 172, 255)) // Dark Blue
  pyodide.globals.set('PURPLE', color(200, 122, 255, 255)) // Purple
  pyodide.globals.set('VIOLET', color(135, 60, 190, 255)) // Violet
  pyodide.globals.set('DARKPURPLE', color(112, 31, 126, 255)) // Dark Purple
  pyodide.globals.set('BEIGE', color(211, 176, 131, 255)) // Beige
  pyodide.globals.set('BROWN', color(127, 106, 79, 255)) // Brown
  pyodide.globals.set('DARKBROWN', color(76, 63, 47, 255)) // Dark Brown
  pyodide.globals.set('WHITE', color(255, 255, 255, 255)) // White
  pyodide.globals.set('BLACK', color(0, 0, 0, 255)) // Black
  pyodide.globals.set('BLANK', color(0, 0, 0, 0)) // Blank (Transparent)
  pyodide.globals.set('MAGENTA', color(255, 0, 255, 255)) // Magenta
  pyodide.globals.set('RAYWHITE', color(245, 245, 245, 255)) // My own White (raylib logo)

  return pyodide
}
