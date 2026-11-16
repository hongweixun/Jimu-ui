import { onUnmounted, watch, type Ref } from 'vue'
import { lockScroll, unlockScroll } from '../utils'

/**
 * 滚动锁定（useLockScroll）
 * ---------------------------------------------------------------------------
 * 弹层开着时页面不该跟着滚（body overflow: hidden）。真正的难点是**多层弹层**：
 * Dialog 上再开 ActionSheet，底下 Dialog 关了就把锁解了，顶层还在滚。
 *
 * utils 里已有计数式 lockScroll/unlockScroll（弹层组件在用），
 * 本组合式函数把它接到响应式状态上：active 变 true 上锁、false 解锁，
 * 组件卸载时兜底解锁——声明式使用，不用关心计数细节。
 *
 * @example
 *   const visible = ref(false)
 *   useLockScroll(visible)            // visible 开关自动带锁
 */
export function useLockScroll(
  active: Ref<boolean> | (() => boolean),
  options: { immediate?: boolean } = {},
): void {
  const get = () => (typeof active === 'function' ? active() : active.value)

  if (options.immediate && get()) lockScroll()

  watch(get, (on, was) => {
    if (on && !was) lockScroll()
    else if (!on && was) unlockScroll()
  })

  onUnmounted(() => {
    if (get()) unlockScroll()
  })
}

export default useLockScroll
