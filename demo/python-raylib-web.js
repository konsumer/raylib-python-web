import Module from './raylib.js'

export default async function setup (canvas) {
  const mod = await Module({ canvas })
  const pyodide = await loadPyodide()
  window.mod = mod
  pyodide.globals.set('_mod', mod)

  // just for dev, pull wrapper from seperate file
  const wrapper = await fetch('wrapper.py').then(r => r.text())
  pyodide.runPython(wrapper)

  return pyodide
}
