<script setup lang="ts">
import { computed, provide, toRef, watch } from 'vue'
import { toCssSize } from '../utils'
import { GRID_KEY } from './grid-context'

defineOptions({ name: 'JmGrid' })

const props = withDefaults(
  defineProps<{
    /** 每行列数 */
    columns?: number
    /** 格子间距，数字按 px */
    gutter?: number | string
    /** 格子间细线分隔 */
    border?: boolean
    /** 内容水平居中 */
    center?: boolean
    /** 强制每格为正方形（头像宫格、功能入口常用） */
    square?: boolean
    /** row=图标在上（默认），column=图标在左（列表式） */
    direction?: 'row' | 'column'
    /** 整组可点击（单项也可单独覆盖） */
    clickable?: boolean
    /** 圆角，配合背景可做卡片 */
    radius?: number | string
    /** 背景色 */
    background?: string
  }>(),
  {
    columns: 4,
    gutter: 0,
    border: false,
    center: true,
    square: false,
    direction: 'row',
    clickable: false,
  },
)

const emit = defineEmits<{ click: [index: number] }>()

/** 给未传 index 的 GridItem 按挂载顺序发号 */
let seed = 0

/* columns 传 0 / 负数或非数字会把 grid-template-columns 写坏，这里收敛到 1 */
const safeColumns = computed(() => {
  const n = Math.floor(Number(props.columns))
  return Number.isFinite(n) && n >= 1 ? n : 1
})

watch(
  () => props.columns,
  (v) => {
    const n = Math.floor(Number(v))
    if (!Number.isFinite(n) || n < 1) {
      console.warn(`[JmGrid] columns 应为 >=1 的整数，当前为 ${v}，已按 1 处理`)
    }
  },
)

const styles = computed(() => {
  const s: Record<string, string> = { '--jm-grid-columns': String(safeColumns.value) }
  const g = toCssSize(props.gutter)
  if (g) s['--jm-grid-gutter'] = g
  const r = toCssSize(props.radius)
  if (r) s['--jm-grid-radius'] = r
  if (props.background) s['--jm-grid-bg'] = props.background
  return s
})

provide(GRID_KEY, {
  columns: safeColumns,
  square: toRef(props, 'square'),
  clickable: toRef(props, 'clickable'),
  center: toRef(props, 'center'),
  border: toRef(props, 'border'),
  direction: toRef(props, 'direction'),
  onItemClick: (index: number) => emit('click', index),
  claimIndex: () => seed++,
})
</script>

<template>
  <div class="jm-grid" :class="{ 'has-border': border }" :style="styles">
    <slot />
  </div>
</template>

<style>
.jm-grid {
  display: grid;
  grid-template-columns: repeat(var(--jm-grid-columns, 4), 1fr);
  gap: var(--jm-grid-gutter, 0);
  border-radius: var(--jm-grid-radius, 0);
  background: var(--jm-grid-bg, transparent);
  overflow: hidden;
  font-family: var(--jm-font-family);
}
</style>
