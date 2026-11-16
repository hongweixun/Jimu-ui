<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, provide, reactive, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import { TABS_KEY, type TabItem, type TabName } from './tabs-context'

defineOptions({ name: 'JmTabs' })

const props = withDefaults(
  defineProps<{
    modelValue?: TabName
    /** line 下划线 / card 卡片 / segment 分段 */
    type?: 'line' | 'card' | 'segment'
    size?: 'small' | 'medium' | 'large'
    color?: string
    radius?: number | string
    /** 内容区是否加内边距 */
    padded?: boolean
    /** 内容切换动效：track 平移过渡 */
    animated?: boolean
    /** 手势滑动切换内容（Pointer Events，鼠标 / 触屏都支持；自动启用 track 布局） */
    swipeable?: boolean
    /** 动效时长，数字按 ms */
    duration?: number | string
    /** 标签栏是否可横向滚动（标签过多时开启，激活项自动滚动居中） */
    scrollable?: boolean
    /** scrollable 时一屏可见的标签数量 */
    visibleCount?: number
    /** line 指示器宽度：默认跟激活项文字等宽；传数字 / px 则固定宽度并居中 */
    lineWidth?: number | string
    /**
     * 切换前钩子：返回 false 或 reject 则不切换。
     * 适合「表单没保存，先弹确认框」的场景，异步期间不会重复触发。
     */
    beforeChange?: (name: TabName) => boolean | Promise<boolean>
  }>(),
  { type: 'line', size: 'medium', padded: true, duration: 300 },
)

const emit = defineEmits<{
  'update:modelValue': [value: TabName]
  change: [value: TabName]
  /** 点击标签时触发（disabled 也会触发，由业务自行拦截） */
  click: [name: TabName]
}>()

const tabs = reactive<TabItem[]>([])

const activeName = computed<TabName | undefined>(() =>
  props.modelValue !== undefined ? props.modelValue : tabs[0]?.name,
)

/** 拦截中的一个切换还没结论时，后来的点击先忽略，避免连点叠起多次确认 */
let changing = false

async function setActive(name: TabName) {
  const tab = tabs.find((t) => t.name === name)
  if (tab?.disabled) return
  if (changing) return
  if (props.beforeChange && name !== activeName.value) {
    changing = true
    try {
      const ok = await props.beforeChange(name)
      if (!ok) return
    } catch {
      return
    } finally {
      changing = false
    }
  }
  emit('update:modelValue', name)
  emit('change', name)
}

function addTab(tab: TabItem) {
  if (!tabs.some((t) => t.name === tab.name)) tabs.push(tab)
}

function removeTab(name: TabName) {
  const i = tabs.findIndex((t) => t.name === name)
  if (i > -1) tabs.splice(i, 1)
}

const activeIndex = computed(() => Math.max(0, tabs.findIndex((t) => t.name === activeName.value)))

/* ---------- track 模式：animated / swipeable 共用同一套平移布局 ----------
 * 外层内容区只负责 overflow 裁剪，内层 .jm-tabs__track 负责平移——
 * 裁剪发生在元素自身局部坐标系，如果裁剪和平移在同一元素上，翻页后
 * 后面的面板会永远落在裁剪区外被裁掉 */
const trackMode = computed(() => !!(props.animated || props.swipeable))

const durationMs = computed(() => {
  const n = Number(props.duration)
  return Number.isFinite(n) && n >= 0 ? n : 300
})

provide(TABS_KEY, {
  active: activeName,
  animated: trackMode,
  setActive,
  addTab,
  removeTab,
})

/* ---------- 指示器：line 默认跟激活项文字等宽，segment 仍是整格色块 ---------- */
const listRef = ref<HTMLElement>()
const navRef = ref<HTMLElement>()
const itemEls: (HTMLElement | undefined)[] = []
const indicator = ref<{ x: number; w: number } | null>(null)

function setItemRef(el: unknown, i: number) {
  itemEls[i] = (el as HTMLElement) || undefined
}

