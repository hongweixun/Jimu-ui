<script setup lang="ts">
import { computed, provide } from 'vue'
import { CHECKBOX_GROUP_KEY, type CheckboxValue } from './checkbox-context'

defineOptions({ name: 'JmCheckboxGroup' })

const props = withDefaults(
  defineProps<{
    modelValue?: CheckboxValue[]
    disabled?: boolean
    /** 统一覆盖选中色 */
    color?: string
    direction?: 'horizontal' | 'vertical'
    gap?: number | string
    /** 最多可选数量，超出时拦截勾选并触发 overLimit */
    max?: number
    /** 最少保留数量，低于时拦截取消并触发 overLimit */
    min?: number
  }>(),
  { modelValue: () => [], direction: 'horizontal' },
)

const emit = defineEmits<{
  'update:modelValue': [value: CheckboxValue[]]
  /** 超出 max / 低于 min 时触发（本次操作已被拦截） */
  overLimit: [payload: { value: CheckboxValue; type: 'max' | 'min'; selected: CheckboxValue[] }]
}>()

provide(CHECKBOX_GROUP_KEY, {
  value: computed(() => props.modelValue),
  disabled: computed(() => props.disabled),
  color: computed(() => props.color),
  toggle: (val, checked) => {
    const set = new Set(props.modelValue)
    if (checked) {
      if (props.max !== undefined && props.max >= 0 && set.size >= props.max) {
        emit('overLimit', { value: val, type: 'max', selected: Array.from(set) })
        return
      }
      set.add(val)
    } else {
      if (props.min !== undefined && props.min > 0 && set.size <= props.min) {
        emit('overLimit', { value: val, type: 'min', selected: Array.from(set) })
        return
      }
      set.delete(val)
    }
    emit('update:modelValue', Array.from(set))
  },
})

const styles = computed(() => ({
  gap: typeof props.gap === 'number' ? `${props.gap}px` : props.gap,
}))
</script>

<template>
  <div
    class="jm-checkbox-group"
    :class="`jm-checkbox-group--${direction}`"
    :style="styles"
    role="group"
  >
    <slot />
  </div>
</template>

<style>
.jm-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--jm-space-4);
  font-family: var(--jm-font-family);
}

.jm-checkbox-group--vertical {
  flex-direction: column;
  align-items: flex-start;
  gap: var(--jm-space-2);
}
</style>
