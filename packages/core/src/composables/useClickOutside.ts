import { isRef, onUnmounted, watch, type Ref } from 'vue'

/**
 * 点击外部检测（useClickOutside）
 * ---------------------------------------------------------------------------
 * 弹层收起的另一半逻辑：Popover / 下拉面板 / 日期选择器打开后，
 * 点面板外面任何地方都应该收起。手写容易踩两个坑：
 *   1. 监听 click —— 打开面板的那次点击（冒泡到 document）会立刻把面板关掉；
 *   2. 只判一个元素 —— 触发器和面板是两个兄弟节点，点触发器也该被豁免。
 *
 * 统一处理：
 *   - 事件用 pointerdown（capture 阶段），先于大多数交互逻辑，也不会被
 *     某些组件 stopPropagation 的 click 卡住；
 *   - 武装延迟两帧（双 rAF）：面板由"点击"打开时，打开的那次事件已经彻底
 *     结束才注册监听，不会自己把自己关掉；也不需要"跳过下一条"的猜测——
 *     用户打开后紧接着点外部，第一次就能正常收起；
 *   - target 支持单个 ref 或 ref 数组，命中任意一个都算"内部"。
 */

export interface UseClickOutsideOptions {
  /** 监听的事件类型，默认 pointerdown */
  event?: 'pointerdown' | 'mousedown' | 'touchstart'
  /** 武装延迟帧数，默认 2（双 rAF），一般不用改 */
  delayFrames?: number
}

type Target = Ref<Element | null | undefined> | Array<Ref<Element | null | undefined>>

function contains(targets: Target, point: EventTarget | null): boolean {
  if (!(point instanceof Node)) return false
  const list = Array.isArray(targets) ? targets : [targets]
  return list.some((t) => isRef(t) && t.value?.contains(point))
}

export function useClickOutside(
  target: Target,
  handler: (event: PointerEvent | MouseEvent | TouchEvent) => void,
  options: UseClickOutsideOptions = {},
): { stop: () => void } {
  const { event = 'pointerdown', delayFrames = 2 } = options

  function onEvent(e: PointerEvent | MouseEvent | TouchEvent) {
    if (!contains(target, e.target)) handler(e)
  }

  /* 双 rAF：等"打开面板"的那次事件走完（含冒泡与浏览器默认行为）再武装 */
  const rafIds: number[] = []
  let armed = false
  for (let i = 0; i < delayFrames; i += 1) {
    rafIds.push(
      requestAnimationFrame(() => {
        if (i === delayFrames - 1) {
          armed = true
          document.addEventListener(event, onEvent, true)
        }
      }),
    )
  }

  function stop() {
    rafIds.forEach((id) => cancelAnimationFrame(id))
    rafIds.length = 0
    if (armed) document.removeEventListener(event, onEvent, true)
    armed = false
  }

  onUnmounted(stop)

  return { stop }
}

/** 受控版：只在 active 为 true 时监听（面板开着才需要点外部收起） */
export function useClickOutsideWhen(
  active: Ref<boolean>,
  target: Target,
  handler: (event: PointerEvent | MouseEvent | TouchEvent) => void,
  options: UseClickOutsideOptions = {},
): { stop: () => void } {
  let inner: { stop: () => void } | null = null

  watch(
    active,
    (on) => {
      if (on) inner = useClickOutside(target, handler, options)
      else {
        inner?.stop()
        inner = null
      }
    },
    { immediate: true },
  )

  onUnmounted(() => {
    inner?.stop()
    inner = null
  })

  return {
    stop: () => {
      inner?.stop()
      inner = null
    },
  }
}

export default useClickOutside