function measureIndicator() {
  if (props.type !== 'line') return
  const list = listRef.value
  const el = itemEls[activeIndex.value]
  if (!list || !el) return
  const label = (el.querySelector('.jm-tabs__label') as HTMLElement | null) || el
  const listRect = list.getBoundingClientRect()
  const rect = label.getBoundingClientRect()
  let w: number
  if (props.lineWidth !== undefined) {
    const size = toCssSize(props.lineWidth)
    w = (size ? parseFloat(size) : NaN) || rect.width
  } else {
    w = rect.width
  }
  indicator.value = { x: rect.left - listRect.left + (rect.width - w) / 2, w }
}

/** scrollable 时激活项自动滚动到标签栏中间 */
function scrollToActive() {
  if (!props.scrollable) return
  const nav = navRef.value
  const el = itemEls[activeIndex.value]
  if (!nav || !el) return
  const target = el.offsetLeft - (nav.clientWidth - el.offsetWidth) / 2
  nav.scrollTo({ left: Math.max(0, target), behavior: 'smooth' })
}

/* ---------- 键盘：Tab 只停在激活项上，← → / Home / End 在标签间移动 ----------
 * 这是 WAI-ARIA tabs 的标准交互：整组标签对外只占一个 Tab 停靠点，
 * 进去之后用方向键在标签间切换，避免用户按十几次 Tab 才穿过去 */
function onNavKeydown(e: KeyboardEvent) {
  if (!tabs.length) return
  if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) return

  let next = -1
  if (e.key === 'Home') {
    // 首尾也可能被禁用，取该方向上第一个可用标签
    next = tabs.findIndex((t) => !t.disabled)
  } else if (e.key === 'End') {
    for (let i = tabs.length - 1; i >= 0; i--) {
      if (!tabs[i].disabled) {
        next = i
        break
      }
    }
  } else {
    const dir = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : -1
    const n = tabs.length
    // 环形查找下一个可用标签，跳过 disabled
    for (let step = 1; step <= n; step++) {
      const i = (activeIndex.value + dir * step + n * 2) % n
      if (!tabs[i].disabled) {
        next = i
        break
      }
    }
  }
  if (next < 0) return
  e.preventDefault()
  void setActive(tabs[next].name)
  nextTick(() => itemEls[next]?.focus())
}

let ro: ResizeObserver | undefined

onMounted(() => {
  nextTick(() => {
    measureIndicator()
    scrollToActive()
  })
  if (typeof ResizeObserver !== 'undefined' && listRef.value) {
    ro = new ResizeObserver(() => measureIndicator())
    ro.observe(listRef.value)
  }
  // 字体异步加载完成会改变文字宽度，重新测量一次
  document.fonts?.ready.then(() => measureIndicator()).catch(() => {})
})

onBeforeUnmount(() => ro?.disconnect())

watch(
  [activeIndex, () => props.lineWidth, () => props.scrollable, () => tabs.length],
  () =>
    nextTick(() => {
      measureIndicator()
      scrollToActive()
    }),
)

const indicatorStyle = computed(() => {
  if (props.type === 'segment') {
    const n = tabs.length || 1
    return { width: `calc(100% / ${n})`, transform: `translateX(${activeIndex.value * 100}%)` }
  }
  const ind = indicator.value
  if (!ind) return { opacity: '0' }
  return { width: `${ind.w}px`, transform: `translateX(${ind.x}px)` }
})

/* ---------- 手势滑动切换：Pointer Events，触屏与鼠标统一处理 ---------- */
const contentRef = ref<HTMLElement>()
const dragX = ref(0)
const isDragging = ref(false)
let startX = 0
let startY = 0
let axis: 'x' | 'y' | null = null
let pointerId: number | null = null

function onPointerDown(e: PointerEvent) {
  if (!trackMode.value || tabs.length < 2) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  pointerId = e.pointerId
  startX = e.clientX
  startY = e.clientY
  axis = null
  isDragging.value = false
}

