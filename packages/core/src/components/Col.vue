<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'JmCol' })

const props = withDefaults(
  defineProps<{
    /** 占多少列（1~24），默认整行 */
    span?: number
    /** 向右偏移多少列 */
    offset?: number
    /** 排序，数字小的在前 */
    order?: number
  }>(),
  { span: 24, offset: 0 },
)

function clampCol(n: number, min: number, max: number): number {
  const v = Math.round(Number(n) || 0)
  return Math.min(max, Math.max(min, v))
}

const styles = computed(() => ({
  '--jm-col-span': String(clampCol(props.span, 0, 24)),
  '--jm-col-offset': String(clampCol(props.offset, 0, 24)),
  '--jm-col-order': String(Number(props.order) || 0),
}))
</script>

<template>
  <div class="jm-col" :style="styles">
    <slot />
  </div>
</template>

<style>
.jm-col {
  box-sizing: border-box;
  flex: 0 0 calc(100% / 24 * var(--jm-col-span, 24));
  max-width: calc(100% / 24 * var(--jm-col-span, 24));
  padding-left: calc(var(--jm-row-gutter-x, 0px) / 2);
  padding-right: calc(var(--jm-row-gutter-x, 0px) / 2);
  margin-left: calc(100% / 24 * var(--jm-col-offset, 0));
  order: var(--jm-col-order, 0);
  min-width: 0;
}
</style>
