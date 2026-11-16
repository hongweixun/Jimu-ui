<script setup lang="ts">
import { computed, watch } from 'vue'

defineOptions({ name: 'JmProgress' })

const props = withDefaults(
  defineProps<{
    /** 进度 0~100，越界自动收敛 */
    percentage?: number
    /** 轨道粗细，数字按 px */
    strokeWidth?: number | string
    /** 进度条颜色 */
    color?: string
    /** 轨道颜色 */
    trackColor?: string
    /** 是否在右侧显示百分比文字 */
    showText?: boolean
    /** 置灰（如任务暂停态） */
    inactive?: boolean
  }>(),
  { percentage: 0, strokeWidth: 6, showText: true, inactive: false },
)

const safe = computed(() => Math.min(100, Math.max(0, Number(props.percentage) || 0)))

const styles = computed(() => {
  const s: Record<string, string> = {}
  const w = typeof props.strokeWidth === 'number' ? `${props.strokeWidth}px` : props.strokeWidth
  if (w) s['--jm-progress-height'] = w
  if (props.color) s['--jm-progress-color'] = props.color
  if (props.trackColor) s['--jm-progress-track-color'] = props.trackColor
  return s
})

/* 数值越界时也收敛，避免宽度溢出 */
watch(
  () => props.percentage,
  (v) => {
    const n = Number(v)
    if (n > 100 || n < 0) console.warn(`[JmProgress] percentage 应在 0~100 之间，当前为 ${v}`)
  },
)
</script>

<template>
  <div class="jm-progress" :class="{ 'is-inactive': inactive }" :style="styles" role="progressbar" :aria-valuenow="safe" aria-valuemin="0" aria-valuemax="100">
    <div class="jm-progress__track">
      <div class="jm-progress__bar" :style="{ width: `${safe}%` }" />
    </div>
    <span v-if="showText" class="jm-progress__text">{{ safe }}%</span>
  </div>
</template>

<style>
/**
 * Progress 进度条
 * --------------------------------------------------------------------------- */
.jm-progress {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-progress__track {
  flex: 1;
  min-width: 0;
  height: var(--jm-progress-height, 6px);
  overflow: hidden;
  border-radius: var(--jm-radius-round);
  background: var(--jm-progress-track-color, var(--jm-bg-input));
}

.jm-progress__bar {
  width: 0;
  height: 100%;
  border-radius: var(--jm-radius-round);
  background: var(--jm-progress-color, var(--jm-color-primary));
  /* 宽度过渡是进度条的签名动效：300ms 标准缓动，只动 width */
  transition: width 300ms var(--jm-ease-standard, ease-out);
}

.jm-progress__text {
  flex: 0 0 auto;
  min-width: 3em;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.jm-progress.is-inactive .jm-progress__bar {
  background: var(--jm-gray-400);
}
</style>
