/**
 * 防抖 / 节流（useDebounceFn / useThrottleFn）
 * ---------------------------------------------------------------------------
 * 搜索框输入联想、resize 重排、滚动加载的标配。和手写 setTimeout 比多了两件事：
 *   1. 自动清理 —— 组件卸载时取消 pending 调用，不会在已销毁的回调里碰 DOM；
 *   2. 可控取消 —— 返回 cancel()/flush()，切页面前把最后一次真正刷出去。
 *
 * useDebounceFn：连续触发只在停止后 trailing 一次（搜索联想要"最终值"）。
 * useThrottleFn：固定频率放行（滚动加载要"过程中的采样"），leading 默认开——
 *   用户滚动第一屏就该出结果，不用等第一个间隔。
 */

import { onUnmounted } from 'vue'

export interface UseDebounceFnOptions {
  /** 延迟毫秒，默认 300 */
  delay?: number
  /** 是否同时触发 leading（开始时立刻执行一次），默认 false */
  leading?: boolean
}

export interface PausableFn<T extends (...args: never[]) => unknown> {
  (...args: Parameters<T>): void
  /** 取消 pending 调用 */
  cancel: () => void
  /** 立刻执行 pending 的调用（有 pending 才执行） */
  flush: () => void
}

export interface UseThrottleFnOptions {
  /** 间隔毫秒，默认 200 */
  interval?: number
  /** 间隔开头放行，默认 true */
  leading?: boolean
  /** 间隔结尾补一次（保证最后一拍不丢），默认 true */
  trailing?: boolean
}

type AnyFn = (...args: unknown[]) => unknown

export function useDebounceFn<T extends AnyFn>(
  fn: T,
  options: UseDebounceFnOptions | number = {},
): PausableFn<T> {
  const opts = typeof options === 'number' ? { delay: options } : options
  const delay = opts.delay ?? 300
  const leading = opts.leading ?? false

  let timer: number | null = null
  let pendingArgs: Parameters<T> | null = null
  let firstCall = true

  function cancel() {
    if (timer !== null) {
      window.clearTimeout(timer)
      timer = null
    }
    pendingArgs = null
    firstCall = true
  }

  function flush() {
    if (timer === null || pendingArgs === null) return
    window.clearTimeout(timer)
    timer = null
    const args = pendingArgs
    pendingArgs = null
    firstCall = true
    fn(...args)
  }

  const wrapped = (...args: Parameters<T>) => {
    pendingArgs = args
    if (timer !== null) window.clearTimeout(timer)
    if (leading && firstCall) {
      firstCall = false
      fn(...args)
      pendingArgs = null
      /* leading 已执行，本次等待期内的后续触发再进 trailing */
    }
    timer = window.setTimeout(() => {
      timer = null
      const call = pendingArgs
      pendingArgs = null
      firstCall = true
      if (call) fn(...call)
    }, delay)
  }

  onUnmounted(cancel)

  return Object.assign(wrapped, { cancel, flush })
}

export function useThrottleFn<T extends AnyFn>(
  fn: T,
  options: UseThrottleFnOptions | number = {},
): PausableFn<T> {
  const opts = typeof options === 'number' ? { interval: options } : options
  const interval = opts.interval ?? 200
  const leading = opts.leading ?? true
  const trailing = opts.trailing ?? true

  let lastExec = 0
  let timer: number | null = null
  let pendingArgs: Parameters<T> | null = null

  function invoke(args: Parameters<T>) {
    lastExec = Date.now()
    fn(...args)
  }

  function cancel() {
    if (timer !== null) {
      window.clearTimeout(timer)
      timer = null
    }
    pendingArgs = null
  }

  function flush() {
    if (pendingArgs === null) return
    const args = pendingArgs
    cancel()
    invoke(args)
  }

  const wrapped = (...args: Parameters<T>) => {
    pendingArgs = args
    const now = Date.now()
    const elapsed = now - lastExec

    /* leading：间隔开头立即放行 */
    if (leading && elapsed >= interval) {
      cancel()
      invoke(args)
      return
    }
    /* trailing：把最后一拍补在间隔末尾；leading=false 时第一次也要等满一个间隔 */
    if (trailing) {
      if (timer !== null) window.clearTimeout(timer)
      const wait = elapsed >= interval ? (leading ? 0 : interval) : interval - elapsed
      timer = window.setTimeout(() => {
        timer = null
        const call = pendingArgs
        pendingArgs = null
        if (call) invoke(call)
      }, wait)
    }
  }

  onUnmounted(cancel)

  return Object.assign(wrapped, { cancel, flush })
}
