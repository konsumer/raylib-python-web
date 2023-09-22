import 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js'
import setup from 'https://konsumer.js.org/raylib-python-web/python-raylib-web.js'

class RaylibPythonComponent extends HTMLElement {
  constructor () {
    super()
    this.shadow = this.attachShadow({ mode: 'open' })
    this.canvas = document.createElement('canvas')
    this.style.display = 'none'
    window.addEventListener('resize', this.onResize.bind(this))
    this.shadow.innerHTML = `
<style>
canvas.landscape {
  height: 100vh;
  max-width: 100vw;
}
canvas.portrait {
  width: 100vw;
  max-height: 100vh;
}
canvas {
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
  object-fit: contain;
}
</style>
`
    this.shadow.appendChild(this.canvas)
    this.start(this.getAttribute('src'))
    this.canvas.addEventListener('contextmenu', e => e.preventDefault())
  }

  onResize () {
    if (this.fill) {
      const { clientWidth, clientHeight } = document.body
      this.canvas.className = clientWidth > clientHeight ? 'landscape' : 'portrait'
    }
  }

  static get observedAttributes () {
    return ['src', 'fill']
  }

  attributeChangedCallback (name, oldValue, newValue) {
    if (name === 'fill') {
      this.fill = typeof newValue !== 'undefined'
      this.onResize()
    }
    if (name === 'src') {
      this.start(newValue)
    }
  }

  async start (src) {
    let userCode = this.textContent
    if (src) {
      userCode = await fetch(src).then(r => r.text())
    }
    this.style.display = 'block'
    const python = await setup(this.canvas)
    python.runPython(userCode)
    python.runPython('init()')
    const update = () => {
      python.runPython('update()')
      requestAnimationFrame(update)
    }
    update()
  }

  connectedCallback () {
    const observer = new MutationObserver((mutations) => {
      this.start(this.src)
    })
    observer.observe(this, { childList: true })
  }
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    window.customElements.define('raylib-python-game', RaylibComponent)
  })
}
