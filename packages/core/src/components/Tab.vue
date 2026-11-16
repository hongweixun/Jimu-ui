<script setup lang="ts">
import { inject, onBeforeUnmount, onMounted, reactive, watch } from 'vue'
import { TABS_KEY, type TabItem, type TabName } from './tabs-context'

defineOptions({ name: 'JmTab' })

const props = withDefaults(
  defineProps<{
    name: TabName
    label: string
    disabled?: boolean
    badge?: string | number
  }>(),
  {},
)

const ctx = inject(TABS_KEY, null)

const tab = reactive<TabItem>({
  name: props.name,
  label: props.label,
  disabled: props.disabled,
  badge: props.badge,
})

watch(
  () => [props.label, props.disabled, props.badge],
  () => {
    tab.label = props.label
    tab.disabled = props.disabled
    tab.badge = props.badge
  },
)

onMounted(() => ctx?.addTab(tab))
onBeforeUnmount(() => ctx?.removeTab(props.name))
</script>

<template>
  <div
    v-show="ctx && (ctx.animated.value || ctx.active.value === name)"
    class="jm-tab-panel"
    role="tabpanel"
    :aria-hidden="ctx && !ctx.animated.value && ctx.active.value !== name ? 'true' : undefined"
  >
    <slot />
  </div>
</template>

<style>
.jm-tab-panel {
  font-family: var(--jm-font-family);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  line-height: var(--jm-line-height);
}
</style>
