<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { showImagePreview } from './image-preview'
import JmIcon from './Icon.vue'
import type { PhotoWallItem } from './photo-wall-context'

defineOptions({ name: 'JmPhotoWall' })

interface Cell {
  uid: number
  item: PhotoWallItem
}

interface Slot {
  x: number
  y: number
  w: number
  h: number
}

const props = withDefaults(
  defineProps<{
    /** 图片列表 */
    items?: PhotoWallItem[]
    /** 固定列数；不传则按容器宽度与 columnWidth 自动计算 */
    columns?: number
    /** 单列基准宽度（px），决定响应式列数 */
    columnWidth?: number
    /** 间距（px） */
    gap?: number
    /** 圆角 */
    radius?: number | string
    /** 懒加载：进入视口附近才加载图片 */
    lazy?: boolean
    /** 懒加载提前量 */
    lazyOffset?: string
    /** 点击打开大图预览 */
    preview?: boolean
    /** 预览挂载容器（内嵌手机模拟框 / 弹窗内演示时传入） */
    previewTarget?: HTMLElement | null
    /** 长按拖拽排序 */
    sortable?: boolean
    /** 长按进入拖拽的时长（ms），0 表示按下即可拖 */
    sortDelay?: number
    /** 图片比例未测量前的占位比例（height / width） */
    fallbackRatio?: number
    /** 虚拟渲染：只挂载视口附近的格子。不传则按 virtualThreshold 自动判断 */
    virtual?: boolean
    /** 超过这个数量自动开启虚拟渲染（默认 200） */
    virtualThreshold?: number
    /** 虚拟渲染时视口上下额外保留的像素，滚动时更不容易露白 */
    virtualBuffer?: number
  }>(),
  {
    items: () => [],
    columnWidth: 150,
    gap: 8,
    radius: 8,
    lazy: true,
    lazyOffset: '200px',
    preview: true,
    sortable: false,
    sortDelay: 300,
    fallbackRatio: 1,
    virtual: undefined,
    virtualThreshold: 200,
    virtualBuffer: 400,
  },
)

const emit = defineEmits<{
  (e: 'update:items', items: PhotoWallItem[]): void
  (e: 'click', item: PhotoWallItem, index: number): void
  (e: 'sort', payload: { from: number; to: number; items: PhotoWallItem[] }): void
}>()

const rootEl = ref<HTMLElement | null>(null)
/** 内部按当前顺序排列的单元格，拖拽排序时只改它 */
const cells = ref<Cell[]>([])
const positions = ref<Record<number, Slot>>({})
const wallHeight = ref(0)
const width = ref(0)
/** 已测量出的真实比例（uid → h/w） */
const ratios = ref<Record<number, number>>({})
/** 已进入视口、可以加载的 uid */
const loaded = ref<Set<number>>(new Set())

/** 可视带（相册自身坐标系）：虚拟渲染据此决定挂哪些格子 */
const viewTop = ref(0)
const viewBottom = ref(0)
const radiusValue = ref('8px')
const dragUid = ref<number | null>(null)
const dragging = ref(false)
const dragFrom = ref(0)
const dragTo = ref(0)
const dragPos = ref({ x: 0, y: 0 })

let uidSeed = 0
let lastEmitted: PhotoWallItem[] | null = null
let io: IntersectionObserver | null = null
let ro: ResizeObserver | null = null
let pressTimer = 0
let pressCell: Cell | null = null
let pressStart = { x: 0, y: 0 }
let pressOrigin = { left: 0, top: 0 }
let grabOffset = { x: 0, y: 0 }
let justDragged = false
const elMap = new Map<number, HTMLElement>()

function setEl(uid: number, el: unknown) {
  if (el instanceof HTMLElement) elMap.set(uid, el)
  else elMap.delete(uid)
}

/* ---------------- 布局 ---------------- */

function columnCount() {
  const gap = props.gap
  if (props.columns && props.columns > 0) return props.columns
  const w = width.value
  if (!w) return 1
  return Math.max(1, Math.floor((w + gap) / (props.columnWidth + gap)))
}

