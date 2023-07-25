import Module from './raylib.js'

export default async function setup (canvas) {
  const mod = await Module({ canvas })
  mod.mem = new DataView(mod.HEAPU8.buffer)
  const pyodide = await loadPyodide()
  window.mod = mod
  pyodide.globals.set('_mod', mod)

  // just for dev, pull wrapper from seperate file
  const wrapper = await fetch('wasmraypy/__init__.py').then(r => r.text())
  pyodide.runPython(wrapper)

  return pyodide
}
