<script setup lang="ts">
import { computed, onBeforeUnmount, watch } from 'vue'
import JmIcon from './Icon.vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmNotify' })

const props = withDefaults(
  defineProps<{
    show?: boolean
    /** 主题色，决定左侧图标与默认底色 */
    type?: 'primary' | 'success' | 'warning' | 'danger'
    title?: string
    message?: string
    /** 自动关闭毫秒数，0 表示不自动关 */
    duration?: number
    closeable?: boolean
    /** 自定义图标名，覆盖 type 推导出的图标 */
    icon?: string
    color?: string
    background?: string
    /** 顶部留出安全区（刘海屏 / 状态栏） */
    safeAreaInsetTop?: boolean
    /** 面板层级 */
    zIndex?: number
    /** false 时不挂到 body，跟着父容器走（演示框里用） */
    teleport?: boolean | string | Element
    /** 静态流式布局：不再 fixed，用于自定义容器内的堆叠渲染 */
    inline?: boolean
  }>(),
  {
    show: false,
    type: 'danger',
    duration: 3000,
    closeable: true,
    safeAreaInsetTop: false,
    teleport: true,
    inline: false,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  click: [event: MouseEvent]
  close: []
  closed: []
}>()

const ICONS: Record<string, string> = {
  primary: 'info',
  success: 'check-circle',
  warning: 'warning',
  danger: 'close-circle',
}

const iconName = computed(() => props.icon ?? ICONS[props.type] ?? 'info')

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.color) s['--jm-notify-color'] = props.color
  if (props.background) s['--jm-notify-bg'] = props.background
  if (props.zIndex !== undefined) s.zIndex = String(props.zIndex)
  return s
})

let timer: ReturnType<typeof setTimeout> | null = null

function clearTimer() {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
}

function close() {
  clearTimer()
  emit('update:show', false)
  emit('close')
}

watch(
  () => [props.show, props.duration] as const,
  ([show]) => {
    clearTimer()
    if (show && props.duration > 0) {
      timer = setTimeout(close, props.duration)
    }
  },
  { immediate: true },
)

onBeforeUnmount(clearTimer)
</script>

<template>
  <Teleport to="body" :disabled="inline || !teleport">
    <Transition name="jm-notify-slide" @after-leave="emit('closed')">
      <div
        v-if="show"
        class="jm-notify"
        :class="[`jm-notify--${type}`, { 'is-inline': inline, 'has-safe-top': safeAreaInsetTop }]"
        :style="styles"
        role="alert"
        aria-live="assertive"
        @click="emit('click', $event)"
      >
        <span class="jm-notify__icon" aria-hidden="true">
          <jm-icon :name="iconName" size="18px" :stroke-width="1.9" />
        </span>
        <div class="jm-notify__body">
          <div v-if="title || $slots.title" class="jm-notify__title">
            <slot name="title">{{ title }}</slot>
          </div>
          <div v-if="message || $slots.default" class="jm-notify__message">
            <slot>{{ message }}</slot>
          </div>
        </div>
        <button
          v-if="closeable"
          type="button"
          class="jm-notify__close"
          aria-label="关闭"
          @click.stop="close"
        >
          <jm-icon name="close" size="14px" :stroke-width="2.2" />
        </button>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
.jm-notify {
  --jm-notify-color: #fff;
  --jm-notify-bg: var(--jm-color-danger);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 2100;
  display: flex;
  align-items: flex-start;
  gap: var(--jm-space-2);
  padding: 11px var(--jm-space-4);
  box-sizing: border-box;
  background: var(--jm-notify-bg);
  color: var(--jm-notify-color);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  line-height: 1.5;
  box-shadow: var(--jm-shadow-2);
}

/* 演示框 / 自定义容器内的渲染：交给外层容器定位 */
.jm-notify.is-inline {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  width: auto;
  box-shadow: none;
}

.jm-notify.has-safe-top {
  padding-top: calc(11px + env(safe-area-inset-top, 0px));
}

.jm-notify--primary {
  --jm-notify-bg: var(--jm-color-primary);
}

.jm-notify--success {
  --jm-notify-bg: var(--jm-color-success);
}

.jm-notify--warning {
  --jm-notify-bg: var(--jm-color-warning);
  --jm-notify-color: #3a2a00;
}

.jm-notify--danger {
  --jm-notify-bg: var(--jm-color-danger);
}

.jm-notify__icon {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  height: 21px;
  color: currentColor;
}

.jm-notify__body {
  flex: 1 1 0%;
  min-width: 0;
}

.jm-notify__title {
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.4;
}

.jm-notify__message {
  word-break: break-word;
  opacity: 0.95;
}

.jm-notify__title + .jm-notify__message {
  margin-top: 2px;
  font-size: var(--jm-font-size-xs);
  opacity: 0.88;
}

.jm-notify__close {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 21px;
  padding: 0;
  border: 0;
  background: none;
  color: currentColor;
  opacity: 0.8;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-notify__close:active {
  opacity: 1;
}

/* 从顶部滑入、滑出，位移用 translate3d 走合成层 */
.jm-notify-slide-enter-active,
.jm-notify-slide-leave-active {
  transition:
    transform var(--jm-duration-3) var(--jm-motion-enter-ease),
    opacity var(--jm-duration-2) var(--jm-motion-enter-ease);
  will-change: transform, opacity;
}

.jm-notify-slide-leave-active {
  transition:
    transform 200ms var(--jm-motion-exit-ease),
    opacity 200ms var(--jm-motion-exit-ease);
}

.jm-notify-slide-enter-from,
.jm-notify-slide-leave-to {
  transform: translate3d(0, -100%, 0);
  opacity: 0.6;
}

[data-motion='off'] .jm-notify-slide-enter-active,
[data-motion='off'] .jm-notify-slide-leave-active {
  transition: opacity 120ms linear;
}

[data-motion='off'] .jm-notify-slide-enter-from,
[data-motion='off'] .jm-notify-slide-leave-to {
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-notify-slide-enter-active,
  .jm-notify-slide-leave-active {
    transition: opacity 120ms linear;
  }

  .jm-notify-slide-enter-from,
  .jm-notify-slide-leave-to {
    transform: none;
  }
}
</style>