/** 瀑布流：逐个塞进当前最矮的一列 */
function relayout() {
  const w = width.value
  const gap = props.gap
  if (!w || !cells.value.length) {
    positions.value = {}
    wallHeight.value = 0
    return
  }
  const cols = columnCount()
  const colW = (w - gap * (cols - 1)) / cols
  const heights = new Array(cols).fill(0)
  const next: Record<number, Slot> = {}

  cells.value.forEach((cell) => {
    const ratio = ratios.value[cell.uid] ?? cell.item.ratio ?? props.fallbackRatio
    const h = Math.max(1, Math.round(colW * ratio))
    let col = 0
    for (let i = 1; i < cols; i++) {
      if (heights[i] < heights[col] - 0.5) col = i
    }
    const x = col * (colW + gap)
    const y = heights[col]
    next[cell.uid] = { x, y, w: colW, h }
    heights[col] = y + h + gap
  })

  positions.value = next
  wallHeight.value = Math.max(0, Math.max(...heights) - gap)
  // 行高/列数变化后可视带要重新算，否则虚拟渲染会挂着不该挂的格子
  if (useVirtual.value) scheduleView()
}

/* ---------------- 虚拟渲染 ---------------- */

const useVirtual = computed(() =>
  props.virtual === undefined ? cells.value.length >= props.virtualThreshold : props.virtual,
)

/** 需要挂到 DOM 上的格子：可视带 + buffer；正在拖的那个必须留着 */
const renderCells = computed(() => {
  const all = cells.value
  if (!useVirtual.value) return all.map((cell, index) => ({ cell, index }))
  const top = viewTop.value - props.virtualBuffer
  const bottom = viewBottom.value + props.virtualBuffer
  const out: Array<{ cell: Cell; index: number }> = []
  all.forEach((cell, index) => {
    const slot = positions.value[cell.uid]
    if (!slot) return
    if (cell.uid === dragUid.value || (slot.y + slot.h >= top && slot.y <= bottom)) {
      out.push({ cell, index })
    }
  })
  return out
})

let scrollParents: HTMLElement[] = []
let viewRaf = 0

function collectScrollParents() {
  scrollParents = []
  let el: HTMLElement | null = rootEl.value?.parentElement ?? null
  while (el) {
    const style = getComputedStyle(el)
    if (/(auto|scroll)/.test(style.overflowY + style.overflow)) scrollParents.push(el)
    el = el.parentElement
  }
}

/** 求相册与所有滚动祖先、浏览器视口的交集，换算成相册内坐标 */
function updateView() {
  const root = rootEl.value
  if (!root) return
  if (!useVirtual.value) {
    viewTop.value = 0
    viewBottom.value = wallHeight.value
    return
  }
  let top = 0
  let bottom = window.innerHeight || document.documentElement.clientHeight
  scrollParents.forEach((el) => {
    const r = el.getBoundingClientRect()
    top = Math.max(top, r.top)
    bottom = Math.min(bottom, r.bottom)
  })
  const rr = root.getBoundingClientRect()
  viewTop.value = Math.max(0, top - rr.top)
  viewBottom.value = Math.min(wallHeight.value, Math.max(0, bottom - rr.top))
  nextTick(observeCells)
}

function scheduleView() {
  if (viewRaf) return
  viewRaf = requestAnimationFrame(() => {
    viewRaf = 0
    updateView()
  })
}

/* ---------------- 懒加载 ---------------- */

function isLoaded(cell: Cell) {
  return !props.lazy || loaded.value.has(cell.uid)
}

function markLoaded(uid: number) {
  if (loaded.value.has(uid)) return
  const next = new Set(loaded.value)
  next.add(uid)
  loaded.value = next
}

function ensureObserver() {
  if (!props.lazy || io || typeof IntersectionObserver === 'undefined') return
  io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        const el = entry.target as HTMLElement
        const uid = Number(el.dataset.uid)
        if (uid) markLoaded(uid)
        io?.unobserve(el)
      })
    },
    { root: null, rootMargin: props.lazyOffset },
  )
}

function observeCells() {
  if (!props.lazy) return
  ensureObserver()
  if (!io) return
  cells.value.forEach((cell) => {
    if (loaded.value.has(cell.uid)) return
    const el = elMap.get(cell.uid)
    if (el) io!.observe(el)
  })
}

