<script setup lang="ts">
import { computed, inject, ref, watch } from 'vue'
import { FORM_ITEM_KEY, FORM_KEY } from './form-context'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmStepper' })

const props = withDefaults(
  defineProps<{
    modelValue?: number
    /** 最小值 */
    min?: number
    /** 最大值 */
    max?: number
    /** 步长 */
    step?: number
    /** 只允许整数（false 时可输入小数） */
    integer?: boolean
    disabled?: boolean
    /** 禁止手动输入，只能点按钮加减 */
    disableInput?: boolean
    /** 输入框宽度，数字按 px */
    inputWidth?: number | string
    /** 按钮尺寸（正方形边长），数字按 px */
    buttonSize?: number | string
  }>(),
  { modelValue: 1, min: 1, max: Infinity, step: 1, integer: true },
)

const emit = defineEmits<{
  'update:modelValue': [value: number]
  change: [value: number]
  /** 点击加减按钮后超出 min/max 范围时触发（值不变） */
  'over-limit': [action: 'minus' | 'plus']
  blur: [event: FocusEvent]
}>()

/* 放在 FormItem 里时，值变化触发 change 时机校验 */
const formItem = inject(FORM_ITEM_KEY, null)
const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || formItem?.disabled.value || false)


/** 输入框里的实时草稿：允许输入过程中的中间态（如清空、打半截数字） */
const draft = ref<string | null>(null)
const focused = ref(false)

const displayValue = computed(() => (draft.value !== null ? draft.value : String(props.modelValue ?? '')))

const canMinus = computed(() => !disabled.value && props.modelValue - props.step >= props.min)
const canPlus = computed(() => !disabled.value && props.modelValue + props.step <= props.max)

function clamp(v: number) {
  let next = v
  if (!props.integer && props.step < 1) {
    /* 小数步长时对齐到步长精度，避免 0.1 + 0.2 的浮点尾巴 */
    const decimals = (String(props.step).split('.')[1] || '').length
    next = Number(next.toFixed(decimals))
  }
  return Math.min(props.max, Math.max(props.min, next))
}

function commit(v: number) {
  const next = clamp(v)
  const changed = next !== props.modelValue
  emit('update:modelValue', next)
  if (changed) {
    emit('change', next)
    formItem?.onChange()
  }
}

function onMinus() {
  if (disabled.value) return
  if (!canMinus.value) {
    emit('over-limit', 'minus')
    return
  }
  commit(props.modelValue - props.step)
}

function onPlus() {
  if (disabled.value) return
  if (!canPlus.value) {
    emit('over-limit', 'plus')
    return
  }
  commit(props.modelValue + props.step)
}

function onInput(e: Event) {
  const el = e.target as HTMLInputElement
  const raw = el.value
  /* 允许输入中的中间态：负号、小数点、空串都先放行 */
  const pattern = props.integer ? /^-?\d*$/ : /^-?\d*\.?\d*$/
  if (raw !== '' && !pattern.test(raw)) {
    el.value = displayValue.value
    return
  }
  draft.value = raw
}

function onBlur(e: FocusEvent) {
  focused.value = false
  draft.value = null
  const parsed = Number(displayValue.value)
  if (displayValue.value === '' || Number.isNaN(parsed)) {
    commit(props.min)
  } else {
    commit(props.integer ? Math.round(parsed) : parsed)
  }
  emit('blur', e)
  formItem?.onBlur()
}

function onFocus() {
  focused.value = true
  /* 聚焦时把当前值放进草稿，避免模型值和显示值打架 */
  draft.value = String(props.modelValue ?? '')
}

/* 外部改值时退出草稿态 */
watch(
  () => props.modelValue,
  () => {
    if (!focused.value) draft.value = null
  },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const w = typeof props.inputWidth === 'number' ? `${props.inputWidth}px` : props.inputWidth
  if (w) s['--jm-stepper-input-width'] = w
  const b = typeof props.buttonSize === 'number' ? `${props.buttonSize}px` : props.buttonSize
  if (b) s['--jm-stepper-button-size'] = b
  return s
})
</script>

<template>
  <div class="jm-stepper" :class="{ 'is-disabled': disabled }" :style="styles" role="group" aria-label="步进器">
    <button
      type="button"
      class="jm-stepper__btn"
      :class="{ 'is-limit': !canMinus && !disabled }"
      :disabled="disabled || !canMinus"
      aria-label="减少"
      @click="onMinus"
    >
      <jm-icon name="minus" size="14px" :stroke-width="2.6" />
    </button>

    <input
      class="jm-stepper__input"
      type="text"
      :value="displayValue"
      :disabled="disabled"
      :readonly="disableInput"
      :inputmode="integer ? 'numeric' : 'decimal'"
      aria-label="当前值"
      @input="onInput"
      @focus="onFocus"
      @blur="onBlur"
    />

    <button
      type="button"
      class="jm-stepper__btn"
      :class="{ 'is-limit': !canPlus && !disabled }"
      :disabled="disabled || !canPlus"
      aria-label="增加"
      @click="onPlus"
    >
      <jm-icon name="plus" size="14px" :stroke-width="2.6" />
    </button>
  </div>
</template>

<style>
/**
 * Stepper 步进器
 * --------------------------------------------------------------------------- */
.jm-stepper {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-family: var(--jm-font-family);
  -webkit-tap-highlight-color: transparent;
}

.jm-stepper__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: var(--jm-stepper-button-size, calc(28px * var(--jm-size-scale)));
  height: var(--jm-stepper-button-size, calc(28px * var(--jm-size-scale)));
  padding: 0;
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: var(--jm-bg-input);
  color: var(--jm-text-color);
  cursor: pointer;
  transition:
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-stepper__btn:active {
  background: var(--jm-bg-active);
}

.jm-stepper__btn:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

/* 到达边界但未被禁用（disabled=false 且已到 min/max）：压淡提示不可再加 */
.jm-stepper__btn.is-limit {
  color: var(--jm-text-color-4);
}

.jm-stepper__input {
  width: var(--jm-stepper-input-width, calc(32px * var(--jm-size-scale)));
  height: var(--jm-stepper-button-size, calc(28px * var(--jm-size-scale)));
  padding: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--jm-text-color);
  font-family: var(--jm-font-family-number, inherit);
  font-size: var(--jm-font-size-md);
  font-variant-numeric: tabular-nums;
  text-align: center;
  -webkit-appearance: none;
  appearance: none;
}

.jm-stepper__input:disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-stepper__input:read-only {
  cursor: default;
}

.jm-stepper.is-disabled {
  opacity: 0.6;
}
</style>
