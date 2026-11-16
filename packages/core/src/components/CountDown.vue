<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import type { CountDownTimeData } from '../types'

defineOptions({ name: 'JmCountDown' })

const props = withDefaults(
  defineProps<{
    /** 剩余毫秒数 */
    time?: number
    /** DD 天 / HH 时 / mm 分 / ss 秒 / S 毫秒 */
    format?: string
    autoStart?: boolean
    /** 显示毫秒：开启后按帧刷新 */
    millisecond?: boolean
  }>(),
  {
    time: 0,
    format: 'HH:mm:ss',
    autoStart: true,
    millisecond: false,
  },
)

const emit = defineEmits<{ change: [data: CountDownTimeData]; finish: [] }>()

const pad = (n: number, len = 2) => String(Math.max(0, n)).padStart(len, '0')

const remain = ref(Math.max(0, props.time))
const running = ref(false)
let raf = 0
let timer: ReturnType<typeof setInterval> | null = null
let finished = false
let lastEmitSec = -1

const timeData = computed<CountDownTimeData>(() => {
  const total = Math.max(0, remain.value)
  return {
    total,
    days: Math.floor(total / 86400000),
    hours: Math.floor(total / 3600000) % 24,
    minutes: Math.floor(total / 60000) % 60,
    seconds: Math.floor(total / 1000) % 60,
    milliseconds: Math.floor(total % 1000),
  }
})

/** 把 format 拆成「数字令牌 + 字面量」片段，渲染时分别套样式 */
const segments = computed(() => {
  const map: Record<string, string> = {
    DD: pad(timeData.value.days, 2),
    HH: pad(timeData.value.hours),
    mm: pad(timeData.value.minutes),
    ss: pad(timeData.value.seconds),
    S: pad(timeData.value.milliseconds, 3),
  }
  const out: { token: string | null; text: string }[] = []
  const re = /DD|HH|mm|ss|S/g
  let cursor = 0
  let m: RegExpExecArray | null
  while ((m = re.exec(props.format))) {
    if (m.index > cursor) out.push({ token: null, text: props.format.slice(cursor, m.index) })
    out.push({ token: m[0], text: map[m[0]] ?? '' })
    cursor = m.index + m[0].length
  }
  if (cursor < props.format.length) out.push({ token: null, text: props.format.slice(cursor) })
  return out
})

function emitChange() {
  const d = timeData.value
  // 秒级组件不用每帧都通知外部
  if (!props.millisecond && Math.floor(d.total / 1000) === lastEmitSec) return
  lastEmitSec = Math.floor(d.total / 1000)
  emit('change', d)
}

function stop() {
  running.value = false
  if (raf) {
    cancelAnimationFrame(raf)
    raf = 0
  }
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function tick() {
  if (!running.value) return
  const now = performance.now()
  remain.value = Math.max(0, endAt - now)
  emitChange()
  if (remain.value <= 0) {
    stop()
    if (!finished) {
      finished = true
      emit('finish')
    }
    return
  }
  if (props.millisecond) raf = requestAnimationFrame(tick)
}

let endAt = 0

function start() {
  if (remain.value <= 0) return
  stop()
  finished = false
  endAt = performance.now() + remain.value
  running.value = true
  if (props.millisecond) {
    raf = requestAnimationFrame(tick)
  } else {
    // 50ms 一检，秒数变化才算准时，但不会因为定时器漂移而跑偏
    timer = setInterval(tick, 50)
  }
}

function pause() {
  if (!running.value) return
  stop()
}

function reset(next?: number) {
  stop()
  remain.value = Math.max(0, next ?? props.time)
  finished = false
  lastEmitSec = -1
  emitChange()
  if (props.autoStart) start()
}

watch(
  () => props.time,
  (v) => reset(v),
)

watch(
  () => props.millisecond,
  () => {
    if (running.value) start()
  },
)

onMounted(() => {
  if (props.autoStart) start()
})

onBeforeUnmount(stop)

defineExpose({ start, pause, reset, timeData })
</script>

<template>
  <span class="jm-count-down" role="timer" aria-live="off">
    <slot v-bind="{ timeData }">
      <template v-for="(seg, i) in segments" :key="i">
        <span v-if="seg.token" class="jm-count-down__num">{{ seg.text }}</span>
        <span v-else class="jm-count-down__char">{{ seg.text }}</span>
      </template>
    </slot>
  </span>
</template>

<style>
.jm-count-down {
  display: inline-flex;
  align-items: baseline;
  font-family: var(--jm-font-family-number), var(--jm-font-family);
  font-variant-numeric: tabular-nums;
  color: var(--jm-text-color);
}

.jm-count-down__num {
  display: inline-block;
  min-width: 1.1em;
  text-align: center;
  font-weight: var(--jm-font-weight-medium);
}

.jm-count-down__char {
  padding: 0 1px;
  color: var(--jm-text-color-2);
}
</style>
