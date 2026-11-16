<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import { FORM_ITEM_KEY, FORM_KEY } from './form-context'

defineOptions({ name: 'JmSwitch' })

const props = withDefaults(
  defineProps<{
    modelValue?: boolean
    disabled?: boolean
    loading?: boolean
    size?: 'small' | 'medium' | 'large'
    /** 打开时的颜色，默认走主题主色 */
    activeColor?: string
    inactiveColor?: string
    activeText?: string
    inactiveText?: string
    /**
     * 切换前钩子：返回 false 取消本次切换；
     * 返回 Promise 时开关进入 loading，等结果再落状态（适合先调接口再放开）
     */
    beforeChange?: (value: boolean) => boolean | void | Promise<boolean | void>
  }>(),
  { modelValue: false, size: 'medium' },
)

/* 放在 FormItem 里时，切换后立刻按 change 时机校验 */
const formItem = inject(FORM_ITEM_KEY, null)
const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || formItem?.disabled.value || false)


const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  change: [value: boolean]
  click: [event: MouseEvent]
}>()

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.activeColor) s['--jm-switch-active'] = props.activeColor
  if (props.inactiveColor) s['--jm-switch-inactive'] = props.inactiveColor
  return s
})

const text = computed(() => (props.modelValue ? props.activeText : props.inactiveText))

/** 钩子返回 Promise / 业务传 loading 期间的中间态 */
const pending = ref(false)
const isBusy = computed(() => pending.value || props.loading)

async function onToggle(e: MouseEvent) {
  if (disabled.value || isBusy.value) return
  const next = !props.modelValue

  const hook = props.beforeChange
  if (hook) {
    try {
      pending.value = true
      const result = await hook(next)
      if (result === false) return
    } catch {
      return
    } finally {
      pending.value = false
    }
  }

  emit('update:modelValue', next)
  emit('change', next)
  emit('click', e)
  formItem?.onChange()
}
</script>

<template>
  <button
    type="button"
    role="switch"
    class="jm-switch"
    :class="[`jm-switch--${size}`, { 'is-checked': modelValue, 'is-disabled': disabled }]"
    :style="styles"
    :aria-checked="modelValue"
    :aria-busy="isBusy"
    :disabled="disabled || isBusy"
    @click="onToggle"
  >
    <span class="jm-switch__track">
      <span class="jm-switch__handle">
        <span v-if="isBusy" class="jm-switch__loading" aria-hidden="true" />
      </span>
    </span>
    <span v-if="text" class="jm-switch__text">{{ text }}</span>
  </button>
</template>

<style>
.jm-switch {
  --jm-switch-travel: 20px;
  display: inline-flex;
  align-items: center;
  gap: var(--jm-space-2);
  padding: 0;
  margin: 0;
  border: 0;
  background: none;
  font-family: var(--jm-font-family);
  cursor: pointer;
  outline: none;
  -webkit-tap-highlight-color: transparent;
}

.jm-switch__track {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 26px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-switch-inactive, var(--jm-gray-400));
  transition:
    background-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    box-shadow var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-switch__handle {
  position: absolute;
  top: 2px;
  left: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(16, 21, 26, 0.24);
  /* 滑块走弹性曲线：过冲一点点，手感像有惯性 */
  transform-origin: left center;
  transition: transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease);
  will-change: transform;
}

.jm-switch__loading {
  width: 12px;
  height: 12px;
  border: 1.5px solid var(--jm-switch-active, var(--jm-color-primary));
  border-top-color: transparent;
  border-radius: 50%;
  animation: jm-switch-spin 0.7s linear infinite;
}

@keyframes jm-switch-spin {
  to {
    transform: rotate(360deg);
  }
}

.jm-switch.is-checked .jm-switch__track {
  background: var(--jm-switch-active, var(--jm-color-primary));
}

.jm-switch.is-checked .jm-switch__handle {
  transform: translateX(var(--jm-switch-travel));
  /* 选中后从左锚点换到右锚点，按下拉伸时才是朝"开"的方向变长 */
  transform-origin: right center;
}

.jm-switch__text {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
  white-space: nowrap;
}

.jm-switch--small {
  --jm-switch-travel: 16px;
}

.jm-switch--small .jm-switch__track {
  width: 36px;
  height: 20px;
}

.jm-switch--small .jm-switch__handle {
  width: 16px;
  height: 16px;
}

.jm-switch--large {
  --jm-switch-travel: 24px;
}

.jm-switch--large .jm-switch__track {
  width: 56px;
  height: 32px;
}

.jm-switch--large .jm-switch__handle {
  width: 28px;
  height: 28px;
}

.jm-switch:focus-visible .jm-switch__track {
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

/* 按下时轻微拉伸：用 transform 而不是 width，避免每帧触发布局重排 */
.jm-switch:active:not(.is-disabled) .jm-switch__handle {
  transform: scaleX(1.14);
}

.jm-switch.is-checked:active:not(.is-disabled) .jm-switch__handle {
  transform: translateX(var(--jm-switch-travel)) scaleX(1.14);
}

.jm-switch.is-disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
</style>
