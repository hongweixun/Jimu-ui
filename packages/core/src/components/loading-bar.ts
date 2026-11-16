import { createVNode, reactive, render } from 'vue'
import LoadingBarHost from './LoadingBarHost.vue'
import { nextZIndex } from '../utils/z-index'

export interface LoadingBarOptions {
  /** 进度条颜色，默认主色 */
  color?: string
  /** 失败态颜色，默认危险色 */
  errorColor?: string
  /** 高度（px），默认 2 */
  height?: number
  /** 起始进度 0-100 */
  progress?: number
  /** 挂载容器：传了就在容器内绝对定位（手机模拟框、弹层里演示） */
  target?: HTMLElement | null
}

export interface LoadingBarController {
  /** 手动推进到某个进度（0-100），不调则自动朝 94% 收敛 */
  update: (progress: number) => void
  /** 完成：补满到 100% 后淡出 */
  finish: () => void
  /** 失败：变红补满后淡出 */
  error: () => void
  /** 立刻收起并清空状态 */
  destroy: () => void
}

export const loadingBarState = reactive({
  visible: false,
  progress: 0,
  failed: false,
  color: '',
  errorColor: '',
  height: 2,
  inline: false,
  zIndex: 2300,
})

let container: HTMLElement | null = null
let tickTimer: ReturnType<typeof setInterval> | null = null
let hideTimer: ReturnType<typeof setTimeout> | null = null
/** 并发计数：多个请求同时进行时，最后一个结束才收尾 */
let pending = 0

function clamp(v: number) {
  return Math.min(100, Math.max(0, v))
}

function mountHost(target?: HTMLElement | null) {
  if (typeof document === 'undefined') return
  const parent = target ?? document.body

  if (container && container.parentElement === parent) return
  if (container) {
    render(null, container)
    container.remove()
    container = null
  }

  container = document.createElement('div')
  container.setAttribute('data-jm-loading-bar-host', '')
  if (target) {
    container.style.position = 'absolute'
    container.style.top = '0'
    container.style.right = '0'
    container.style.left = '0'
    container.style.pointerEvents = 'none'
  }
  parent.appendChild(container)
  render(createVNode(LoadingBarHost), container)
}

function stopTick() {
  if (tickTimer) {
    clearInterval(tickTimer)
    tickTimer = null
  }
}

function clearHideTimer() {
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
}

/** 假装在加载：越接近 94% 走得越慢，永远不到 100，等 finish 补满 */
function startTick() {
  if (tickTimer) return
  tickTimer = setInterval(() => {
    if (!loadingBarState.visible || loadingBarState.failed) return
    const gap = 94 - loadingBarState.progress
    if (gap <= 0.2) return
    loadingBarState.progress += Math.max(0.5, gap * 0.12)
  }, 120)
}

function hide() {
  clearHideTimer()
  hideTimer = setTimeout(() => {
    loadingBarState.visible = false
    loadingBarState.progress = 0
    loadingBarState.failed = false
    hideTimer = null
  }, 320)
}

/**
 * 顶部加载条（函数式）。
 *
 * ```ts
 * const bar = showLoadingBar()
 * await request()
 * bar.finish()
 * ```
 */
export function showLoadingBar(options: LoadingBarOptions = {}): LoadingBarController {
  const noop: LoadingBarController = {
    update: () => {},
    finish: () => {},
    error: () => {},
    destroy: () => {},
  }
  if (typeof document === 'undefined') return noop

  mountHost(options.target)
  clearHideTimer()
  pending += 1

  loadingBarState.failed = false
  loadingBarState.color = options.color ?? ''
  loadingBarState.errorColor = options.errorColor ?? ''
  loadingBarState.height = options.height ?? loadingBarState.height
  loadingBarState.inline = !!options.target
  loadingBarState.zIndex = nextZIndex(3000)

  if (!loadingBarState.visible) {
    loadingBarState.progress = clamp(options.progress ?? 0)
    loadingBarState.visible = true
  } else if (options.progress !== undefined) {
    loadingBarState.progress = clamp(options.progress)
  }
  startTick()

  let settled = false

  function settle() {
    if (settled) return
    settled = true
    pending = Math.max(0, pending - 1)
    if (pending > 0) return
    stopTick()
    hide()
  }

  return {
    update(progress: number) {
      if (settled) return
      loadingBarState.progress = clamp(progress)
    },
    finish() {
      if (settled) return
      loadingBarState.progress = 100
      settle()
    },
    error() {
      if (settled) return
      loadingBarState.failed = true
      loadingBarState.progress = 100
      settle()
    },
    destroy() {
      settled = true
      pending = 0
      stopTick()
      clearHideTimer()
      loadingBarState.visible = false
      loadingBarState.progress = 0
      loadingBarState.failed = false
    },
  }
}

/** 收起当前加载条（不论并发计数） */
export function hideLoadingBar() {
  pending = 0
  stopTick()
  clearHideTimer()
  loadingBarState.visible = false
  loadingBarState.progress = 0
  loadingBarState.failed = false
}
