<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'
import type { TableColumn } from './table-context'

defineOptions({ name: 'JmTable' })

const props = withDefaults(
  defineProps<{
    columns?: TableColumn[]
    data?: Record<string, any>[]
    /** 行唯一键字段名，不给则用下标 */
    rowKey?: string
    /** 斑马纹 */
    stripe?: boolean
    /** 单元格竖线 */
    bordered?: boolean
    /** 表格最大高度：超出后表体滚动、表头吸顶 */
    maxHeight?: number | string
    /** 表头吸顶 */
    stickyHeader?: boolean
    emptyText?: string
    /** 行可点击（只影响指针样式与键盘可达） */
    clickable?: boolean
  }>(),
  {
    columns: () => [],
    data: () => [],
    emptyText: '暂无数据',
  },
)

const emit = defineEmits<{
  'row-click': [row: Record<string, any>, index: number]
  'cell-click': [payload: { row: Record<string, any>; column: TableColumn; value: unknown; index: number }]
}>()

const wrapStyle = computed(() => ({ maxHeight: toCssSize(props.maxHeight) }))

function colWidth(col: TableColumn) {
  return toCssSize(col.width)
}

function colMinWidth(col: TableColumn) {
  return toCssSize(col.minWidth)
}

function cellText(col: TableColumn, row: Record<string, any>, index: number) {
  const value = col.key ? row[col.key] : ''
  if (col.formatter) return col.formatter(value, row, index)
  return value === undefined || value === null || value === '' ? '—' : String(value)
}

function rowKeyOf(row: Record<string, any>, index: number) {
  if (props.rowKey && row[props.rowKey] !== undefined) return row[props.rowKey]
  return index
}

function onRowClick(row: Record<string, any>, index: number, e: MouseEvent) {
  emit('row-click', row, index)
  const cell = (e.target as HTMLElement).closest('td')
  if (!cell) return
  const colIndex = Number((cell as HTMLElement).dataset.col)
  const column = props.columns[colIndex]
  if (column) emit('cell-click', { row, column, value: row[column.key], index })
}

function onRowKeydown(row: Record<string, any>, index: number, e: KeyboardEvent) {
  if (e.key !== 'Enter' && e.key !== ' ') return
  e.preventDefault()
  emit('row-click', row, index)
}
</script>

<template>
  <div class="jm-table__wrap" :class="{ 'is-bordered': bordered }" :style="wrapStyle">
    <table class="jm-table" :class="{ 'is-stripe': stripe }">
      <colgroup>
        <col v-for="(col, i) in columns" :key="col.key || i" :style="{ width: colWidth(col) }" />
      </colgroup>
      <thead :class="{ 'is-sticky': stickyHeader }">
        <tr>
          <th
            v-for="(col, i) in columns"
            :key="col.key || i"
            scope="col"
            :class="[
              col.className,
              {
                'is-fixed-left': col.fixed === 'left',
                [`is-${col.align || 'left'}`]: true,
              },
            ]"
            :style="{ minWidth: colMinWidth(col) || colWidth(col) }"
          >
            {{ col.title ?? '' }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, index) in data"
          :key="rowKeyOf(row, index)"
          :tabindex="clickable ? 0 : undefined"
          :class="{ 'is-clickable': clickable }"
          @click="onRowClick(row, index, $event)"
          @keydown="clickable && onRowKeydown(row, index, $event)"
        >
          <td
            v-for="(col, ci) in columns"
            :key="col.key || ci"
            :data-col="ci"
            :class="[
              {
                'is-fixed-left': col.fixed === 'left',
                'is-ellipsis': col.ellipsis,
                [`is-${col.align || 'left'}`]: true,
              },
            ]"
            :style="{ minWidth: colMinWidth(col) || colWidth(col), maxWidth: col.ellipsis ? colWidth(col) : undefined }"
          >
            <slot
              :name="`cell-${col.key}`"
              :row="row"
              :value="row[col.key]"
              :index="index"
              :column="col"
            >
              {{ cellText(col, row, index) }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!data.length" class="jm-table__empty">
      <slot name="empty">{{ emptyText }}</slot>
    </div>
  </div>
</template>

<style scoped>
.jm-table__wrap {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  overflow: auto;
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-container);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

.jm-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: inherit;
  color: inherit;
}

.jm-table th,
.jm-table td {
  box-sizing: border-box;
  padding: 12px 12px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid var(--jm-border-color);
}

.jm-table thead th {
  position: relative;
  z-index: 1;
  background: var(--jm-bg-input);
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  color: var(--jm-text-color-2);
}

.jm-table thead.is-sticky th {
  position: sticky;
  top: 0;
  z-index: 3;
}

.jm-table tbody tr {
  --jm-table-row-bg: var(--jm-bg-container);
  background: var(--jm-table-row-bg);
}

.jm-table.is-stripe tbody tr:nth-child(even) {
  --jm-table-row-bg: var(--jm-bg-input);
}

.jm-table tbody tr:last-child td {
  border-bottom: none;
}

.jm-table tbody tr.is-clickable {
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-table tbody tr.is-clickable:active {
  --jm-table-row-bg: var(--jm-bg-active);
}

.jm-table tbody tr.is-clickable:focus-visible {
  outline: var(--jm-focus-ring-width, 2px) solid var(--jm-focus-ring-color, #00a0e9);
  outline-offset: -2px;
}

.jm-table th.is-center,
.jm-table td.is-center {
  text-align: center;
}

.jm-table th.is-right,
.jm-table td.is-right {
  text-align: right;
}

.jm-table td.is-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 固定首列：横向滚动时不动，用一条阴影与右侧内容分开 */
.jm-table th.is-fixed-left,
.jm-table td.is-fixed-left {
  position: sticky;
  left: 0;
  z-index: 2;
}

.jm-table td.is-fixed-left {
  background: var(--jm-table-row-bg, var(--jm-bg-container));
  box-shadow: 1px 0 0 var(--jm-border-color);
}

.jm-table th.is-fixed-left {
  z-index: 4;
  box-shadow: 1px 0 0 var(--jm-border-color);
}

/* 有背景的单元格才能盖住滚动内容；普通单元格交给行的底色 */
.jm-table tbody tr td {
  background: var(--jm-table-row-bg, var(--jm-bg-container));
}

.jm-table.is-bordered th + th,
.jm-table.is-bordered td + td {
  border-left: 1px solid var(--jm-border-color);
}

.jm-table__empty {
  padding: 36px 16px;
  text-align: center;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

[data-motion='off'] .jm-table tbody tr {
  transition: none;
}
</style>
