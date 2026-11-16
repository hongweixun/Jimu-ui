<script setup lang="ts">
import { computed, provide } from 'vue'
import { COLLAPSE_KEY, type CollapseName } from './collapse-context'

defineOptions({ name: 'JmCollapse' })

const props = withDefaults(
  defineProps<{
    /** 手风琴模式传单个 name，普通模式传数组 */
    modelValue?: CollapseName | CollapseName[]
    accordion?: boolean
    border?: boolean
  }>(),
  { border: true },
)

const emit = defineEmits<{
  'update:modelValue': [value: CollapseName | CollapseName[]]
  change: [value: CollapseName | CollapseName[]]
}>()

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
  <div class="jm-collapse" :class="{ 'is-border': border }">
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
</style>
