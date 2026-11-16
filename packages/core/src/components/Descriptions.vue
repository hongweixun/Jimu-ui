<script setup lang="ts">
import { computed, provide, toRef } from 'vue'
import { toCssSize } from '../utils'
import { descriptionsContextKey } from './descriptions-context'

defineOptions({ name: 'JmDescriptions' })

const props = withDefaults(
  defineProps<{
    /** 一行放几项 */
    column?: number
    /** 表格线 */
    border?: boolean
    /** 标签列宽，数字按 px，字符串原样（百分比、em 都可以） */
    labelWidth?: number | string
    labelAlign?: 'left' | 'right'
    /** horizontal：标签在左值在右；vertical：标签在上值在下 */
    direction?: 'horizontal' | 'vertical'
    /** 标签后是否带冒号 */
    colon?: boolean
    size?: 'small' | 'medium' | 'large'
    title?: string
  }>(),
  {
    column: 1,
    border: false,
    labelAlign: 'left',
    direction: 'horizontal',
    colon: true,
    size: 'medium',
  },
)

provide(descriptionsContextKey, {
  direction: toRef(props, 'direction'),
  column: computed(() => Math.max(1, Math.floor(props.column))),
  border: toRef(props, 'border'),
  colon: toRef(props, 'colon'),
  labelAlign: toRef(props, 'labelAlign'),
  size: toRef(props, 'size'),
})

const columns = computed(() => Math.max(1, Math.floor(props.column)))

const classes = computed(() => [
  `jm-descriptions--${props.direction}`,
  `jm-descriptions--${props.size}`,
  {
    'is-border': props.border,
    'is-colon': props.colon && props.direction === 'horizontal',
    'is-label-right': props.labelAlign === 'right',
  },
])

/**
 * horizontal 时每项占「标签 + 值」两格，所以总列数是 column * 2。
 * 标签列宽固定在模板里，值列吃掉剩余空间，多列之间才对得齐。
 */
const gridStyle = computed(() => {
  if (props.direction === 'vertical') {
    return { gridTemplateColumns: `repeat(${columns.value}, minmax(0, 1fr))` }
  }
  const w = toCssSize(props.labelWidth) || 'var(--jm-desc-label-w, 72px)'
  return { gridTemplateColumns: `repeat(${columns.value}, ${w} minmax(0, 1fr))` }
})
</script>

<template>
  <dl class="jm-descriptions" :class="classes" :style="gridStyle">
    <div v-if="title || $slots.title" class="jm-descriptions__title">
      <slot name="title">{{ title }}</slot>
    </div>
    <slot />
  </dl>
</template>

<style>
.jm-descriptions {
  --jm-desc-label-w: 72px;
  --jm-desc-border-color: var(--jm-border-color);
  --jm-desc-label-bg: var(--jm-bg-page);
  --jm-desc-padding-y: 8px;
  --jm-desc-padding-x: 10px;
  box-sizing: border-box;
  display: grid;
  margin: 0;
  column-gap: 12px;
  align-items: stretch;
  position: relative;
  font-family: var(--jm-font-family);
  color: var(--jm-text-color);
  background: var(--jm-bg-elevated);
}

.jm-descriptions--small {
  --jm-desc-padding-y: 5px;
  --jm-desc-padding-x: 8px;
}

.jm-descriptions--large {
  --jm-desc-padding-y: 12px;
  --jm-desc-padding-x: 14px;
}

.jm-descriptions__title {
  grid-column: 1 / -1;
  padding: 0 0 8px;
  font-size: var(--jm-font-size-md);
  font-weight: 600;
  line-height: 1.4;
}

/* 每一项用 display: contents：标签和值直接成为容器 grid 的子项，
   跨列（span）才能在「标签+值」这一对上正确生效 */
.jm-descriptions__item {
  display: contents;
}

/* vertical 时 item 变回普通块级 grid item，标签与值在 item 内部上下排 */
.jm-descriptions--vertical .jm-descriptions__item {
  display: block;
}

.jm-descriptions__cell {
  box-sizing: border-box;
  min-width: 0;
  /* dd 默认有 margin-left，重置掉 */
  margin: 0;
  padding: var(--jm-desc-padding-y) 0;
  font-size: var(--jm-font-size-sm);
  line-height: 1.6;
}

.jm-descriptions__label {
  font-weight: 400;
  color: var(--jm-text-color-2);
  word-break: break-word;
}

.jm-descriptions--horizontal .jm-descriptions__label {
  padding-right: 0;
}

.jm-descriptions.is-label-right .jm-descriptions__label {
  text-align: right;
  padding-right: 4px;
}

.jm-descriptions--horizontal .jm-descriptions__value {
  padding-left: 2px;
}

.jm-descriptions.is-label-right .jm-descriptions__value {
  padding-left: 4px;
}

.jm-descriptions__value {
  color: var(--jm-text-color);
  word-break: break-word;
}

.jm-descriptions.is-colon .jm-descriptions__label::after {
  content: '：';
  margin-left: 1px;
}

/* 表格线：容器只画上、左两条边，右、下由每个单元格补，
   这样最后一行 / 最后一列的外框正好由单元格自己的边收口，不用单独去线 */
.jm-descriptions.is-border {
  border-top: 1px solid var(--jm-desc-border-color);
  border-left: 1px solid var(--jm-desc-border-color);
  border-radius: var(--jm-radius-md);
  overflow: hidden;
  column-gap: 0;
}

.jm-descriptions.is-border .jm-descriptions__cell {
  padding: var(--jm-desc-padding-y) var(--jm-desc-padding-x);
  border-right: 1px solid var(--jm-desc-border-color);
  border-bottom: 1px solid var(--jm-desc-border-color);
}

.jm-descriptions.is-border .jm-descriptions__label {
  background: var(--jm-desc-label-bg);
  font-size: var(--jm-font-size-sm);
}

.jm-descriptions.is-border .jm-descriptions__value {
  background: var(--jm-bg-elevated);
}

/* 无边框时行与行之间不需要额外间距，垂直方向靠上下 padding 撑开 */
.jm-descriptions--vertical .jm-descriptions__label {
  padding-bottom: 0;
  font-size: var(--jm-font-size-xs);
}

.jm-descriptions--vertical .jm-descriptions__value {
  padding-top: 2px;
}

.jm-descriptions--vertical.is-border .jm-descriptions__value {
  padding-top: var(--jm-desc-padding-y);
}
</style>
