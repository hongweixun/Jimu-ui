import { computed, onUnmounted, ref, type Ref } from 'vue'

/**
 * 倒计时（useCountDown）
 * ---------------------------------------------------------------------------
 * 验证码按钮（"60s 后重发"）、秒杀、考试计时都长这样：一个不断递减的数字 +
 * 开始 / 暂停 / 结束。和 setTimeout 数格子比，时间戳驱动有个关键优势：
 * 后台标签页被浏览器降频节流后，回来时读的是真实剩余时间，不会越走越慢。
 *
 * 设计：
 *   - 对外暴露"剩余秒数"而不是毫秒——移动端场景几乎全是秒级文案，
 *     要毫秒精度直接读 remainingMs。
 *   - formatted 默认 mm:ss（差旅计时/秒杀风格），验证码传 format 接管。
 *   - pause/resume 用真实剩余时间做锚点，暂停多久都不会多扣。
 */

export interface UseCountDownOptions {
  /** 归零回调 */
  onFinish?: () => void
  /** 格式化输出，默认 mm:ss（两位数补零，分钟不封顶） */
  format?: (seconds: number) => string
  /** 校准间隔（ms），默认 250——足够顺滑又不会频繁重排 */
  interval?: number
}

export interface UseCountDownReturn {
  /** 剩余秒数（向上取整：剩 0.4s 显示 1，不会提前跳 0） */
  remaining: Ref<number>
  /** 剩余毫秒 */
  remainingMs: Ref<number>
  /** 是否在倒数 */
  running: Ref<boolean>
  /** 格式化后的文案，默认 mm:ss */
  formatted: Ref<string>
  /** 开始/重新开始，可传入新的总秒数（默认沿用上次） */
  start: (seconds?: number) => void
  pause: () => void
  resume: () => void
  /** 归零并停止 */
  stop: () => void
}

function pad(n: number): string {
  return n < 10 ? `0${n}` : String(n)
}

export function useCountDown(
  total = 60,
  options: UseCountDownOptions = {},
): UseCountDownReturn {
  const { onFinish, interval = 250 } = options
  const format = options.format ?? ((s: number) => `${pad(Math.floor(s / 60))}:${pad(s % 60)}`)

  const remainingMs = ref(0)
  const running = ref(false)
  let totalMs = total * 1000
  /* 暂停/节流恢复的锚点：真实剩余时间 = deadline - now */
  let deadline = 0
  let timer: number | null = null

  const remaining = computed(() => Math.ceil(remainingMs.value / 1000))
  const formatted = computed(() => format(remaining.value))

  function tick() {
    const left = Math.max(0, deadline - Date.now())
    remainingMs.value = left
    if (left <= 0) {
      stopTimer()
      running.value = false
      onFinish?.()
    }
  }

  function stopTimer() {
    if (timer !== null) {
      window.clearInterval(timer)
      timer = null
    }
  }

  function start(seconds?: number) {
    if (typeof seconds === 'number') totalMs = Math.max(0, seconds * 1000)
    stopTimer()
    remainingMs.value = totalMs
    deadline = Date.now() + totalMs
    running.value = true
    if (totalMs > 0) timer = window.setInterval(tick, interval)
    tick()
  }

  function pause() {
    if (!running.value) return
    stopTimer()
    remainingMs.value = Math.max(0, deadline - Date.now())
    running.value = false
  }

  function resume() {
    if (running.value || remainingMs.value <= 0) return
    deadline = Date.now() + remainingMs.value
    running.value = true
    timer = window.setInterval(tick, interval)
  }

  function stop() {
    stopTimer()
    running.value = false
    remainingMs.value = 0
  }

  onUnmounted(stopTimer)

  return { remaining, remainingMs, running, formatted, start, pause, resume, stop }
}

export default useCountDown
