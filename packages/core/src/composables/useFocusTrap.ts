import { onScopeDispose } from 'vue'

/**
 * 焦点陷阱
 * ---------------------------------------------------------------------------
 * 模态弹层打开后，键盘用户按 Tab 不应该跑到背后的页面上。
 * 做法：打开时记住触发元素 → 把焦点移进面板 → Tab / Shift+Tab 在面板内首尾循环 →
 * 关闭时把焦点还给触发元素（否则焦点掉到 body，屏幕阅读器从文档开头重新读）。
 *
 * 只处理键盘，不吞鼠标：点击面板外仍然是各组件自己的遮罩逻辑。
 */

const FOCUSABLE = [
  'a[href]',
  'area[href]',
  'button:not([disabled])',
  'input:not([disabled]):not([type="hidden"])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  'iframe',
  'audio[controls]',
  'video[controls]',
  '[contenteditable="true"]',
  '[tabindex]:not([tabindex="-1"])',
].join(',')

/** 元素是否真的可见（display:none / visibility:hidden / 尺寸为 0 都排除） */
function isVisible(el: HTMLElement): boolean {
  if (el.hidden) return false
  const style = window.getComputedStyle(el)
  if (style.display === 'none' || style.visibility === 'hidden') return false
  return el.getClientRects().length > 0
}

export interface FocusTrapOptions {
  /** 打开后优先聚焦的元素；不传则聚焦面板内第一个可聚焦元素，再退化为面板本身 */
  initialFocus?: () => HTMLElement | null | undefined
  /** 关闭时是否把焦点还给打开前的元素，默认 true */
  returnFocus?: boolean
}

export function useFocusTrap() {
  let container: HTMLElement | null = null
  let previous: HTMLElement | null = null
  let active = false

  function focusables(): HTMLElement[] {
    if (!container) return []
    return Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE)).filter(isVisible)
  }

  function focusSafely(el: HTMLElement | null | undefined) {
    if (!el || typeof el.focus !== 'function') return
    try {
      el.focus({ preventScroll: true })
    } catch {
      el.focus()
    }
  }

  function onKeydown(e: KeyboardEvent) {
    if (!active || e.key !== 'Tab' || !container) return
    const list = focusables()

    /* 面板里一个可聚焦元素都没有（纯文本弹窗）：把 Tab 锁在面板上，
       否则焦点会跑到背景页面，屏幕阅读器就"离开"了弹窗 */
    if (!list.length) {
      e.preventDefault()
      focusSafely(container)
      return
    }

    const first = list[0]
    const last = list[list.length - 1]
    const current = document.activeElement as HTMLElement | null
    const inside = !!current && container.contains(current)

    if (e.shiftKey) {
      if (!inside || current === first) {
        e.preventDefault()
        focusSafely(last)
      }
    } else if (!inside || current === last) {
      e.preventDefault()
      focusSafely(first)
    }
  }

  /** 打开弹层时调用：传入面板根节点（需要能接收焦点，模板里给 tabindex="-1"） */
  function activate(el: HTMLElement | null | undefined, options: FocusTrapOptions = {}) {
    if (!el || active) return
    container = el
    previous = (document.activeElement as HTMLElement | null) ?? null
    active = true
    document.addEventListener('keydown', onKeydown, true)

    const preferred = options.initialFocus?.()
    const list = focusables()
    // 默认聚焦第一个可聚焦元素（通常是关闭/主按钮），纯文本弹窗聚焦面板本身
    focusSafely(preferred ?? list[0] ?? el)
  }

  /** 关闭弹层时调用：解绑并把焦点还给触发元素 */
  function deactivate(options: FocusTrapOptions = {}) {
    if (!active) return
    active = false
    document.removeEventListener('keydown', onKeydown, true)
    const back = previous
    container = null
    previous = null
    if (options.returnFocus === false) return
    // 触发元素可能已被销毁（列表项删除等），只还给它还在文档里的时候
    if (back && document.contains(back)) focusSafely(back)
  }

  /* 组件被卸载时兜底解绑，避免 document 上残留监听 */
  onScopeDispose(() => {
    if (!active) return
    active = false
    document.removeEventListener('keydown', onKeydown, true)
    container = null
    previous = null
  })

  return {
    activate,
    deactivate,
    /** 当前陷阱是否生效（调试 / 探针用） */
    isActive: () => active,
  }
}
