<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { lockScroll, unlockScroll } from '../utils'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmImagePreview' })

const props = withDefaults(
  defineProps<{
    show?: boolean
    images?: string[]
    /** 打开时停留的下标 */
    startPosition?: number
    /** 右下角 "2 / 5" */
    showIndex?: boolean
    /** 右上角关闭按钮 */
    closeable?: boolean
    /** 点遮罩关闭 */
    closeOnClickMask?: boolean
    /** 点图片关闭（默认关，避免想放大却关掉了） */
    closeOnClickImage?: boolean
    /** 挂载目标：false 就地渲染（手机模拟框内演示用） */
    teleport?: boolean | string | Element
    zIndex?: number
    /** 蒙层背景 */
    maskColor?: string
    /** 双击 / 双指缩放（放大后单指拖动看细节） */
    zoomable?: boolean
    /** 最大放大倍数 */
    maxScale?: number
    /** 双击放大到几倍 */
    doubleTapScale?: number
  }>(),
  {
    images: () => [],
    startPosition: 0,
    showIndex: true,
    closeable: true,
    closeOnClickMask: true,
    closeOnClickImage: false,
    teleport: true,
    zIndex: 2200,
    zoomable: true,
    maxScale: 4,
    doubleTapScale: 2.5,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  change: [index: number]
  close: []
  /** 缩放变化（双击、捏合、回弹都触发） */
  zoom: [scale: number]
}>()

const index = ref(0)
const root = ref<HTMLElement | null>(null)
const size = ref(0)
const height = ref(0)
const offset = ref(0)
const animated = ref(false)

/* 缩放与平移（只作用于当前这一张）。放在 watch 之前：初始即打开时 watcher
   会在 setup 阶段跑到 resetZoom，ref 必须已经初始化（否则 TDZ） */
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
/** 松手回弹 / 双击缩放期间打开 CSS 过渡，跟手阶段关掉 */
const zooming = ref(false)
let zoomTimer = 0
/** 单击关闭的延迟句柄（要等第二下，双击才能取消） */
let tapTimer = 0

const count = computed(() => props.images.length)

const trackStyle = computed(() => ({
  transform: `translate3d(${-index.value * size.value + offset.value}px, 0, 0)`,
  transition: animated.value ? 'transform 300ms cubic-bezier(0.22, 0.61, 0.36, 1)' : 'none',
}))

const rootStyle = computed(() => {
  const s: Record<string, string> = { zIndex: String(props.zIndex) }
  if (props.maskColor) s['--jm-preview-mask'] = props.maskColor
  return s
})

const inline = computed(() => props.teleport === false)

const target = computed<string | Element>(() => {
  if (typeof props.teleport === 'string') return props.teleport
  /* SSR（Node）下没有 Element 全局，直接 instanceof 会抛 ReferenceError */
  if (typeof Element !== 'undefined' && props.teleport instanceof Element) return props.teleport
  return 'body'
})

/* ---------------- 打开 / 关闭 ---------------- */
let locked = false

function syncLock(open: boolean) {
  if (inline.value) return // 内嵌场景锁 body 会把整页冻住
  if (open && !locked) {
    lockScroll()
    locked = true
  } else if (!open && locked) {
    unlockScroll()
    locked = false
  }
}

function measure() {
  if (!root.value) return
  size.value = root.value.clientWidth
  height.value = root.value.clientHeight
}

function close() {
  clearTapTimer()
  resetZoom(false)
  emit('update:show', false)
  emit('close')
}

/* ---------------- 键盘：← → 切换、Home / End 跳首尾、Esc 关闭 ---------------- */
let prevFocus: HTMLElement | null = null

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    e.preventDefault()
    close()
    return
  }

  /* 缩放也能用键盘：+ 放大、- 缩小、0 复位（以视口中心为焦点） */
  if (props.zoomable && (e.key === '+' || e.key === '=' || e.key === '-' || e.key === '_' || e.key === '0')) {
    e.preventDefault()
    const rect = root.value?.getBoundingClientRect()
    const cx = rect ? rect.left + rect.width / 2 : 0
    const cy = rect ? rect.top + rect.height / 2 : 0
    if (e.key === '0') {
      zoomTo(1, cx, cy)
    } else {
      const factor = e.key === '-' || e.key === '_' ? 1 / 1.5 : 1.5
      zoomTo(scale.value * factor, cx, cy)
    }
    return
  }

  if (count.value <= 1) return
  if (e.key === 'ArrowLeft') {
    e.preventDefault()
    goTo(index.value - 1)
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    goTo(index.value + 1)
  } else if (e.key === 'Home') {
    e.preventDefault()
    goTo(0)
  } else if (e.key === 'End') {
    e.preventDefault()
    goTo(count.value - 1)
  }
}

