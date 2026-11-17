<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useId, watch } from 'vue'
import { useFocusTrap } from '../composables/useFocusTrap'
import { vRipple } from '../utils/ripple'
import { lockScroll, nextZIndex, toCssSize, unlockScroll } from '../utils'

defineOptions({ name: 'JmDialog' })

const props = withDefaults(
  defineProps<{
    show?: boolean
    title?: string
    message?: string
    showCancel?: boolean
    showConfirm?: boolean
    /** 按钮形态：text=分隔线文字按钮（默认），pill=胶囊，square=方形 */
    buttonStyle?: 'text' | 'pill' | 'square'
    confirmText?: string
    cancelText?: string
    round?: boolean
    mask?: boolean
    closeOnClickMask?: boolean
    lock?: boolean
    zIndex?: number
    confirmColor?: string
    cancelColor?: string
    radius?: number | string
    /** 竖排按钮：移动端长文案更稳 */
    verticalActions?: boolean
    /**
     * 点击按钮后先跑这个钩子，返回 false 阻止本次操作；
     * 返回 Promise 时按钮自动进入 loading，适合「提交后才关弹窗」的场景
     */
    beforeClose?: (action: 'confirm' | 'cancel') => boolean | void | Promise<boolean | void>
    /** 外部控制的确认按钮 loading（如接口请求中） */
    confirmButtonLoading?: boolean
    /** 外部控制的取消按钮 loading */
    cancelButtonLoading?: boolean
    /** 按 Esc 关闭（等同点取消；有 beforeClose 时同样走拦截） */
    closeOnEsc?: boolean
    /** 打开后是否把键盘焦点限制在弹窗内，并在关闭时归还给触发元素 */
    trapFocus?: boolean
    teleport?: boolean | string | Element
  }>(),
  {
    showCancel: true,
    showConfirm: true,
    buttonStyle: 'text',
    confirmText: '确定',
    cancelText: '取消',
    round: true,
    mask: true,
    closeOnClickMask: false,
    lock: true,
    zIndex: 1100,
    closeOnEsc: true,
    trapFocus: true,
    teleport: true,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  confirm: []
  cancel: []
  closed: []
}>()

/** 打开时领取递增层级，后开的弹层盖住先开的（与 Popup 同一套计数器） */
const zIndex = ref(props.zIndex)

/** 标题 / 正文的 id：给 role="dialog" 挂 aria-labelledby / aria-describedby */
const uid = useId()
const titleId = `jm-dialog-title-${uid}`
const messageId = `jm-dialog-message-${uid}`

const panelRef = ref<HTMLElement | null>(null)
const trap = useFocusTrap()

let locked = false

/** Esc 只关最上层：叠了多个弹窗时，底层不能抢按键 */
function onEsc(e: KeyboardEvent) {
  if (e.key !== 'Escape' || busy.value) return
  const panels = Array.from(document.querySelectorAll<HTMLElement>('.jm-dialog'))
  const top = panels.reduce((max, el) => Math.max(max, Number(getComputedStyle(el).zIndex) || 0), 0)
  if (top > zIndex.value) return
  e.stopPropagation()
  void handle('cancel')
}

watch(
  () => props.show,
  (v) => {
    if (typeof document === 'undefined') return
    if (v) {
      zIndex.value = Math.max(zIndex.value, props.zIndex, nextZIndex())
      if (props.closeOnEsc) document.addEventListener('keydown', onEsc, true)
      if (props.trapFocus) {
        // 面板要等 v-if 渲染出来才拿得到；再等一帧让进场动画完成，聚焦时不会连带动画跳一下
        nextTick(() => requestAnimationFrame(() => trap.activate(panelRef.value)))
      }
    } else {
      document.removeEventListener('keydown', onEsc, true)
      trap.deactivate()
    }
    if (!props.lock) return
    if (v && !locked) {
      lockScroll()
      locked = true
    } else if (!v && locked) {
      unlockScroll()
      locked = false
    }
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onEsc, true)
  if (locked) {
    unlockScroll()
    locked = false
  }
})

/* 初始就带 show 打开（非 v-model 切换）时，watcher 跑在 ref 赋值前，这里补一次 */
onMounted(() => {
  if (!props.show || !props.trapFocus) return
  nextTick(() => requestAnimationFrame(() => trap.activate(panelRef.value)))
})

function onCancel() {
  if (busy.value) return
  void handle('cancel')
}

function onConfirm() {
  if (busy.value) return
  void handle('confirm')
}

/** 内建 loading：beforeClose 返回 Promise 期间按钮自己转圈，不用业务再传 prop */
const pending = ref<'confirm' | 'cancel' | null>(null)

const confirmLoading = computed(() => !!props.confirmButtonLoading || pending.value === 'confirm')
const cancelLoading = computed(() => !!props.cancelButtonLoading || pending.value === 'cancel')
const busy = computed(() => !!pending.value || confirmLoading.value || cancelLoading.value)

