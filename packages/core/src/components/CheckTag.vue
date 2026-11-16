<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'JmCheckTag' })

const props = withDefaults(
  defineProps<{
    modelValue?: boolean
    disabled?: boolean
    size?: 'small' | 'medium' | 'large'
    /** round 胶囊、square 小圆角 */
    shape?: 'round' | 'square'
    /** 选中后的实底颜色，传了会变成白字强调样式 */
    checkedColor?: string
    /** 未选中时的文字色 */
    color?: string
  }>(),
  {
    modelValue: false,
    size: 'medium',
    shape: 'round',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  change: [value: boolean]
}>()

const checked = computed(() => props.modelValue)

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.checkedColor) {
    s['--jm-checktag-checked-bg'] = props.checkedColor
    s['--jm-checktag-checked-color'] = '#fff'
    s['--jm-checktag-checked-border'] = props.checkedColor
  }
  if (props.color) s['--jm-checktag-color'] = props.color
  return s
})

function toggle() {
  if (props.disabled) return
  const next = !checked.value
  emit('update:modelValue', next)
  emit('change', next)
}
</script>

<template>
  <button
    type="button"
    role="checkbox"
    class="jm-checktag"
    :class="[
      `jm-checktag--${size}`,
      `jm-checktag--${shape}`,
      { 'is-checked': checked, 'is-disabled': disabled },
    ]"
    :style="styles"
    :aria-checked="checked"
    :disabled="disabled"
    @click="toggle"
  >
    <span v-if="checked" class="jm-checktag__mark" aria-hidden="true">
      <jm-icon name="check" size="11px" :stroke-width="3" />
    </span>
    <span class="jm-checktag__label"><slot /></span>
  </button>
</template>

<style>
.jm-checktag {
  --jm-checktag-bg: var(--jm-bg-elevated);
  --jm-checktag-border: var(--jm-border-color);
  --jm-checktag-color: var(--jm-text-color-2);
  --jm-checktag-checked-bg: var(--jm-color-primary-light);
  --jm-checktag-checked-border: var(--jm-color-primary);
  --jm-checktag-checked-color: var(--jm-color-primary);
  display: inline-flex;
  align-items: center;
  gap: 3px;
  height: 28px;
  padding: 0 12px;
  box-sizing: border-box;
  border: 1px solid var(--jm-checktag-border);
  border-radius: var(--jm-radius-round);
  background: var(--jm-checktag-bg);
  color: var(--jm-checktag-color);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-xs);
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition:
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    border-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-checktag--square {
  border-radius: var(--jm-radius-sm);
}

.jm-checktag--small {
  height: 24px;
  padding: 0 9px;
  font-size: 11px;
}

.jm-checktag--large {
  height: 34px;
  padding: 0 15px;
  font-size: var(--jm-font-size-sm);
}

.jm-checktag.is-checked {
  background: var(--jm-checktag-checked-bg);
  border-color: var(--jm-checktag-checked-border);
  color: var(--jm-checktag-checked-color);
  font-weight: var(--jm-font-weight-medium);
}

.jm-checktag__mark {
  display: inline-flex;
  align-items: center;
  margin-left: -3px;
}

.jm-checktag__label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.jm-checktag:active:not(.is-disabled) {
  transform: scale(0.96);
}

.jm-checktag.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.jm-checktag:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

[data-motion='off'] .jm-checktag {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-checktag {
    transition: none;
  }
}
</style>
