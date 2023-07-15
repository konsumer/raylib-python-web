import Module from './raylib.js'

export default async function setup (canvas) {
  const mod = await Module({ canvas })
  const pyodide = await loadPyodide()
  window.mod = mod
  pyodide.globals.set('_mod', mod)

  // just for dev, pull wrapper from seperate file
  const wrapper = await fetch('wrapper.py').then(r => r.text())

  pyodide.runPython(wrapper)

  // here we do all the binding: this will be generated
  // most wasm functions can be exposed directly with _NAME
  // these will eventually be in python-space, I think

  pyodide.globals.set('InitWindow', mod._InitWindow)
  pyodide.globals.set('BeginDrawing', mod._BeginDrawing)
  pyodide.globals.set('DrawFPS', mod._DrawFPS)
  pyodide.globals.set('EndDrawing', mod._EndDrawing)

  // these are functions that are not in the api JSON
  pyodide.globals.set('DrawTextBoxedSelectable', mod.cwrap('DrawTextBoxedSelectable', 'void', ['pointer', 'string', 'pointer', 'f32', 'f32', 'bool', 'pointer', 'i32', 'pointer', 'pointer']))
  pyodide.globals.set('DrawTextBoxed', mod.cwrap('DrawTextBoxed', 'void', ['pointer', 'string', 'pointer', 'f32', 'f32', 'bool', 'pointer']))

  return pyodide
}
