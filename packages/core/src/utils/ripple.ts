import type { Directive, DirectiveBinding } from 'vue'

/**
 * 水波纹（Ripple）
 * ---------------------------------------------------------------------------
 * 几何与 Varlet 一致：
 *   半径 = √(w² + h²) / 2（对角线一半，保证扩散后必然盖满整个元素）
 *   起点 = 触点坐标 - 半径；终点 = 元素居中位置；缩放从 0.3 到 1
 *
 * 真机上的历史问题（0.25.9 及之前）：
 *   旧实现按下后延迟 24ms 才创建波纹，靠"还没到位就抬手/开始滑"取消它。
 *   真机上快速轻点（< 24ms 抬手）与轻微手指抖动（> 8px）都会命中取消路径，
 *   结果是「按钮 :active 压暗了、click 也触发了，但根本没有波纹」——
 *   用户看到的就是"有时候有、有时候只有底色变了一下"。
 *
 * 现在的策略（按下即有，绝不丢反馈）：
 *   1. pointerdown 当帧立即创建波纹，不再有延迟窗口 —— 任何真实按压必出水波；
 *   2. 位移容差放宽到 12px，覆盖真机手指落地时的自然抖动；
 *   3. 超过容差（判定为滑动）或 pointercancel（浏览器接管滚动）时，
 *      波纹不硬删，而是立即快速淡出 —— 列表滚动不会留下明显水波；
 *   4. 抬手时按 MIN_HOLD 补足最短展示时长，极快点也能看到完整扩散；
 *   5. 不支持 PointerEvent 的内核（部分老 iOS / 内嵌 WebView）自动降级到
 *      touch / mouse 事件，行为一致 —— 这类环境此前是完全没有任何波纹的。
 *
 * 契约：宿主元素需要能裁剪溢出，模块在挂载时补上 position: relative + overflow: hidden。
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
/** 手指位移超过该值视为滑动，放弃波纹（12px：覆盖真机手指落地抖动） */
const MOVE_TOLERANCE = 12
/** 扩散完成后至少停留的时长，快速点击才能看到完整波纹 */
const MIN_HOLD = 180
/** transitionend 的兜底（关闭动效时事件可能不触发） */
const FADE_FALLBACK = 260

