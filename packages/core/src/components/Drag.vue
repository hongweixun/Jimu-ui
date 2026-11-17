<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useAttrs, watch, type CSSProperties } from 'vue'

/* 根节点是 Teleport：自动继承会把父组件的 style/class 挂到 Teleport 上被丢弃，
   关掉后手动绑到内层 div，用户写的 style="left: 40px" 才能生效 */
defineOptions({ name: 'JmDrag', inheritAttrs: false })

const attrs = useAttrs()

const props = withDefaults(
  defineProps<{
    /** 允许拖动的方向 */
    direction?: 'x' | 'y' | 'xy'
    /** 松手后吸附到最近的边，不传则停在哪里就是哪里 */
    attraction?: 'x' | 'y' | 'xy'
    disabled?: boolean
    /** 距视口（或 target 容器）边缘的留白，元素始终留在该范围内 */
    boundary?: { top?: number | string; bottom?: number | string; left?: number | string; right?: number | string }
    zIndex?: number | string
    /** 挂载位置；false 表示原地渲染（文档手机框内演示用） */
    teleport?: string | false
    /** 约束容器选择器：传入后改为在容器内绝对定位拖拽（默认相对视口 fixed） */
    target?: string | false
  }>(),
  {
    direction: 'xy',
    disabled: false,
    zIndex: 90,
    teleport: false,
    target: false,
  },
)

const emit = defineEmits<{
  click: [event: Event]
}>()

const rootRef = ref<HTMLElement | null>(null)

const style = computed(() => {
  const s: CSSProperties = { zIndex: String(props.zIndex) }
  return s
})

/* ---------- 位置状态 ---------- */
/** 用户写的 left/top（style 上的初始值），reset 回这里 */
let initialLeft = 0
let initialTop = 0
const left = ref(0)
const top = ref(0)

function num(v: unknown, fallback = 0): number {
  if (typeof v === 'number') return v
  const n = parseFloat(String(v))
  return Number.isNaN(n) ? fallback : n
}

function readInitial() {
  const el = rootRef.value
  if (!el) return
  const st = getComputedStyle(el)
  if (st.left === 'auto') {
    const r = el.getBoundingClientRect()
    const cr = containerEl?.getBoundingClientRect()
    initialLeft = cr ? Math.round(r.left - cr.left) : Math.round(r.left)
    initialTop = cr ? Math.round(r.top - cr.top) : Math.round(r.top)
  } else {
    initialLeft = num(st.left)
    initialTop = num(st.top)
  }
  left.value = initialLeft
  top.value = initialTop
}

function applyPosition() {
  const el = rootRef.value
  if (!el) return
  el.style.left = `${left.value}px`
  el.style.top = `${top.value}px`
}

watch([left, top], applyPosition)

/* ---------- 边界约束 ---------- */
let containerEl: HTMLElement | null = null

function bounds() {
  const el = rootRef.value
  if (!el || typeof window === 'undefined') return { minX: 0, maxX: 0, minY: 0, maxY: 0 }
  const w = el.offsetWidth
  const h = el.offsetHeight
  const vw = containerEl ? containerEl.clientWidth : window.innerWidth
  const vh = containerEl ? containerEl.clientHeight : window.innerHeight
  const b = props.boundary || {}
  return {
    minX: num(b.left),
    maxX: vw - w - num(b.right),
    minY: num(b.top),
    maxY: vh - h - num(b.bottom),
  }
}

/* ---------- 指针拖拽 ---------- */
let dragging = false
let startX = 0
let startY = 0
let originLeft = 0
let originTop = 0
let moved = false

function onPointerDown(e: PointerEvent) {
  if (props.disabled || e.button > 0) return
  const el = rootRef.value
  if (!el) return
  if (left.value === 0 && top.value === 0 && el.style.left === '') readInitial()

  dragging = true
  moved = false
  startX = e.clientX
  startY = e.clientY
  originLeft = left.value
  originTop = top.value
  el.setPointerCapture?.(e.pointerId)
  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', onPointerUp)
  window.addEventListener('pointercancel', onPointerUp)
}

