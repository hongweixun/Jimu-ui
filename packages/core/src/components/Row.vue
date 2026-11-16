<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmRow' })

const props = withDefaults(
  defineProps<{
    /** 列间距。数字按 px；传数组为 [横向, 纵向] */
    gutter?: number | string | [number | string, number | string]
    /** 交叉轴对齐 */
    align?: 'top' | 'middle' | 'bottom' | 'stretch'
    /** 主轴分布 */
    justify?: 'start' | 'center' | 'end' | 'between' | 'around'
    /** 是否换行（默认换行，24 栅格靠换行堆叠） */
    wrap?: boolean
  }>(),
  { align: 'top', justify: 'start', wrap: true },
)

const ALIGN: Record<string, string> = {
  top: 'flex-start',
  middle: 'center',
  bottom: 'flex-end',
  stretch: 'stretch',
}

const JUSTIFY: Record<string, string> = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  between: 'space-between',
  around: 'space-around',
}

const styles = computed(() => {
  const [x, y] = Array.isArray(props.gutter)
    ? props.gutter
    : [props.gutter ?? 0, 0]
  return {
    '--jm-row-gutter-x': toCssSize(x) ?? '0px',
    '--jm-row-gutter-y': toCssSize(y) ?? '0px',
    '--jm-row-align': ALIGN[props.align] ?? 'flex-start',
    '--jm-row-justify': JUSTIFY[props.justify] ?? 'flex-start',
  }
})
</script>

<template>
  <div
    class="jm-row"
    :class="{ 'is-nowrap': !wrap }"
    :style="styles"
  >
    <slot />
  </div>
</template>

<style>
.jm-row {
  display: flex;
  flex-wrap: wrap;
  /* 纵向间距用 row-gap，横向靠 Col 的内边距 + 这里的负外边距抵消外沿 */
  row-gap: var(--jm-row-gutter-y, 0px);
  margin-left: calc(var(--jm-row-gutter-x, 0px) / -2);
  margin-right: calc(var(--jm-row-gutter-x, 0px) / -2);
  align-items: var(--jm-row-align, flex-start);
  justify-content: var(--jm-row-justify, flex-start);
  min-width: 0;
  font-family: var(--jm-font-family);
}

.jm-row.is-nowrap {
  flex-wrap: nowrap;
}
</style>
