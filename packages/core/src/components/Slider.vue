<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import { toCssSize } from '../utils'
import { FORM_KEY } from './form-context'

defineOptions({ name: 'JmSlider' })

const props = withDefaults(
  defineProps<{
    /** 单值传 number，双滑块传 [起始, 结束] */
    modelValue?: number | [number, number]
    /** 显式声明双滑块；modelValue 传数组时自动开启 */
    range?: boolean
    min?: number
    max?: number
    step?: number
    disabled?: boolean
    /** 轨道高度，数字按 px */
    barHeight?: number | string
    /** 滑块直径，数字按 px */
    buttonSize?: number | string
    activeColor?: string
    inactiveColor?: string
    /** 拖动时上方显示数值气泡 */
    showTooltip?: boolean
    /** 双滑块之间的最小间隔 */
    minGap?: number
    /** 自定义数值文案 */
    format?: (value: number) => string
  }>(),
  {
    modelValue: 0,
    min: 0,
    max: 100,
    step: 1,
    barHeight: 4,
    buttonSize: 20,
    showTooltip: false,
    minGap: 0,
  },
)

const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || false)

const emit = defineEmits<{
  'update:modelValue': [value: number | [number, number]]
  change: [value: number | [number, number]]
  'drag-start': []
  'drag-end': []
}>()

const root = ref<HTMLElement>()
const track = ref<HTMLElement>()
const draggingIndex = ref<number | null>(null)

const isRange = computed(() => props.range || Array.isArray(props.modelValue))

/** step 的小数位数，用来消掉 0.1+0.2 这类浮点尾巴 */
const decimals = computed(() => {
  const s = String(props.step)
  const i = s.indexOf('.')
  return i < 0 ? 0 : s.length - i - 1
})

function snap(v: number): number {
  const raw = Math.round((v - props.min) / props.step) * props.step + props.min
  const fixed = Number(raw.toFixed(decimals.value))
  return Math.min(props.max, Math.max(props.min, fixed))
}

const values = computed<number[]>(() => {
  if (isRange.value) {
    const raw = Array.isArray(props.modelValue) ? props.modelValue : [props.min, Number(props.modelValue) || 0]
    return [snap(raw[0] ?? props.min), snap(raw[1] ?? props.max)].sort((a, b) => a - b)
  }
  return [snap(Number(props.modelValue) || 0)]
})

const percent = (v: number) => {
  const span = props.max - props.min || 1
  return ((v - props.min) / span) * 100
}

const barStyle = computed(() => {
  if (isRange.value) {
    const [a, b] = values.value
    return { left: `${percent(a)}%`, width: `${percent(b) - percent(a)}%` }
  }
  return { left: '0%', width: `${percent(values.value[0])}%` }
})

/** show-tooltip 时常态显示气泡，拖动时也只显示被拖的那个 */
function tooltipVisible(i: number): boolean {
  return draggingIndex.value === i || (props.showTooltip && draggingIndex.value === null)
}
const dragging = computed(() => draggingIndex.value !== null)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const bh = toCssSize(props.barHeight)
  const bs = toCssSize(props.buttonSize)
  if (bh) s['--jm-slider-bar-height'] = bh
  if (bs) s['--jm-slider-button-size'] = bs
  if (props.activeColor) s['--jm-slider-active'] = props.activeColor
  if (props.inactiveColor) s['--jm-slider-inactive'] = props.inactiveColor
  return s
})

function display(v: number): string {
  return props.format ? props.format(v) : String(v)
}

function emitValue(next: number[]) {
  const payload: number | [number, number] = isRange.value
    ? [next[0], next[1]]
    : next[0]
  emit('update:modelValue', payload)
}

function valueFromClientX(x: number): number {
  const rect = (track.value ?? root.value)?.getBoundingClientRect()
  if (!rect || !rect.width) return props.min
  const ratio = (x - rect.left) / rect.width
  return snap(props.min + ratio * (props.max - props.min))
}

function nearestIndex(v: number): number {
  if (!isRange.value) return 0
  const [a, b] = values.value
  return Math.abs(v - a) <= Math.abs(v - b) ? 0 : 1
}

function applyValue(index: number, v: number) {
  const next = [...values.value]
  if (!isRange.value) {
    next[0] = v
  } else if (index === 0) {
    next[0] = Math.min(v, next[1] - props.minGap)
  } else {
    next[1] = Math.max(v, next[0] + props.minGap)
  }
  if (next[0] === values.value[0] && next[1] === values.value[1]) return
  emitValue(next)
}

function onPointerDown(e: PointerEvent) {
  if (disabled.value) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  const hit = (e.target as HTMLElement)?.dataset?.index
  const v = valueFromClientX(e.clientX)
  draggingIndex.value = hit !== undefined ? Number(hit) : nearestIndex(v)
  // 点轨道直接跳过去，比"必须按在滑块上"省事
  if (hit === undefined) applyValue(draggingIndex.value, v)
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件或指针已释放时捕获会失败，忽略即可 */
  }
  emit('drag-start')
}

