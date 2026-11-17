<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, useId, watch } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmTooltip' })

const props = withDefaults(
  defineProps<{
    /** 提示文案，也可用 #content 插槽 */
    content?: string
    placement?: 'top' | 'bottom' | 'left' | 'right'
    /** 贴着触发元素的那条边怎么对齐（左右方向忽略） */
    align?: 'start' | 'center' | 'end'
    /** hover：桌面鼠标移上；longpress：移动端长按；click：点一下；manual：完全受控 */
    trigger?: 'hover' | 'longpress' | 'click' | 'manual'
    theme?: 'dark' | 'light'
    /** 与触发元素的间距 */
    offset?: number
    maxWidth?: number | string
    arrow?: boolean
    disabled?: boolean
    /** hover 进入后延迟多久出现，避免扫过一片图标时气泡乱闪 */
    showDelay?: number
    hideDelay?: number
    /** 长按多久触发 */
    longpressDuration?: number
    /** 长按触发后，抬手再过多久自动收起 */
    autoHideDelay?: number
    /** 空间不够时自动翻到对面 */
    autoFlip?: boolean
    zIndex?: number
    /** 受控显示，配合 update:show */
    show?: boolean
  }>(),
  {
    // 布尔 prop 不给显式默认值时会被 Vue 强制转成 false，
    // 受控模式就永远打不开，必须显式声明 undefined
    show: undefined,
    placement: 'top',
    align: 'center',
    trigger: 'hover',
    theme: 'dark',
    offset: 8,
    maxWidth: 220,
    arrow: true,
    showDelay: 120,
    hideDelay: 60,
    longpressDuration: 450,
    autoHideDelay: 1600,
    autoFlip: true,
    zIndex: 1300,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  show: []
  hide: []
}>()

const uid = `jm-tooltip-${useId()}`

const innerShow = ref(false)
const visible = computed({
  get: () => (props.show === undefined ? innerShow.value : props.show),
  set: (v: boolean) => {
    if (innerShow.value === v && props.show === undefined) return
    innerShow.value = v
    emit('update:show', v)
    if (v) emit('show')
    else emit('hide')
  },
})

/* 实际生效的方向与对齐：空间不足时会和 props 不一致 */
const realPlacement = ref(props.placement)
const realAlign = ref(props.align)
/** 定位算完之前先把面板藏成透明，避免翻转时那一帧的位移被看到 */
const positioned = ref(false)

const root = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)

let showTimer = 0
let hideTimer = 0
let pressTimer = 0
let autoHideTimer = 0

function clearTimers() {
  ;[showTimer, hideTimer, pressTimer, autoHideTimer].forEach((id) => {
    if (id) window.clearTimeout(id)
  })
  showTimer = hideTimer = pressTimer = autoHideTimer = 0
}

function open() {
  if (props.disabled) return
  clearTimers()
  if (visible.value) return
  visible.value = true
}

function openDelayed() {
  if (props.disabled || visible.value) return
  if (props.showDelay > 0) {
    window.clearTimeout(showTimer)
    showTimer = window.setTimeout(() => {
      showTimer = 0
      open()
    }, props.showDelay)
  } else {
    open()
  }
}

function close(delay = props.hideDelay) {
  window.clearTimeout(showTimer)
  showTimer = 0
  window.clearTimeout(hideTimer)
  if (delay > 0) {
    hideTimer = window.setTimeout(() => {
      hideTimer = 0
      visible.value = false
    }, delay)
  } else {
    visible.value = false
  }
}

/* ---------------- 各触发方式 ---------------- */

function onHoverEnter() {
  if (props.trigger !== 'hover') return
  window.clearTimeout(hideTimer)
  hideTimer = 0
  openDelayed()
}

function onHoverLeave() {
  if (props.trigger !== 'hover') return
  close()
}

function onFocusIn() {
  if (props.trigger !== 'hover') return
  // 键盘 Tab 到触发元素时也显示，否则纯图标按钮对键盘用户等于没有说明
  open()
}

function onFocusOut() {
  if (props.trigger !== 'hover') return
  close(0)
}

function onClick() {
  if (props.trigger !== 'click') return
  if (visible.value) close(0)
  else open()
}

let startX = 0
let startY = 0

function onTouchStart(e: TouchEvent) {
  if (props.trigger !== 'longpress' || props.disabled) return
  const t = e.touches[0]
  if (!t) return
  startX = t.clientX
  startY = t.clientY
  clearTimers()
  pressTimer = window.setTimeout(() => {
    pressTimer = 0
    visible.value = true
  }, props.longpressDuration)
}

