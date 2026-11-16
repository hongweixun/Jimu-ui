<script setup lang="ts">
import { computed, useAttrs } from 'vue'
import JmPopup from './Popup.vue'
import type { ActionSheetAction } from '../types'
import { toCssSize } from '../utils'
import { vRipple } from '../utils/ripple'

/* 根是 Teleport，属性透传会丢；手动转发到内部面板，class/style 才能正常覆盖 */
defineOptions({ name: 'JmActionSheet', inheritAttrs: false })

const props = withDefaults(
  defineProps<{
    show?: boolean
    actions?: ActionSheetAction[]
    title?: string
    description?: string
    cancelText?: string
    /** 是否显示右上角关闭图标 */
    closeable?: boolean
    /** 关闭图标：字符串为 SVG 的 path d 值，复杂图标用 #close-icon 插槽整块替换 */
    closeIcon?: string
    round?: boolean
    closeOnClickAction?: boolean
    /** 取消按钮与列表之间留一条灰色间隙（Vant 同款），默认紧贴 */
    cancelGap?: boolean
    teleport?: boolean | string | Element
    /** 标题区背景：任意 CSS background 值，颜色、渐变、url(...) 都可 */
    titleBackground?: string
    /** 标题区背景图：图片地址（自动补 url()），盖在 title-background 之上 */
    titleImage?: string
    /** 标题文字颜色 */
    titleColor?: string
    /** 标题字号：数字按 px 处理 */
    titleSize?: number | string
    /** 面板整体背景：任意 CSS background 值（颜色 / 渐变 / url(...)） */
    background?: string
    /** 面板整体背景图：图片地址（自动补 url()），铺满整张面板 */
    backgroundImage?: string
    backgroundSize?: string
    backgroundPosition?: string
    /** 背景之上的压暗层，保证文字可读：0-1 数字生成黑色蒙层，也可传任意颜色/渐变 */
    backgroundMask?: string | number
    /** 按 Esc 关闭（走关闭按钮同一条路径） */
    closeOnEsc?: boolean
    /** 键盘焦点锁在面板内，关闭时归还触发元素 */
    trapFocus?: boolean
  }>(),
  {
    actions: () => [],
    cancelText: '取消',
    closeable: false,
    closeIcon: 'M6 6l12 12M18 6L6 18',
    cancelGap: false,
    round: true,
    closeOnClickAction: true,
    teleport: true,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    closeOnEsc: true,
    trapFocus: true,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  select: [action: ActionSheetAction, index: number]
  cancel: []
}>()

/** 已是 CSS 函数（url()/渐变等）就原样用，纯路径补 url() —— 让「传路径」和「传完整值」都成立 */
const CSS_FN = /^(url|(repeating-)?(linear|radial|conic)-gradient|image-set|cross-fade)\(/i

function toImage(value: string): string {
  const v = value.trim()
  return CSS_FN.test(v) ? v : `url("${v}")`
}

const hasHeader = computed(() => !!(props.title || props.description || props.closeable))

const panelStyle = computed<Record<string, string>>(() => {
  const s: Record<string, string> = {}
  if (props.background) s.background = props.background
  if (props.backgroundImage) {
    s.backgroundImage = toImage(props.backgroundImage)
    s.backgroundSize = props.backgroundSize
    s.backgroundPosition = props.backgroundPosition
  }
  return s
})

const headerStyle = computed<Record<string, string>>(() => {
  const s: Record<string, string> = {}
  if (props.titleBackground) s.background = props.titleBackground
  if (props.titleImage) {
    s.backgroundImage = toImage(props.titleImage)
    s.backgroundSize = props.backgroundSize
    s.backgroundPosition = props.backgroundPosition
  }
  if (props.titleColor) s.color = props.titleColor
  const size = toCssSize(props.titleSize)
  if (size) s.fontSize = size
  return s
})

/** 蒙层：数字当透明度生成黑色遮罩，字符串直接当 background 值（可传渐变做上下渐隐） */
const maskStyle = computed<Record<string, string> | undefined>(() => {
  const m = props.backgroundMask
  if (m === undefined || m === '') return undefined
  return { background: typeof m === 'number' ? `rgba(0, 0, 0, ${m})` : m }
})

const attrs = useAttrs()
const restAttrs = computed(() => {
  const { style: _style, ...rest } = attrs as Record<string, unknown>
  return rest
})
const mergedStyle = computed(() => [attrs.style as unknown as string, panelStyle.value])

function onSelect(action: ActionSheetAction, index: number) {
  if (action.disabled || action.loading) return
  emit('select', action, index)
  if (props.closeOnClickAction) emit('update:show', false)
}

function onCancel() {
  emit('cancel')
  emit('update:show', false)
}

function onShowChange(v: boolean) {
  emit('update:show', v)
}
</script>

<template>
  <JmPopup
    :show="show"
    position="bottom"
    :round="round"
    :teleport="teleport"
    :close-on-esc="closeOnEsc"
    :trap-focus="trapFocus"
    :aria-label="title || '操作面板'"
    @update:show="onShowChange"
  >
    <div class="jm-action-sheet" :class="{ 'has-cancel-gap': cancelGap }" v-bind="restAttrs" :style="mergedStyle">
      <!-- 背景压暗层：在背景图之上、内容之下，不拦截点击 -->
      <div v-if="maskStyle" class="jm-action-sheet__scrim" :style="maskStyle" aria-hidden="true" />

      <button
        v-if="closeable"
        type="button"
        class="jm-action-sheet__close"
        aria-label="关闭"
        @click="onCancel"
      >
        <slot name="close-icon">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              :d="closeIcon"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />
          </svg>
        </slot>
      </button>

      <div
        v-if="hasHeader"
        class="jm-action-sheet__header"
        :class="{ 'has-close': closeable }"
        :style="headerStyle"
      >
        <slot name="header">
          <div v-if="title" class="jm-action-sheet__title">{{ title }}</div>
          <div v-if="description" class="jm-action-sheet__subtitle">{{ description }}</div>
          <slot name="description" />
        </slot>
      </div>

      <div class="jm-action-sheet__list">
        <button
          v-for="(action, index) in actions"
          :key="action.name ?? index"
          v-ripple="{ disabled: !!action.disabled }"
          type="button"
          class="jm-action-sheet__item"
          :class="{ 'is-disabled': action.disabled, 'is-loading': action.loading }"
          :style="action.color ? { color: action.color } : undefined"
          :disabled="action.disabled || action.loading"
          @click="onSelect(action, index)"
        >
          <span class="jm-action-sheet__item-label">
            <span v-if="action.loading" class="jm-action-sheet__spinner" aria-hidden="true" />
            <svg
              v-else-if="action.icon"
              class="jm-action-sheet__item-icon"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                :d="action.icon"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            {{ action.label }}
          </span>
          <span v-if="action.subLabel" class="jm-action-sheet__item-sub">{{ action.subLabel }}</span>
        </button>

        <slot />
      </div>

      <div v-if="cancelText && cancelGap" class="jm-action-sheet__gap" aria-hidden="true" />

      <button
        v-if="cancelText"
        v-ripple
        type="button"
        class="jm-action-sheet__cancel"
        :class="{ 'is-gap': cancelGap }"
        @click="onCancel"
      >
        <slot name="cancel">{{ cancelText }}</slot>
      </button>
    </div>
  </JmPopup>
</template>

<style>
.jm-action-sheet {
  position: relative;
  display: flex;
  flex-direction: column;
  /* 内容多时限高滚动，不把整块顶穿屏幕 */
  max-height: var(--jm-action-sheet-max-height, 80vh);
  overflow: hidden;
  padding-bottom: var(--jm-space-2);
  background: var(--jm-bg-elevated);
  font-family: var(--jm-font-family);
  /* 弹层里的大面积条目，波纹比默认淡一档 */
  --jm-ripple-opacity: 0.1;
}

.jm-action-sheet__scrim {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.jm-action-sheet__header {
  position: relative;
  z-index: 1;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  justify-content: center;
  /* 只有关闭按钮、没有文案时也要留出够高的着陆区 */
  min-height: var(--jm-action-sheet-header-min-height, 52px);
  box-sizing: border-box;
  padding: var(--jm-space-4) var(--jm-space-4) var(--jm-space-3);
  text-align: center;
  border-bottom: 1px solid var(--jm-action-sheet-header-border, var(--jm-border-color));
}

/* 有关闭按钮时左右对称留白，标题不会视觉偏移 */
.jm-action-sheet__header.has-close {
  padding-left: calc(var(--jm-space-4) + 28px);
  padding-right: calc(var(--jm-space-4) + 28px);
}

.jm-action-sheet__title {
  font-size: var(--jm-action-sheet-title-size, var(--jm-font-size-md));
  font-weight: var(--jm-font-weight-medium);
  color: var(--jm-action-sheet-title-color, var(--jm-text-color));
  line-height: 1.4;
}

.jm-action-sheet__subtitle {
  margin-top: var(--jm-space-1);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-action-sheet-subtitle-color, var(--jm-text-color-3));
  line-height: 1.4;
}

/* 关闭按钮：贴面板右上角，没有 title 时也照样在 */
.jm-action-sheet__close {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--jm-action-sheet-close-color, var(--jm-text-color-3));
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

@media (hover: hover) {
  .jm-action-sheet__close:hover {
    color: var(--jm-text-color-2);
  }
}

.jm-action-sheet__close img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.jm-action-sheet__list {
  position: relative;
  z-index: 1;
  flex: 1 1 auto;
  padding: var(--jm-space-2) 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.jm-action-sheet__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  width: 100%;
  min-height: calc(52px * var(--jm-size-scale));
  padding: var(--jm-space-3) var(--jm-space-4);
  border: 0;
  background: none;
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

@media (hover: hover) {
  .jm-action-sheet__item:hover {
    background: var(--jm-bg-hover);
  }
}

.jm-action-sheet__item.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-action-sheet__item.is-loading {
  cursor: default;
}

.jm-action-sheet__item-label {
  display: inline-flex;
  align-items: center;
  gap: var(--jm-space-2);
  line-height: var(--jm-line-height);
}

.jm-action-sheet__item-icon {
  flex: 0 0 auto;
  width: 18px;
  height: 18px;
}

.jm-action-sheet__spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: jm-action-sheet-spin 700ms linear infinite;
}

@keyframes jm-action-sheet-spin {
  to {
    transform: rotate(360deg);
  }
}

.jm-action-sheet__item-sub {
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
}

/* 间隙模式：列表与取消按钮之间一条灰隙（Vant 同款），两块视觉上分离 */
.jm-action-sheet.has-cancel-gap {
  padding-bottom: 0;
}

.jm-action-sheet.has-cancel-gap .jm-action-sheet__list {
  padding-bottom: 0;
}

.jm-action-sheet__gap {
  flex: 0 0 auto;
  height: var(--jm-action-sheet-cancel-gap-height, 10px);
  /* gray-100：gray-50 太浅，白面板上几乎看不出来 */
  background: var(--jm-action-sheet-cancel-gap-bg, var(--jm-gray-100));
}

.jm-action-sheet__cancel {
  position: relative;
  z-index: 1;
  flex: 0 0 auto;
  width: 100%;
  min-height: calc(52px * var(--jm-size-scale));
  margin-top: var(--jm-space-2);
  border: 0;
  border-top: 1px solid var(--jm-action-sheet-header-border, var(--jm-border-color));
  background: none;
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  color: var(--jm-action-sheet-cancel-color, var(--jm-text-color-2));
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

/* 间隙模式：分隔线与外边距都交给灰隙，按钮自身干净贴合 */
.jm-action-sheet__cancel.is-gap {
  margin-top: 0;
  border-top: 0;
}
</style>
