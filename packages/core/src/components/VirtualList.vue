<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmVirtualList' })

const props = withDefaults(
  defineProps<{
    /** 数据源 */
    items: unknown[]
    /**
     * 行高（px）。`dynamic` 为 false 时是固定行高；为 true 时仅作为「未测量前的估值」。
     */
    itemHeight?: number
    /**
     * 动态行高：行高由内容决定，渲染后逐行测量。
     * 打开后每行不再受 `item-height` 约束（只作首屏估值），适合聊天气泡、富文本这类行高不齐的数据。
     */
    dynamic?: boolean
    /** 动态模式下未测量行的估值（不传则用 itemHeight） */
    estimatedItemHeight?: number
    /** 视口上下各多渲染几行，滚动时减小白屏概率 */
    overscan?: number
    /** 视口高度；不传则撑满父容器（父容器需有确定高度） */
    height?: number | string
    /** 行 key：字段名或取值函数，不传用索引 */
    itemKey?: string | ((item: unknown, index: number) => string | number)
  }>(),
  { itemHeight: 48, overscan: 5, dynamic: false },
)

const emit = defineEmits<{
  /** 滚动事件（passive 节流到 rAF） */
  scroll: [offsetTop: number]
  /** 滚动到底部（含 buffer 内），常用于触发加载更多 */
  'scroll-bottom': []
}>()

const viewport = ref<HTMLElement | null>(null)
const scrollTop = ref(0)
const viewHeight = ref(0)

const viewportStyle = computed(() => {
  const s: Record<string, string> = {}
  const h = toCssSize(props.height)
  if (h) {
    s.height = h
    s.overflowY = 'auto'
  }
  return s
})

const total = computed(() => props.items.length)
/** 未测量行的估值 */
const estimate = computed(() => props.estimatedItemHeight ?? props.itemHeight)

/**
 * 已测量行高，按行 key 存。
 * 用 key 而不是下标，是为了在头部插入数据（加载更早的聊天记录）时，
 * 已测量的高度不会整体错位到别的行上。
 */
const sizes = reactive(new Map<string | number, number>())

function resolveKey(item: unknown, index: number): string | number {
  const k = props.itemKey
  if (!k) return index
  if (typeof k === 'function') return k(item, index)
  const v = (item as Record<string, unknown> | undefined)?.[k]
  return typeof v === 'string' || typeof v === 'number' ? v : index
}

function heightAt(index: number): number {
  if (!props.dynamic) return props.itemHeight
  return sizes.get(resolveKey(props.items[index], index)) ?? estimate.value
}

/** 每行的 y 起点（前缀和），长度 n+1，最后一项即内容总高 */
const offsets = computed(() => {
  const n = total.value
  const out = new Array<number>(n + 1)
  let acc = 0
  for (let i = 0; i < n; i++) {
    out[i] = acc
    acc += heightAt(i)
  }
  out[n] = acc
  return out
})

const contentHeight = computed(() => offsets.value[total.value] ?? 0)

/** 可视区间（含 overscan）：用二分找起点，O(log n) */
const range = computed(() => {
  const n = total.value
  if (!n) return { start: 0, end: 0 }
  const offs = offsets.value
  const top = scrollTop.value
  const h = viewHeight.value || 360

  let lo = 0
  let hi = n - 1
  let start = 0
  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    if (offs[mid] <= top) {
      start = mid
      lo = mid + 1
    } else {
      hi = mid - 1
    }
  }

  const bottom = top + h
  let end = start
  while (end < n && offs[end] < bottom) end++

  return {
    start: Math.max(0, start - props.overscan),
    end: Math.min(n, end + props.overscan),
  }
})

const list = computed(() => {
  const { start, end } = range.value
  const offs = offsets.value
  const out: Array<{ item: unknown; index: number; key: string | number; top: number }> = []
  for (let i = start; i < end; i++) {
    const item = props.items[i]
    out.push({ item, index: i, key: resolveKey(item, i), top: offs[i] })
  }
  return out
})

function itemStyle(row: { top: number; index: number }) {
  const s: Record<string, string> = { transform: `translateY(${row.top}px)` }
  // 固定行高时把高度写死，行内容超高也不会把后续行顶歪；动态模式让内容自己撑
  if (!props.dynamic) s.height = `${props.itemHeight}px`
  return s
}

let rafId = 0

