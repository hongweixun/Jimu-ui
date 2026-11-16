<script setup lang="ts">
import { computed, provide } from 'vue'
import { TIMELINE_KEY } from './timeline-context'

defineOptions({ name: 'JmTimeline' })

const props = withDefaults(
  defineProps<{
    /** 轴线样式 */
    lineStyle?: 'solid' | 'dashed'
    /** 轴线颜色 */
    lineColor?: string
    /** 默认圆点直径（px） */
    dotSize?: number
    /** 左侧时间列宽度，如 '60px'、'4em' */
    timeWidth?: string
  }>(),
  { lineStyle: 'solid', dotSize: 10, timeWidth: '60px' },
)

const styles = computed(() => {
  const s: Record<string, string> = {
    '--jm-timeline-dot-size': `${props.dotSize}px`,
    '--jm-timeline-time-width': props.timeWidth,
  }
  if (props.lineColor) s['--jm-timeline-line'] = props.lineColor
  return s
})

provide(TIMELINE_KEY, {
  get lineStyle() {
    return props.lineStyle
  },
})
</script>

<template>
  <div class="jm-timeline" :class="`jm-timeline--${lineStyle}`" :style="styles">
    <slot />
  </div>
</template>

<style>
.jm-timeline {
  --jm-timeline-line: var(--jm-border-color-2);
  --jm-timeline-gap: 18px;
  display: flex;
  flex-direction: column;
  width: 100%;
  font-family: var(--jm-font-family);
}
</style>
