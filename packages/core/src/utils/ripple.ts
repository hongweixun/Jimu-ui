import type { Directive, DirectiveBinding } from 'vue'

/**
 * 水波纹（Ripple）
 * ---------------------------------------------------------------------------
 * 触感参照 Varlet UI 的实现，尺寸与位移算法与之一致：
 *   半径 = √(w² + h²) / 2（对角线一半，保证扩散后必然盖满整个元素）
 *   起点 = 触点坐标 - 半径；终点 = 元素居中位置；缩放从 0.3 到 1
 *
 * 与 Varlet 的差异（都是移动端体感取舍，不是随意改）：
 *   1. Varlet 只监听 touchstart，桌面调试时鼠标点不出效果。这里统一用 pointerdown，
 *      触屏/鼠标/手写笔一套代码，也便于文档站的 PC 预览。
 *   2. Varlet 起手延迟 30ms 再创建，靠 touchmove 取消。这里同一套思路但用 pointer 事件，
 *      滑动超过 8px 直接丢弃 —— 列表滚动时不会闪出一片水波。
 *   3. 动画时长、缓动、颜色、透明度全部走 CSS 令牌，因此 data-motion="off" 与
 *      prefers-reduced-motion 天然生效（且关闭时根本不创建 DOM）。
 *
 * 契约：宿主元素需要能裁剪溢出，模块会在首次交互时补上 position: relative + overflow: hidden。
 */

export interface RippleOptions {
  /** 水波纹颜色，默认 currentColor（深色按钮上是白波，浅色元素上是主色波） */
  color?: string
  /** 关闭水波纹 */
  disabled?: boolean
  /** 忽略触点，固定从元素中心扩散（用于列表项这类不需要精确触点的场景） */
  centered?: boolean
}

const CLASS = 'jm-ripple'
const VISIBLE = 'is-visible'
const FADING = 'is-fading'
/** 手指位移超过该值视为滑动，放弃水波纹 */
const MOVE_TOLERANCE = 8
/** 起手延迟，用来区分"按下"和"开始滚动" */
const START_DELAY = 24
/** 扩散完成后至少停留的时长，快速点击才能看到完整波纹 */
const MIN_HOLD = 180
/** transitionend 的兜底（关闭动效时事件可能不触发） */
const FADE_FALLBACK = 260

function normalize(value: RippleOptions | boolean | undefined | null): RippleOptions {
  if (value === true) return {}
  if (value === false) return { disabled: true }
  return value ?? {}
}

