import type { Directive, DirectiveBinding } from 'vue'
import { useIntersection, type UseIntersectionOptions } from '../composables/useIntersection'

/**
 * 懒加载指令（v-lazy）
 * ---------------------------------------------------------------------------
 * 元素滚进视口（提前 200px）才真正加载，首屏只请求看得见的图。
 *
 * 两种用法：
 *   1. 图片：v-lazy="'https://…'" 或对象形式，进入视口后写入 src
 *      （元素是 IMG 就设 src，否则设 background-image）
 *   2. 通用：v-lazy="{ onVisible }"，进入视口时回调，内容自行接管
 *
 * 加载前宿主保持透明占位（不抽走 DOM，避免布局跳动），
 * IMG 加载成功后淡入；失败的占位标记 is-error 供宿主自定义兜底。
 */

export interface LazyOptions extends UseIntersectionOptions {
  /** 图片地址（IMG 设 src，其他元素设 background-image） */
  src?: string
  /** 加载完成的回调（真实图片 load 后触发） */
  onLoad?: () => void
  /** 图片加载失败回调 */
  onError?: (event: Event) => void
  /** 进入视口回调（通用懒加载入口） */
  onVisible?: () => void
}

const VISIBLE_CLASS = 'jm-lazy-visible'
const ERROR_CLASS = 'jm-lazy-error'

function normalize(value: LazyOptions | string | undefined | null): LazyOptions {
  if (typeof value === 'string') return { src: value }
  return value ?? {}
}

type LazyHost = HTMLElement & { __jmLazy?: { stop: () => void } }

/* 样式只注入一次 */
const STYLE_ID = 'jm-lazy-style'
function ensureStyle() {
  if (document.getElementById(STYLE_ID)) return
  const style = document.createElement('style')
  style.id = STYLE_ID
  style.textContent = `
    [data-jm-lazy] { opacity: 0; transition: opacity .3s ease; }
    [data-jm-lazy].${VISIBLE_CLASS} { opacity: 1; }
  `
  document.head.appendChild(style)
}

function loadImage(el: LazyHost, options: LazyOptions, src: string) {
  if (el.tagName === 'IMG') {
    const img = el as HTMLImageElement
    img.addEventListener(
      'load',
      () => {
        el.classList.add(VISIBLE_CLASS)
        options.onLoad?.()
      },
      { once: true },
    )
    img.addEventListener(
      'error',
      (e) => {
        el.classList.add(ERROR_CLASS)
        el.classList.add(VISIBLE_CLASS)
        options.onError?.(e)
      },
      { once: true },
    )
    img.src = src
  } else {
    el.style.backgroundImage = `url("${src}")`
    const probe = new Image()
    probe.onload = () => {
      el.classList.add(VISIBLE_CLASS)
      options.onLoad?.()
    }
    probe.onerror = (e) => {
      el.classList.add(ERROR_CLASS)
      el.classList.add(VISIBLE_CLASS)
      options.onError?.(e as Event)
    }
    probe.src = src
  }
}

/**
 * v-lazy 指令
 *   <img v-lazy="'https://cdn…/a.jpg'" alt="…" />
 *   <div v-lazy="{ src: '…', margin: '400px' }" class="poster" />
 *   <div v-lazy="{ onVisible: loadComments }">评论区</div>
 */
export const vLazy: Directive<LazyHost, LazyOptions | string | undefined | null> = {
  mounted(el: LazyHost, binding) {
    const options = normalize(binding.value)
    if (!options.src && !options.onVisible) return
    ensureStyle()
    el.setAttribute('data-jm-lazy', '')

    const { stop } = useIntersection(() => el, {
      once: options.once ?? true,
      margin: options.margin,
      threshold: options.threshold,
      root: options.root,
      onEnter: () => {
        if (options.src) loadImage(el, options, options.src)
        options.onVisible?.()
      },
    })
    el.__jmLazy = { stop }
  },
  updated(el: LazyHost, binding) {
    /* 值更新且已可见时，直接用新地址换图（例如列表复用节点） */
    const options = normalize(binding.value)
    const host = el as LazyHost
    if (options.src && host.__jmLazy && el.classList.contains(VISIBLE_CLASS)) {
      if (el.tagName === 'IMG') {
        const img = el as HTMLImageElement
        if (img.src !== options.src) img.src = options.src
      }
    }
  },
  beforeUnmount(el: LazyHost) {
    el.__jmLazy?.stop()
    delete el.__jmLazy
  },
}

export default vLazy
