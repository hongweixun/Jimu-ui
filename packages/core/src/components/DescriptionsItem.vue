<script setup lang="ts">
import { computed, inject } from 'vue'
import { descriptionsContextKey } from './descriptions-context'

defineOptions({ name: 'JmDescriptionsItem' })

const props = withDefaults(
  defineProps<{
    label?: string
    value?: string | number
    /** 跨几项，horizontal 下占「标签+值」共 2 × span 格 */
    span?: number
  }>(),
  { span: 1 },
)

const ctx = inject(descriptionsContextKey, null)

const spanCount = computed(() => {
  const s = Math.max(1, Math.floor(props.span))
  return ctx ? Math.min(s, ctx.column.value) : s
})

/**
 * horizontal：item 用 display: contents，label/value 直接成为容器 grid 的子项，
 * 跨列在「标签+值」这一对上生效。
 * vertical：item 自身是 grid item 占一列，label/value 在 item 内部上下排列——
 * 否则 grid 按行填充会把同一项的标签和值排到两个列里。
 */
const itemStyle = computed(() => {
  if (ctx && ctx.direction.value === 'vertical') {
    return { gridColumn: `span ${spanCount.value}` }
  }
  return undefined
})

const labelStyle = computed(() => ({
  gridColumn: ctx && ctx.direction.value === 'vertical' ? undefined : 'span 1',
}))

const valueStyle = computed(() => ({
  gridColumn:
    ctx && ctx.direction.value === 'vertical'
      ? undefined
      : `span ${spanCount.value * 2 - 1}`,
}))
</script>

<template>
  <div class="jm-descriptions__item" :style="itemStyle">
    <dt class="jm-descriptions__cell jm-descriptions__label" :style="labelStyle">
      <slot name="label">{{ label }}</slot>
    </dt>
    <dd class="jm-descriptions__cell jm-descriptions__value" :style="valueStyle">
      <slot>{{ value }}</slot>
    </dd>
  </div>
</template>
