<script setup lang="ts">
import { computed, provide } from 'vue'
import { RADIO_GROUP_KEY, type RadioValue } from './radio-context'

defineOptions({ name: 'JmRadioGroup' })

const props = withDefaults(
  defineProps<{
    modelValue?: RadioValue
    disabled?: boolean
    color?: string
    direction?: 'horizontal' | 'vertical'
    gap?: number | string
  }>(),
  { direction: 'horizontal' },
)

const emit = defineEmits<{ 'update:modelValue': [value: RadioValue] }>()

provide(RADIO_GROUP_KEY, {
  value: computed(() => props.modelValue),
  disabled: computed(() => props.disabled),
  color: computed(() => props.color),
  select: (val) => emit('update:modelValue', val),
})

const styles = computed(() => ({
  gap: typeof props.gap === 'number' ? `${props.gap}px` : props.gap,
}))
</script>

<template>
  <div class="jm-radio-group" :class="`jm-radio-group--${direction}`" :style="styles" role="radiogroup">
    <slot />
  </div>
</template>

<style>
.jm-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--jm-space-4);
  font-family: var(--jm-font-family);
}

.jm-radio-group--vertical {
  flex-direction: column;
  align-items: flex-start;
  gap: var(--jm-space-2);
}
</style>
