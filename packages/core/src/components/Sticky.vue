<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSticky' })

const props = withDefaults(
  defineProps<{
    /** 吸顶后距离滚动容器顶部的偏移（数字按 px） */
    offsetTop?: number | string
    /** 吸顶层的 z-index */
    zIndex?: number | string
  }>(),
  { offsetTop: 0, zIndex: 99 },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const t = toCssSize(props.offsetTop)
  if (t && t !== '0px') s['--jm-sticky-top'] = t
  if (props.zIndex !== undefined) s['--jm-sticky-z'] = String(props.zIndex)
  return s
})
</script>

<template>
  <div class="jm-sticky" :style="styles">
    <slot />
  </div>
</template>

<style>
/**
 * Sticky 粘性布局
 * ---------------------------------------------------------------------------
 * 用原生 position: sticky 实现：由最近的滚动容器驱动，不监听 scroll、不克隆
 * 节点、不打破文档流。包住 Tabs / NavBar / 索引栏即可在内容滚过时吸顶。
 */
.jm-sticky {
  position: sticky;
  top: var(--jm-sticky-top, 0);
  z-index: var(--jm-sticky-z, 99);
}
</style>