interface ActiveRipple {
  el: HTMLElement
  born: number
}

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
  private active: ActiveRipple[] = []
  private startPoint = { x: 0, y: 0 }
  private pointerId: number | null = null
  private options: RippleOptions
  private hasPointer = typeof window !== 'undefined' && 'PointerEvent' in window

  constructor(
    private host: HTMLElement,
    options: RippleOptions,
  ) {
    this.options = options
    /* 裁剪能力在挂载时就位：首次点击不用再做一次 getComputedStyle + 样式重算 */
    ensureClip(host)
    if (this.hasPointer) {
      host.addEventListener('pointerdown', this.onPointerdown, { passive: true })
    } else {
      host.addEventListener('touchstart', this.onTouchstart, { passive: true })
      host.addEventListener('mousedown', this.onMousedown)
    }
    host.addEventListener('keydown', this.onKeydown)
  }

  setOptions(options: RippleOptions) {
    this.options = options
  }

  /* ---------------- 按下即创建 ---------------- */

  private begin(x: number, y: number) {
    this.startPoint = { x, y }
    this.spawn(x, y)
  }

  private onPointerdown = (e: PointerEvent) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return
    this.pointerId = e.pointerId
    window.addEventListener('pointermove', this.onPointermove, { passive: true })
    window.addEventListener('pointerup', this.onPointerup, { passive: true })
    window.addEventListener('pointercancel', this.onPointercancel, { passive: true })
    this.begin(e.clientX, e.clientY)
  }

  private onPointermove = (e: PointerEvent) => {
    if (this.pointerId !== null && e.pointerId !== this.pointerId) return
    this.trackMove(e.clientX, e.clientY)
  }

  private onPointerup = () => {
    this.cleanupWindowListeners()
    this.release(false)
  }

  private onPointercancel = () => {
    this.cleanupWindowListeners()
    /* 浏览器接管滚动（真机滚动列表里按下再滑）：快速淡出，不留长尾 */
    this.release(true)
  }

  /* ---------------- 无 PointerEvent 内核的降级路径 ---------------- */

  private onTouchstart = (e: TouchEvent) => {
    const t = e.touches[0]
    if (!t) return
    this.pointerId = t.identifier
    window.addEventListener('touchmove', this.onTouchmove, { passive: true })
    window.addEventListener('touchend', this.onTouchend, { passive: true })
    window.addEventListener('touchcancel', this.onTouchcancel, { passive: true })
    this.begin(t.clientX, t.clientY)
  }

  private onTouchmove = (e: TouchEvent) => {
    const t = [...e.touches].find((p) => p.identifier === this.pointerId) ?? e.touches[0]
    if (!t) return
    this.trackMove(t.clientX, t.clientY)
  }

  private onTouchend = () => {
    this.cleanupWindowListeners()
    this.release(false)
  }

  private onTouchcancel = () => {
    this.cleanupWindowListeners()
    this.release(true)
  }

  private onMousedown = (e: MouseEvent) => {
    if (e.button !== 0) return
    window.addEventListener('mousemove', this.onMousemove)
    window.addEventListener('mouseup', this.onMouseup)
    this.begin(e.clientX, e.clientY)
  }

  private onMousemove = (e: MouseEvent) => this.trackMove(e.clientX, e.clientY)

  private onMouseup = () => {
    this.cleanupWindowListeners()
    this.release(false)
  }

  /* ---------------- 键盘 ---------------- */

  private onKeydown = (e: KeyboardEvent) => {
    if (e.key !== 'Enter' && e.key !== ' ') return
    if (e.repeat) return
    this.host.addEventListener('keyup', this.onKeyup)
    this.host.addEventListener('blur', this.onKeyup)
    this.spawn()
  }

  private onKeyup = () => {
    this.host.removeEventListener('keyup', this.onKeyup)
    this.host.removeEventListener('blur', this.onKeyup)
    this.release(false)
  }

  /* ---------------- 内部 ---------------- */

  private trackMove(x: number, y: number) {
    const dx = x - this.startPoint.x
    const dy = y - this.startPoint.y
    if (Math.hypot(dx, dy) <= MOVE_TOLERANCE) return
    /* 手指在按钮上滑出去了：判定为滑动/滚动，波纹快速淡出（不硬删，避免闪断） */
    this.release(true)
  }

  private cleanupWindowListeners() {
    this.pointerId = null
    window.removeEventListener('pointermove', this.onPointermove)
    window.removeEventListener('pointerup', this.onPointerup)
    window.removeEventListener('pointercancel', this.onPointercancel)
    window.removeEventListener('touchmove', this.onTouchmove)
    window.removeEventListener('touchend', this.onTouchend)
    window.removeEventListener('touchcancel', this.onTouchcancel)
    window.removeEventListener('mousemove', this.onMousemove)
    window.removeEventListener('mouseup', this.onMouseup)
  }

  private spawn(x?: number, y?: number) {
    if (this.options.disabled || motionOff(this.host)) return
    const host = this.host
    const { clientWidth: w, clientHeight: h } = host
    if (!w || !h) return

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
    // 强制一次布局让初始 transform/opacity 落地，下一帧再加 is-visible 才会真的"扩开"
    void el.offsetWidth
    requestAnimationFrame(() => {
      if (el.isConnected && !el.classList.contains(FADING)) el.classList.add(VISIBLE)
    })

    this.active.push({ el, born: performance.now() })
  }

  /** quick = true：滑动/滚动取消，立即淡出；false：正常抬手，补足 MIN_HOLD */
  private release(quick: boolean) {
    if (!this.active.length) return
    const ripples = this.active
    this.active = []

    ripples.forEach(({ el, born }) => {
      const wait = quick ? 0 : Math.max(0, MIN_HOLD - (performance.now() - born))
      if (wait === 0) this.fade(el, quick)
      else window.setTimeout(() => this.fade(el, quick), wait)
    })
  }

  private fade(el: HTMLElement, quick: boolean) {
    if (!el.isConnected) return
    /* 从没来得及显示过（按下即滚动取消）：直接移除，避免闪一下 */
    if (!el.classList.contains(VISIBLE)) {
      el.remove()
      return
    }
    el.classList.add(FADING)
    if (quick) el.style.transitionDuration = '0ms, 90ms'
    const done = () => {
      el.removeEventListener('transitionend', onEnd)
      window.clearTimeout(timer)
      el.remove()
    }
    const onEnd = (event: TransitionEvent) => {
      if (event.propertyName === 'opacity') done()
    }
    const timer = window.setTimeout(done, quick ? 120 : FADE_FALLBACK)
    el.addEventListener('transitionend', onEnd)
  }

  destroy() {
    if (this.hasPointer) this.host.removeEventListener('pointerdown', this.onPointerdown)
    else {
      this.host.removeEventListener('touchstart', this.onTouchstart)
      this.host.removeEventListener('mousedown', this.onMousedown)
    }
    this.host.removeEventListener('keydown', this.onKeydown)
    this.host.removeEventListener('keyup', this.onKeyup)
    this.host.removeEventListener('blur', this.onKeyup)
    this.cleanupWindowListeners()
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
