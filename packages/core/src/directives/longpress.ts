import type { Directive, DirectiveBinding } from 'vue'

/**
 * 长按指令（v-longpress）
 * ---------------------------------------------------------------------------
 * 移动端最常用的"隐藏操作"入口：长按消息多选、长按卡片出菜单、长按图片识别。
 *
 * 时序：
 *   pointerdown → 计时开始（触发 onStart，供宿主做按压反馈）
 *   ├─ 移动超过 moveTolerance   → 取消（滑动列表时不会误触）
 *   ├─ 提前松手 / pointercancel → 取消
 *   └─ 到达 duration            → 触发 onLongPress，此后松手不再算点击
 *
 * 键盘可访问：Enter / Space 按住相当于长按（与 pointer 同一套计时），松开提前取消。
 * 统一用 pointer 事件，触屏/鼠标/手写笔一套代码。
 */

export interface LongPressOptions {
  /** 长按触发回调 */
  onLongPress: (event: PointerEvent | KeyboardEvent) => void
  /** 按下时回调（用来做按压反馈，比如加个 is-pressing class） */
  onStart?: () => void
  /** 长按被取消（提前松手 / 移动超限 / 触发完成后的收尾），state: 'done' 表示已触发 */
  onEnd?: (state: 'done' | 'cancelled') => void
  /** 按住多久算长按，默认 500ms */
  duration?: number
  /** 移动超过该距离（px）视为滑动，取消长按，默认 8 */
  moveTolerance?: number
  /** 禁用长按 */
  disabled?: boolean
}

const MOVE_TOLERANCE = 8
const DURATION = 500

function normalize(
  value: LongPressOptions | undefined | null,
): LongPressOptions {
  return value ?? { onLongPress: () => {} }
}

class LongPress {
  private timer: number | null = null
  private startPoint = { x: 0, y: 0 }
  private pressed = false
  private options: LongPressOptions

  constructor(
    private host: HTMLElement,
    options: LongPressOptions,
  ) {
    this.options = options
    host.addEventListener('pointerdown', this.onDown, { passive: true })
    host.addEventListener('keydown', this.onKeydown)
    host.addEventListener('keyup', this.onKeyup)
    host.addEventListener('blur', this.onKeyup)
  }

  setOptions(options: LongPressOptions) {
    this.options = options
  }

  private onDown = (e: PointerEvent) => {
    if (this.options.disabled) return
    this.startPoint = { x: e.clientX, y: e.clientY }
    this.pressed = true
    this.options.onStart?.()
    window.addEventListener('pointermove', this.onMove, { passive: true })
    window.addEventListener('pointerup', this.onUp, { passive: true })
    window.addEventListener('pointercancel', this.onUp, { passive: true })
    const duration = this.options.duration ?? DURATION
    this.timer = window.setTimeout(() => {
      this.timer = null
      this.options.onLongPress(e)
      this.reset('done')
    }, duration)
  }

  private onKeydown = (e: KeyboardEvent) => {
    if (e.key !== 'Enter' && e.key !== ' ') return
    if (e.repeat || this.options.disabled || this.pressed) return
    this.pressed = true
    this.options.onStart?.()
    const duration = this.options.duration ?? DURATION
    this.timer = window.setTimeout(() => {
      this.timer = null
      this.options.onLongPress(e)
      this.reset('done')
    }, duration)
  }

  private onKeyup = () => {
    if (!this.pressed) return
    /* 键盘路径：松开时还没触发就取消；已触发则 reset 在 timeout 里完成 */
    if (this.timer !== null) this.cancel('cancelled')
  }

  private onMove = (e: PointerEvent) => {
    const tolerance = this.options.moveTolerance ?? MOVE_TOLERANCE
    const dx = e.clientX - this.startPoint.x
    const dy = e.clientY - this.startPoint.y
    if (Math.hypot(dx, dy) > tolerance) this.cancel('cancelled')
  }

  private onUp = () => {
    /* 提前松手：还没触发就取消 */
    if (this.timer !== null) this.cancel('cancelled')
    else this.reset('done')
  }

  private cancel(state: 'done' | 'cancelled') {
    if (this.timer !== null) {
      window.clearTimeout(this.timer)
      this.timer = null
    }
    this.options.onEnd?.(state)
    this.cleanup()
  }

  private reset(state: 'done' | 'cancelled') {
    this.options.onEnd?.(state)
    this.cleanup()
  }

  private cleanup() {
    this.pressed = false
    window.removeEventListener('pointermove', this.onMove)
    window.removeEventListener('pointerup', this.onUp)
    window.removeEventListener('pointercancel', this.onUp)
  }

  destroy() {
    if (this.timer !== null) window.clearTimeout(this.timer)
    this.host.removeEventListener('pointerdown', this.onDown)
    this.host.removeEventListener('keydown', this.onKeydown)
    this.host.removeEventListener('keyup', this.onKeyup)
    this.host.removeEventListener('blur', this.onKeyup)
    this.cleanup()
  }
}

type LongPressHost = HTMLElement & { __jmLongPress?: LongPress }

/**
 * v-longpress 指令
 *   <div v-longpress="{ onLongPress: () => delete() }">长按删除</div>
 *   <div v-longpress="{ duration: 800, onStart: press, onEnd: release }">…</div>
 */
export const vLongPress: Directive<
  LongPressHost,
  LongPressOptions | undefined | null
> = {
  mounted(el: LongPressHost, binding) {
    el.__jmLongPress = new LongPress(el, normalize(binding.value))
  },
  updated(el: LongPressHost, binding) {
    el.__jmLongPress?.setOptions(normalize(binding.value))
  },
  beforeUnmount(el: LongPressHost) {
    el.__jmLongPress?.destroy()
    delete el.__jmLongPress
  },
}

export default vLongPress
