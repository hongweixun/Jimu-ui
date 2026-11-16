<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmSignature' })

interface Point {
  x: number
  y: number
}

const props = withDefaults(
  defineProps<{
    /** 签名图（dataURL），支持 v-model */
    modelValue?: string
    /** 画布高度，数字按 px 处理 */
    height?: number | string
    /** 笔迹颜色 */
    penColor?: string
    /** 笔迹粗细（px） */
    lineWidth?: number
    /** 画布底色，传空字符串则透明 */
    backgroundColor?: string
    /** 只读：只展示，不可书写 */
    readonly?: boolean
    /** 导出时裁掉四周空白 */
    trim?: boolean
    /** 导出格式 */
    format?: 'png' | 'jpeg'
    /** 笔画上限，超出后丢弃最早的（防内存膨胀） */
    maxStrokes?: number
    /** 内置工具栏（撤销 / 清空） */
    showToolbar?: boolean
    /** 空状态提示文字 */
    placeholder?: string
    /** 清空按钮文案 */
    clearText?: string
    /** 撤销按钮文案 */
    undoText?: string
  }>(),
  {
    height: 200,
    penColor: '#1f2937',
    lineWidth: 3,
    backgroundColor: '#ffffff',
    readonly: false,
    trim: true,
    format: 'png',
    maxStrokes: 200,
    showToolbar: false,
    placeholder: '请在此处签名',
    clearText: '清空',
    undoText: '撤销',
  },
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
  (e: 'start'): void
  (e: 'end'): void
  (e: 'clear'): void
}>()

const canvasEl = ref<HTMLCanvasElement>()
const drawing = ref(false)
/** 画布上是否有内容（笔画或回显的图片） */
const empty = ref(true)

const cssHeight = computed(() =>
  typeof props.height === 'number' ? `${props.height}px` : props.height,
)

let ctx: CanvasRenderingContext2D | null = null
let dpr = 1
let box = { w: 0, h: 0 }
/** 笔画：每条是 CSS 像素坐标系下的点序列 */
let strokes: Point[][] = []
let current: Point[] | null = null
let prevMid: Point | null = null
let hasImage = false
/** 回显图片的源，尺寸变化后重画用 */
let imageSrc = ''
let lastEmitted = ''
let ro: ResizeObserver | null = null

function paintBackground(c: CanvasRenderingContext2D) {
  if (props.backgroundColor) {
    c.fillStyle = props.backgroundColor
    c.fillRect(0, 0, box.w, box.h)
  }
}

function strokeStyle(c: CanvasRenderingContext2D) {
  c.lineCap = 'round'
  c.lineJoin = 'round'
  c.lineWidth = props.lineWidth
  c.strokeStyle = props.penColor
  c.fillStyle = props.penColor
}

/** 单条笔画的平滑绘制：以相邻点中点为锚，二次贝塞尔过原始点 */
function paintStroke(c: CanvasRenderingContext2D, points: Point[]) {
  if (points.length === 0) return
  if (points.length === 1) {
    c.beginPath()
    c.arc(points[0].x, points[0].y, props.lineWidth / 2, 0, Math.PI * 2)
    c.fill()
    return
  }
  c.beginPath()
  c.moveTo(points[0].x, points[0].y)
  for (let i = 1; i < points.length - 1; i++) {
    const p = points[i]
    const next = points[i + 1]
    c.quadraticCurveTo(p.x, p.y, (p.x + next.x) / 2, (p.y + next.y) / 2)
  }
  const last = points[points.length - 1]
  c.lineTo(last.x, last.y)
  c.stroke()
}

function render() {
  const c = ctx
  const el = canvasEl.value
  if (!c || !el) return
  c.setTransform(dpr, 0, 0, dpr, 0, 0)
  c.clearRect(0, 0, box.w, box.h)
  paintBackground(c)
  strokeStyle(c)
  strokes.forEach((points) => paintStroke(c, points))
}

/** 尺寸变化：按比例缩放已有坐标，保证笔迹不跑位 */
function resize() {
  const el = canvasEl.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const w = Math.max(1, Math.round(rect.width))
  const h = Math.max(1, Math.round(rect.height))
  if (w === box.w && h === box.h && ctx) return

  const prev = { ...box }
  box = { w, h }
  dpr = Math.min(typeof window !== 'undefined' ? window.devicePixelRatio || 1 : 1, 3)
  el.width = Math.round(w * dpr)
  el.height = Math.round(h * dpr)
  ctx = el.getContext('2d')
  if (!ctx) return

  if (prev.w > 0 && (prev.w !== w || prev.h !== h)) {
    const rx = w / prev.w
    const ry = h / prev.h
    strokes = strokes.map((points) => points.map((p) => ({ x: p.x * rx, y: p.y * ry })))
    current = null
  }
  render()
  if (hasImage && imageSrc) loadImage(imageSrc)
}