function onScroll() {
  if (rafId) return
  rafId = requestAnimationFrame(() => {
    rafId = 0
    const el = viewport.value
    if (!el) return
    scrollTop.value = el.scrollTop
    viewHeight.value = el.clientHeight
    emit('scroll', el.scrollTop)
    const threshold = props.dynamic ? Math.max(40, estimate.value) : props.itemHeight
    if (el.scrollTop + el.clientHeight >= contentHeight.value - threshold) {
      emit('scroll-bottom')
    }
  })
}

/* ------------------------------------------------------------------ */
/* 动态行高：测量 + 滚动锚定                                             */
/* ------------------------------------------------------------------ */

let ro: ResizeObserver | undefined
const observed = new Set<Element>()

/** 把当前渲染出来的行挂到 ResizeObserver 上，卸载的行摘掉 */
function syncObserved() {
  const el = viewport.value
  if (!ro || !el) return
  observed.forEach((node) => {
    if (!node.isConnected) {
      ro!.unobserve(node)
      observed.delete(node)
    }
  })
  el.querySelectorAll<HTMLElement>('.jm-virtual-list__item').forEach((node) => {
    if (observed.has(node)) return
    ro!.observe(node)
    observed.add(node)
  })
}

/**
 * 落地一批测量结果。
 * 行高变化会让后面的行整体位移，如果变化的行在视口上方，用户会看到内容「跳」一下——
 * 所以把上方行的增量补进 scrollTop，视觉位置保持不动。
 */
function applySizes(updates: Map<number, number>) {
  if (!updates.size) return
  const el = viewport.value
  const prev = offsets.value
  let shift = 0
  let changed = false

  updates.forEach((h, index) => {
    const item = props.items[index]
    if (item === undefined) return
    const key = resolveKey(item, index)
    const old = sizes.get(key) ?? estimate.value
    if (Math.abs(old - h) < 0.5) return
    if (el && prev[index] + old <= el.scrollTop + 0.5) shift += h - old
    sizes.set(key, h)
    changed = true
  })

  // 跳行锚点还在生效期：按最新的行高把目标行校正到位（哪怕这次测的行不在视口上方）
  if (changed && pendingAnchor) {
    scheduleAnchor()
    return
  }
  if (!changed || !shift || !el) return
  const target = el.scrollTop + shift
  // 等 DOM 按新高度排完再改滚动位置，rAF 保证布局已刷新（nextTick 可能赶在渲染前）
  requestAnimationFrame(() => {
    const node = viewport.value
    if (!node) return
    node.scrollTop = target
    scrollTop.value = node.scrollTop
  })
}

function onItemResize(entries: ResizeObserverEntry[]) {
  if (!props.dynamic) return
  const updates = new Map<number, number>()
  entries.forEach((entry) => {
    const node = entry.target as HTMLElement
    const index = Number(node.dataset.index)
    const h = node.offsetHeight
    if (Number.isFinite(index) && h > 0) updates.set(index, h)
  })
  applySizes(updates)
}

let lastWidth = 0

function measure(): boolean {
  const el = viewport.value
  if (!el) return false
  const width = el.clientWidth
  viewHeight.value = el.clientHeight
  // 宽度变了，换行位置全变，旧测量值全部作废，按估值重排后重新测量
  const reset = props.dynamic && !!lastWidth && Math.abs(width - lastWidth) > 0.5
  if (reset) {
    sizes.clear()
    nextTick(syncObserved)
  }
  lastWidth = width
  return reset
}

function dropAnchor() {
  pendingAnchor = null
  lastAnchorTop = -1
  clearTimeout(anchorTimer)
}

onMounted(() => {
  measure()
  viewport.value?.addEventListener('scroll', onScroll, { passive: true })
  viewport.value?.addEventListener('touchstart', dropAnchor, { passive: true })
  viewport.value?.addEventListener('wheel', dropAnchor, { passive: true })
  viewport.value?.addEventListener('pointerdown', dropAnchor, { passive: true })
  if (typeof ResizeObserver !== 'undefined') {
    ro = new ResizeObserver((entries) => {
      /* 同一批回调里可能既有视口又有行（首次 observe 时就是这样），
         必须分开处理：只看有没有视口会把行条目一起丢掉，测量就永远不生效 */
      const rows = entries.filter((e) => e.target !== viewport.value)
      const viewportEntry = entries.find((e) => e.target === viewport.value)
      const reset = viewportEntry ? measure() : false
      // 宽度刚变过，这批行高是按旧宽度量的，丢掉等重排后的新回调
      if (rows.length && !reset) onItemResize(rows)
    })
  }
  if (viewport.value && ro) {
    ro.observe(viewport.value)
    if (props.dynamic) nextTick(syncObserved)
  }
})

