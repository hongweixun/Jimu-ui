<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSkeletonAvatar' })

const props = withDefaults(
  defineProps<{
    /** 尺寸；数字按 px */
    size?: number | string
    shape?: 'circle' | 'square'
  }>(),
  { size: 48, shape: 'circle' },
)

const style = computed(() => {
  const s = toCssSize(props.size) ?? '48px'
  return { width: s, height: s }
})
</script>

<template>
  <div
    class="jm-skeleton__avatar jm-skeleton__block"
    :class="`is-${shape}`"
    :style="style"
    aria-hidden="true"
  />
</template>
