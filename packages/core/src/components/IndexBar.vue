<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, provide, ref } from 'vue'
import { INDEX_BAR_KEY } from './index-bar-context'

defineOptions({ name: 'JmIndexBar' })

const props = withDefaults(
  defineProps<{
    /** 索引列表；不传则按锚点注册顺序自动生成 */
    indexList?: string[]
    /** 分组标题吸顶 */
    sticky?: boolean
    /** 高亮色 */
    highlightColor?: string
    /** 滚动容器：CSS 选择器或元素，默认整页 */
    scrollContainer?: string | HTMLElement
  }>(),
  {
    sticky: true,
  },
)

const emit = defineEmits<{ change: [index: string] }>()

interface Entry {
  index: string
  getEl: () => HTMLElement | undefined
}

/* 按注册顺序（= DOM 顺序）保存锚点 */
const entries = ref<Entry[]>([])

function register(index: string, getEl: () => HTMLElement | undefined) {
  entries.value = [...entries.value.filter((e) => e.index !== index), { index, getEl }]
  nextTick(() => {
    measure()
    if (!active.value) active.value = entries.value[0]?.index ?? ''
  })
  return () => {
    entries.value = entries.value.filter((e) => e.index !== index)
  }
}

const list = computed(() => props.indexList ?? entries.value.map((e) => e.index))
const active = ref('')

provide(INDEX_BAR_KEY, {
  active,
  register,
  sticky: computed(() => props.sticky),
})

/* ---------------- 滚动容器 ---------------- */
function container(): HTMLElement | Window {
  const s = props.scrollContainer
  if (!s) return window
  if (typeof s === 'string') return (document.querySelector(s) as HTMLElement) ?? window
  return s
}

function containerTop(): number {
  const c = container()
  return c === window ? 0 : (c as HTMLElement).getBoundingClientRect().top
}

/** 找出最后一个「标题已到达容器顶部」的分组 */
function measure() {
  const top = containerTop()
  let current = entries.value[0]?.index ?? ''
  for (const e of entries.value) {
    const el = e.getEl()
    if (!el) continue
    if (el.getBoundingClientRect().top - top <= 1) current = e.index
  }
  if (current && current !== active.value) {
    active.value = current
    emit('change', current)
  }
}

function onScroll() {
  measure()
}

let ro: ResizeObserver | null = null

onMounted(() => {
  const c = container()
  c.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
  if (typeof ResizeObserver !== 'undefined') {
    ro = new ResizeObserver(() => measure())
    entries.value.forEach((e) => {
      const el = e.getEl()
      if (el) ro?.observe(el)
    })
  }
  nextTick(measure)
})

onBeforeUnmount(() => {
  const c = container()
  c.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
  ro?.disconnect()
})

/* ---------------- 点击 / 滑动定位 ---------------- */
function scrollToIndex(index: string, smooth = true) {
  const entry = entries.value.find((e) => e.index === index)
  const el = entry?.getEl()
  if (!el) return
  const c = container()
  const behavior: ScrollBehavior = smooth ? 'smooth' : 'auto'
  const delta = el.getBoundingClientRect().top - containerTop()
  if (c === window) {
    window.scrollTo({ top: window.scrollY + delta, behavior })
  } else {
    ;(c as HTMLElement).scrollTo({ top: (c as HTMLElement).scrollTop + delta, behavior })
  }
  if (active.value !== index) {
    active.value = index
    emit('change', index)
  }
}

/** 触摸/拖动时的大号提示气泡 */
const tip = ref<{ text: string; top: number } | null>(null)
const bar = ref<HTMLElement>()
const root = ref<HTMLElement>()

/** 把视口坐标换算成相对组件的偏移，气泡才会贴着索引条而不是飘到视口另一头 */
function tipTop(clientY: number): number {
  const rect = root.value?.getBoundingClientRect()
  return rect ? clientY - rect.top : clientY
}

function indexAt(clientY: number): string | null {
  const el = bar.value
  if (!el) return null
  const rect = el.getBoundingClientRect()
  if (!list.value.length) return null
  const itemH = rect.height / list.value.length
  const i = Math.floor((clientY - rect.top) / itemH)
  return list.value[Math.min(Math.max(i, 0), list.value.length - 1)] ?? null
}

function onPointerDown(e: PointerEvent) {
  const text = indexAt(e.clientY)
  if (!text) return
  tip.value = { text, top: tipTop(e.clientY) }
  scrollToIndex(text, false)
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件下捕获会失败，忽略 */
  }
}

function onPointerMove(e: PointerEvent) {
  if (!tip.value) return
  const text = indexAt(e.clientY)
  if (!text) return
  if (text !== tip.value.text) {
    tip.value = { text, top: tipTop(e.clientY) }
    scrollToIndex(text, false)
  } else {
    tip.value = { ...tip.value, top: tipTop(e.clientY) }
  }
}

function onPointerUp() {
  tip.value = null
}

const barStyle = computed(() =>
  props.highlightColor ? { '--jm-index-bar-active': props.highlightColor } : {},
)

defineExpose({ scrollToIndex, active })
</script>

<template>
  <div ref="root" class="jm-index-bar" :style="barStyle">
    <div class="jm-index-bar__content">
      <slot />
    </div>

    <div
      ref="bar"
      class="jm-index-bar__sidebar"
      role="navigation"
      aria-label="索引"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
      @pointerleave="onPointerUp"
    >
      <span
        v-for="item in list"
        :key="item"
        class="jm-index-bar__item"
        :class="{ 'is-active': item === active }"
        >{{ item }}</span
      >
    </div>

    <div v-if="tip" class="jm-index-bar__tip" :style="{ top: `${tip.top}px` }">
      {{ tip.text }}
    </div>
  </div>
</template>

<style>
.jm-index-bar {
  --jm-index-bar-active: var(--jm-color-primary);
  position: relative;
  display: flex;
  align-items: flex-start;
  font-family: var(--jm-font-family);
}

.jm-index-bar__content {
  flex: 1;
  min-width: 0;
}

/* 索引条跟随滚动贴在容器顶部，高度超出时自己滚动 */
.jm-index-bar__sidebar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: none;
  width: 22px;
  padding: var(--jm-space-1) 0;
  margin-left: var(--jm-space-1);
  max-height: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  touch-action: none;
  user-select: none;
  -webkit-user-select: none;
}

.jm-index-bar__sidebar::-webkit-scrollbar {
  display: none;
}

.jm-index-bar__item {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 16px;
  font-size: var(--jm-font-size-xs);
  line-height: 1.2;
  color: var(--jm-text-color-3);
  cursor: pointer;
  transition: color var(--jm-duration-fast, 0.15s) ease;
}

.jm-index-bar__item.is-active {
  color: var(--jm-index-bar-active);
  font-weight: var(--jm-font-weight-medium);
}

/* 拖拽时的大号提示气泡 */
.jm-index-bar__tip {
  position: absolute;
  right: 26px;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-top: -28px;
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-mask);
  color: var(--jm-text-color-inverse);
  font-size: 22px;
  font-weight: var(--jm-font-weight-medium);
  pointer-events: none;
}
</style>
