<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmCellGroup' })

const props = withDefaults(
  defineProps<{
    title?: string
    /** 卡片式：左右留白 + 圆角 */
    inset?: boolean
    radius?: number | string
    background?: string
  }>(),
  { inset: true },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-cell-group-radius'] = r
  if (props.background) s['--jm-cell-group-bg'] = props.background
  return s
})
</script>

<template>
  <div class="jm-cell-group" :class="{ 'is-inset': inset }" :style="styles">
    <div v-if="title || $slots.title" class="jm-cell-group__title">
      <slot name="title">{{ title }}</slot>
    </div>
    <div class="jm-cell-group__body">
      <slot />
    </div>
  </div>
</template>

<style>
.jm-cell-group {
  --jm-cell-group-radius: var(--jm-radius);
  font-family: var(--jm-font-family);
}

.jm-cell-group.is-inset {
  padding: 0 var(--jm-space-4);
}

.jm-cell-group__title {
  padding: var(--jm-space-4) var(--jm-space-1) var(--jm-space-2);
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.4;
  color: var(--jm-text-color-2);
}

.jm-cell-group__body {
  overflow: hidden;
  background: var(--jm-cell-group-bg, var(--jm-bg-container));
  border-radius: var(--jm-cell-group-radius);
}

/* 组内单元格自动分割线，最后一个不出线 */
.jm-cell-group__body > .jm-cell::after {
  display: none;
}

.jm-cell-group__body > .jm-cell:not(:last-child) {
  border-bottom: 1px solid var(--jm-border-color);
}
</style>