function onPointerMove(e: PointerEvent) {
  if (!dragging) return
  let dx = e.clientX - startX
  let dy = e.clientY - startY
  if (Math.abs(dx) > 4 || Math.abs(dy) > 4) moved = true
  if (props.direction === 'x') dy = 0
  if (props.direction === 'y') dx = 0
  const { minX, maxX, minY, maxY } = bounds()
  left.value = Math.min(Math.max(originLeft + dx, Math.min(minX, maxX)), Math.max(minX, maxX))
  top.value = Math.min(Math.max(originTop + dy, Math.min(minY, maxY)), Math.max(minY, maxY))
  e.preventDefault()
}

function onPointerUp() {
  if (!dragging) return
  dragging = false
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
  window.removeEventListener('pointercancel', onPointerUp)
  if (moved) attractionSnap()
}

/** 松手后朝最近的边吸附 */
function attractionSnap() {
  const dir = props.attraction
  if (!dir) return
  const { minX, maxX, minY, maxY } = bounds()
  if (dir === 'x' || dir === 'xy') {
    const mid = (minX + maxX) / 2
    left.value = left.value < mid ? minX : maxX
  }
  if (dir === 'y' || dir === 'xy') {
    const mid = (minY + maxY) / 2
    top.value = top.value < mid ? minY : maxY
  }
}

function onClickCapture(e: Event) {
  /* 拖拽过的松手不算点击，避免误触业务 click */
  if (moved) {
    e.stopPropagation()
    e.preventDefault()
    return
  }
  emit('click', e)
}

function onClick(e: MouseEvent) {
  onClickCapture(e)
}

/* ---------- 对外方法 ---------- */
function reset() {
  left.value = initialLeft
  top.value = initialTop
}

function resize() {
  const { minX, maxX, minY, maxY } = bounds()
  left.value = Math.min(Math.max(left.value, minX), maxX)
  top.value = Math.min(Math.max(top.value, minY), maxY)
}

defineExpose({ reset, resize })

/* teleport=false 时不脱离文档流；target 给了容器则在容器内绝对定位 */
onMounted(() => {
  const el = rootRef.value
  if (!el) return
  if (props.target) containerEl = document.querySelector(props.target)
  /* 等 CSS 就绪后再测量；用户写了 inline left/top 则直接采用，不受样式加载时序影响 */
  requestAnimationFrame(() => {
    if (el.style.left !== '' && el.style.top !== '') {
      initialLeft = num(el.style.left)
      initialTop = num(el.style.top)
      left.value = initialLeft
      top.value = initialTop
      applyPosition()
    } else {
      const st = getComputedStyle(el)
      if (st.position !== 'fixed' && st.position !== 'absolute') {
        /* 用户没写位置：按当前视觉位置固定下来 */
        const r = el.getBoundingClientRect()
        const cr = containerEl?.getBoundingClientRect()
        initialLeft = cr ? Math.round(r.left - cr.left) : Math.round(r.left)
        initialTop = cr ? Math.round(r.top - cr.top) : Math.round(r.top)
        el.style.left = `${initialLeft}px`
        el.style.top = `${initialTop}px`
        left.value = initialLeft
        top.value = initialTop
      } else {
        readInitial()
        applyPosition()
      }
    }
    window.addEventListener('resize', resize)
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
  window.removeEventListener('pointercancel', onPointerUp)
})
</script>

<template>
  <Teleport :to="typeof teleport === 'string' ? teleport : undefined" :disabled="teleport === false || !teleport">
    <div
      ref="rootRef"
      v-bind="attrs"
      class="jm-drag"
      :class="{ 'is-disabled': disabled, 'is-contained': !!target }"
      :style="style"
      @pointerdown="onPointerDown"
      @click="onClick"
    >
      <slot />
    </div>
  </Teleport>
</template>

<style>
.jm-drag {
  position: fixed;
  touch-action: none;
  user-select: none;
  -webkit-user-select: none;
  -webkit-tap-highlight-color: transparent;
  cursor: grab;
}

/* target 容器模式：在容器内绝对定位，跟随容器滚动 */
.jm-drag.is-contained {
  position: absolute;
}

.jm-drag:active {
  cursor: grabbing;
}

.jm-drag.is-disabled {
  cursor: auto;
  pointer-events: none;
}
</style>