async function handle(action: 'confirm' | 'cancel') {
  const hook = props.beforeClose
  if (hook) {
    try {
      pending.value = action
      const result = await hook(action)
      if (result === false) return
    } catch {
      // 钩子里抛错等同于「不放行」，避免弹窗状态被半路改掉
      return
    } finally {
      pending.value = null
    }
  }

  if (action === 'confirm') {
    emit('confirm')
  } else {
    emit('cancel')
    emit('update:show', false)
  }
}

function onMask() {
  if (props.closeOnClickMask) emit('update:show', false)
}

const panelStyle = computed(() => {
  const s: Record<string, string> = { zIndex: String(zIndex.value) }
  const r = toCssSize(props.radius)
  if (r) s['--jm-dialog-radius'] = r
  return s
})

/** 胶囊 / 方形按钮：confirm-color 变底色（文字模式仍是文字色） */
const isFilledActions = computed(() => props.buttonStyle !== 'text')

const confirmStyle = computed(() => {
  if (!props.confirmColor) return undefined
  return isFilledActions.value
    ? { background: props.confirmColor, borderColor: props.confirmColor }
    : { color: props.confirmColor }
})

const cancelStyle = computed(() =>
  props.cancelColor ? { color: props.cancelColor } : undefined,
)
</script>

<template>
  <Teleport to="body" :disabled="!teleport">
    <Transition name="jm-dialog-fade">
      <div
        v-if="show && mask"
        class="jm-dialog__mask"
        :class="{ 'is-inline': !teleport }"
        :style="{ zIndex: String(zIndex - 1) }"
        @click="onMask"
      />
    </Transition>

    <Transition name="jm-dialog-zoom" @after-leave="emit('closed')">
      <div
        v-if="show"
        ref="panelRef"
        class="jm-dialog"
        :class="{ 'is-round': round, 'is-inline': !teleport, 'is-vertical': verticalActions }"
        :style="panelStyle"
        role="dialog"
        aria-modal="true"
        tabindex="-1"
        :aria-labelledby="title || $slots.title ? titleId : undefined"
        :aria-describedby="message || $slots.default ? messageId : undefined"
      >
        <div class="jm-dialog__body">
          <div v-if="title || $slots.title" :id="titleId" class="jm-dialog__title">
            <slot name="title">{{ title }}</slot>
          </div>
          <div v-if="message || $slots.default" :id="messageId" class="jm-dialog__message">
            <slot>{{ message }}</slot>
          </div>
        </div>

        <div
          v-if="showCancel || showConfirm || $slots.footer"
          class="jm-dialog__footer"
          :class="`jm-dialog__footer--${buttonStyle}`"
        >
          <slot name="footer">
            <button
              v-if="showCancel"
              v-ripple
              type="button"
              class="jm-dialog__button jm-dialog__button--cancel"
              :class="{ 'is-loading': cancelLoading }"
              :style="cancelStyle"
              :disabled="busy"
              @click="onCancel"
            >
              <span v-if="cancelLoading" class="jm-dialog__spinner" aria-hidden="true" />
              {{ cancelText }}
            </button>
            <button
              v-ripple="{ color: isFilledActions ? '#fff' : undefined }"
              type="button"
              class="jm-dialog__button jm-dialog__button--primary"
              :class="{ 'is-loading': confirmLoading }"
              :style="confirmStyle"
              :disabled="busy"
              @click="onConfirm"
            >
              <span v-if="confirmLoading" class="jm-dialog__spinner" aria-hidden="true" />
              {{ confirmText }}
            </button>
          </slot>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
.jm-dialog__mask {
  position: fixed;
  inset: 0;
  background: var(--jm-bg-mask);
}

.jm-dialog__mask.is-inline {
  position: absolute;
}

.jm-dialog {
  --jm-dialog-radius: var(--jm-radius-lg);
  position: fixed;
  top: 50%;
  left: 50%;
  z-index: 1100;
  transform: translate(-50%, -50%);
  width: 78%;
  max-width: 320px;
  overflow: hidden;
  background: var(--jm-bg-elevated);
  border-radius: 4px;
  font-family: var(--jm-font-family);
  box-shadow: var(--jm-shadow-3);
}

/* 面板自己是焦点落点（tabindex="-1"），整块描边没有意义，焦点由内部按钮体现 */
.jm-dialog:focus-visible {
  outline: none;
}

.jm-dialog.is-inline {
  position: absolute;
}

.jm-dialog.is-round {
  border-radius: var(--jm-dialog-radius);
}

.jm-dialog__body {
  padding: var(--jm-space-6) var(--jm-space-5) var(--jm-space-5);
  text-align: center;
}

.jm-dialog__title {
  font-size: var(--jm-font-size-lg);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.4;
  color: var(--jm-text-color);
}

