<script setup lang="ts">
import { computed, provide } from 'vue'
import { toCssSize } from '../utils'
import { COLLAPSE_KEY, type CollapseName } from './collapse-context'

defineOptions({ name: 'JmCollapse' })

const props = withDefaults(
  defineProps<{
    /** 手风琴模式传单个 name，普通模式传数组 */
    modelValue?: CollapseName | CollapseName[]
    accordion?: boolean
    /** 上下外边框（整体模块的）；item 之间的分隔线不受它控制 */
    border?: boolean
    /** 整体圆角：true 用默认大圆角，数字按 px，字符串原样 */
    round?: boolean | number | string
  }>(),
  { border: true },
)

const emit = defineEmits<{
  'update:modelValue': [value: CollapseName | CollapseName[]]
  change: [value: CollapseName | CollapseName[]]
}>()

const roundStyles = computed(() => {
  if (!props.round) return undefined
  const s: Record<string, string> = {}
  const r = toCssSize(props.round === true ? '' : props.round)
  if (r) s['--jm-collapse-radius'] = r
  return s
})

const activeList = computed<CollapseName[]>(() => {
  const v = props.modelValue
  if (v === undefined || v === null || v === '') return []
  return Array.isArray(v) ? v : [v]
})

function isExpanded(name: CollapseName) {
  return activeList.value.includes(name)
}

function toggle(name: CollapseName) {
  if (props.accordion) {
    const next: CollapseName = isExpanded(name) ? '' : name
    emit('update:modelValue', next)
    emit('change', next)
    return
  }
  const list = activeList.value.slice()
  const index = list.indexOf(name)
  if (index > -1) list.splice(index, 1)
  else list.push(name)
  emit('update:modelValue', list)
  emit('change', list)
}

provide(COLLAPSE_KEY, {
  isExpanded,
  toggle,
  get accordion() {
    return !!props.accordion
  },
})
</script>

<template>
  <div
    class="jm-collapse"
    :class="{ 'is-border': border, 'is-round': !!round }"
    :style="roundStyles"
  >
    <slot />
  </div>
</template>

<style>
.jm-collapse {
  width: 100%;
  background: var(--jm-bg-container);
  font-family: var(--jm-font-family);
  color: var(--jm-text-color);
}

.jm-collapse.is-border {
  border-top: var(--jm-border-width) solid var(--jm-border-color);
  border-bottom: var(--jm-border-width) solid var(--jm-border-color);
}

/* 圆角卡片：整体裁切圆角；去上下边框时给一层浅阴影做卡片质感 */
.jm-collapse.is-round {
  border-radius: var(--jm-collapse-radius, var(--jm-radius-lg));
  overflow: hidden;
}

.jm-collapse.is-round.is-border {
  border: var(--jm-border-width) solid var(--jm-border-color);
}

.jm-collapse.is-round:not(.is-border) {
  box-shadow: var(--jm-shadow-1);
}
</style>
