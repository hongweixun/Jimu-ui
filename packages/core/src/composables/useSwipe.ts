import { ref, onUnmounted, watch, type Ref } from 'vue'

/**
 * 滑动手势（useSwipe）
 * ---------------------------------------------------------------------------
 * 轮播、侧滑删除、抽屉拖拽的底层手势：按下 → 跟手位移 → 松手判方向。
 * 统一 pointer 事件（触屏/鼠标一套），不需要 element 加 touch-action 之外的任何配置。
 *
 * direction 判定：位移超过 threshold 且耗时在 duration 内才算一次有效滑动，
 * 以主导轴为准（|dx| 与 |dy| 谁大听谁的），避免斜着滑 45° 时来回抖。
 *
 * @example
 *   const { direction, offsetX, offsetY } = useSwipe(card, {
 *     onSwipeEnd: (dir) => { if (dir === 'left') showDelete() },
 *   })
 */

export type SwipeDirection = '' | 'up' | 'down' | 'left' | 'right'

export interface UseSwipeOptions {
  /** 触发滑动的最小位移（px），默认 30 */
  threshold?: number
  /** 手势最长时长（ms），超过不算滑动（长按后拖动通常是另一个意图），默认 1000 */
  duration?: number
  /** 手势开始（真实按下即触发，供宿主做跟随反馈） */
  onSwipeStart?: (e: PointerEvent) => void
  /** 手势进行中（跟随位移） */
  onSwipe?: () => void
  /** 手势结束；dir 为空串表示未达到滑动阈值 */
  onSwipeEnd?: (direction: SwipeDirection, offsetX: number, offsetY: number) => void
}

export interface UseSwipeReturn {
  /** 本次手势的方向，未滑动为 ''；松手后保留到下一次手势开始 */
  direction: Ref<SwipeDirection>
  /** 实时 X 位移（px），相对按下点 */
  offsetX: Ref<number>
  /** 实时 Y 位移（px） */
  offsetY: Ref<number>
  /** 手势进行中 */
  isSwiping: Ref<boolean>
  stop: () => void
}

export function useSwipe(
  target: Ref<HTMLElement | null | undefined> | (() => HTMLElement | null | undefined),
  options: UseSwipeOptions = {},
): UseSwipeReturn {
  const { threshold = 30, duration = 1000, onSwipeStart, onSwipe, onSwipeEnd } = options

  const direction = ref<SwipeDirection>('') as Ref<SwipeDirection>
  const offsetX = ref(0)
  const offsetY = ref(0)
  const isSwiping = ref(false)

  let startX = 0
  let startY = 0
  let startTime = 0
  let active = false

  function getEl(): HTMLElement | null | undefined {
    return typeof target === 'function' ? target() : target?.value
  }

  function onDown(e: PointerEvent) {
    active = true
    startX = e.clientX
    startY = e.clientY
    startTime = Date.now()
    offsetX.value = 0
    offsetY.value = 0
    direction.value = ''
    isSwiping.value = true
    onSwipeStart?.(e)
    window.addEventListener('pointermove', onMove, { passive: true })
    window.addEventListener('pointerup', onUp, { passive: true })
    window.addEventListener('pointercancel', onUp, { passive: true })
  }

  function onMove(e: PointerEvent) {
    if (!active) return
    offsetX.value = e.clientX - startX
    offsetY.value = e.clientY - startY
    onSwipe?.()
  }

  function onUp() {
    if (!active) return
    active = false
    isSwiping.value = false
    window.removeEventListener('pointermove', onMove)
    window.removeEventListener('pointerup', onUp)
    window.removeEventListener('pointercancel', onUp)

    const dx = offsetX.value
    const dy = offsetY.value
    let dir: SwipeDirection = ''
    if (Math.hypot(dx, dy) >= threshold && Date.now() - startTime <= duration) {
      if (Math.abs(dx) >= Math.abs(dy)) dir = dx > 0 ? 'right' : 'left'
      else dir = dy > 0 ? 'down' : 'up'
    }
    direction.value = dir
    onSwipeEnd?.(dir, dx, dy)
  }

  let bound: HTMLElement | null = null
  function bind() {
    const el = getEl()
    if (el && el !== bound) {
      el.addEventListener('pointerdown', onDown)
      bound = el
    }
  }
  bind()
  /* setup 阶段 template ref 还是 null：挂载后/目标变化时补绑 */
  watch(getEl, (el, was) => {
    if (was) was.removeEventListener('pointerdown', onDown)
    bound = null
    bind()
  })

  function stop() {
    if (bound) bound.removeEventListener('pointerdown', onDown)
    bound = null
    window.removeEventListener('pointermove', onMove)
    window.removeEventListener('pointerup', onUp)
    window.removeEventListener('pointercancel', onUp)
  }

  onUnmounted(stop)

  return { direction, offsetX, offsetY, isSwiping, stop }
}

export default useSwipe
