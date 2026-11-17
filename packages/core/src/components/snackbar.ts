import { createVNode, reactive, render } from 'vue'
import SnackbarHost from './SnackbarHost.vue'
import { nextZIndex } from '../utils/z-index'

export type SnackbarType = 'normal' | 'success' | 'warning' | 'info' | 'error' | 'loading'
export type SnackbarPosition = 'top' | 'center' | 'bottom'

export interface SnackbarOptions {
  /** 消息内容 */
  content: string
  type?: SnackbarType
  position?: SnackbarPosition
  /** 显示时长 ms；loading 类型默认 0（常驻，需手动 clear） */
  duration?: number
  /** 内容与操作按钮竖排 */
  vertical?: boolean
  /** 操作按钮文字（消息条右侧/下方） */
  action?: string
  /** 点击操作按钮 */
  onAction?: () => void
  /** 禁止穿透点击（loading 默认 true） */
  forbidClick?: boolean
  onClose?: () => void
}

export interface SnackbarHandle {
  clear: () => void
}

export interface SnackbarItem extends Omit<SnackbarOptions, 'action' | 'onAction' | 'onClose' | 'duration'> {
  id: number
  zIndex: number
  duration: number
  action?: string
  onAction?: () => void
  onClose?: () => void
}

export const snackbarState = reactive({
  items: [] as SnackbarItem[],
})

let uid = 0
let multiple = false
let defaults: Partial<SnackbarOptions> = {}

function removeItem(id: number) {
  const idx = snackbarState.items.findIndex((it) => it.id === id)
  if (idx === -1) return
  const it = snackbarState.items[idx]
  snackbarState.items.splice(idx, 1)
  it.onClose?.()
}

function normalize(options: SnackbarOptions | string): SnackbarOptions {
  const opts = typeof options === 'string' ? { content: options } : options
  return { ...defaults, ...opts } as SnackbarOptions
}

function mountHost() {
  if (typeof document === 'undefined' || document.querySelector('[data-jm-snackbar-host]')) return
  const container = document.createElement('div')
  container.setAttribute('data-jm-snackbar-host', '')
  document.body.appendChild(container)
  render(createVNode(SnackbarHost), container)
}

/** 显示消息条，返回带 clear 的实例句柄 */
export function showSnackbar(options: SnackbarOptions | string): SnackbarHandle {
  mountHost()
  const opts = normalize(options)
  const id = ++uid

  // 单例模式：先清掉旧的再开新的
  if (!multiple) snackbarState.items.splice(0).forEach((it) => it.onClose?.())

  const type = opts.type ?? 'normal'
  const item: SnackbarItem = {
    id,
    content: opts.content,
    type,
    position: opts.position ?? 'top',
    duration: opts.duration ?? (type === 'loading' ? 0 : 3000),
    vertical: opts.vertical ?? false,
    forbidClick: opts.forbidClick ?? type === 'loading',
    zIndex: nextZIndex(),
    action: opts.action,
    onAction: opts.onAction,
    onClose: opts.onClose,
  }
  snackbarState.items.push(item)

  if (item.duration > 0) {
    setTimeout(() => removeItem(id), item.duration)
  }

  return { clear: () => removeItem(id) }
}

function withType(type: SnackbarType) {
  return (options: SnackbarOptions | string): SnackbarHandle =>
    showSnackbar({ type, ...(typeof options === 'string' ? { content: options } : options) })
}

/** 关闭当前（单例）或全部（多例）消息条 */
export function clearSnackbar(): void {
  snackbarState.items.splice(0).forEach((it) => it.onClose?.())
}

showSnackbar.success = withType('success')
showSnackbar.warning = withType('warning')
showSnackbar.info = withType('info')
showSnackbar.error = withType('error')
showSnackbar.loading = withType('loading')

/** 是否开启多例模式（默认单例：新消息会顶掉旧消息） */
showSnackbar.allowMultiple = (v: boolean) => {
  multiple = v
}

showSnackbar.setDefaultOptions = (opts: Partial<SnackbarOptions>) => {
  defaults = opts
}

showSnackbar.resetDefaultOptions = () => {
  defaults = {}
}
