<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSpace' })

type SpaceSize = 'small' | 'medium' | 'large' | number | string

const props = withDefaults(
  defineProps<{
    /** 排列方向 */
    direction?: 'horizontal' | 'vertical'
    /** 间距。数字按 px；传数组为 [横向, 纵向]；也支持 small/medium/large 预设 */
    size?: SpaceSize | [SpaceSize, SpaceSize]
    /** 交叉轴对齐 */
    align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
    /** 主轴分布 */
    justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly'
    /** 自动换行 */
    wrap?: boolean
    /** 行内（inline-flex）而非占满整行 */
    inline?: boolean
  }>(),
  { direction: 'horizontal', size: 'small', align: 'center', justify: 'start' },
)

const ALIGN: Record<string, string> = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  baseline: 'baseline',
  stretch: 'stretch',
}

const JUSTIFY: Record<string, string> = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
}

const PRESET: Record<string, string> = {
  small: 'var(--jm-space-2)',
  medium: 'var(--jm-space-4)',
  large: 'var(--jm-space-6)',
}

function resolve(v: SpaceSize): string {
  if (typeof v === 'string' && PRESET[v]) return PRESET[v]
  return toCssSize(v) ?? '0'
}

const styles = computed(() => {
  const s: Record<string, string> = {
    '--jm-space-align': ALIGN[props.align] ?? 'center',
    '--jm-space-justify': JUSTIFY[props.justify] ?? 'flex-start',
  }
  if (Array.isArray(props.size)) {
    s['--jm-space-gap-x'] = resolve(props.size[0])
    s['--jm-space-gap-y'] = resolve(props.size[1])
  } else {
    s['--jm-space-gap-x'] = resolve(props.size)
    s['--jm-space-gap-y'] = resolve(props.size)
  }
  return s
})
</script>

<template>
  <div
    class="jm-space"
    :class="[`jm-space--${direction}`, { 'is-wrap': wrap, 'is-inline': inline }]"
    :style="styles"
  >
    <slot />
  </div>
</template>

<style>
.jm-space {
  display: flex;
  flex-direction: row;
  gap: var(--jm-space-gap-y, var(--jm-space-2)) var(--jm-space-gap-x, var(--jm-space-2));
  align-items: var(--jm-space-align, center);
  justify-content: var(--jm-space-justify, flex-start);
  min-width: 0;
  font-family: var(--jm-font-family);
}

.jm-space.is-inline {
  display: inline-flex;
}

.jm-space.is-wrap {
  flex-wrap: wrap;
}

.jm-space--vertical {
  flex-direction: column;
}
</style>
