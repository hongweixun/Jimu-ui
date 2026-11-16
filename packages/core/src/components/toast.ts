import { createVNode, reactive, render } from 'vue'
import ToastHost from './ToastHost.vue'
import { nextZIndex } from '../utils/z-index'

export type ToastType = 'text' | 'success' | 'fail' | 'loading'
export type ToastPosition = 'top' | 'middle' | 'bottom'

export interface ToastOptions {
  message: string
  type?: ToastType
  duration?: number
  position?: ToastPosition
  mask?: boolean
  /** 自定义图标名（内置图标），会替代 type 对应的图标 */
  icon?: string
  /** 点击提示本身即关闭 */
  closeOnClick?: boolean
  /** 关闭时回调（自动消失、手动关闭、被新提示顶掉都会触发） */
  onClose?: () => void
  /** 指定挂载容器，提示会限制在这个容器内显示（嵌入弹窗、模拟框时很有用） */
  target?: HTMLElement | null
}

export const toastState = reactive({
  visible: false,
  message: '',
  type: 'text' as ToastType,
  position: 'middle' as ToastPosition,
  mask: false,
  icon: '',
  closeOnClick: false,
  inline: false,
  zIndex: 2000,
  onClose: undefined as (() => void) | undefined,
})

let timer: ReturnType<typeof setTimeout> | null = null
let container: HTMLElement | null = null

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
  container.setAttribute('data-jm-toast-host', '')
  if (target) {
    container.style.position = 'absolute'
    container.style.top = '0'
    container.style.right = '0'
    container.style.bottom = '0'
    container.style.left = '0'
    container.style.pointerEvents = 'none'
  }
  parent.appendChild(container)
  render(createVNode(ToastHost), container)
}

export function closeToast(): void {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
  const wasVisible = toastState.visible
  const onClose = toastState.onClose
  toastState.visible = false
  toastState.onClose = undefined
  if (wasVisible && onClose) onClose()
}

export function showToast(options: ToastOptions | string): void {
  const opts: ToastOptions = typeof options === 'string' ? { message: options } : options

  mountHost(opts.target)
  closeToast()

  toastState.inline = !!opts.target
  toastState.message = opts.message
  toastState.type = opts.type ?? 'text'
  toastState.position = opts.position ?? 'middle'
  toastState.mask = opts.mask ?? false
  toastState.icon = opts.icon ?? ''
  toastState.closeOnClick = opts.closeOnClick ?? false
  toastState.onClose = opts.onClose
  toastState.zIndex = nextZIndex()
  toastState.visible = true

  // loading 默认常驻，业务处理完自己 closeToast()
  const duration = opts.duration ?? (toastState.type === 'loading' ? 0 : 2000)
  if (duration > 0) timer = setTimeout(closeToast, duration)
}
