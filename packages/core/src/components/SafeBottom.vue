<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSafeBottom' })

/**
 * 安全区占位（SafeBottom）
 * ---------------------------------------------------------------------------
 * iPhone 刘海屏 / Home Indicator 的底部安全距离：在滚动内容末尾放一个占位块，
 * 让最后一个元素不被小黑条遮住；或给 fixed 底栏让出空间。
 *
 * 页面 meta 需要带 viewport-fit=cover 才有非零的 env() 值——文档站与模板
 * 已内置；数值来自 tokens.css 的 --jm-safe-bottom（env(safe-area-inset-bottom)），
 * PC / 安卓大多数设备为 0，不占空间。
 */

const props = withDefaults(
  defineProps<{
    /** 占位哪一侧：bottom 底部 / top 顶部（刘海） */
    position?: 'bottom' | 'top'
    /** 最小占位高度：env 为 0 时兜底，数字按 px */
    minHeight?: number | string
    /** 背景色，跟随父容器时留空 */
    background?: string
  }>(),
  {
    position: 'bottom',
    minHeight: undefined,
    background: undefined,
  },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const h = toCssSize(props.minHeight)
  if (h) s[`--jm-safe-min-${props.position}`] = h
  if (props.background) s.background = props.background
  return s
})
</script>

<template>
  <div
    class="jm-safe-spacer"
    :class="position === 'top' ? 'is-top' : 'is-bottom'"
    :style="styles"
    aria-hidden="true"
  />
</template>

<style>
.jm-safe-spacer {
  flex-shrink: 0;
  width: 100%;
  pointer-events: none;
}

.jm-safe-spacer.is-bottom {
  height: max(var(--jm-safe-bottom, 0px), var(--jm-safe-min-bottom, 0px));
}

.jm-safe-spacer.is-top {
  height: max(var(--jm-safe-top, 0px), var(--jm-safe-min-top, 0px));
}
</style>
