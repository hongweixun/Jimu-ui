<script setup lang="ts">
import { computed, inject } from 'vue'
import { CHECKBOX_GROUP_KEY, type CheckboxValue } from './checkbox-context'
import { FORM_KEY } from './form-context'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmCheckbox' })

const props = withDefaults(
  defineProps<{
    modelValue?: boolean
    /** 在 CheckboxGroup 中的取值 */
    value?: CheckboxValue
    label?: string
    disabled?: boolean
    shape?: 'square' | 'circle'
    size?: 'small' | 'medium' | 'large'
    color?: string
    /** 半选：列表全选常用 */
    indeterminate?: boolean
  }>(),
  { modelValue: false, shape: 'square', size: 'medium' },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  change: [value: boolean]
}>()

const group = inject(CHECKBOX_GROUP_KEY, null)
const form = inject(FORM_KEY, null)

const checked = computed(() =>
  group ? group.value.value.includes(props.value as CheckboxValue) : props.modelValue,
)

const isDisabled = computed(() => props.disabled || form?.disabled.value || (group ? group.disabled.value : false))
const activeColor = computed(() => props.color || group?.color.value)

const styles = computed(() =>
  activeColor.value ? { '--jm-checkbox-active': activeColor.value } : {},
)

function onChange(e: Event) {
  if (isDisabled.value) return
  const next = (e.target as HTMLInputElement).checked
  if (group) {
    group.toggle(props.value as CheckboxValue, next)
  } else {
    emit('update:modelValue', next)
  }
  emit('change', next)
}
</script>

<template>
  <label
    class="jm-checkbox"
    :class="[
      `jm-checkbox--${size}`,
      `jm-checkbox--${shape}`,
      {
        'is-checked': checked,
        'is-indeterminate': indeterminate && !checked,
        'is-disabled': isDisabled,
      },
    ]"
    :style="styles"
  >
    <input
      class="jm-checkbox__input"
      type="checkbox"
      :checked="checked"
      :disabled="isDisabled"
      @change="onChange"
    />
    <span class="jm-checkbox__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" class="jm-checkbox__mark">
        <path
          v-if="indeterminate && !checked"
          d="M7 12h10"
          fill="none"
          stroke="currentColor"
          stroke-width="3"
          stroke-linecap="round"
        />
        <path
          v-else
          d="M6 12.5l4 4 8-8.5"
          fill="none"
          stroke="currentColor"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </span>
    <span v-if="label || $slots.default" class="jm-checkbox__label">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<style>
.jm-checkbox {
  --jm-checkbox-size: 20px;
  display: inline-flex;
  align-items: center;
  gap: var(--jm-space-2);
  min-height: var(--jm-tap-min);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-checkbox__input {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

.jm-checkbox__icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: var(--jm-checkbox-size);
  height: var(--jm-checkbox-size);
  border: 1.5px solid var(--jm-border-color-2);
  border-radius: var(--jm-radius-sm);
  background: var(--jm-bg-container);
  color: transparent;
  transition:
    background-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    border-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-checkbox--circle .jm-checkbox__icon {
  border-radius: 50%;
}

.jm-checkbox__mark {
  width: 100%;
  height: 100%;
  color: #fff;
}

.jm-checkbox__mark path {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  /* 描线用减速曲线：起笔快、收笔稳，勾出来的过程才看得清 */
  transition: stroke-dashoffset var(--jm-motion-transition-duration) var(--jm-motion-enter-ease);
}

.jm-checkbox.is-checked .jm-checkbox__icon,
.jm-checkbox.is-indeterminate .jm-checkbox__icon {
  background: var(--jm-checkbox-active, var(--jm-color-primary));
  border-color: var(--jm-checkbox-active, var(--jm-color-primary));
}

.jm-checkbox.is-checked .jm-checkbox__mark path,
.jm-checkbox.is-indeterminate .jm-checkbox__mark path {
  stroke-dashoffset: 0;
}

.jm-checkbox__label {
  line-height: var(--jm-line-height);
}

/* 尺寸 */
.jm-checkbox--small {
  --jm-checkbox-size: 16px;
  min-height: 36px;
  font-size: var(--jm-font-size-sm);
}

.jm-checkbox--large {
  --jm-checkbox-size: 24px;
  font-size: var(--jm-font-size-lg);
}

/* 交互 */
.jm-checkbox:active:not(.is-disabled) .jm-checkbox__icon {
  transform: scale(0.9);
}

.jm-checkbox__input:focus-visible + .jm-checkbox__icon {
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

.jm-checkbox.is-disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
</style>
