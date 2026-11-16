<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import type { CircleColorStop } from '../types'

defineOptions({ name: 'JmCircle' })

const props = withDefaults(
  defineProps<{
    /** 进度 0 ~ 100 */
    percentage?: number
    /** 直径 */
    size?: number | string
    strokeWidth?: number
    /** 单色，或渐变（按 percentage 分布色标） */
    color?: string | CircleColorStop[]
    /** 底环颜色 */
    layerColor?: string
    /** 圆内填充色 */
    fill?: string
    /** 走完 100% 用时（ms），按增量比例分配 */
    speed?: number
    /** 中心文案，默认显示百分比 */
    text?: string
    textColor?: string
    /** 逆时针增长 */
    clockwise?: boolean
    strokeLinecap?: 'round' | 'square' | 'butt'
  }>(),
  {
    percentage: 0,
    size: 100,
    strokeWidth: 8,
    layerColor: 'var(--jm-border-color-2)',
    speed: 1000,
    clockwise: true,
    strokeLinecap: 'round',
  },
)

const warn = (msg: string) => {
  if (import.meta.env.DEV) console.warn(`[Jimu UI] ${msg}`)
}

const current = ref(clamp(props.percentage))

function clamp(v: number) {
  const n = Number(v)
  if (Number.isNaN(n)) return 0
  if (n < 0 || n > 100) {
    warn('Circle 的 percentage 应在 0 ~ 100 之间，已自动收敛')
    return Math.min(100, Math.max(0, n))
  }
  return n
}

const radius = computed(() => 50 - props.strokeWidth / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)

/** 动画时长按本次变化量占 100% 的比例折算，快速小幅变化不会拖沓 */
const duration = ref(0)
let timer: ReturnType<typeof setTimeout> | null = null

watch(
  () => props.percentage,
  (v) => {
    const next = clamp(v)
    const delta = Math.abs(next - current.value)
    duration.value = Math.round((props.speed * delta) / 100)
    current.value = next
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => (duration.value = 0), Math.max(16, duration.value))
  },
)

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})

const dashOffset = computed(() => circumference.value * (1 - current.value / 100))

const gradientStops = computed<CircleColorStop[] | null>(() =>
  Array.isArray(props.color) ? props.color : null,
)

const uid = `jm-circle-${Math.random().toString(36).slice(2, 8)}`
const strokeColor = computed(() => (Array.isArray(props.color) ? `url(#${uid})` : props.color))

const sizeValue = computed(() => (typeof props.size === 'number' ? `${props.size}px` : props.size))
const fontSize = computed(() =>
  typeof props.size === 'number' ? `${Math.max(12, Math.round(props.size * 0.18))}px` : '16px',
)

const barStyle = computed(() => ({
  strokeDasharray: `${circumference.value}px`,
  strokeDashoffset: `${dashOffset.value}px`,
  transitionDuration: `${duration.value}ms`,
  strokeLinecap: props.strokeLinecap,
}))

const rootStyle = computed(() => ({
  width: sizeValue.value,
  height: sizeValue.value,
  fontSize: fontSize.value,
  ...(props.textColor ? { '--jm-circle-text-color': props.textColor } : {}),
}))
</script>

<template>
  <div class="jm-circle" :style="rootStyle" role="img" :aria-label="`${current}%`">
    <svg class="jm-circle__svg" :class="{ 'is-reverse': !clockwise }" viewBox="0 0 100 100">
      <defs v-if="gradientStops">
        <linearGradient :id="uid" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop
            v-for="(stop, i) in gradientStops"
            :key="i"
            :offset="`${Math.min(100, Math.max(0, stop.percentage * 100))}%`"
            :stop-color="stop.color"
          />
        </linearGradient>
      </defs>

      <circle
        class="jm-circle__layer"
        cx="50"
        cy="50"
        :r="radius"
        :fill="fill ?? 'none'"
        :stroke="layerColor"
        :stroke-width="strokeWidth"
      />
      <circle
        class="jm-circle__bar"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="strokeColor"
        :stroke-width="strokeWidth"
        :style="barStyle"
      />
    </svg>

    <div class="jm-circle__text">
      <slot>{{ text ?? `${current}%` }}</slot>
    </div>
  </div>
</template>

<style>
.jm-circle {
  --jm-circle-text-color: var(--jm-text-color);
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--jm-font-family);
  color: var(--jm-circle-text-color);
}

.jm-circle__svg {
  width: 100%;
  height: 100%;
  /* 从 12 点方向开始画 */
  transform: rotate(-90deg);
}

/* 逆时针：水平镜像，起点仍在顶部 */
.jm-circle__svg.is-reverse {
  transform: rotate(-90deg) scale(-1, 1);
}

.jm-circle__bar {
  transition-property: stroke-dashoffset;
  transition-timing-function: linear;
}

.jm-circle__text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--jm-font-weight-medium);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
</style>