.jm-dialog__message {
  margin-top: var(--jm-space-2);
  font-size: var(--jm-font-size-sm);
  line-height: 1.6;
  color: var(--jm-text-color-2);
  word-break: break-word;
}

.jm-dialog__footer {
  display: flex;
  border-top: 1px solid var(--jm-border-color);
}

.jm-dialog__button {
  flex: 1;
  min-height: calc(50px * var(--jm-size-scale));
  border: 0;
  background: none;
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color-2);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
  --jm-ripple-opacity: 0.1;
}

.jm-dialog__button + .jm-dialog__button {
  border-left: 1px solid var(--jm-border-color);
}

.jm-dialog__button--primary {
  color: var(--jm-color-primary);
  font-weight: var(--jm-font-weight-medium);
}

/* loading 态：按钮内联小转圈，颜色跟着按钮文字走；禁用时保留原色不置灰 */
.jm-dialog__button.is-loading {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  opacity: 1;
}

.jm-dialog__button:disabled {
  cursor: not-allowed;
}

.jm-dialog__button:disabled:not(.is-loading) {
  opacity: 0.5;
}

.jm-dialog__spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 1.6px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: jm-dialog-spin 0.7s linear infinite;
}

@keyframes jm-dialog-spin {
  to {
    transform: rotate(360deg);
  }
}

/* ---------- 胶囊 / 方形按钮：按钮浮在面板内，分隔线让位给间距 ---------- */
.jm-dialog__footer--pill,
.jm-dialog__footer--square {
  gap: var(--jm-space-3);
  padding: var(--jm-space-4) var(--jm-space-5);
  border-top: 0;
}

.jm-dialog__footer--pill .jm-dialog__button,
.jm-dialog__footer--square .jm-dialog__button {
  min-height: var(--jm-control-height-md);
  padding: 0 var(--jm-space-4);
  border-left: 0;
  font-weight: var(--jm-font-weight-medium);
  transition:
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    box-shadow var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-dialog__footer--pill .jm-dialog__button {
  border-radius: var(--jm-radius-round);
}

.jm-dialog__footer--square .jm-dialog__button {
  border-radius: var(--jm-radius-sm);
}

/* 取消按钮：描边中性款，与实心确认按钮拉开层级 */
.jm-dialog__footer--pill .jm-dialog__button--cancel,
.jm-dialog__footer--square .jm-dialog__button--cancel {
  color: var(--jm-text-color);
  background: transparent;
  box-shadow: inset 0 0 0 1px var(--jm-border-color);
}

/* 确认按钮：实心主色（confirm-color 会覆盖底色） */
.jm-dialog__footer--pill .jm-dialog__button--primary,
.jm-dialog__footer--square .jm-dialog__button--primary {
  color: #fff;
  background: var(--jm-color-primary);
}

.jm-dialog__footer--pill .jm-dialog__button--primary:active,
.jm-dialog__footer--square .jm-dialog__button--primary:active {
  opacity: 0.85;
}

/* 竖排 + 填充按钮：去掉横排遗留的分隔线 */
.jm-dialog.is-vertical .jm-dialog__footer--pill .jm-dialog__button + .jm-dialog__button,
.jm-dialog.is-vertical .jm-dialog__footer--square .jm-dialog__button + .jm-dialog__button {
  border-bottom: 0;
}

.jm-dialog.is-vertical .jm-dialog__footer--pill,
.jm-dialog.is-vertical .jm-dialog__footer--square {
  flex-direction: column-reverse;
}

.jm-dialog.is-vertical .jm-dialog__footer {
  flex-direction: column-reverse;
}

.jm-dialog.is-vertical .jm-dialog__button + .jm-dialog__button {
  border-left: 0;
  border-bottom: 1px solid var(--jm-border-color);
}

/* 过渡：遮罩与面板分开——遮罩只负责明暗，面板负责位移/缩放。
   进场 300ms 减速，退场 200ms 加速，关得快一档 */
/* 移动端弹层节奏（参照 Varlet）：遮罩与内容同时长 250ms，进出对称 */
.jm-dialog-fade-enter-active,
.jm-dialog-fade-leave-active {
  transition: opacity var(--jm-motion-scrim-duration) var(--jm-motion-scrim-ease);
}

.jm-dialog-fade-enter-from,
.jm-dialog-fade-leave-to {
  opacity: 0;
}

.jm-dialog-zoom-enter-active,
.jm-dialog-zoom-leave-active {
  transition:
    transform var(--jm-motion-sheet-duration) var(--jm-motion-sheet-ease),
    opacity var(--jm-motion-scrim-duration) var(--jm-motion-scrim-ease);
}

.jm-dialog-zoom-enter-from,
.jm-dialog-zoom-leave-to {
  transform: translate(-50%, -50%) scale(var(--jm-motion-scale-pop));
  opacity: 0;
}
</style>