watch(
  () => props.show,
  (v) => {
    if (typeof document === 'undefined') return
    syncLock(!!v)
    if (!v) {
      document.removeEventListener('keydown', onKeydown, true)
      clearTapTimer()
      resetZoom(false)
      // 关闭后把焦点还给打开预览的元素（相册格子 / 缩略图按钮），键盘用户不用重新找位置
      if (prevFocus && document.contains(prevFocus)) prevFocus.focus({ preventScroll: true })
      prevFocus = null
      return
    }
    prevFocus = (document.activeElement as HTMLElement | null) ?? null
    document.addEventListener('keydown', onKeydown, true)
    index.value = Math.min(Math.max(0, props.startPosition), Math.max(0, count.value - 1))
    offset.value = 0
    resetZoom(false)
    // 等一帧拿到容器宽度，首屏不能带过渡，否则会从第 0 张滑过去
    requestAnimationFrame(() => {
      measure()
      // 预览是模态层：把焦点移进来，读屏与 Tab 才不会留在背后的页面
      root.value?.focus({ preventScroll: true })
      requestAnimationFrame(() => {
        animated.value = true
      })
    })
  },
  { immediate: true },
)

/* 翻页时缩放必须归零：上一张放大的倍率带到下一张会让人以为图没换 */
watch(index, () => {
  clearTapTimer()
  resetZoom(false)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeydown, true)
  if (locked) {
    unlockScroll()
    locked = false
  }
})

/* ---------------- 手势：左右切换 + 双击/双指缩放 ----------------
 * 三种手势共用一套 Pointer 序列，按「当前缩放手数」决定归属：
 *   1 指 + scale=1  → 左右切换
 *   1 指 + scale>1  → 平移（放大后拖看细节）
 *   2 指            → 捏合缩放，焦点跟着两指中点
 * 双指时浏览器原生缩放会被 touch-action:none 挡掉，全部自己算。
 */
let startX = 0
let startY = 0
let startTime = 0
let dragging = false
let axis: 'x' | 'y' | null = null
let moved = false

const maxScale = computed(() => Math.max(1, props.maxScale))

const zoomStyle = computed(() => ({
  transform: `translate3d(${panX.value}px, ${panY.value}px, 0) scale(${scale.value})`,
  transition: zooming.value ? 'transform 240ms cubic-bezier(0.22, 0.61, 0.36, 1)' : 'none',
}))

function clampScale(s: number): number {
  return Math.min(maxScale.value, Math.max(1, s))
}

/** 放大后允许的平移范围：图片被撑出容器的部分的一半 */
function panBounds(s = scale.value) {
  return {
    x: Math.max(0, (size.value * (s - 1)) / 2),
    y: Math.max(0, (height.value * (s - 1)) / 2),
  }
}

function clampPan(x: number, y: number, s = scale.value) {
  const b = panBounds(s)
  return { x: Math.min(b.x, Math.max(-b.x, x)), y: Math.min(b.y, Math.max(-b.y, y)) }
}

function stopZoomTimer() {
  if (zoomTimer) {
    window.clearTimeout(zoomTimer)
    zoomTimer = 0
  }
}

function finishZoom() {
  zooming.value = true
  stopZoomTimer()
  zoomTimer = window.setTimeout(() => {
    zooming.value = false
    zoomTimer = 0
  }, 260)
}