function onPointerMove(e: PointerEvent) {
  if (draggingIndex.value === null || disabled.value) return
  applyValue(draggingIndex.value, valueFromClientX(e.clientX))
}

function onPointerUp() {
  if (draggingIndex.value === null) return
  draggingIndex.value = null
  const payload: number | [number, number] = isRange.value
    ? [values.value[0], values.value[1]]
    : values.value[0]
  emit('change', payload)
  emit('drag-end')
}

function onKeydown(e: KeyboardEvent, index: number) {
  if (disabled.value) return
  const map: Record<string, number> = {
    ArrowRight: props.step,
    ArrowUp: props.step,
    ArrowLeft: -props.step,
    ArrowDown: -props.step,
    PageUp: props.step * 10,
    PageDown: -props.step * 10,
  }
  let next: number | null = null
  if (e.key in map) next = values.value[index] + map[e.key]
  else if (e.key === 'Home') next = props.min
  else if (e.key === 'End') next = props.max
  if (next === null) return
  e.preventDefault()
  applyValue(index, snap(next))
  const payload: number | [number, number] = isRange.value
    ? [values.value[0], values.value[1]]
    : values.value[0]
  emit('change', payload)
}
</script>

<template>
  <div
    ref="root"
    class="jm-slider"
    :class="{ 'is-disabled': disabled, 'is-range': isRange, 'is-dragging': dragging }"
    :style="styles"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
  >
    <div ref="track" class="jm-slider__track">
      <div class="jm-slider__bar" :style="barStyle" />
    </div>

    <div
      v-for="(v, i) in values"
      :key="i"
      class="jm-slider__button"
      :class="{ 'is-dragging': draggingIndex === i }"
      :style="{ left: `${percent(v)}%` }"
      role="slider"
      :tabindex="disabled ? -1 : 0"
      :aria-valuemin="min"
      :aria-valuemax="max"
      :aria-valuenow="v"
      :aria-disabled="disabled"
      :data-index="i"
      @keydown="onKeydown($event, i)"
    >
      <span
        v-if="tooltipVisible(i)"
        class="jm-slider__tooltip"
        aria-hidden="true"
      >{{ display(v) }}</span>
    </div>
  </div>
</template>

<style>
.jm-slider {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  height: var(--jm-slider-button-size, 20px);
  padding: 0 calc(var(--jm-slider-button-size, 20px) / 2);
  box-sizing: border-box;
  /* 拖动滑块时不触发页面滚动/长按选中 */
  touch-action: none;
  user-select: none;
  cursor: pointer;
  font-family: var(--jm-font-family);
}

.jm-slider__track {
  position: relative;
  width: 100%;
  height: var(--jm-slider-bar-height, 4px);
  border-radius: var(--jm-radius-round);
  background: var(--jm-slider-inactive, var(--jm-bg-input));
}

.jm-slider__bar {
  position: absolute;
  top: 0;
  height: 100%;
  border-radius: var(--jm-radius-round);
  background: var(--jm-slider-active, var(--jm-color-primary));
  transition: width 0.12s linear, left 0.12s linear;
}

.jm-slider__button {
  position: absolute;
  top: 50%;
  width: var(--jm-slider-button-size, 20px);
  height: var(--jm-slider-button-size, 20px);
  margin-top: calc(var(--jm-slider-button-size, 20px) / -2);
  margin-left: calc(var(--jm-slider-button-size, 20px) / -2);
  border-radius: 50%;
  background: var(--jm-bg-container);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.18), 0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: transform 0.12s ease, box-shadow 0.12s ease, left 0.12s linear;
  cursor: grab;
  outline: none;
}

.jm-slider__button.is-dragging {
  transform: scale(1.12);
  cursor: grabbing;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.22), 0 0 0 1px var(--jm-color-primary-border);
}

.jm-slider__button:focus-visible {
  box-shadow: 0 0 0 3px var(--jm-color-primary-light), 0 0 0 1px var(--jm-color-primary);
}

.jm-slider__tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  min-width: 24px;
  padding: 2px 6px;
  border-radius: var(--jm-radius-xs);
  background: var(--jm-text-primary);
  color: var(--jm-bg-container);
  font-size: var(--jm-font-size-xs);
  line-height: 1.5;
  text-align: center;
  white-space: nowrap;
  pointer-events: none;
}

.jm-slider.is-disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.jm-slider.is-disabled .jm-slider__button {
  cursor: not-allowed;
}

/* 拖动中关掉位置过渡，否则滑块会滞后于手指 */
.jm-slider.is-dragging .jm-slider__bar,
.jm-slider.is-dragging .jm-slider__button {
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
</style>
