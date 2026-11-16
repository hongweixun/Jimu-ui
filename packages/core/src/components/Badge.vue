<script setup lang="ts">
import { computed, useSlots } from 'vue'

defineOptions({ name: 'JmBadge' })

const props = withDefaults(
  defineProps<{
    content?: string | number
    /** 小红点模式 */
    dot?: boolean
    max?: number
    color?: string
    showZero?: boolean
    show?: boolean
    /** 位置微调 [x, y] */
    offset?: [number, number]
  }>(),
  { max: 99, show: true },
)

const slots = useSlots()
const hasSlot = computed(() => !!slots.default)

const display = computed(() => {
  const c = props.content
  if (c === undefined || c === null || c === '') return ''
  if (typeof c === 'number' && c > props.max) return `${props.max}+`
  return String(c)
})

const visible = computed(() => {
  if (!props.show) return false
  if (props.dot) return true
  if (display.value === '') return false
  if (props.content === 0 || props.content === '0') return props.showZero
  return true
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.color) s['--jm-badge-bg'] = props.color
  if (props.offset) s['--jm-badge-offset'] = `${props.offset[0]}px, ${props.offset[1]}px`
  return s
})
</script>

<template>
  <span
    class="jm-badge"
    :class="{ 'is-dot': dot, 'is-standalone': !hasSlot }"
    :style="styles"
  >
    <slot />
    <sup v-if="visible" class="jm-badge__content" :class="{ 'is-dot': dot }">
      <slot name="content">{{ display }}</slot>
    </sup>
  </span>
</template>

<style>
.jm-badge {
  --jm-badge-bg: var(--jm-color-danger);
  position: relative;
  display: inline-flex;
  vertical-align: middle;
  font-family: var(--jm-font-family);
}

.jm-badge__content {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
  transform: translate(50%, -50%) translate(var(--jm-badge-offset, 0px, 0px));
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 16px;
  height: 16px;
  padding: 0 5px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-badge-bg);
  color: #fff;
  font-size: 11px;
  font-weight: var(--jm-font-weight-medium);
  line-height: 1;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  box-shadow: 0 0 0 1.5px var(--jm-bg-container);
  transition: transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease);
}

.jm-badge__content.is-dot {
  min-width: 8px;
  width: 8px;
  height: 8px;
  padding: 0;
}

.jm-badge.is-standalone .jm-badge__content {
  position: static;
  transform: none;
  box-shadow: none;
}

.jm-badge.is-standalone.is-dot .jm-badge__content {
  display: inline-block;
}
</style>