function resetZoom(animate = false) {
  if (scale.value === 1 && panX.value === 0 && panY.value === 0) {
    zooming.value = false
    return
  }
  zooming.value = animate
  scale.value = 1
  panX.value = 0
  panY.value = 0
  if (animate) finishZoom()
  else zooming.value = false
  emit('zoom', 1)
}

/** 松手后归位：小于 1 回弹到 1，超出上限收敛到上限，平移卡回边界内 */
function settleZoom() {
  const s = scale.value < 1.02 ? 1 : clampScale(scale.value)
  const p = s === 1 ? { x: 0, y: 0 } : clampPan(panX.value, panY.value, s)
  if (s === scale.value && p.x === panX.value && p.y === panY.value) {
    zooming.value = false
    return
  }
  zooming.value = true
  scale.value = s
  panX.value = p.x
  panY.value = p.y
  finishZoom()
  emit('zoom', s)
}

function zoomTo(target: number, focusX: number, focusY: number, animate = true) {
  const next = clampScale(target)
  const rect = root.value?.getBoundingClientRect()
  const cx = rect ? rect.left + rect.width / 2 : 0
  const cy = rect ? rect.top + rect.height / 2 : 0
  zooming.value = animate
  scale.value = next
  if (next === 1) {
    panX.value = 0
    panY.value = 0
  } else {
    // 让手指落点/图片中心保持不动：content = (f - c - pan) / s
    const p = clampPan((focusX - cx) * (1 - next), (focusY - cy) * (1 - next), next)
    panX.value = p.x
    panY.value = p.y
  }
  if (animate) finishZoom()
  emit('zoom', next)
}

/* ---------------- 指针簿记 ---------------- */
const pointers = new Map<number, { x: number; y: number }>()
let pinch: { dist: number; cx: number; cy: number; scale: number; panX: number; panY: number } | null = null
let panning = false
let panStartX = 0
let panStartY = 0
let panOriginX = 0
let panOriginY = 0

/* 双击判定：第一次点下不能立刻关，否则双击放大永远等不到第二下 */
let lastTapTime = 0
let lastTapX = 0
let lastTapY = 0

function clearTapTimer() {
  if (tapTimer) {
    window.clearTimeout(tapTimer)
    tapTimer = 0
  }
}

function onPointerDown(e: PointerEvent) {
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY })
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件下捕获会失败，忽略 */
  }

  /* 第二根手指落下 → 立刻进入捏合，之前累积的左右滑位移作废 */
  if (pointers.size === 2 && props.zoomable) {
    const [a, b] = [...pointers.values()]
    pinch = {
      dist: Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)),
      cx: (a.x + b.x) / 2,
      cy: (a.y + b.y) / 2,
      scale: scale.value,
      panX: panX.value,
      panY: panY.value,
    }
    dragging = false
    panning = false
    moved = true
    offset.value = 0
    zooming.value = false
    return
  }
  if (pointers.size > 2) return

  dragging = count.value > 1
  axis = null
  moved = false
  startX = e.clientX
  startY = e.clientY
  startTime = Date.now()
  offset.value = 0
  animated.value = false

  /* 已经在放大状态：单指变成平移，不再翻页 */
  if (scale.value > 1.01) {
    panning = true
    dragging = false
    panStartX = e.clientX
    panStartY = e.clientY
    panOriginX = panX.value
    panOriginY = panY.value
    zooming.value = false
  }
}