function onImgLoad(cell: Cell, event: Event) {
  const img = event.target as HTMLImageElement
  if (cell.item.ratio || !img.naturalWidth) return
  const ratio = img.naturalHeight / img.naturalWidth
  if (!Number.isFinite(ratio) || ratio <= 0) return
  // 量到真实比例后重排一次：占位方块收成图片原本的高度
  ratios.value = { ...ratios.value, [cell.uid]: ratio }
  relayout()
}

/* ---------------- 数据同步 ---------------- */

function ingest() {
  if (props.items === lastEmitted) return
  cells.value = (props.items ?? []).map((item) => ({ uid: ++uidSeed, item }))
  ratios.value = {}
  loaded.value = new Set()
  elMap.clear()
  nextTick(() => {
    collectScrollParents()
    updateView()
    observeCells()
    relayout()
    scheduleView()
  })
}

/* ---------------- 拖拽排序 ---------------- */

function cancelPress() {
  if (pressTimer) {
    clearTimeout(pressTimer)
    pressTimer = 0
  }
}

function blockTouch(e: TouchEvent) {
  if (dragging.value) e.preventDefault()
}

function activateDrag(clientX: number, clientY: number) {
  const cell = pressCell
  if (!cell) return
  const slot = positions.value[cell.uid]
  if (!slot) return
  cancelPress()
  dragUid.value = cell.uid
  dragFrom.value = cells.value.findIndex((c) => c.uid === cell.uid)
  dragTo.value = dragFrom.value
  grabOffset = { x: clientX - pressOrigin.left - slot.x, y: clientY - pressOrigin.top - slot.y }
  dragPos.value = { x: slot.x, y: slot.y }
  dragging.value = true
  document.addEventListener('touchmove', blockTouch, { passive: false })
  document.body.style.userSelect = 'none'
}

function onItemPointerDown(e: PointerEvent, cell: Cell) {
  if (!props.sortable) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  // 已经在拖了，忽略
  if (dragUid.value != null) return
  pressCell = cell
  pressStart = { x: e.clientX, y: e.clientY }
  const rect = rootEl.value?.getBoundingClientRect()
  pressOrigin = { left: rect?.left ?? 0, top: rect?.top ?? 0 }
  if (props.sortDelay <= 0) {
    activateDrag(e.clientX, e.clientY)
    return
  }
  cancelPress()
  pressTimer = window.setTimeout(() => activateDrag(pressStart.x, pressStart.y), props.sortDelay)
}

function nearestIndex(point: { x: number; y: number }) {
  let best = dragTo.value
  let bestDist = Infinity
  cells.value.forEach((cell, i) => {
    if (cell.uid === dragUid.value) return
    const slot = positions.value[cell.uid]
    if (!slot) return
    const dx = point.x - (slot.x + slot.w / 2)
    const dy = point.y - (slot.y + slot.h / 2)
    const dist = dx * dx + dy * dy
    if (dist < bestDist) {
      bestDist = dist
      best = i
    }
  })
  return best
}

function moveTo(target: number) {
  const from = cells.value.findIndex((c) => c.uid === dragUid.value)
  if (from === -1 || from === target) return
  const next = [...cells.value]
  const [moved] = next.splice(from, 1)
  next.splice(target, 0, moved)
  cells.value = next
  dragTo.value = target
  relayout()
}

function onPointerMove(e: PointerEvent) {
  if (dragUid.value == null) {
    // 长按计时中：手指先动了就放弃拖拽，把滚动让给页面
    if (pressTimer && Math.hypot(e.clientX - pressStart.x, e.clientY - pressStart.y) > 8) {
      cancelPress()
    }
    return
  }
  if (e.cancelable) e.preventDefault()
  const rect = rootEl.value?.getBoundingClientRect()
  const left = rect?.left ?? 0
  const top = rect?.top ?? 0
  dragPos.value = {
    x: e.clientX - left - grabOffset.x,
    y: e.clientY - top - grabOffset.y,
  }
  const slot = positions.value[dragUid.value]
  const center = {
    x: dragPos.value.x + (slot?.w ?? 0) / 2,
    y: dragPos.value.y + (slot?.h ?? 0) / 2,
  }
  const target = nearestIndex(center)
  if (target !== dragTo.value) moveTo(target)
}