/* PC 鼠标长按：pointerType 门控为 mouse，避免触屏上与 touch 事件双触发 */
function onMousePress(e: PointerEvent) {
  if (props.trigger !== 'longpress' || props.disabled) return
  if (e.pointerType !== 'mouse') return
  startX = e.clientX
  startY = e.clientY
  clearTimers()
  pressTimer = window.setTimeout(() => {
    pressTimer = 0
    visible.value = true
  }, props.longpressDuration)
}

function onMousePressMove(e: PointerEvent) {
  if (props.trigger !== 'longpress' || !pressTimer) return
  if (e.pointerType !== 'mouse') return
  if (Math.abs(e.clientX - startX) > 8 || Math.abs(e.clientY - startY) > 8) {
    window.clearTimeout(pressTimer)
    pressTimer = 0
  }
}

function onTouchMove(e: TouchEvent) {
  if (props.trigger !== 'longpress' || !pressTimer) return
  const t = e.touches[0]
  if (!t) return
  // 手指移动超过 8px 视为滚动列表，取消长按
  if (Math.abs(t.clientX - startX) > 8 || Math.abs(t.clientY - startY) > 8) {
    window.clearTimeout(pressTimer)
    pressTimer = 0
  }
}

function onTouchEnd() {
  if (props.trigger !== 'longpress') return
  window.clearTimeout(pressTimer)
  pressTimer = 0
  if (!visible.value) return
  autoHideTimer = window.setTimeout(() => {
    autoHideTimer = 0
    visible.value = false
  }, props.autoHideDelay)
}

/* ---------------- 定位与翻转 ---------------- */

function measure() {
  const el = panel.value
  if (!el) return
  if (!props.autoFlip) {
    positioned.value = true
    return
  }
  const r = el.getBoundingClientRect()
  const vw = document.documentElement.clientWidth
  const vh = document.documentElement.clientHeight
  const pad = 6
  let p = props.placement
  let a = props.align

  if (p === 'top' && r.top < pad) p = 'bottom'
  else if (p === 'bottom' && r.bottom > vh - pad) p = 'top'
  else if (p === 'left' && r.left < pad) p = 'right'
  else if (p === 'right' && r.right > vw - pad) p = 'left'

  // 上下方向再修一次左右越界：居中的气泡贴着屏幕左边时改成左对齐
  if (p === 'top' || p === 'bottom') {
    if (a === 'center' && r.left < pad) a = 'start'
    else if (a === 'center' && r.right > vw - pad) a = 'end'
  }

  realPlacement.value = p
  realAlign.value = a
  positioned.value = true
}

watch(visible, async (v) => {
  if (v) {
    realPlacement.value = props.placement
    realAlign.value = props.align
    positioned.value = false
    await nextTick()
    // nextTick 之后元素已在 DOM 里，但样式可能还没算完，等一帧再量
    requestAnimationFrame(() => measure())
  } else {
    positioned.value = false
    clearTimers()
  }
})

watch(
  () => props.placement,
  (p) => {
    realPlacement.value = p
  },
)

onBeforeUnmount(clearTimers)

const panelStyle = computed(() => {
  const s: Record<string, string> = { zIndex: String(props.zIndex) }
  const gap = toCssSize(props.offset)
  if (gap) s['--jm-tooltip-offset'] = gap
  const max = toCssSize(props.maxWidth)
  if (max) s.maxWidth = max
  return s
})

defineExpose({
  show: open,
  hide: () => close(0),
  toggle: () => (visible.value ? close(0) : open()),
})
</script>

<template>
  <span
    ref="root"
    class="jm-tooltip"
    :class="[`is-${realPlacement}`, `is-align-${realAlign}`, { 'is-open': visible }]"
    :aria-describedby="visible ? uid : undefined"
    @mouseenter="onHoverEnter"
    @mouseleave="onHoverLeave"
    @focusin="onFocusIn"
    @focusout="onFocusOut"
    @click="onClick"
    @touchstart.passive="onTouchStart"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
    @touchcancel="onTouchEnd"
    @pointerdown="onMousePress"
    @pointermove="onMousePressMove"
    @pointerup="onTouchEnd"
    @pointercancel="onTouchEnd"
  >
    <slot />

    <Transition name="jm-tooltip-fade">
      <div
        v-if="visible"
        :id="uid"
        ref="panel"
        class="jm-tooltip__panel"
        :class="[`is-${theme}`, { 'is-ready': positioned, 'has-arrow': arrow }]"
        :style="panelStyle"
        role="tooltip"
      >
        <span v-if="arrow" class="jm-tooltip__arrow" aria-hidden="true" />
        <slot name="content">{{ content }}</slot>
      </div>
    </Transition>
  </span>
</template>

