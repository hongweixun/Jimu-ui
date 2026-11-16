<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'
import { getIcon, warnMissingIcon } from './icons'

defineOptions({ name: 'JmIcon' })

const props = withDefaults(
  defineProps<{
    /** 图标名，见 `iconNames()`；未注册的名字会告警并让出占位 */
    name: string
    /**
     * 尺寸。默认 '1em' —— 跟着父级字号走，正文里内联最省心；
     * 传数字按 px 处理。
     */
    size?: number | string
    /** 颜色，默认继承文字颜色 */
    color?: string
    /** 旋转动画（loading 类图标） */
    spin?: boolean
    /** 固定旋转角度，数字按 deg */
    rotate?: number | string
    /** 描边粗细，实心图标忽略 */
    strokeWidth?: number
    /** 无障碍标签；不传则视为纯装饰（aria-hidden） */
    label?: string
  }>(),
  { size: '1em', strokeWidth: 1.8 },
)

const def = computed(() => {
  const found = getIcon(props.name)
  if (!found) warnMissingIcon(props.name)
  return found
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  const size = toCssSize(props.size)
  if (size) {
    s.fontSize = size
    s.width = size
    s.height = size
  }
  if (props.color) s.color = props.color
  if (props.rotate !== undefined && props.rotate !== '') {
    const deg = typeof props.rotate === 'number' ? `${props.rotate}deg` : props.rotate
    s.transform = `rotate(${deg})`
  }
  return s
})

const filled = computed(() => Boolean(def.value?.filled))
</script>

<template>
  <svg
    v-if="def"
    class="jm-icon"
    :class="{ 'jm-icon--spin': spin, 'jm-icon--filled': filled }"
    :style="styles"
    :viewBox="def.viewBox ?? '0 0 24 24'"
    :fill="filled ? 'currentColor' : 'none'"
    :stroke="filled ? 'none' : 'currentColor'"
    :stroke-width="filled ? undefined : strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    :role="label ? 'img' : undefined"
    :aria-label="label"
    :aria-hidden="label ? undefined : 'true'"
    focusable="false"
  >
    <path v-for="(d, i) in def.paths" :key="i" :d="d" />
  </svg>
  <!-- 未注册的图标不改布局：占一个 1em 的空位，页面不会跳 -->
  <span v-else class="jm-icon jm-icon--empty" :style="styles" aria-hidden="true" />
</template>

<style>
.jm-icon {
  display: inline-block;
  flex: none;
  vertical-align: -0.125em;
  overflow: visible;
}

.jm-icon--empty {
  display: inline-block;
  flex: none;
  width: 1em;
  height: 1em;
  vertical-align: -0.125em;
}

.jm-icon--spin {
  animation: jm-icon-spin 1s linear infinite;
}

@keyframes jm-icon-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .jm-icon--spin {
    animation-duration: 2.4s;
  }
}
</style>
