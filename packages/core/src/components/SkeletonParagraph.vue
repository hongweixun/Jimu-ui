<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSkeletonParagraph' })

const props = withDefaults(
  defineProps<{
    /** 段落行数 */
    row?: number
    /** 行宽；传数组可逐行指定，超出循环复用 */
    rowWidth?: number | string | (number | string)[]
    /** 最后一行收窄 */
    lastRowWidth?: number | string
  }>(),
  { row: 3, lastRowWidth: '58%' },
)

const list = computed(() => {
  const total = Math.max(0, props.row)
  const widths: (number | string)[] = []
  for (let i = 0; i < total; i++) {
    if (Array.isArray(props.rowWidth)) {
      if (props.rowWidth.length === 0) {
        widths.push(i === total - 1 && total > 1 ? props.lastRowWidth : '100%')
      } else {
        widths.push(props.rowWidth[Math.min(i, props.rowWidth.length - 1)])
      }
    } else if (props.rowWidth !== undefined) {
      widths.push(props.rowWidth)
    } else {
      widths.push(i === total - 1 && total > 1 ? props.lastRowWidth : '100%')
    }
  }
  return widths.map((w) => ({ width: toCssSize(w) ?? '100%' }))
})
</script>

<template>
  <div class="jm-skeleton__paragraph" aria-hidden="true">
    <div
      v-for="(style, i) in list"
      :key="i"
      class="jm-skeleton__row jm-skeleton__block"
      :style="style"
    />
  </div>
</template>