function onPointerMove(e: PointerEvent) {
  if (!trackMode.value || pointerId === null || e.pointerId !== pointerId) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY
  if (!axis) {
    if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return
    // 方向锁：只有横向意图才接管；纵向交给浏览器（touch-action: pan-y）
    axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y'
    if (axis === 'x') {
      isDragging.value = true
      // 鼠标拖出内容区也能继续跟手
      try {
        contentRef.value?.setPointerCapture(e.pointerId)
      } catch {
        /* ignore */
      }
    }
  }
  if (axis !== 'x') return
  let offset = dx
  // 两端越界给 1/3 阻尼，暗示"到头了"
  if ((activeIndex.value === 0 && dx > 0) || (activeIndex.value === tabs.length - 1 && dx < 0)) {
    offset = dx / 3
  }
  dragX.value = offset
}

function onPointerUp(e: PointerEvent) {
  if (pointerId === null || (e.pointerId !== undefined && e.pointerId !== pointerId)) {
    pointerId = null
    axis = null
    return
  }
  const horizontal = axis === 'x'
  const dx = dragX.value
  pointerId = null
  axis = null
  if (!horizontal) return
  isDragging.value = false
  const width = contentRef.value?.clientWidth || 1
  const threshold = width * 0.25
  let target = activeIndex.value
  if (dx <= -threshold && activeIndex.value < tabs.length - 1) target = activeIndex.value + 1
  else if (dx >= threshold && activeIndex.value > 0) target = activeIndex.value - 1
  dragX.value = 0
  const tab = tabs[target]
  if (tab && !tab.disabled) setActive(tab.name)
}

const trackStyle = computed(() => {
  if (!trackMode.value) return undefined
  return {
    transform: `translateX(calc(${activeIndex.value * -100}% + ${dragX.value}px))`,
    transition: isDragging.value
      ? 'none'
      : `transform ${durationMs.value}ms var(--jm-motion-transition-ease)`,
  }
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-tabs-radius'] = r
  if (props.color) s['--jm-tabs-color'] = props.color
  if (props.visibleCount) s['--jm-tabs-visible-count'] = String(props.visibleCount)
  return s
})

watch(
  () => tabs.length,
  () => {
    if (props.modelValue === undefined && tabs[0]) setActive(tabs[0].name)
  },
)

defineExpose({ resize: measureIndicator, scrollToActive })
</script>

<template>
  <div
    class="jm-tabs"
    :class="[
      `jm-tabs--${type}`,
      `jm-tabs--${size}`,
      { 'is-padded': padded, 'is-scrollable': scrollable },
    ]"
    :style="styles"
  >
    <div ref="navRef" class="jm-tabs__nav" role="tablist" @keydown="onNavKeydown">
      <div ref="listRef" class="jm-tabs__list">
        <button
          v-for="(tab, i) in tabs"
          :key="String(tab.name)"
          :ref="(el) => setItemRef(el, i)"
          type="button"
          role="tab"
          class="jm-tabs__item"
          :class="{ 'is-active': tab.name === activeName, 'is-disabled': tab.disabled }"
          :aria-selected="tab.name === activeName"
          :tabindex="tab.name === activeName ? 0 : -1"
          :disabled="tab.disabled"
          @click="emit('click', tab.name); setActive(tab.name)"
        >
          <span class="jm-tabs__label">{{ tab.label }}</span>
          <span v-if="tab.badge !== undefined" class="jm-tabs__badge">{{ tab.badge }}</span>
        </button>
        <span
          v-if="type === 'line' || type === 'segment'"
          class="jm-tabs__indicator"
          :style="indicatorStyle"
          aria-hidden="true"
        />
      </div>
    </div>

    <div
      ref="contentRef"
      class="jm-tabs__content"
      :class="{ 'jm-tabs__content--track': trackMode, 'is-dragging': isDragging }"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
    >
      <div v-if="trackMode" class="jm-tabs__track" :style="trackStyle">
        <slot />
      </div>
      <slot v-else />
    </div>
  </div>
</template>

<style>
.jm-tabs {
  --jm-tabs-color: var(--jm-color-primary);
  --jm-tabs-radius: var(--jm-radius);
  width: 100%;
  font-family: var(--jm-font-family);
  color: var(--jm-text-color);
}

