<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSwipeCell' })

type Side = 'left' | 'right'

const props = withDefaults(
  defineProps<{
    /** 禁用滑动 */
    disabled?: boolean
    /** 左滑露出的按钮总宽度，不传按实际内容测量 */
    rightWidth?: number | string
    /** 右滑露出的按钮总宽度，不传按实际内容测量 */
    leftWidth?: number | string
    /** 打开判定阈值占按钮宽度的比例 */
    threshold?: number
    /** 打开时自动关闭其他已打开的单元格（列表里通常保持开启） */
    autoCloseOthers?: boolean
    /** 初始是否打开 */
    openSide?: Side | null
    /** 点击按钮后是否自动收起（默认 false，保持旧行为） */
    closeOnAction?: boolean
    /**
     * 点击按钮前钩子：返回 false 或 reject 则保持展开（适合「确定删除？」二次确认）。
     * 异步期间按钮进入 loading，不会重复触发。
     */
    beforeClose?: (payload: {
      side: Side
      action: HTMLElement
      event: MouseEvent
    }) => boolean | Promise<boolean>
  }>(),
  { threshold: 0.4, autoCloseOthers: true, openSide: null, closeOnAction: false },
)

const emit = defineEmits<{
  open: [side: Side]
  close: []
  /** 点击内容区（未发生滑动时） */
  click: [event: MouseEvent]
  /** 点击了左右侧按钮 */
  action: [side: Side, event: MouseEvent]
}>()

/* ---------- 同一时刻只允许一个单元格打开 ---------- */
let activeCloser: (() => void) | null = null

const root = ref<HTMLElement>()
const track = ref<HTMLElement>()
const leftEl = ref<HTMLElement>()
const rightEl = ref<HTMLElement>()

const offset = ref(0)
const dragging = ref(false)
const current = ref<Side | null>(props.openSide ?? null)
const leftWidth = ref(0)
const rightWidth = ref(0)

const draggingRef = ref(false)
/** 本次手势是否真的移动过：用于吞掉滑动结束后的误触 click */
let moved = false
let startX = 0
let startY = 0
let startOffset = 0
let axis: 'x' | 'y' | null = null
let lastX = 0
let lastT = 0
let velocity = 0

const fixedLeft = computed(() => toCssSize(props.leftWidth))
const fixedRight = computed(() => toCssSize(props.rightWidth))

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (fixedLeft.value) s['--jm-swipe-cell-left'] = fixedLeft.value
  if (fixedRight.value) s['--jm-swipe-cell-right'] = fixedRight.value
  s['--jm-swipe-cell-offset'] = `${offset.value}px`
  return s
})

function measure() {
  leftWidth.value = fixedLeft.value ? sizeToPx(fixedLeft.value, leftEl.value) : (leftEl.value?.offsetWidth ?? 0)
  rightWidth.value = fixedRight.value ? sizeToPx(fixedRight.value, rightEl.value) : (rightEl.value?.offsetWidth ?? 0)
}

function sizeToPx(v: string, el?: HTMLElement): number {
  if (v.endsWith('px')) return parseFloat(v)
  // 百分比等无法直接换算，退回实测宽度
  return el?.offsetWidth ?? 0
}

function clamp(v: number): number {
  return Math.min(leftWidth.value, Math.max(-rightWidth.value, v))
}

function setOffset(v: number, animated = true) {
  dragging.value = !animated
  offset.value = clamp(v)
}

function open(side: Side) {
  measure()
  const target = side === 'left' ? leftWidth.value : -rightWidth.value
  if (!target) return
  current.value = side
  setOffset(target)
  if (props.autoCloseOthers && activeCloser && activeCloser !== close) {
    const other = activeCloser
    activeCloser = null
    other()
  }
  activeCloser = close
  document.addEventListener('pointerdown', onDocPointerDown, true)
  emit('open', side)
}

function close(animated = true) {
  if (current.value === null && offset.value === 0) return
  current.value = null
  setOffset(0, animated)
  if (activeCloser === close) activeCloser = null
  document.removeEventListener('pointerdown', onDocPointerDown, true)
  emit('close')
}

function toggle(side: Side) {
  if (current.value === side) close()
  else open(side)
}

/* 点空白处收起 */
function onDocPointerDown(e: PointerEvent) {
  if (!root.value) return
  if (!root.value.contains(e.target as Node)) close()
}

function onPointerDown(e: PointerEvent) {
  if (props.disabled) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  measure()
  moved = false
  axis = null
  startX = e.clientX
  startY = e.clientY
  startOffset = offset.value
  lastX = e.clientX
  lastT = performance.now()
  velocity = 0
  dragging.value = true
  draggingRef.value = true
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件或指针已释放时捕获会失败，忽略即可 */
  }
}

function onPointerMove(e: PointerEvent) {
  if (!draggingRef.value) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY

  if (!axis) {
    if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return
    axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y'
    if (axis === 'y') {
      // 判定为纵向滚动，直接交还给页面
      draggingRef.value = false
      dragging.value = false
      return
    }
  }

  moved = true
  const now = performance.now()
  velocity = (e.clientX - lastX) / Math.max(1, now - lastT)
  lastX = e.clientX
  lastT = now

  let next = startOffset + dx
  // 超出按钮宽度的一侧加阻尼：能拉出一点，但明显费劲（橡皮筋手感）
  if (next > leftWidth.value) next = leftWidth.value + (next - leftWidth.value) * 0.25
  if (next < -rightWidth.value) next = -rightWidth.value + (next + rightWidth.value) * 0.25
  offset.value = next
}