function endDrag() {
  cancelPress()
  if (dragUid.value == null) {
    pressCell = null
    return
  }
  const from = dragFrom.value
  const to = dragTo.value
  dragging.value = false
  dragUid.value = null
  pressCell = null
  document.removeEventListener('touchmove', blockTouch)
  document.body.style.userSelect = ''
  relayout()

  if (from !== to) {
    const items = cells.value.map((c) => c.item)
    lastEmitted = items
    emit('update:items', items)
    emit('sort', { from, to, items })
  }
  // 拖完抬手会紧跟一次 click，吞掉它，免得顺手打开预览
  justDragged = true
  window.setTimeout(() => (justDragged = false), 80)
}

/* ---------------- 预览 ---------------- */

/** 预览挂载点：优先显式传入，其次找最近的 data-jm-preview-scope（如手机模拟框） */
function resolvePreviewTarget(): HTMLElement | null {
  if (props.previewTarget) return props.previewTarget
  let el: HTMLElement | null = rootEl.value?.parentElement ?? null
  while (el) {
    if (el.hasAttribute('data-jm-preview-scope')) return el
    el = el.parentElement
  }
  return null
}

function onItemClick(cell: Cell, index: number) {
  if (justDragged) return
  emit('click', cell.item, index)
  if (!props.preview) return
  const images = cells.value.map((c) => c.item.full || c.item.src).filter(Boolean)
  if (!images.length) return
  showImagePreview({
    images,
    startPosition: Math.max(0, cells.value.findIndex((c) => c.uid === cell.uid)),
    target: resolvePreviewTarget(),
  })
}

function cellStyle(cell: Cell) {
  const slot = positions.value[cell.uid]
  if (!slot) return { display: 'none' }
  if (cell.uid === dragUid.value) {
    return {
      width: `${slot.w}px`,
      height: `${slot.h}px`,
      transform: `translate3d(${dragPos.value.x}px, ${dragPos.value.y}px, 0) scale(1.04)`,
      transition: 'none',
      zIndex: 20,
    }
  }
  return {
    width: `${slot.w}px`,
    height: `${slot.h}px`,
    transform: `translate3d(${slot.x}px, ${slot.y}px, 0)`,
  }
}

onMounted(() => {
  radiusValue.value = typeof props.radius === 'number' ? `${props.radius}px` : props.radius
  width.value = rootEl.value?.clientWidth ?? 0
  ingest()
  relayout()

  if (typeof ResizeObserver !== 'undefined' && rootEl.value) {
    ro = new ResizeObserver(() => {
      const w = rootEl.value?.clientWidth ?? 0
      if (w === width.value) return
      width.value = w
      relayout()
    })
    ro.observe(rootEl.value)
  }

  window.addEventListener('pointermove', onPointerMove, { passive: false })
  window.addEventListener('pointerup', endDrag)
  window.addEventListener('pointercancel', endDrag)

  collectScrollParents()
  updateView()
  scrollParents.forEach((el) => el.addEventListener('scroll', scheduleView, { passive: true }))
  window.addEventListener('scroll', scheduleView, { passive: true })
  window.addEventListener('resize', scheduleView)
})

onBeforeUnmount(() => {
  cancelPress()
  ro?.disconnect()
  ro = null
  io?.disconnect()
  io = null
  document.removeEventListener('touchmove', blockTouch)
  document.body.style.userSelect = ''
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', endDrag)
  window.removeEventListener('pointercancel', endDrag)
  scrollParents.forEach((el) => el.removeEventListener('scroll', scheduleView))
  scrollParents = []
  window.removeEventListener('scroll', scheduleView)
  window.removeEventListener('resize', scheduleView)
  if (viewRaf) cancelAnimationFrame(viewRaf)
})

watch(
  () => props.items,
  () => ingest(),
)
watch(
  () => [props.columns, props.columnWidth, props.gap, props.fallbackRatio],
  () => relayout(),
)
watch(
  () => props.lazy,
  () => {
    io?.disconnect()
    io = null
    nextTick(observeCells)
  },
)
watch(
  () => [props.virtual, props.virtualThreshold, props.virtualBuffer],
  () => {
    collectScrollParents()
    updateView()
  },
)
watch(
  () => props.radius,
  (v) => {
    radiusValue.value = typeof v === 'number' ? `${v}px` : v
  },
)

