<script setup lang="ts">
import { computed } from 'vue'
import { hexToRgba, toCssSize } from '../utils'
import { vRipple } from '../utils/ripple'

defineOptions({ name: 'JmButton' })

type ButtonType = 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
type ButtonVariant = 'solid' | 'outline' | 'ghost' | 'text'
type ButtonSize = 'small' | 'medium' | 'large'

const props = withDefaults(
  defineProps<{
    type?: ButtonType
    variant?: ButtonVariant
    size?: ButtonSize
    /** 圆角：数字按 px，字符串原样透传（如 '50%' / '12px'） */
    radius?: number | string
    /** 胶囊形态：radius 传了这个属性时以 radius 为准 */
    round?: boolean
    block?: boolean
    disabled?: boolean
    loading?: boolean
    /** 水波纹触感，移动端建议保留（关掉动效时自动不出现） */
    ripple?: boolean
    /** 自定义颜色，自动派生浅底与描边 */
    color?: string
    nativeType?: 'button' | 'submit' | 'reset'
  }>(),
  {
    type: 'default',
    variant: 'solid',
    size: 'medium',
    ripple: true,
    nativeType: 'button',
  },
)

const emit = defineEmits<{ click: [event: MouseEvent] }>()

const classes = computed(() => [
  `jm-button--${props.type}`,
  `jm-button--${props.variant}`,
  `jm-button--${props.size}`,
  `jm--${props.type}`,
  {
    'is-block': props.block,
    'is-round': props.round,
    'is-disabled': props.disabled,
    'is-loading': props.loading,
    'has-ripple': props.ripple,
  },
])

const rippleBinding = computed(() => ({
  disabled: !props.ripple || !!props.disabled || !!props.loading,
}))

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-button-radius'] = r
  if (props.color) {
    s['--jm-local-color'] = props.color
    s['--jm-local-light'] = hexToRgba(props.color, 0.12)
    s['--jm-local-border'] = hexToRgba(props.color, 0.4)
    s['--jm-local-contrast'] = '#ffffff'
  }
  return s
})

function handleClick(e: MouseEvent) {
  if (props.disabled || props.loading) {
    e.stopPropagation()
    e.preventDefault()
    return
  }
  emit('click', e)
}
</script>

<template>
  <button
    v-ripple="rippleBinding"
    class="jm-button"
    :class="classes"
    :style="styles"
    :type="nativeType"
    :disabled="disabled || loading"
    :aria-disabled="disabled || loading || undefined"
    :aria-busy="loading || undefined"
    @click="handleClick"
  >
    <span v-if="loading" class="jm-button__spinner" aria-hidden="true" />
    <span v-else-if="$slots.icon" class="jm-button__icon" aria-hidden="true">
      <slot name="icon" />
    </span>
    <span class="jm-button__text"><slot /></span>
  </button>
</template>

<style>
.jm-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  /* 按压反馈：默认只压暗、不改几何尺寸。
     对整个按钮做 scale 会把文字一起缩放，字形需要重新栅格化，
     在小字号 + 高 DPR 屏上表现为"字忽大忽小、像在跳"，所以默认关掉。
     想要 iOS 那种回弹手感，把 --jm-button-press-scale 设成 0.97 即可恢复。 */
  --jm-button-press-scale: 1;
  --jm-button-press-overlay: 0.12;
  gap: 6px;
  height: var(--jm-control-height-md);
  padding: 0 18px;
  margin: 0;
  border: var(--jm-border-width) solid transparent;
  border-radius: var(--jm-button-radius, var(--jm-radius));
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1;
  letter-spacing: 0.2px;
  background: transparent;
  color: var(--jm-text-color);
  outline: none;
  cursor: pointer;
  -webkit-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  transition:
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    background-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    border-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    box-shadow var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-button__text {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
}

.jm-button__icon {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  font-size: 1.1em;
}

/**
 * 按压覆盖层
 * 用一层纯色薄幕表达"按下去了"，按钮的宽高、文字位置、字形都不发生任何变化，
 * 因此不会出现缩放导致的重排与字形重栅格化。文案和图标始终是静止且锐利的。
 * z-index: 0 让它落在文字之下：白字保持纯白，只有底色变深，对比度不因按压而下降。
 */
