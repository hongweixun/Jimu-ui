import type { Directive, DirectiveBinding } from 'vue'
import { showSnackbar } from '../components/snackbar'

/**
 * 复制指令（v-copy）
 * ---------------------------------------------------------------------------
 * 点击宿主元素把文本复制进剪贴板。移动端典型场景：复制订单号、邀请码、
 * 卡号——用户通常不知道系统输入框可以长按全选，"点一下就复制"是最省事的交互。
 *
 * 实现策略（多一层降级）：
 *   1. navigator.clipboard.writeText —— 现代浏览器首选，但只在安全上下文可用；
 *   2. textarea + document.execCommand('copy') —— 老设备 / 非安全上下文兜底，
 *      需要把 textarea 挪到视口外再选中，复制完立刻移除（不闪屏、不抢焦点滚动）。
 *
 * 反馈：剪贴板用户看不见，复制成功默认弹一条「复制成功」消息条（feedback 关闭
 * 或传自定义文案可覆盖）；没有任何反馈用户根本不知道复制成没成功。
 *
 * 文本在触发时取值（binding.value 可以是字符串或返回字符串的函数），
 * 保证复制到的是点击那一刻的最新内容。
 */

export interface CopyOptions {
  /** 要复制的文本；传函数则点击时求值（动态内容推荐） */
  text: string | (() => string)
  /**
   * 复制成功提示：默认 true 弹「复制成功」消息条；
   * 传字符串自定义文案；传 false 关闭（完全自己接管，比如用 onSuccess）
   */
  feedback?: boolean | string
  /** 复制成功回调 */
  onSuccess?: (text: string) => void
  /** 复制失败回调（极少出现：非安全上下文 + execCommand 也被禁时） */
  onError?: (reason: unknown) => void
}

type CopyValue = string | CopyOptions

function normalize(value: CopyValue | undefined | null): CopyOptions {
  if (typeof value === 'string' || typeof value === 'function') {
    return { text: value }
  }
  return value ?? { text: '' }
}

async function writeClipboard(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }
  throw new Error('clipboard unavailable')
}

function fallbackCopy(text: string): boolean {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  textarea.style.top = '0'
  document.body.appendChild(textarea)
  textarea.select()
  textarea.setSelectionRange(0, text.length)
  let ok = false
  try {
    ok = document.execCommand('copy')
  } catch {
    ok = false
  }
  textarea.remove()
  return ok
}

type CopyHost = HTMLElement & { __jmCopy?: (e: Event) => void }

async function doCopy(el: HTMLElement, options: CopyOptions, event: Event) {
  const text = typeof options.text === 'function' ? options.text() : options.text
  if (!text) {
    options.onError?.(new Error('empty text'))
    return
  }
  try {
    await writeClipboard(text)
    if (options.feedback !== false) {
      showSnackbar({
        content: typeof options.feedback === 'string' ? options.feedback : '复制成功',
        duration: 1500,
      })
    }
    options.onSuccess?.(text)
  } catch (err) {
    if (fallbackCopy(text)) {
      if (options.feedback !== false) {
        showSnackbar({
          content: typeof options.feedback === 'string' ? options.feedback : '复制成功',
          duration: 1500,
        })
      }
      options.onSuccess?.(text)
    } else {
      if (!options.onError && options.feedback !== false) {
        showSnackbar({ content: '复制失败，请长按手动复制', duration: 2000 })
      }
      options.onError?.(err)
    }
  }
}

/**
 * v-copy 指令
 *   <div v-copy="'JM20261116001'">点我复制</div>
 *   <div v-copy="{ text: () => orderNo, onSuccess: tip }">动态复制</div>
 */
export const vCopy: Directive<CopyHost, CopyValue | undefined | null> = {
  mounted(el: CopyHost, binding) {
    const handler = (e: Event) => doCopy(el, normalize(binding.value), e)
    el.__jmCopy = handler
    el.addEventListener('click', handler)
    /* 可访问性：让 div 宿主可被键盘触发 */
    if (el.tagName !== 'BUTTON' && el.tagName !== 'A' && !el.hasAttribute('tabindex')) {
      el.setAttribute('tabindex', '0')
      el.setAttribute('role', 'button')
    }
  },
  beforeUnmount(el: CopyHost) {
    if (el.__jmCopy) el.removeEventListener('click', el.__jmCopy)
    delete el.__jmCopy
  },
}

export default vCopy