function motionOff(el: Element): boolean {
  if (typeof window === 'undefined') return true
  if (el.closest('[data-motion="off"]')) return true
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function ensureClip(host: HTMLElement) {
  const cs = getComputedStyle(host)
  if (cs.position === 'static') host.style.position = 'relative'
  if (cs.overflow !== 'hidden') host.style.overflow = 'hidden'
}

class Ripple {
  private startTimer: number | null = null
  private active: Array<{ el: HTMLElement; born: number }> = []
  private startPoint = { x: 0, y: 0 }
  private options: RippleOptions

  constructor(
    private host: HTMLElement,
    options: RippleOptions,
  ) {
    this.options = options
    host.addEventListener('pointerdown', this.onPointerdown, { passive: true })
    host.addEventListener('keydown', this.onKeydown)
  }

  setOptions(options: RippleOptions) {
    this.options = options
  }

  private onPointerdown = (e: PointerEvent) => {
    this.startPoint = { x: e.clientX, y: e.clientY }
    window.addEventListener('pointermove', this.onPointermove, { passive: true })
    window.addEventListener('pointerup', this.onRelease, { passive: true })
    window.addEventListener('pointercancel', this.onRelease, { passive: true })
    this.schedule(e.clientX, e.clientY)
  }

  private onKeydown = (e: KeyboardEvent) => {
    if (e.key !== 'Enter' && e.key !== ' ') return
    if (e.repeat) return
    this.host.addEventListener('keyup', this.onKeyup)
    this.host.addEventListener('blur', this.onKeyup)
    this.schedule()
  }

  private onKeyup = () => {
    this.host.removeEventListener('keyup', this.onKeyup)
    this.host.removeEventListener('blur', this.onKeyup)
    this.release()
  }

  private onPointermove = (e: PointerEvent) => {
    const dx = e.clientX - this.startPoint.x
    const dy = e.clientY - this.startPoint.y
    if (Math.hypot(dx, dy) <= MOVE_TOLERANCE) return
    this.cancelPending()
    this.release()
  }

  private onRelease = () => {
    this.cleanupWindowListeners()
    this.release()
  }

  private cleanupWindowListeners() {
    window.removeEventListener('pointermove', this.onPointermove)
    window.removeEventListener('pointerup', this.onRelease)
    window.removeEventListener('pointercancel', this.onRelease)
  }

  private cancelPending() {
    if (this.startTimer !== null) {
      window.clearTimeout(this.startTimer)
      this.startTimer = null
    }
  }

  private schedule(x?: number, y?: number) {
    if (this.options.disabled || motionOff(this.host)) return
    this.cancelPending()
    this.startTimer = window.setTimeout(() => {
      this.startTimer = null
      this.spawn(x, y)
    }, START_DELAY)
  }

  private spawn(x?: number, y?: number) {
    const host = this.host
    const { clientWidth: w, clientHeight: h } = host
    if (!w || !h) return
    ensureClip(host)

    const rect = host.getBoundingClientRect()
    const radius = Math.hypot(w, h) / 2
    const fromCenter = this.options.centered || x === undefined || y === undefined
    const localX = fromCenter ? w / 2 : x - rect.left - host.clientLeft
    const localY = fromCenter ? h / 2 : y - rect.top - host.clientTop

    const el = document.createElement('span')
    el.className = CLASS
    el.style.width = `${radius * 2}px`
    el.style.height = `${radius * 2}px`
    el.style.setProperty('--jm-ripple-x', `${localX - radius}px`)
    el.style.setProperty('--jm-ripple-y', `${localY - radius}px`)
    el.style.setProperty('--jm-ripple-cx', `${(w - radius * 2) / 2}px`)
    el.style.setProperty('--jm-ripple-cy', `${(h - radius * 2) / 2}px`)
    if (this.options.color) el.style.backgroundColor = this.options.color

    host.appendChild(el)
    // 强制一次布局，让初始的 transform 落地，否则会从终点直接闪现
    void el.offsetWidth
    el.classList.add(VISIBLE)

    this.active.push({ el, born: performance.now() })
  }

  private release() {
    this.cancelPending()
    if (!this.active.length) return
    const ripples = this.active
    this.active = []

    ripples.forEach(({ el, born }) => {
      const wait = Math.max(0, MIN_HOLD - (performance.now() - born))
      window.setTimeout(() => this.fade(el), wait)
    })
  }

  private fade(el: HTMLElement) {
    if (!el.isConnected) return
    el.classList.add(FADING)
    const done = () => {
      el.removeEventListener('transitionend', onEnd)
      window.clearTimeout(timer)
      el.remove()
    }
    const onEnd = (event: TransitionEvent) => {
      if (event.propertyName === 'opacity') done()
    }
    const timer = window.setTimeout(done, FADE_FALLBACK)
    el.addEventListener('transitionend', onEnd)
  }

  destroy() {
    this.host.removeEventListener('pointerdown', this.onPointerdown)
    this.host.removeEventListener('keydown', this.onKeydown)
    this.host.removeEventListener('keyup', this.onKeyup)
    this.host.removeEventListener('blur', this.onKeyup)
    this.cleanupWindowListeners()
    this.cancelPending()
    this.active.forEach(({ el }) => el.remove())
    this.active = []
  }
}

type RippleHost = HTMLElement & { __jmRipple?: Ripple }

/**
 * v-ripple 指令
 *   <div v-ripple>…</div>
 *   <div v-ripple="{ color: '#fff', centered: true }">…</div>
 */
export const vRipple: Directive<RippleHost, RippleOptions | boolean | undefined> = {
  mounted(el: RippleHost, binding: DirectiveBinding<RippleOptions | boolean | undefined>) {
    el.__jmRipple = new Ripple(el, normalize(binding.value))
  },
  updated(el: RippleHost, binding: DirectiveBinding<RippleOptions | boolean | undefined>) {
    el.__jmRipple?.setOptions(normalize(binding.value))
  },
  beforeUnmount(el: RippleHost) {
    el.__jmRipple?.destroy()
    delete el.__jmRipple
  },
}

export default vRipple