function pointFrom(e: PointerEvent): Point {
  const el = canvasEl.value
  if (!el) return { x: 0, y: 0 }
  const rect = el.getBoundingClientRect()
  return { x: e.clientX - rect.left, y: e.clientY - rect.top }
}

/** 实时描边：只画新增的一小段，避免每次 move 全量重绘 */
function appendPoint(p: Point) {
  const c = ctx
  const points = current
  if (!c || !points) return
  points.push(p)
  strokeStyle(c)
  if (points.length === 1) {
    // 单点（点一下没拖动）：直接画个圆点，给出即时反馈
    c.beginPath()
    c.arc(p.x, p.y, props.lineWidth / 2, 0, Math.PI * 2)
    c.fill()
    return
  }

  if (points.length === 2) {
    c.beginPath()
    c.moveTo(points[0].x, points[0].y)
    c.lineTo(p.x, p.y)
    c.stroke()
    prevMid = { x: (points[0].x + p.x) / 2, y: (points[0].y + p.y) / 2 }
    return
  }

  const from = prevMid ?? points[points.length - 2]
  const prev = points[points.length - 2]
  const mid = { x: (prev.x + p.x) / 2, y: (prev.y + p.y) / 2 }
  c.beginPath()
  c.moveTo(from.x, from.y)
  c.quadraticCurveTo(prev.x, prev.y, mid.x, mid.y)
  c.stroke()
  prevMid = mid
}

function onPointerDown(e: PointerEvent) {
  if (props.readonly) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  e.preventDefault()
  if (strokes.length >= props.maxStrokes) {
    strokes.shift()
    render()
  }
  current = []
  strokes.push(current)
  prevMid = null
  hasImage = false
  drawing.value = true
  appendPoint(pointFrom(e))
  emit('start')
}

function onPointerMove(e: PointerEvent) {
  if (!drawing.value) return
  e.preventDefault()
  // 合并同一帧内的采样点，笔迹更顺滑（指针事件可能一帧多个）
  const events = typeof e.getCoalescedEvents === 'function' ? e.getCoalescedEvents() : []
  if (events.length > 1) {
    events.forEach((ev) => appendPoint(pointFrom(ev)))
  } else {
    appendPoint(pointFrom(e))
  }
}

function finishStroke() {
  if (!drawing.value) return
  drawing.value = false
  current = null
  prevMid = null
  // 松手后按平滑算法重绘一次，保证屏幕与导出结果完全一致
  render()
  empty.value = strokes.length === 0 && !hasImage
  if (strokes.length) emitChange()
  emit('end')
}

function computeBBox() {
  let minX = Infinity
  let minY = Infinity
  let maxX = -Infinity
  let maxY = -Infinity
  strokes.forEach((points) =>
    points.forEach((p) => {
      if (p.x < minX) minX = p.x
      if (p.y < minY) minY = p.y
      if (p.x > maxX) maxX = p.x
      if (p.y > maxY) maxY = p.y
    }),
  )
  if (!Number.isFinite(minX)) return null
  return { minX, minY, maxX, maxY }
}

function toDataURL(type?: 'png' | 'jpeg') {
  const el = canvasEl.value
  if (!el) return ''
  const fmt = type ?? props.format
  const mime = `image/${fmt}`
  const original = () => (fmt === 'jpeg' ? el.toDataURL(mime, 0.92) : el.toDataURL(mime))

  if (!props.trim) return original()
  const bbox = computeBBox()
  if (!bbox) return original()

  const pad = Math.ceil(props.lineWidth) + 4
  const sx = Math.max(0, bbox.minX - pad)
  const sy = Math.max(0, bbox.minY - pad)
  const ex = Math.min(box.w, bbox.maxX + pad)
  const ey = Math.min(box.h, bbox.maxY + pad)
  const w = ex - sx
  const h = ey - sy
  if (w <= 0 || h <= 0) return original()

  const out = document.createElement('canvas')
  out.width = Math.max(1, Math.round(w * dpr))
  out.height = Math.max(1, Math.round(h * dpr))
  const c = out.getContext('2d')
  if (!c) return original()
  if (props.backgroundColor) {
    c.fillStyle = props.backgroundColor
    c.fillRect(0, 0, out.width, out.height)
  }
  // 源图是 devicePixel 位图，裁切参数也要乘 dpr
  c.drawImage(
    el,
    sx * dpr,
    sy * dpr,
    w * dpr,
    h * dpr,
    0,
    0,
    out.width,
    out.height,
  )
  return fmt === 'jpeg' ? out.toDataURL(mime, 0.92) : out.toDataURL(mime)
}

function emitChange() {
  const value = toDataURL()
  lastEmitted = value
  emit('update:modelValue', value)
  emit('change', value)
}

