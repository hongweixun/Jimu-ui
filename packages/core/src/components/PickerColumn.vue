<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { PickerOption } from './picker-context'

defineOptions({ name: 'JmPickerColumn' })

const props = withDefaults(
  defineProps<{
    options: PickerOption[]
    /** 当前选中下标 */
    index: number
    itemHeight?: number
    visibleCount?: number
  }>(),
  { itemHeight: 44, visibleCount: 5 },
)

const emit = defineEmits<{
  'update:index': [index: number]
  change: [index: number]
}>()

const height = computed(() => props.itemHeight * props.visibleCount)
/* 上下各留出 (visibleCount-1)/2 个空位，让首尾选项也能停在中间 */
const padding = computed(() => ((props.visibleCount - 1) / 2) * props.itemHeight)

const offset = ref(0) // 拖拽位移
const animated = ref(true)

const wrapperStyle = computed(() => ({
  transform: `translate3d(0, ${-props.index * props.itemHeight + offset.value}px, 0)`,
  transition: animated.value ? 'transform 260ms cubic-bezier(0.22, 0.61, 0.36, 1)' : 'none',
  paddingTop: `${padding.value}px`,
  paddingBottom: `${padding.value}px`,
  '--jm-picker-item-height': `${props.itemHeight}px`,
}))

let startY = 0
let startTime = 0
let dragging = false

function nearestEnabled(target: number): number {
  const max = props.options.length - 1
  const clamped = Math.min(Math.max(0, target), max)
  if (!props.options[clamped]?.disabled) return clamped
  // 落点不可选时向两侧找最近的可用项
  for (let d = 1; d <= max; d += 1) {
    const up = clamped - d
    if (up >= 0 && !props.options[up]?.disabled) return up
    const down = clamped + d
    if (down <= max && !props.options[down]?.disabled) return down
  }
  return clamped
}

function commit(next: number, silent = false) {
  if (next === props.index) return
  emit('update:index', next)
  if (!silent) emit('change', next)
}

function onPointerDown(e: PointerEvent) {
  if (e.pointerType === 'mouse' && e.button !== 0) return
  dragging = true
  startY = e.clientY
  startTime = Date.now()
  offset.value = 0
  animated.value = false
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件或指针已释放时捕获会失败，忽略即可 */
  }
}

function onPointerMove(e: PointerEvent) {
  if (!dragging) return
  const dy = e.clientY - startY
  // 到顶/到底后再拉会有"拽不动"的手感，加阻尼提示边界
  const raw = -props.index * props.itemHeight + dy
  const maxScroll = 0
  const minScroll = -(props.options.length - 1) * props.itemHeight
  let d = dy
  if (raw > maxScroll) d = dy - (raw - maxScroll) * 0.65
  else if (raw < minScroll) d = dy - (raw - minScroll) * 0.65
  offset.value = d
}

function onPointerUp(e: PointerEvent) {
  if (!dragging) return
  dragging = false
  const dy = e.clientY - startY
  const speed = Math.abs(dy) / Math.max(1, Date.now() - startTime)
  const moved = props.index * props.itemHeight - dy
  // 快速轻扫时多给一格，慢速拖动按最近项吸附
  const bias = speed > 0.5 ? Math.sign(-dy) * 0.5 : 0
  const target = nearestEnabled(Math.round(moved / props.itemHeight + bias))
  offset.value = 0
  animated.value = true
  commit(target)
}

function onPointerCancel() {
  if (!dragging) return
  dragging = false
  offset.value = 0
  animated.value = true
}

function onWheel(e: WheelEvent) {
  e.preventDefault()
  const dir = e.deltaY > 0 ? 1 : -1
  commit(nearestEnabled(props.index + dir))
}

function onOptionClick(i: number) {
  if (props.options[i]?.disabled) return
  animated.value = true
  commit(i)
}

watch(
  () => props.index,
  () => {
    animated.value = true
  },
)
</script>

<template>
  <div
    class="jm-picker-column"
    :style="{ height: `${height}px` }"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerCancel"
    @wheel="onWheel"
  >
    <div class="jm-picker-column__wrapper" :style="wrapperStyle">
      <div
        v-for="(opt, i) in options"
        :key="opt.value ?? i"
        class="jm-picker-column__item"
        :class="{ 'is-selected': i === index, 'is-disabled': opt.disabled }"
        :style="{ height: `${itemHeight}px`, lineHeight: `${itemHeight}px` }"
        @click="onOptionClick(i)"
      >
        {{ opt.text }}
      </div>
    </div>
  </div>
</template>

<style>
.jm-picker-column {
  position: relative;
  flex: 1 1 0;
  min-width: 0;
  overflow: hidden;
  /* 纵向手势归本列，横向交给外层 */
  touch-action: none;
  cursor: grab;
  user-select: none;
}

.jm-picker-column:active {
  cursor: grabbing;
}

.jm-picker-column__wrapper {
  will-change: transform;
}

.jm-picker-column__item {
  padding: 0 var(--jm-space-2);
  overflow: hidden;
  color: var(--jm-text-color);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color var(--jm-motion-transition-duration, 200ms) var(--jm-ease-out, ease-out);
  cursor: pointer;
}

.jm-picker-column__item.is-selected {
  color: var(--jm-color-primary);
  font-weight: var(--jm-font-weight-medium);
}

.jm-picker-column__item.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}
</style>