<style>
.jm-tooltip {
  --jm-tooltip-offset: 8px;
  position: relative;
  display: inline-flex;
  vertical-align: middle;
  max-width: 100%;
  font-family: var(--jm-font-family);
}

.jm-tooltip__panel {
  position: absolute;
  z-index: 1300;
  box-sizing: border-box;
  width: max-content;
  padding: 6px 10px;
  border-radius: var(--jm-radius-md);
  font-size: var(--jm-font-size-xs);
  line-height: 1.5;
  text-align: left;
  word-break: break-word;
  /* 气泡只是给人看的，不能挡住底下的点击 */
  pointer-events: none;
  opacity: 0;
}

.jm-tooltip__panel.is-ready {
  opacity: 1;
}

.jm-tooltip__panel.is-dark {
  background: rgba(16, 21, 26, 0.92);
  color: #fff;
  box-shadow: var(--jm-shadow-2);
}

.jm-tooltip__panel.is-light {
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  border: 1px solid var(--jm-border-color);
  box-shadow: var(--jm-shadow-2);
}

/* 四个方向：面板贴住触发元素，间距由 --jm-tooltip-offset 控制 */
.jm-tooltip.is-top .jm-tooltip__panel {
  bottom: calc(100% + var(--jm-tooltip-offset));
}

.jm-tooltip.is-bottom .jm-tooltip__panel {
  top: calc(100% + var(--jm-tooltip-offset));
}

.jm-tooltip.is-left .jm-tooltip__panel {
  right: calc(100% + var(--jm-tooltip-offset));
  top: 50%;
  transform: translateY(-50%);
}

.jm-tooltip.is-right .jm-tooltip__panel {
  left: calc(100% + var(--jm-tooltip-offset));
  top: 50%;
  transform: translateY(-50%);
}

/* 水平对齐：左右方向垂直居中，忽略 align */
.jm-tooltip.is-align-center .jm-tooltip__panel {
  left: 50%;
  transform: translateX(-50%);
}

.jm-tooltip.is-align-start .jm-tooltip__panel {
  left: 0;
}

.jm-tooltip.is-align-end .jm-tooltip__panel {
  right: 0;
}

.jm-tooltip.is-left .jm-tooltip__panel,
.jm-tooltip.is-right .jm-tooltip__panel {
  left: auto;
  right: auto;
  /* 左右方向垂直居中：transform 必须在这里重申，
     否则会被下面（源码顺序更后的）is-align-center 的 translateX 覆盖 */
  transform: translateY(-50%);
}

.jm-tooltip.is-right .jm-tooltip__panel {
  left: calc(100% + var(--jm-tooltip-offset));
}

.jm-tooltip.is-left .jm-tooltip__panel {
  right: calc(100% + var(--jm-tooltip-offset));
}

.jm-tooltip__arrow {
  position: absolute;
  width: 6px;
  height: 6px;
  background: inherit;
  border-radius: 1px;
  pointer-events: none;
}

.jm-tooltip.is-top .jm-tooltip__arrow {
  bottom: -3px;
  transform: rotate(45deg);
}

.jm-tooltip.is-bottom .jm-tooltip__arrow {
  top: -3px;
  transform: rotate(45deg);
}

.jm-tooltip.is-left .jm-tooltip__arrow {
  right: -3px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
}

.jm-tooltip.is-right .jm-tooltip__arrow {
  left: -3px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
}

.jm-tooltip.is-align-center .jm-tooltip__arrow {
  left: 50%;
  margin-left: -3px;
}

.jm-tooltip.is-align-start .jm-tooltip__arrow {
  left: 10px;
}

.jm-tooltip.is-align-end .jm-tooltip__arrow {
  right: 10px;
}

.jm-tooltip.is-left .jm-tooltip__arrow,
.jm-tooltip.is-right .jm-tooltip__arrow {
  left: auto;
  right: auto;
  margin-left: 0;
}

.jm-tooltip.is-right .jm-tooltip__arrow {
  left: -3px;
}

.jm-tooltip.is-left .jm-tooltip__arrow {
  right: -3px;
}

.jm-tooltip-fade-enter-active {
  transition: opacity 120ms var(--jm-motion-enter-ease, ease-out);
}

.jm-tooltip-fade-leave-active {
  transition: opacity 90ms var(--jm-motion-exit-ease, ease-in);
}

.jm-tooltip-fade-enter-from,
.jm-tooltip-fade-leave-to {
  opacity: 0;
}

[data-motion='off'] .jm-tooltip-fade-enter-active,
[data-motion='off'] .jm-tooltip-fade-leave-active {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-tooltip-fade-enter-active,
  .jm-tooltip-fade-leave-active {
    transition: none;
  }
}
</style>
