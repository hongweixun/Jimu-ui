<script setup lang="ts">
import { computed, inject } from 'vue'
import { vRipple } from '../utils/ripple'
import { RADIO_GROUP_KEY, type RadioValue } from './radio-context'
import { FORM_KEY } from './form-context'

defineOptions({ name: 'JmRadio' })

const props = withDefaults(
  defineProps<{
    modelValue?: RadioValue
    value?: RadioValue
    label?: string
    disabled?: boolean
    size?: 'small' | 'medium' | 'large'
    color?: string
    /** 选中时的圆点样式 */
    dot?: 'solid' | 'ring'
    /** 选中后文字是否跟随主色（Varlet 的做法），改成 inherit 则文字保持常规色 */
    labelColor?: 'active' | 'inherit'
    /** 水波纹触感，关掉动效时自动不出现 */
    ripple?: boolean
  }>(),
  { size: 'medium', dot: 'solid', labelColor: 'inherit', ripple: true },
)

const emit = defineEmits<{
  'update:modelValue': [value: RadioValue]
  change: [value: RadioValue]
}>()

const group = inject(RADIO_GROUP_KEY, null)
const form = inject(FORM_KEY, null)

const checked = computed(() =>
  group ? group.value.value === props.value : props.modelValue === props.value,
)

const isDisabled = computed(() => props.disabled || form?.disabled.value || (group ? group.disabled.value : false))
const activeColor = computed(() => props.color || group?.color.value)
const styles = computed(() => (activeColor.value ? { '--jm-radio-active': activeColor.value } : {}))
const rippleBinding = computed(() => ({ disabled: !props.ripple || isDisabled.value }))

function onChange() {
  if (isDisabled.value) return
  if (group) group.select(props.value as RadioValue)
  else emit('update:modelValue', props.value as RadioValue)
  emit('change', props.value as RadioValue)
}
</script>

<template>
  <label
    class="jm-radio"
    :class="[
      `jm-radio--${size}`,
      `jm-radio--label-${labelColor}`,
      { 'is-checked': checked, 'is-disabled': isDisabled },
    ]"
    :style="styles"
  >
    <input
      class="jm-radio__input"
      type="radio"
      :checked="checked"
      :disabled="isDisabled"
      @change="onChange"
    />
    <!-- action 是水波纹与 hover/focus 圆底的载体：外圈留白让圆形热区刚好压在图标上 -->
    <span class="jm-radio__action" v-ripple="rippleBinding">
      <!--
        图标用 SVG 绘制：HTML 小元素在分数像素（非整数 DPR、20px 内嵌 1.5px 边框）下
        两侧抗锯齿落点不同，圆点几何居中但看起来偏。SVG 由坐标系保证同心，永远不歪。
        环粗细仍可用 --jm-radio-border 调（映射为 stroke-width）。
      -->
      <svg class="jm-radio__icon" viewBox="0 0 24 24" aria-hidden="true">
        <circle class="jm-radio__track" cx="12" cy="12" r="11.25" />
        <circle
          v-if="dot === 'solid'"
          class="jm-radio__dot"
          cx="12"
          cy="12"
          r="7.2"
        />
        <circle v-else class="jm-radio__halo" cx="12" cy="12" r="6.6" />
      </svg>
    </span>
    <span v-if="label || $slots.default" class="jm-radio__label">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<style>
/**
 * Radio
 * ---------------------------------------------------------------------------
 * 视觉参照 Varlet：
 *   · 图标外再包一层圆形 action（图标 + 内边距），点击时从这里散开水波纹
 *   · 文案保持常规色，只有图标变色（Varlet 同款），label-color="active" 可让文字一起亮
 *   · 左侧负外边距抵消 action 的留白，让图标与周围文字视觉对齐
 * 勾选标记本身保留自己的弹簧曲线：从 0 弹到 1，比 Varlet 的图标硬切换更有确认感。
 */
.jm-radio {
  --jm-radio-size: 24px;
  --jm-radio-action-padding: 5px;
  --jm-radio-border: 1.5px;
  /* 环粗细可覆盖：--jm-radio-border: 3px */

  display: inline-flex;
  align-items: center;
  /* action 的 6px 内边距本身就是图标到文字的距离，不再叠加 gap */
  gap: 0;
  min-height: var(--jm-tap-min);
  /* 抵消 action 的圆形留白，图标左缘与不带 action 的元素（如 Cell 文案）对齐 */
  margin-left: calc(-1 * var(--jm-radio-action-padding));
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-radio__input {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  border: 0;
}

.jm-radio__action {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  padding: var(--jm-radio-action-padding);
  border-radius: 50%;
  /* 未选中环用深灰（Varlet 是 #555 级别），浅灰会显得发虚 */
  color: var(--jm-radio-unchecked, var(--jm-text-color-3));
  transition: color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
  -webkit-tap-highlight-color: transparent;
}

.jm-radio__icon {
  position: relative;
  z-index: 1;
  display: block;
  flex: 0 0 auto;
  width: var(--jm-radio-size);
  height: var(--jm-radio-size);
  overflow: visible;
}

/* 外环：stroke-width 读 --jm-radio-border（SVG 里 1px = 1 个 viewBox 单位，
   随图标尺寸等比缩放），粗细照旧可用这个变量调 */
.jm-radio__track {
  fill: none;
  stroke: currentColor;
  stroke-width: var(--jm-radio-border);
}

/* 选中圆点 / 空心环：绕自身圆心缩放（fill-box + center），
   弹簧动画照旧，几何上与外环绝对同心 */
.jm-radio__dot {
  fill: var(--jm-radio-active, var(--jm-color-primary));
  transform-box: fill-box;
  transform-origin: center;
  transform: scale(0);
  transition: transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease);
}

.jm-radio__halo {
  fill: none;
  stroke: var(--jm-radio-active, var(--jm-color-primary));
  stroke-width: 3;
  transform-box: fill-box;
  transform-origin: center;
  transform: scale(0);
  transition: transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease);
}

.jm-radio.is-checked .jm-radio__action {
  color: var(--jm-radio-active, var(--jm-color-primary));
}

.jm-radio.is-checked .jm-radio__dot,
.jm-radio.is-checked .jm-radio__halo {
  transform: scale(1);
}

.jm-radio__label {
  line-height: var(--jm-line-height);
  transition: color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-radio--label-active.is-checked .jm-radio__label {
  color: var(--jm-radio-active, var(--jm-color-primary));
}

.jm-radio--small {
  --jm-radio-size: 20px;
  --jm-radio-action-padding: 4px;
  min-height: 36px;
  font-size: var(--jm-font-size-sm);
}

.jm-radio--large {
  --jm-radio-size: 28px;
  --jm-radio-border: 1.75px;
  font-size: var(--jm-font-size-lg);
}

/* 按下时图标收一下：只缩图标，不动文字，避免整行跟着抖 */
.jm-radio:active:not(.is-disabled) .jm-radio__icon {
  transform: scale(0.92);
}

.jm-radio__input:focus-visible + .jm-radio__action {
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

.jm-radio.is-disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
</style>