.jm-button::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  background: #000;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

/* 浅色底的按钮不压黑，改用主色薄涂，按压时能看出"这是它的颜色" */
.jm-button--outline::after,
.jm-button--ghost::after,
.jm-button--text::after,
.jm-button--solid.jm-button--default::after {
  background: currentColor;
}

.jm-button:not(.is-disabled):active::after {
  opacity: var(--jm-button-press-overlay);
}

/* 有水波纹时，底色压暗减半：波纹本身就是"按下"的反馈，两层都重会显得脏 */
.jm-button.has-ripple {
  --jm-button-press-overlay: 0.06;
}

.jm-button--outline:not(.is-disabled):active::after,
.jm-button--ghost:not(.is-disabled):active::after,
.jm-button--text:not(.is-disabled):active::after {
  opacity: calc(var(--jm-button-press-overlay) * 0.8);
}

.jm-button:focus-visible {
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

/* ---------- 尺寸 ---------- */
.jm-button--small {
  height: var(--jm-control-height-sm);
  padding: 0 12px;
  font-size: var(--jm-font-size-sm);
  gap: 4px;
}

.jm-button--large {
  height: var(--jm-control-height-lg);
  padding: 0 22px;
  font-size: var(--jm-font-size-lg);
  gap: 8px;
}

.jm-button.is-block {
  display: flex;
  width: 100%;
}

/* 胶囊：radius 属性显式传值时以内联样式为准 */
.jm-button.is-round {
  --jm-button-radius: var(--jm-radius-round);
}

/* ---------- 样式：实心 ---------- */
.jm-button--solid.jm-button--default {
  background: var(--jm-bg-container);
  color: var(--jm-text-color);
  border-color: var(--jm-border-color-2);
}

.jm-button--solid:not(.jm-button--default) {
  background: var(--jm-local-color);
  color: var(--jm-local-contrast);
  border-color: var(--jm-local-color);
  box-shadow: var(--jm-shadow-1);
}

/* ---------- 样式：描边 ---------- */
.jm-button--outline {
  background: transparent;
  color: var(--jm-local-color);
  border-color: var(--jm-local-color);
}

.jm-button--outline.jm-button--default {
  background: var(--jm-bg-container);
  color: var(--jm-text-color);
  border-color: var(--jm-border-color-2);
}

/* ---------- 样式：浅底 ---------- */
.jm-button--ghost {
  background: var(--jm-local-light);
  color: var(--jm-local-color);
  border-color: transparent;
}

/* ---------- 样式：纯文字 ---------- */
.jm-button--text {
  height: auto;
  min-height: var(--jm-control-height-sm);
  padding: 0 6px;
  background: transparent;
  color: var(--jm-local-color);
  border-color: transparent;
}

.jm-button--text.jm-button--default {
  color: var(--jm-text-color-2);
}

/* ---------- 交互 ---------- */
/* 悬停与按压都只改底色，不改透明度、不改尺寸：文字亮度始终不变 */
@media (hover: hover) {
  .jm-button:not(.is-disabled):hover::after {
    opacity: calc(var(--jm-button-press-overlay) * 0.55);
  }

  .jm-button--text:not(.is-disabled):hover {
    background: var(--jm-bg-hover);
  }

  .jm-button--text:not(.is-disabled):hover::after {
    opacity: 0;
  }
}

.jm-button:not(.is-disabled):active {
  /* 默认值为 1（不缩放）；业务方显式设成 0.97 才会走缩放 */
  transform: scale(var(--jm-button-press-scale));
}

.jm-button--text:not(.is-disabled):active {
  transform: none;
}

.jm-button.is-disabled {
  cursor: not-allowed;
  opacity: 0.45;
  transform: none;
  box-shadow: none;
}

.jm-button.is-loading {
  cursor: default;
}

/* ---------- 加载态 ---------- */
.jm-button__spinner {
  position: relative;
  z-index: 1;
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  /* 加载指示属于"必要动效"，关闭动效时依然保留（WCAG 允许） */
  animation: jm-button-spin 0.7s linear infinite;
}

@keyframes jm-button-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
