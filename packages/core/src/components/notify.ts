import { createVNode, reactive, render } from 'vue'
import NotifyHost from './NotifyHost.vue'

export type NotifyType = 'primary' | 'success' | 'warning' | 'danger'

export interface NotifyOptions {
  message?: string
  title?: string
  type?: NotifyType
  duration?: number
  color?: string
  background?: string
  icon?: string
  closeable?: boolean
  safeAreaInsetTop?: boolean
  /** 最多同时显示几条，超出时顶掉最早的一条 */
  max?: number
  /** 指定挂载容器，通知会限制在这个容器内显示（嵌入弹窗、手机模拟框时很有用） */
  target?: HTMLElement | null
  onClick?: (event: MouseEvent) => void
  onClose?: () => void
}

export interface NotifyItem extends NotifyOptions {
  id: number
}

/** 宿主渲染的队列：函数式调用的唯一数据源 */
export const notifyState = reactive({
  items: [] as NotifyItem[],
  /** 挂在自定义容器里时为 true，宿主改成绝对定位 */
  inline: false,
})

let seed = 0
let container: HTMLElement | null = null

/** 容器换了（target 变化）就重建宿主，否则复用 */
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
  container.setAttribute('data-jm-notify-host', '')
  if (target) {
    container.style.position = 'absolute'
    container.style.top = '0'
    container.style.right = '0'
    container.style.bottom = '0'
    container.style.left = '0'
    container.style.pointerEvents = 'none'
  }
  parent.appendChild(container)
  render(createVNode(NotifyHost), container)
  notifyState.inline = !!target
}

/** 关闭单条；不传 id 则清空全部 */
export function closeNotify(id?: number): void {
  if (id === undefined) {
    notifyState.items = []
    return
  }
  notifyState.items = notifyState.items.filter((item) => item.id !== id)
}

/** 顶部消息通知，返回本次的 id，可用于提前关闭 */
export function showNotify(options: NotifyOptions | string): number {
  const opts: NotifyOptions = typeof options === 'string' ? { message: options } : options
  mountHost(opts.target)
  // 同一条文案反复触发时不重复堆叠，只把旧的那条刷掉
  if (opts.message) {
    notifyState.items = notifyState.items.filter((item) => item.message !== opts.message)
  }

  const id = ++seed
  notifyState.items.push({ ...opts, id })

  const max = Math.max(1, opts.max ?? 3)
  if (notifyState.items.length > max) {
    notifyState.items = notifyState.items.slice(-max)
  }

  return id
}