defineExpose({
  /** 重新计算布局（容器尺寸被外因改变时可手动调用） */
  relayout,
  /** 当前实际挂载的格子数（虚拟渲染下远小于总数） */
  renderedCount: () => renderCells.value.length,
})
</script>

<template>
  <div
    ref="rootEl"
    class="jm-photo-wall"
    :class="{ 'is-sortable': sortable, 'is-dragging': dragging }"
    :style="{
      height: `${wallHeight}px`,
      '--jm-photo-wall-gap': `${gap}px`,
      '--jm-photo-wall-radius': radiusValue,
    }"
  >
    <div
      v-for="row in renderCells"
      :key="row.cell.uid"
      :ref="(el) => setEl(row.cell.uid, el)"
      class="jm-photo-wall__item"
      :class="{ 'is-drag': row.cell.uid === dragUid }"
      :style="cellStyle(row.cell)"
      :data-uid="row.cell.uid"
      role="button"
      tabindex="0"
      :aria-label="row.cell.item.alt || `第 ${row.index + 1} 张图片`"
      @click="onItemClick(row.cell, row.index)"
      @keydown.enter.prevent="onItemClick(row.cell, row.index)"
      @keydown.space.prevent="onItemClick(row.cell, row.index)"
      @pointerdown="onItemPointerDown($event, row.cell)"
    >
      <img
        v-if="isLoaded(row.cell)"
        class="jm-photo-wall__img"
        :src="row.cell.item.src"
        :alt="row.cell.item.alt || ''"
        draggable="false"
        @load="onImgLoad(row.cell, $event)"
      />
      <img
        v-else-if="row.cell.item.thumb"
        class="jm-photo-wall__img is-thumb"
        :src="row.cell.item.thumb"
        alt=""
        draggable="false"
      />
      <div v-else class="jm-photo-wall__ph" aria-hidden="true">
        <jm-icon name="image" :size="20" />
      </div>

      <slot name="item" :item="row.cell.item" :index="row.index" />
    </div>

    <slot v-if="!cells.length" name="empty" />
  </div>
</template>

<style>
.jm-photo-wall {
  --jm-photo-wall-radius: 8px;
  position: relative;
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-photo-wall__item {
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
  border-radius: var(--jm-photo-wall-radius);
  background: var(--jm-bg-container);
  -webkit-tap-highlight-color: transparent;
  /* 排序动画：位置与尺寸都用 transform / width / height 过渡，重排时是「滑过去」而不是瞬移 */
  transition:
    transform var(--jm-motion-spring-duration, 320ms) var(--jm-motion-spring-ease, cubic-bezier(0.22, 1, 0.36, 1)),
    width 240ms var(--jm-ease-standard),
    height 240ms var(--jm-ease-standard),
    box-shadow 160ms var(--jm-ease-standard);
  will-change: transform;
}

.jm-photo-wall.is-sortable .jm-photo-wall__item {
  cursor: grab;
  /* 允许纵向滚动，长按后再接管手势 */
  touch-action: pan-y;
}

.jm-photo-wall__item:focus-visible {
  outline: 2px solid var(--jm-color-primary);
  outline-offset: 2px;
}

.jm-photo-wall__item.is-drag {
  cursor: grabbing;
  z-index: 20;
  box-shadow: var(--jm-shadow-3);
  border-radius: var(--jm-photo-wall-radius);
}

.jm-photo-wall__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
  -webkit-user-drag: none;
  animation: jm-photo-fade 240ms var(--jm-ease-out) both;
}

.jm-photo-wall__img.is-thumb {
  filter: blur(2px);
  transform: scale(1.02);
}

.jm-photo-wall__ph {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--jm-text-color-4);
  background:
    linear-gradient(
      100deg,
      var(--jm-bg-container) 20%,
      var(--jm-bg-hover) 40%,
      var(--jm-bg-container) 60%
    )
    0 0 / 200% 100%;
  animation: jm-photo-shimmer 1.4s linear infinite;
}

@keyframes jm-photo-fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes jm-photo-shimmer {
  from {
    background-position: 100% 0;
  }
  to {
    background-position: -100% 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .jm-photo-wall__item {
    transition: none;
  }

  .jm-photo-wall__ph,
  .jm-photo-wall__img {
    animation: none;
  }
}
</style>