function undo() {
  if (!strokes.length) return
  strokes.pop()
  hasImage = false
  render()
  empty.value = strokes.length === 0
  if (strokes.length) emitChange()
  else {
    lastEmitted = ''
    emit('update:modelValue', '')
    emit('change', '')
  }
}

function clear() {
  strokes = []
  current = null
  prevMid = null
  hasImage = false
  render()
  empty.value = true
  lastEmitted = ''
  emit('update:modelValue', '')
  emit('change', '')
  emit('clear')
}

/** 外部传入的图（回显）：按 contain 铺到画布中央 */
function loadImage(src: string) {
  const c = ctx
  if (!c) return
  if (!src) {
    strokes = []
    hasImage = false
    render()
    empty.value = true
    return
  }
  if (src === lastEmitted) return
  imageSrc = src
  const img = new Image()
  img.onload = () => {
    const canvas = ctx
    if (!canvas) return
    strokes = []
    current = null
    canvas.setTransform(dpr, 0, 0, dpr, 0, 0)
    canvas.clearRect(0, 0, box.w, box.h)
    paintBackground(canvas)
    const scale = Math.min(box.w / img.width, box.h / img.height)
    const w = img.width * scale
    const h = img.height * scale
    canvas.drawImage(img, (box.w - w) / 2, (box.h - h) / 2, w, h)
    hasImage = true
    empty.value = false
  }
  img.src = src
}

function stopDrawing() {
  if (drawing.value) finishStroke()
}

onMounted(async () => {
  await nextTick()
  resize()
  if (props.modelValue) loadImage(props.modelValue)
  if (typeof window !== 'undefined') {
    window.addEventListener('pointermove', onPointerMove, { passive: false })
    window.addEventListener('pointerup', stopDrawing)
    window.addEventListener('pointercancel', stopDrawing)
  }
  if (typeof ResizeObserver !== 'undefined' && canvasEl.value) {
    ro = new ResizeObserver(() => resize())
    ro.observe(canvasEl.value)
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('pointermove', onPointerMove)
    window.removeEventListener('pointerup', stopDrawing)
    window.removeEventListener('pointercancel', stopDrawing)
  }
  ro?.disconnect()
  ro = null
})

watch(
  () => props.modelValue,
  (v) => {
    if (v !== lastEmitted) loadImage(v ?? '')
  },
)

defineExpose({
  /** 清空画布 */
  clear,
  /** 撤销上一笔 */
  undo,
  /** 导出 dataURL */
  toDataURL,
  /** 画布是否为空 */
  isEmpty: () => strokes.length === 0 && !hasImage,
})
</script>

<template>
  <div class="jm-signature" :class="{ 'is-readonly': readonly }">
    <canvas
      ref="canvasEl"
      class="jm-signature__canvas"
      :style="{ height: cssHeight }"
      role="img"
      aria-label="手写签名画布"
      @pointerdown="onPointerDown"
    />

    <div v-if="empty && placeholder" class="jm-signature__placeholder">
      <jm-icon name="edit" :size="16" />
      <span>{{ placeholder }}</span>
    </div>

    <div v-if="showToolbar && !readonly" class="jm-signature__toolbar">
      <button
        type="button"
        class="jm-signature__btn"
        :disabled="empty"
        @click="undo"
      >
        <jm-icon name="undo" :size="14" />
        <span>{{ undoText }}</span>
      </button>
      <button type="button" class="jm-signature__btn" :disabled="empty" @click="clear">
        <jm-icon name="trash" :size="14" />
        <span>{{ clearText }}</span>
      </button>
    </div>
  </div>
</template>

<style>
.jm-signature {
  position: relative;
  width: 100%;
  overflow: hidden;
  border: 1px solid var(--jm-border-color);
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-elevated);
  font-family: var(--jm-font-family);
}

.jm-signature__canvas {
  display: block;
  width: 100%;
  /* 书写时禁止滚动，否则手指一动页面就跟着走 */
  touch-action: none;
  cursor: crosshair;
}

.jm-signature.is-readonly .jm-signature__canvas {
  cursor: default;
  touch-action: auto;
}

.jm-signature__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: var(--jm-text-color-4);
  font-size: var(--jm-font-size-sm);
  pointer-events: none;
  user-select: none;
}

.jm-signature__toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  padding: 4px 8px;
  border-top: 1px solid var(--jm-border-color-2);
  background: var(--jm-bg-elevated);
}

.jm-signature__btn {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  height: 28px;
  padding: 0 8px;
  border: none;
  border-radius: var(--jm-radius-sm);
  background: transparent;
  color: var(--jm-text-color-2);
  font-family: inherit;
  font-size: var(--jm-font-size-xs);
  line-height: 1;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-signature__btn:active {
  background: var(--jm-bg-active);
}

.jm-signature__btn:disabled {
  color: var(--jm-text-color-4);
  background: transparent;
  cursor: not-allowed;
}
</style>