function onPointerUp() {
  if (!draggingRef.value) return
  draggingRef.value = false
  dragging.value = false

  const shouldOpenLeft =
    leftWidth.value > 0 &&
    (offset.value > leftWidth.value * props.threshold || velocity > 0.35)
  const shouldOpenRight =
    rightWidth.value > 0 &&
    (-offset.value > rightWidth.value * props.threshold || velocity < -0.35)

  if (shouldOpenLeft && offset.value > 0) open('left')
  else if (shouldOpenRight && offset.value < 0) open('right')
  else close()
}

/** 滑动结束后浏览器还会补一次 click，这里吞掉，避免误触列表项。
 *  只吞内容区的：吞完立刻把手指移到露出的按钮上点击是正常操作，不能一起吞。 */
function onClickCapture(e: MouseEvent) {
  if (!moved) return
  moved = false
  const target = e.target as HTMLElement | null
  if (target?.closest('.jm-swipe-cell__side')) return
  e.stopPropagation()
  e.preventDefault()
}

/* ---------- 点击侧边按钮：可选二次确认 ---------- */
const acting = ref(false)

async function onSideClick(e: MouseEvent) {
  const action = (e.target as HTMLElement)?.closest(
    '[data-jm-swipe-action], button, a, .jm-swipe-cell__side > *',
  ) as HTMLElement | null
  if (!action) return
  const side: Side = offset.value > 0 ? 'left' : 'right'
  emit('action', side, e)

  if (!props.closeOnAction) return
  if (!props.beforeClose) {
    close()
    return
  }
  if (acting.value) return

  acting.value = true
  action.classList.add('is-action-loading')
  let ok: boolean | void = false
  try {
    ok = await props.beforeClose({ side, action, event: e })
    if (ok !== false) close()
  } catch {
    /* 钩子内部报错时保持展开，交由业务提示 */
  } finally {
    acting.value = false
    action.classList.remove('is-action-loading')
  }
}

function onContentClick(e: MouseEvent) {
  // 已经打开时，点内容先收起而不是触发业务点击
  if (current.value) {
    close()
    return
  }
  emit('click', e)
}

watch(
  () => props.openSide,
  (side) => {
    if (side) open(side)
    else close()
  },
)

watch([fixedLeft, fixedRight], () => nextTick(measure))

onMounted(() => {
  if (props.openSide) nextTick(() => open(props.openSide as Side))
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', onDocPointerDown, true)
  if (activeCloser === close) activeCloser = null
})

defineExpose({ open, close, toggle, offset })
</script>

<template>
  <div ref="root" class="jm-swipe-cell" :class="{ 'is-disabled': disabled }">
    <div
      ref="track"
      class="jm-swipe-cell__track"
      :class="{ 'is-dragging': dragging }"
      :style="styles"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
      @click.capture="onClickCapture"
    >
      <div
        v-if="$slots.left"
        ref="leftEl"
        class="jm-swipe-cell__side jm-swipe-cell__side--left"
        @click="onSideClick"
      >
        <slot name="left" />
      </div>
      <div class="jm-swipe-cell__content" @click="onContentClick">
        <slot />
      </div>
      <div
        v-if="$slots.right"
        ref="rightEl"
        class="jm-swipe-cell__side jm-swipe-cell__side--right"
        @click="onSideClick"
      >
        <slot name="right" />
      </div>
    </div>
  </div>
</template>

<style>
.jm-swipe-cell {
  position: relative;
  overflow: hidden;
  font-family: var(--jm-font-family);
}

.jm-swipe-cell__track {
  position: relative;
  display: flex;
  align-items: stretch;
  width: 100%;
  background: var(--jm-bg-container);
  transform: translate3d(var(--jm-swipe-cell-offset, 0px), 0, 0);
  transition: transform 0.28s cubic-bezier(0.22, 0.61, 0.36, 1);
  /* 横向我们自己处理，纵向留给页面滚动 */
  touch-action: pan-y;
  will-change: transform;
}

.jm-swipe-cell__track.is-dragging {
  transition: none;
}

.jm-swipe-cell__content {
  flex: 1 1 auto;
  min-width: 0;
}

/* 按钮挂在轨道两侧外面，轨道一平移就露出来 */
.jm-swipe-cell__side {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: stretch;
}

.jm-swipe-cell__side--left {
  right: 100%;
  width: var(--jm-swipe-cell-left, auto);
}

.jm-swipe-cell__side--right {
  left: 100%;
  width: var(--jm-swipe-cell-right, auto);
}

.jm-swipe-cell__side > * {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0 18px;
  border: none;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-color-primary-contrast);
  background: var(--jm-color-primary);
  cursor: pointer;
  white-space: nowrap;
}

.jm-swipe-cell__side > *:active {
  filter: brightness(0.94);
}

.jm-swipe-cell__side .is-action-loading {
  opacity: 0.65;
  pointer-events: none;
}

.jm-swipe-cell.is-disabled .jm-swipe-cell__track {
  transform: translate3d(0, 0, 0);
}
</style>
