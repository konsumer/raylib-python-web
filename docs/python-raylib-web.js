import Module from './raylib.js'

const loc = import.meta.url.replace(/python-raylib-web\.js$/, '')

export default async function setup (canvas) {
  const mod = await Module({ canvas })
  mod.mem = new DataView(mod.HEAPU8.buffer)
  const pyodide = await loadPyodide()
  window.mod = mod
  pyodide.globals.set('_mod', mod)

  console.log()

  // just for dev, pull wrapper from seperate file
  const wrapper = await fetch(`${loc}/wasmraypy/__init__.py`).then(r => r.text())
  pyodide.runPython(wrapper)

  return pyodide
}
