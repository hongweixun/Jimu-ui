<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

defineOptions({ name: 'JmStatistic' })

const props = withDefaults(
  defineProps<{
    /** 标题 */
    title?: string
    /** 数值：数字会滚动动画，非数字（如 '—'）原样展示 */
    value?: number | string
    /** 小数位，默认按 value 的小数位推断 */
    precision?: number
    /** 千分位分隔 */
    separator?: boolean
    /** 千分位符号 */
    groupSeparator?: string
    /** 小数点符号 */
    decimalSeparator?: string
    /** 前缀文字（如 ¥） */
    prefix?: string
    /** 后缀文字（如 元 / 分） */
    suffix?: string
    /** 数字滚动时长（ms），0 表示不做动画 */
    duration?: number
    /** 字号 */
    size?: 'sm' | 'md' | 'lg'
    /** 数值颜色 */
    color?: string
  }>(),
  {
    separator: true,
    groupSeparator: ',',
    decimalSeparator: '.',
    duration: 900,
    size: 'md',
  },
)

/** 把 value 归一成数字；不能归一则返回 null（走原样展示） */
const numeric = computed<number | null>(() => {
  const v = props.value
  if (typeof v === 'number') return Number.isFinite(v) ? v : null
  if (typeof v === 'string') {
    const trimmed = v.replace(/[,\s]/g, '')
    if (trimmed !== '' && !Number.isNaN(Number(trimmed))) return Number(trimmed)
  }
  return null
})

const precisionValue = computed(() => {
  if (props.precision !== undefined) return Math.max(0, Math.min(6, props.precision))
  const v = props.value
  if (typeof v === 'number') {
    const s = String(v)
    const dot = s.indexOf('.')
    return dot === -1 ? 0 : Math.min(6, s.length - dot - 1)
  }
  return 0
})

const display = ref(0)
let raf = 0
let startTime = 0
let from = 0

function stop() {
  if (raf) cancelAnimationFrame(raf)
  raf = 0
}

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

function animateTo(target: number) {
  stop()
  const duration = props.duration
  if (!duration || duration <= 0 || prefersReducedMotion()) {
    display.value = target
    return
  }
  from = display.value
  startTime = 0
  const delta = target - from
  if (delta === 0) return

  const step = (ts: number) => {
    // 首帧只记时间，保证从 0 开始计时（rAF 时间戳可能早于首次绘制）
    if (!startTime) startTime = ts
    const p = Math.min(1, (ts - startTime) / duration)
    // easeOutCubic：先快后慢，像仪表盘落位
    display.value = from + delta * (1 - Math.pow(1 - p, 3))
    if (p < 1) {
      raf = requestAnimationFrame(step)
    } else {
      display.value = target
      raf = 0
    }
  }
  raf = requestAnimationFrame(step)
}

function formatNumber(n: number) {
  const p = precisionValue.value
  const fixed = Math.abs(n).toFixed(p)
  const [int, dec] = fixed.split('.')
  const grouped = props.separator
    ? int.replace(/\B(?=(\d{3})+(?!\d))/g, props.groupSeparator)
    : int
  return `${n < 0 ? '-' : ''}${grouped}${p > 0 ? props.decimalSeparator + dec : ''}`
}

const text = computed(() => {
  if (numeric.value === null) {
    return props.value === undefined || props.value === null ? '' : String(props.value)
  }
  // 注意：渲染的是动画中的 display，而不是目标值，否则滚动动画会被直接跳过
  return formatNumber(display.value)
})

onMounted(() => {
  const n = numeric.value
  if (n === null) return
  display.value = 0
  animateTo(n)
})

watch(
  () => numeric.value,
  (n) => {
    if (n === null) return
    animateTo(n)
  },
)

onBeforeUnmount(stop)

defineExpose({
  /** 跳过滚动动画，直接落到目标值 */
  finish: () => {
    stop()
    display.value = numeric.value ?? 0
  },
})
</script>

<template>
  <div class="jm-statistic" :class="`jm-statistic--${size}`">
    <div v-if="title || $slots.title" class="jm-statistic__title">
      <slot name="title">{{ title }}</slot>
    </div>

    <div class="jm-statistic__value" :style="color ? { color } : undefined">
      <span v-if="prefix || $slots.prefix" class="jm-statistic__prefix">
        <slot name="prefix">{{ prefix }}</slot>
      </span>
      <span class="jm-statistic__number" aria-live="off">{{ text }}</span>
      <span v-if="suffix || $slots.suffix" class="jm-statistic__suffix">
        <slot name="suffix">{{ suffix }}</slot>
      </span>
    </div>

    <div v-if="$slots.default" class="jm-statistic__extra">
      <slot />
    </div>
  </div>
</template>

<style>
.jm-statistic {
  --jm-statistic-color: var(--jm-text-color);
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-statistic__title {
  color: var(--jm-text-color-2);
  font-size: var(--jm-font-size-sm);
  line-height: var(--jm-line-height);
}

.jm-statistic__value {
  display: flex;
  align-items: baseline;
  gap: 2px;
  color: var(--jm-statistic-color);
  font-family: var(--jm-font-family-number);
  font-weight: var(--jm-font-weight-medium);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.jm-statistic__number {
  white-space: nowrap;
}

.jm-statistic--sm .jm-statistic__value {
  font-size: var(--jm-font-size-lg);
}

.jm-statistic--md .jm-statistic__value {
  font-size: 26px;
}

.jm-statistic--lg .jm-statistic__value {
  font-size: 34px;
}

.jm-statistic__prefix {
  font-size: 0.62em;
  font-weight: var(--jm-font-weight-normal);
}

.jm-statistic__suffix {
  color: var(--jm-text-color-2);
  font-size: 0.55em;
  font-weight: var(--jm-font-weight-normal);
}

.jm-statistic__extra {
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-xs);
  line-height: var(--jm-line-height);
}
</style>
