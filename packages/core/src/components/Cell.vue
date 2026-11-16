<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'
import JmIcon from './Icon.vue'
import { vRipple } from '../utils/ripple'

defineOptions({ name: 'JmCell' })

const props = withDefaults(
  defineProps<{
    title?: string
    label?: string
    value?: string | number
    isLink?: boolean
    clickable?: boolean
    /** 点击水波纹，默认跟随 clickable 开启 */
    ripple?: boolean
    /** 底部细线，单独使用时才需要；放进 CellGroup 里由分组统一控制 */
    border?: boolean
    size?: 'small' | 'medium' | 'large'
    radius?: number | string
    align?: 'left' | 'right'
    /** 自定义背景色，适合做成卡片 */
    background?: string
  }>(),
  { size: 'medium', border: true, align: 'left' },
)

const emit = defineEmits<{ click: [event: MouseEvent] }>()

/** 可点击时默认带水波纹；显式传 ripple 可单独控制 */
const hasRipple = computed(() => props.ripple ?? props.clickable)

const rippleBinding = computed(() => ({ disabled: !hasRipple.value, centered: false }))

const classes = computed(() => [
  `jm-cell--${props.size}`,
  `jm-cell--align-${props.align}`,
  {
    'is-clickable': props.clickable,
    'is-link': props.isLink,
    'has-border': props.border,
    'has-ripple': hasRipple.value,
  },
])

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-cell-radius'] = r
  if (props.background) s['--jm-cell-bg'] = props.background
  return s
})

function onClick(e: MouseEvent) {
  if (!props.clickable) return
  emit('click', e)
}

function onEnter(e: KeyboardEvent) {
  if (!props.clickable) return
  emit('click', e as unknown as MouseEvent)
}
</script>

<template>
  <div
    v-ripple="rippleBinding"
    class="jm-cell"
    :class="classes"
    :style="styles"
    :role="clickable ? 'button' : undefined"
    :tabindex="clickable ? 0 : undefined"
    @click="onClick"
    @keydown.enter="onEnter"
  >
    <div v-if="$slots.icon" class="jm-cell__icon"><slot name="icon" /></div>

    <div class="jm-cell__body">
      <div class="jm-cell__content">
        <div class="jm-cell__title">
          <slot name="title">{{ title }}</slot>
        </div>
        <div v-if="label || $slots.label" class="jm-cell__label">
          <slot name="label">{{ label }}</slot>
        </div>
      </div>

      <div v-if="$slots.default || value !== undefined" class="jm-cell__value">
        <slot>{{ value }}</slot>
      </div>
    </div>

    <div v-if="$slots.right || isLink" class="jm-cell__right">
      <slot name="right" />
      <jm-icon v-if="isLink" class="jm-cell__arrow" name="chevron-right" size="18px" :stroke-width="1.8" />
    </div>
  </div>
</template>

<style>
.jm-cell {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--jm-space-3);
  width: 100%;
  min-height: var(--jm-cell-height);
  padding: 12px var(--jm-space-4);
  background: var(--jm-cell-bg, transparent);
  border-radius: var(--jm-cell-radius, 0);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  line-height: var(--jm-line-height);
  color: var(--jm-text-color);
  text-align: left;
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
  -webkit-tap-highlight-color: transparent;
}

.jm-cell.has-border::after {
  content: '';
  position: absolute;
  left: var(--jm-space-4);
  right: 0;
  bottom: 0;
  height: 1px;
  background: var(--jm-border-color);
  transform: scaleY(0.5);
  transform-origin: bottom;
}

.jm-cell__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  font-size: 20px;
  color: var(--jm-text-color-2);
}

.jm-cell__body {
  display: flex;
  align-items: center;
  gap: var(--jm-space-3);
  flex: 1;
  min-width: 0;
}

.jm-cell__content {
  flex: 1;
  min-width: 0;
}

.jm-cell__title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-cell__label {
  margin-top: 2px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
  line-height: 1.4;
}

.jm-cell__value {
  flex: 0 1 auto;
  max-width: 60%;
  color: var(--jm-text-color-2);
  font-size: var(--jm-font-size-sm);
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-cell__right {
  display: inline-flex;
  align-items: center;
  gap: var(--jm-space-1);
  flex: 0 0 auto;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
}

.jm-cell__arrow {
  width: 18px;
  height: 18px;
  color: var(--jm-text-color-4);
}

/* 尺寸 */
.jm-cell--small {
  min-height: calc(36px * var(--jm-size-scale));
  padding-top: 8px;
  padding-bottom: 8px;
  font-size: var(--jm-font-size-sm);
}

.jm-cell--large {
  min-height: calc(58px * var(--jm-size-scale));
  padding-top: 16px;
  padding-bottom: 16px;
  font-size: var(--jm-font-size-lg);
}

/* 对齐 */
.jm-cell--align-right .jm-cell__title {
  text-align: right;
}

/* 交互 */
.jm-cell.is-clickable {
  cursor: pointer;
}

@media (hover: hover) {
  .jm-cell.is-clickable:hover {
    background: var(--jm-cell-bg, var(--jm-bg-hover));
  }
}

.jm-cell.is-clickable:active {
  background: var(--jm-bg-active);
}

/* 有水波纹时不再叠底色变化：波纹已经是"按下"的反馈，两层一起会显脏 */
.jm-cell.is-clickable.has-ripple:active {
  background: var(--jm-cell-bg, transparent);
}

/* 单元格面积大，波纹压淡一档，避免盖住文字 */
.jm-cell.has-ripple {
  --jm-ripple-opacity: 0.12;
}

.jm-cell.is-clickable:focus-visible {
  outline: 2px solid var(--jm-color-primary);
  outline-offset: -2px;
}
</style>