function onPointerMove(e: PointerEvent) {
  if (!pointers.has(e.pointerId)) return
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY })

  /* 双指捏合：距离决定倍率，两指中点决定缩放中心 */
  if (pinch && pointers.size >= 2) {
    const [a, b] = [...pointers.values()]
    const dist = Math.max(1, Math.hypot(a.x - b.x, a.y - b.y))
    const cx = (a.x + b.x) / 2
    const cy = (a.y + b.y) / 2
    const raw = pinch.scale * (dist / pinch.dist)
    // 超过上限时阻尼到 1/4，松手再收敛回来，手感上有"拉不动"的反馈
    const s =
      raw > maxScale.value
        ? maxScale.value + (raw - maxScale.value) * 0.25
        : Math.max(0.8, raw)
    const k = s / pinch.scale
    const rect = root.value?.getBoundingClientRect()
    const ccx = rect ? rect.left + rect.width / 2 : 0
    const ccy = rect ? rect.top + rect.height / 2 : 0
    panX.value = cx - ccx - (pinch.cx - ccx - pinch.panX) * k
    panY.value = cy - ccy - (pinch.cy - ccy - pinch.panY) * k
    scale.value = s
    return
  }

  if (panning) {
    const dx = e.clientX - panStartX
    const dy = e.clientY - panStartY
    if (Math.abs(dx) > 4 || Math.abs(dy) > 4) moved = true
    panX.value = panOriginX + dx
    panY.value = panOriginY + dy
    return
  }

  if (!dragging) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY

  if (!axis) {
    if (Math.abs(dx) < 5 && Math.abs(dy) < 5) return
    axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y'
    if (axis === 'y') {
      dragging = false
      animated.value = true
      return
    }
  }

  if (Math.abs(dx) > 5) moved = true
  let d = dx
  // 首尾加阻尼
  if ((index.value === 0 && dx > 0) || (index.value === count.value - 1 && dx < 0)) d = dx * 0.35
  offset.value = d
}

/** 点击归类：双击缩放 / 单击按配置关闭（放大状态下单击不关） */
function handleTap(x: number, y: number, target: EventTarget | null) {
  const now = Date.now()
  const isDouble = props.zoomable && now - lastTapTime < 300 && Math.hypot(x - lastTapX, y - lastTapY) < 30

  if (isDouble) {
    lastTapTime = 0
    clearTapTimer()
    zoomTo(scale.value > 1.01 ? 1 : props.doubleTapScale, x, y)
    return
  }

  lastTapTime = now
  lastTapX = x
  lastTapY = y

  /* 已经放大时，单击是"看细节"而不是"关掉" */
  if (scale.value > 1.01) return

  const onImage = target instanceof Element && target.classList.contains('jm-image-preview__img')
  const shouldClose = onImage ? props.closeOnClickImage : props.closeOnClickMask
  if (!shouldClose) return

  if (!props.zoomable) {
    close()
    return
  }
  // 留 280ms 等第二下；双击能取消这次关闭
  clearTapTimer()
  tapTimer = window.setTimeout(() => {
    tapTimer = 0
    close()
  }, 280)
}

function onPointerUp(e: PointerEvent) {
  const x = e.clientX
  const y = e.clientY
  const target = e.target
  pointers.delete(e.pointerId)

  if (pinch) {
    if (pointers.size >= 2) return
    pinch = null
    settleZoom()
    const rest = [...pointers.values()][0]
    if (rest) {
      // 还有一根手指没抬：把它当作新的平移起点，避免图像跳一下
      panning = true
      dragging = false
      panStartX = rest.x
      panStartY = rest.y
      panOriginX = panX.value
      panOriginY = panY.value
    }
    return
  }

  if (panning) {
    panning = false
    settleZoom()
    offset.value = 0
    animated.value = true
    if (!moved) handleTap(x, y, target)
    return
  }

  if (!dragging) {
    if (!moved) handleTap(x, y, target)
    return
  }

  dragging = false
  const dx = x - startX
  const speed = Math.abs(dx) / Math.max(1, Date.now() - startTime)
  const threshold = Math.min(size.value * 0.2, 70)
  offset.value = 0
  animated.value = true

  if (Math.abs(dx) > threshold || speed > 0.4) {
    const next = index.value + (dx < 0 ? 1 : -1)
    if (next >= 0 && next < count.value) {
      index.value = next
      emit('change', next)
    }
    return
  }
  if (!moved) handleTap(x, y, target)
}

function onPointerCancel() {
  pointers.clear()
  pinch = null
  panning = false
  dragging = false
  offset.value = 0
  animated.value = true
  settleZoom()
}

function goTo(i: number) {
  const next = Math.min(Math.max(0, i), count.value - 1)
  if (next === index.value) return
  index.value = next
  emit('change', next)
}

