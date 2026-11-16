import { onUnmounted, ref, toValue, type MaybeRefOrGetter, type Ref } from 'vue'

/**
 * 进入视口检测（useIntersection）
 * ---------------------------------------------------------------------------
 * IntersectionObserver 的薄封装：进入视口（默认只关心"第一次"）后置位。
 * 懒加载（v-lazy）、曝光埋点、"滚到评论区才加载评论"都靠它。
 *
 * 设计取舍：
 *   - 默认 once：懒加载和曝光埋点 95% 只需要触发一次，进入过就不撤销，
 *     避免网络图加载完成前元素因布局抖动短暂离开视口导致重复触发。
 *   - 默认 rootMargin '200px'：提前 200px 预加载，用户滚到的时候图已经在了。
 *   - SSR 安全：无 window 时直接报"已可见"，内容不会被永远藏住。
 */

export interface UseIntersectionOptions {
  /** 只触发一次（进入过就算），默认 true */
  once?: boolean
  /** 提前量，同 IntersectionObserver rootMargin，默认 '200px' */
  margin?: string
  /** 相交比例阈值，默认 0 */
  threshold?: number
  /** 观察的滚动容器，默认视口 */
  root?: Element | null
  /** 进入视口回调 */
  onEnter?: () => void
}

export interface UseIntersectionReturn {
  /** 是否已进入视口（once 模式下进入后永久为 true） */
  visible: Ref<boolean>
  /** 当前是否正在视口内（once 模式下与 visible 等价） */
  stop: () => void
}

export function useIntersection(
  target: MaybeRefOrGetter<Element | null | undefined>,
  options: UseIntersectionOptions = {},
): UseIntersectionReturn {
  const { once = true, margin = '200px', threshold = 0, root = null, onEnter } = options
  const visible = ref(false)
  let observer: IntersectionObserver | null = null

  function setup() {
    const el = toValue(target)
    if (!el) return
    if (typeof IntersectionObserver === 'undefined') {
      /* 极老环境：直接当已可见，别把内容藏死 */
      visible.value = true
      onEnter?.()
      return
    }
    observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0]
        if (!entry?.isIntersecting) return
        visible.value = true
        onEnter?.()
        if (once) stop()
      },
      { root, rootMargin: margin, threshold },
    )
    observer.observe(el)
  }

  function stop() {
    observer?.disconnect()
    observer = null
  }

  setup()
  onUnmounted(stop)

  return { visible, stop }
}

export default useIntersection