/* 可滚动：导航条横向滚动、隐藏滚动条；一屏可见标签数可配 */
.jm-tabs.is-scrollable .jm-tabs__nav {
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.jm-tabs.is-scrollable .jm-tabs__nav::-webkit-scrollbar {
  display: none;
}

.jm-tabs.is-scrollable .jm-tabs__item {
  flex: 0 0 auto;
  min-width: calc(100% / var(--jm-tabs-visible-count, 3));
  padding: 0 14px;
}

.jm-tabs__nav {
  position: relative;
}

.jm-tabs__list {
  position: relative;
  display: flex;
  align-items: center;
  gap: 2px;
}

.jm-tabs__item {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex: 1 1 0;
  min-width: 0;
  height: 44px;
  padding: 0 10px;
  border: 0;
  background: none;
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color-2);
  cursor: pointer;
  outline: none;
  white-space: nowrap;
  -webkit-tap-highlight-color: transparent;
  transition: color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-tabs__label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.jm-tabs__item.is-active {
  color: var(--jm-tabs-color);
  font-weight: var(--jm-font-weight-medium);
}

.jm-tabs__item.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-tabs__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 15px;
  height: 15px;
  padding: 0 4px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-danger);
  color: #fff;
  font-size: 10px;
  line-height: 1;
}

.jm-tabs__indicator {
  position: absolute;
  left: 0;
  bottom: 0;
  z-index: 0;
  height: 2.5px;
  border-radius: 2px;
  background: var(--jm-tabs-color);
  /* 宽度 + 位移一起过渡，文字等宽模式下测量值变化也能平滑跟上 */
  transition:
    transform var(--jm-duration-3) var(--jm-motion-transition-ease),
    width var(--jm-duration-3) var(--jm-motion-transition-ease);
}

/* 下划线 */
.jm-tabs--line .jm-tabs__nav {
  border-bottom: 1px solid var(--jm-border-color);
}

.jm-tabs--line .jm-tabs__indicator {
  bottom: -0.5px;
}

/* 卡片 */
.jm-tabs--card .jm-tabs__nav {
  padding: 4px;
  background: var(--jm-bg-input);
  border-radius: var(--jm-tabs-radius);
}

.jm-tabs--card .jm-tabs__item {
  border-radius: calc(var(--jm-tabs-radius) - 3px);
  height: 36px;
}

.jm-tabs--card .jm-tabs__item.is-active {
  background: var(--jm-bg-container);
  color: var(--jm-tabs-color);
  box-shadow: var(--jm-shadow-1);
}

/* 分段 */
.jm-tabs--segment .jm-tabs__nav {
  padding: 3px;
  border: 1px solid var(--jm-border-color);
  border-radius: var(--jm-tabs-radius);
}

.jm-tabs--segment .jm-tabs__indicator {
  top: 3px;
  bottom: 3px;
  height: auto;
  border-radius: calc(var(--jm-tabs-radius) - 2px);
  opacity: 0.12;
}

.jm-tabs--segment .jm-tabs__item.is-active {
  color: var(--jm-tabs-color);
}

/* 尺寸 */
.jm-tabs--small .jm-tabs__item {
  height: 34px;
  font-size: var(--jm-font-size-sm);
}

.jm-tabs--large .jm-tabs__item {
  height: 52px;
  font-size: var(--jm-font-size-lg);
}

/* 内容 */
.jm-tabs__content {
  padding: 0;
}

.jm-tabs.is-padded .jm-tabs__content {
  padding: var(--jm-space-4) 2px;
}

/* track 模式：外层只负责裁剪 + 手势，内层轨道负责平移 */
.jm-tabs__content--track {
  overflow: hidden;
  /* 纵向滚动留给浏览器，横向手势由组件接管 */
  touch-action: pan-y;
  cursor: grab;
}

.jm-tabs__content--track.is-dragging {
  cursor: grabbing;
  user-select: none;
}

.jm-tabs.is-padded .jm-tabs__content--track {
  padding: 0;
}

.jm-tabs__track {
  display: flex;
  align-items: stretch;
  will-change: transform;
}

.jm-tabs__track .jm-tab-panel {
  flex: 0 0 100%;
  min-width: 0;
  display: block;
}

.jm-tabs.is-padded .jm-tabs__track .jm-tab-panel {
  padding: var(--jm-space-4) 2px;
}
</style>
