import type { App, Plugin } from 'vue'

export const isClient = typeof window !== 'undefined'

export { nextZIndex } from './z-index'

export type SFCWithInstall<T> = T & Plugin

/** 给组件补上 install，支持 app.use(Button) 单独注册 */
export function withInstall<T extends { name?: string }>(comp: T): SFCWithInstall<T> {
  const c = comp as SFCWithInstall<T> & { name?: string }
  c.install = (app: App) => {
    if (c.name) app.component(c.name, comp as never)
  }
  return c
}

/** #00A0E9 + 0.12 → rgba(0,160,233,0.12)，用于自定义颜色时生成浅底 */
export function hexToRgba(hex: string, alpha = 1): string {
  let h = hex.replace('#', '').trim()
  if (h.length === 3) h = h.split('').map((c) => c + c).join('')
  if (h.length !== 6) return hex
  const r = parseInt(h.slice(0, 2), 16)
  const g = parseInt(h.slice(2, 4), 16)
  const b = parseInt(h.slice(4, 6), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

/** 把 8 / '8px' / '50%' 统一成 CSS 长度 */
export function toCssSize(v: number | string | undefined): string | undefined {
  if (v === undefined || v === null || v === '') return undefined
  if (typeof v === 'number') return `${v}px`
  const str = String(v).trim()
  // 纯数字字符串（如模板里写 height="120"）补上 px，否则是非法长度会被浏览器丢弃
  return /^-?\d+(\.\d+)?$/.test(str) ? `${str}px` : str
}

/* ---------------- 滚动锁：多个弹层叠加时不会被提前解锁 ---------------- */
let lockCount = 0
let prevOverflow = ''
let prevPaddingRight = ''
let prevGutter = ''

export function lockScroll(): void {
  if (!isClient) return
  if (lockCount === 0) {
    prevOverflow = document.body.style.overflow
    prevPaddingRight = document.body.style.paddingRight
    prevGutter = document.documentElement.style.scrollbarGutter
    /* 先量：滚动条是否真的占了宽度（经典滚动条会占，Win11/Edge 的悬浮式不占）。
       悬浮式页面若设 scrollbar-gutter:stable 会凭空挤出一条槽位，
       整页内容变窄、居中的手机框向左跳——所以 gap 为 0 时什么都不补。 */
    const gap = window.innerWidth - document.documentElement.clientWidth
    const supportsGutter = 'scrollbarGutter' in document.documentElement.style
    document.body.style.overflow = 'hidden'
    if (gap > 0) {
      if (supportsGutter) {
        document.documentElement.style.scrollbarGutter = 'stable'
      } else {
        /* 旧浏览器回退：把滚动条宽度补成 body 的 padding-right */
        document.body.style.paddingRight = `${gap}px`
      }
    }
  }
  lockCount += 1
}

export function unlockScroll(): void {
  if (!isClient) return
  lockCount = Math.max(0, lockCount - 1)
  if (lockCount === 0) {
    document.body.style.overflow = prevOverflow
    document.body.style.paddingRight = prevPaddingRight
    if (prevGutter) document.documentElement.style.scrollbarGutter = prevGutter
    else if ('scrollbarGutter' in document.documentElement.style) {
      document.documentElement.style.removeProperty('scrollbar-gutter')
    }
    prevGutter = ''
  }
}
