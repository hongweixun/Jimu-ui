<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSkeletonTitle' })

const props = withDefaults(
  defineProps<{
    /** 标题宽度；数字按 px，默认 40% */
    width?: number | string
  }>(),
  { width: '40%' },
)

const style = computed(() => ({ width: toCssSize(props.width) ?? '40%' }))
</script>

<template>
  <div class="jm-skeleton__title jm-skeleton__block" :style="style" aria-hidden="true" />
</template>