defineExpose({ goTo, close, index, scale })
</script>

<template>
  <Teleport :to="target" :disabled="inline">
    <Transition name="jm-preview-fade">
      <div
        v-if="show"
        ref="root"
        class="jm-image-preview"
        :class="{ 'is-inline': inline }"
        :style="rootStyle"
        role="dialog"
        aria-modal="true"
        aria-label="图片预览"
        tabindex="-1"
        @pointerdown="onPointerDown"
        @pointermove="onPointerMove"
        @pointerup="onPointerUp"
        @pointercancel="onPointerCancel"
      >
        <div class="jm-image-preview__track" :style="trackStyle">
          <div v-for="(src, i) in images" :key="`${i}-${src}`" class="jm-image-preview__item">
            <img
              class="jm-image-preview__img"
              :class="{ 'is-zoomed': i === index && scale > 1 }"
              :src="src"
              :alt="`第 ${i + 1} 张`"
              draggable="false"
              :style="i === index ? zoomStyle : undefined"
            />
          </div>
        </div>

        <div v-if="showIndex && count > 1" class="jm-image-preview__index" aria-hidden="true">
          {{ index + 1 }} / {{ count }}
        </div>

        <!-- 索引变化播报给读屏软件；视觉文案 aria-hidden，避免重复朗读 -->
        <span class="jm-visually-hidden" aria-live="polite">
          第 {{ index + 1 }} 张，共 {{ count }} 张
        </span>

        <button v-if="closeable" type="button" class="jm-image-preview__close" aria-label="关闭" @click.stop="close">
          <jm-icon name="close" size="20px" :stroke-width="1.8" />
        </button>

        <div v-if="count > 1" class="jm-image-preview__dots">
          <span
            v-for="(_, i) in images"
            :key="i"
            class="jm-image-preview__dot"
            :class="{ 'is-active': i === index }"
            @click.stop="goTo(i)"
          />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
.jm-image-preview {
  position: fixed;
  inset: 0;
  z-index: 2200;
  overflow: hidden;
  background: var(--jm-preview-mask, rgba(0, 0, 0, 0.92));
  /* 双指缩放必须自己接管：交给浏览器会缩放整个页面而不是图片 */
  touch-action: none;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.jm-image-preview.is-inline {
  position: absolute;
}

.jm-image-preview__track {
  display: flex;
  width: 100%;
  height: 100%;
  will-change: transform;
}

.jm-image-preview__item {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  padding: var(--jm-space-4);
  box-sizing: border-box;
}

.jm-image-preview__img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  /* 图片要能作为 pointerdown 的 target（区分「点图」与「点空白」），
     手势仍由容器统一处理：pointer 事件本来就会冒泡上来 */
  pointer-events: auto;
  transform-origin: center center;
  will-change: transform;
  cursor: zoom-in;
}

.jm-image-preview__img.is-zoomed {
  cursor: zoom-out;
}

.jm-image-preview__index {
  position: absolute;
  left: 50%;
  bottom: calc(var(--jm-safe-bottom) + 28px);
  transform: translateX(-50%);
  padding: 3px 10px;
  border-radius: var(--jm-radius-round);
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-xs);
  font-variant-numeric: tabular-nums;
  pointer-events: none;
}

.jm-image-preview__close {
  position: absolute;
  top: calc(var(--jm-safe-top) + 10px);
  right: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  cursor: pointer;
}

.jm-image-preview__dots {
  position: absolute;
  left: 0;
  right: 0;
  bottom: calc(var(--jm-safe-bottom) + 10px);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.jm-image-preview__dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  cursor: pointer;
  transition: background-color var(--jm-motion-transition-duration, 200ms) ease;
}

.jm-image-preview__dot.is-active {
  background: #fff;
}

.jm-preview-fade-enter-active {
  transition: opacity 200ms ease-out;
}

.jm-preview-fade-leave-active {
  transition: opacity 180ms ease-in;
}

.jm-preview-fade-enter-from,
.jm-preview-fade-leave-to {
  opacity: 0;
}
</style>