onBeforeUnmount(() => {
  viewport.value?.removeEventListener('scroll', onScroll)
  viewport.value?.removeEventListener('touchstart', dropAnchor)
  viewport.value?.removeEventListener('wheel', dropAnchor)
  viewport.value?.removeEventListener('pointerdown', dropAnchor)
  clearTimeout(anchorTimer)
  if (anchorRaf) cancelAnimationFrame(anchorRaf)
  ro?.disconnect()
  observed.clear()
  if (rafId) cancelAnimationFrame(rafId)
})

/* 数据量变化后视口高度可能变（撑满父容器场景），补一次测量 */
watch(total, () => measure())

/* 渲染窗口变化时把新出现的行纳入测量（用字符串比对，避免每次滚动都触发） */
watch(
  () => `${range.value.start}:${range.value.end}`,
  () => {
    if (props.dynamic) nextTick(syncObserved)
  },
)

/**
 * 跳行锚点：动态行高时，跳到远处还没测量的行，落地后这一带会被测出真实高度，
 * 内容整体位移会把目标顶走。这里记住「谁应该在哪」，等测量稳定再校正一次。
 */
type Align = 'start' | 'center' | 'end'
let pendingAnchor: { index: number; align: Align } | null = null
/** 上一次校正落到的 scrollTop；两次一致说明已收敛，锚点可以撤了 */
let lastAnchorTop = -1
/** 安全网：最多锚 1.5 秒，防止测量一直不收敛时把用户锁死 */
let anchorTimer = 0
/** 合并多个测量批次触发的校正 */
let anchorRaf = 0

function scheduleAnchor() {
  if (anchorRaf) return
  anchorRaf = requestAnimationFrame(() => {
    anchorRaf = 0
    applyAnchor()
  })
}

function applyAnchor() {
  const el = viewport.value
  const a = pendingAnchor
  if (!el || !a) return
  const offs = offsets.value
  const h = heightAt(a.index)
  let top = offs[a.index]
  if (a.align === 'center') top = offs[a.index] - (el.clientHeight - h) / 2
  else if (a.align === 'end') top = offs[a.index] + h - el.clientHeight
  const target = Math.max(0, top)

  // 目标没变就不动 scrollTop；锚点保持 pending，后续测量还会继续校正
  if (Math.abs(target - lastAnchorTop) < 1) return
  lastAnchorTop = target
  el.scrollTop = target
  scrollTop.value = el.scrollTop

  clearTimeout(anchorTimer)
  anchorTimer = setTimeout(dropAnchor, 1500)
}

/**
 * 滚动到指定行
 * @param index 行下标
 * @param align 对齐方式：start 顶部 / center 居中 / end 底部
 */
function scrollToIndex(index: number, align: Align = 'start') {
  if (!viewport.value || !total.value) return
  const i = Math.min(Math.max(0, Math.round(index)), total.value - 1)
  pendingAnchor = { index: i, align }
  applyAnchor()
}

/** 滚到底部（聊天、日志流的「跳到最新」） */
function scrollToBottom() {
  if (!total.value) return
  scrollToIndex(total.value - 1, 'end')
}

/** 丢掉已测量的高度，按估值重新开始（数据整体换掉或字号变化时用） */
function refresh() {
  dropAnchor()
  sizes.clear()
  nextTick(() => {
    measure()
    syncObserved()
  })
}

defineExpose({ scrollToIndex, scrollToBottom, refresh })
</script>

<template>
  <div ref="viewport" class="jm-virtual-list" :style="viewportStyle">
    <div class="jm-virtual-list__content" :style="{ height: contentHeight + 'px' }">
      <div
        v-for="row in list"
        :key="row.key"
        class="jm-virtual-list__item"
        :class="{ 'is-dynamic': dynamic }"
        :style="itemStyle(row)"
        :data-index="row.index"
      >
        <slot name="item" :item="row.item" :index="row.index" />
      </div>
    </div>
  </div>
</template>

<style>
.jm-virtual-list {
  position: relative;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  /* 浏览器原生滚动锚定和组件自己的补偿会互相打架（上次校正被拉回去），关掉 */
  overflow-anchor: none;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  font-family: var(--jm-font-family);
}

.jm-virtual-list__content {
  position: relative;
  width: 100%;
}

/* 每行绝对定位、用 transform 推到自己的 y 起点：
   动态行高时行高各不相同，统一由 JS 算出的前缀和决定位置 */
.jm-virtual-list__item {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  will-change: transform;
}

/* 动态行高：不再锁高度，由内容撑开，同时避免 margin 塌陷导致测量值偏小 */
.jm-virtual-list__item.is-dynamic {
  display: flow-root;
}
</style>
