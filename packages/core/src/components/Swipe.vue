<script setup lang="ts">
import {
  Comment,
  Fragment,
  Text,
  cloneVNode,
  computed,
  defineComponent,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  useSlots,
  watch,
  type PropType,
  type VNode,
} from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSwipe' })

const props = withDefaults(
  defineProps<{
    /** 自动播放间隔（ms），0 或 false 关闭 */
    autoplay?: number | boolean
    /** 切换动画时长（ms） */
    duration?: number
    /** 初始下标 */
    initialSwipe?: number
    /** 循环播放 */
    loop?: boolean
    /** 纵向轮播 */
    vertical?: boolean
    /** 允许手势拖动 */
    touchable?: boolean
    /** 显示指示点 */
    showIndicators?: boolean
    /** 指示点位置 */
    indicatorPosition?: 'bottom' | 'top'
    indicatorColor?: string
    indicatorActiveColor?: string
    /** 容器高度，数字按 px */
    height?: number | string
    /** 手势结束的判定速度（px/ms） */
    thresholdSpeed?: number
    /** 容器圆角，数字按 px */
    radius?: number | string
  }>(),
  {
    autoplay: 0,
    duration: 400,
    initialSwipe: 0,
    loop: false,
    vertical: false,
    touchable: true,
    showIndicators: true,
    indicatorPosition: 'bottom',
    height: 160,
    thresholdSpeed: 0.35,
  },
)

const emit = defineEmits<{
  change: [index: number]
  click: [index: number]
}>()

/* useSlots() 在默认泛型下会被 vue-tsc 推导成 {}，显式标注避免 slots.default 报错 */
const slots = useSlots() as { default?: (...args: unknown[]) => VNode[] }

/* ---------------- 子项收集 ----------------
   Swipe 不解析业务数据，只把默认插槽里的 vnode 平铺成 slides；
   循环时用 cloneVNode 首尾各复制一份，形成 [last, ...real, first] 的轨道。 */
function flatten(nodes: VNode[]): VNode[] {
  const out: VNode[] = []
  for (const v of nodes) {
    if (!v || v.type === Comment) continue
    if (v.type === Fragment && Array.isArray(v.children)) {
      out.push(...flatten(v.children as VNode[]))
      continue
    }
    if (v.type === Text && !String(v.children ?? '').trim()) continue
    out.push(v)
  }
  return out
}

const slotNodes = computed(() => flatten((slots.default?.() ?? []) as VNode[]))
const count = computed(() => slotNodes.value.length)
const loopEnabled = computed(() => props.loop && count.value > 1)

/** 把已有 vnode 交给 vue 渲染的中转组件（vnode 不能直接写在模板里） */
const SlideRenderer = defineComponent({
  name: 'JmSwipeSlideRenderer',
  props: { vnode: { type: Object as PropType<VNode>, required: true } },
  setup(p) {
    return () => p.vnode
  },
})

const slides = computed<VNode[]>(() => {
  const list = slotNodes.value
  if (!loopEnabled.value) return list
  const first = cloneVNode(list[0], { key: '__jm-swipe-first' })
  const last = cloneVNode(list[list.length - 1], { key: '__jm-swipe-last' })
  return [last, ...list, first]
})

/* ---------------- 状态 ---------------- */
const root = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)

const size = ref(0) // 单屏宽/高（px）
const current = ref(0) // 真实下标
const active = ref(0) // 轨道下标（循环时比 current 多 1）
const offset = ref(0) // 拖拽期间的手势位移
const animated = ref(false)

const trackStyle = computed(() => {
  const base = -active.value * size.value + offset.value
  return {
    transform: props.vertical ? `translate3d(0, ${base}px, 0)` : `translate3d(${base}px, 0, 0)`,
    transition: animated.value
      ? `transform ${props.duration}ms cubic-bezier(0.22, 0.61, 0.36, 1)`
      : 'none',
  }
})

const rootStyle = computed(() => {
  const s: Record<string, string> = {}
  const h = toCssSize(props.height)
  if (h) s['--jm-swipe-height'] = h
  const r = toCssSize(props.radius)
  if (r) s['--jm-swipe-radius'] = r
  if (props.indicatorColor) s['--jm-swipe-dot-color'] = props.indicatorColor
  if (props.indicatorActiveColor) s['--jm-swipe-dot-active-color'] = props.indicatorActiveColor
  return s
})

/* ---------------- 位置控制 ---------------- */
const mod = (n: number, m: number) => ((n % m) + m) % m

function measure() {
  if (!root.value) return
  size.value = props.vertical ? root.value.clientHeight : root.value.clientWidth
}

/** 直接跳到某个真实下标 */
function goTo(index: number, silent = false) {
  if (count.value === 0) return
  const target = Math.min(Math.max(0, Math.floor(index)), count.value - 1)
  current.value = target
  active.value = loopEnabled.value ? target + 1 : target
  offset.value = 0
  animated.value = true
  if (!silent) emit('change', target)
}

/** 前进/后退一格（循环模式下允许 active 越界，结束后由 normalize 归位） */
function step(dir: 1 | -1) {
  if (count.value <= 1) return
  if (loopEnabled.value) {
    active.value += dir
    current.value = mod(active.value - 1, count.value)
    offset.value = 0
    animated.value = true
    emit('change', current.value)
    return
  }
  const next = current.value + dir
  if (next < 0 || next >= count.value) return
  goTo(next)
}

const next = () => step(1)
const prev = () => step(-1)

/** 循环越界后瞬间归位：关掉过渡 → 换到等价位置 → 强制重排 → 恢复过渡 */
async function normalize() {
  if (!loopEnabled.value) return
  let target: number | null = null
  if (active.value === 0) target = count.value
  else if (active.value === count.value + 1) target = 1
  if (target === null) return
  animated.value = false
  active.value = target
  await nextTick()
  void track.value?.offsetHeight
  // 归位这一帧若仍开着过渡，视觉上会看到"倒带"，所以延到下一帧再恢复
  animated.value = true
}

function onTransitionEnd(e: TransitionEvent) {
  if (e.target !== track.value || e.propertyName !== 'transform') return
  void normalize()
}

/* ---------------- 手势 ---------------- */
let startX = 0
let startY = 0
let startTime = 0
const dragging = ref(false)
let axis: 'x' | 'y' | null = null
let moved = false
/** down 阶段不能捕获指针：Chromium 会把随后合成的 click 一并派发给捕获元素，
    指示点等内部元素的 click 就全被劫持了；真正拖起来（move 判定后）再捕获 */
let captured = false

function capturePointer(e: PointerEvent) {
  if (captured) return
  captured = true
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件或指针已释放时捕获会失败，忽略即可 */
  }
}

function onPointerDown(e: PointerEvent) {
  if (!props.touchable || count.value <= 1) return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  dragging.value = true
  axis = null
  moved = false
  captured = false
  startX = e.clientX
  startY = e.clientY
  startTime = Date.now()
  offset.value = 0
  animated.value = false
  stopAutoplay()
}

function onPointerMove(e: PointerEvent) {
  if (!dragging.value) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY

  if (!axis) {
    if (Math.abs(dx) < 5 && Math.abs(dy) < 5) return
    // 方向锁：横向组件只认横向手势，纵向滚动交还给页面
    axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y'
    if ((props.vertical && axis === 'x') || (!props.vertical && axis === 'y')) {
      dragging.value = false
      animated.value = true
      resumeAutoplay()
      return
    }
    // 确认是拖动了才捕获：手指/鼠标拖出组件后 move/up 仍继续派发，拖动不中断
    capturePointer(e)
  }

  const delta = props.vertical ? dy : dx
  if (Math.abs(delta) > 5) moved = true

  let d = delta
  if (!loopEnabled.value) {
    // 两端加阻尼，拖不动但能感到"到头了"
    const atStart = active.value === 0 && delta > 0
    const atEnd = active.value === count.value - 1 && delta < 0
    if (atStart || atEnd) d = delta * 0.35
  }
  offset.value = d
}

function onPointerUp(e: PointerEvent) {
  if (!dragging.value) {
    resumeAutoplay()
    return
  }
  dragging.value = false
  captured = false
  const delta = props.vertical ? e.clientY - startY : e.clientX - startX
  const speed = Math.abs(delta) / Math.max(1, Date.now() - startTime)
  const distThreshold = Math.min(size.value * 0.25, 80)
  const shouldMove = Math.abs(delta) > distThreshold || speed > props.thresholdSpeed

  offset.value = 0
  animated.value = true

  if (shouldMove) {
    const dir = delta < 0 ? 1 : -1
    const canMove = loopEnabled.value || (dir === 1 ? active.value < count.value - 1 : active.value > 0)
    if (canMove) step(dir)
  }
  resumeAutoplay()
}

function onPointerCancel() {
  if (!dragging.value) return
  dragging.value = false
  captured = false
  offset.value = 0
  animated.value = true
  resumeAutoplay()
}

/* ---------------- 自动播放 ---------------- */
let timer: ReturnType<typeof setInterval> | undefined

function stopAutoplay() {
  if (timer) clearInterval(timer)
  timer = undefined
}

function startAutoplay() {
  stopAutoplay()
  const interval = Number(props.autoplay)
  if (!interval || count.value <= 1) return
  timer = setInterval(() => {
    if (dragging.value) return
    if (!loopEnabled.value && current.value >= count.value - 1) {
      goTo(0)
      return
    }
    step(1)
  }, Math.max(1000, interval))
}

function resumeAutoplay() {
  startAutoplay()
}

/* ---------------- 生命周期 ---------------- */
let ro: ResizeObserver | null = null

onMounted(() => {
  current.value = Math.min(Math.max(0, props.initialSwipe), Math.max(0, count.value - 1))
  active.value = loopEnabled.value ? current.value + 1 : current.value
  measure()
  // 首帧先不带过渡落位，避免从 0 滑到初始页
  requestAnimationFrame(() => {
    animated.value = true
  })
  if (typeof ResizeObserver !== 'undefined' && root.value) {
    ro = new ResizeObserver(measure)
    ro.observe(root.value)
  } else if (typeof window !== 'undefined') {
    window.addEventListener('resize', measure)
  }
  startAutoplay()
})

onBeforeUnmount(() => {
  stopAutoplay()
  ro?.disconnect()
  if (typeof window !== 'undefined') window.removeEventListener('resize', measure)
})

watch(
  () => [props.autoplay, count.value],
  () => startAutoplay(),
)

watch(count, (n) => {
  if (current.value > n - 1) goTo(Math.max(0, n - 1), true)
})

function onClick() {
  if (moved) {
    moved = false
    return
  }
  emit('click', current.value)
}

defineExpose({ next, prev, goTo, resize: measure, current, count })
</script>

<template>
  <div
    ref="root"
    class="jm-swipe"
    :class="{ 'jm-swipe--vertical': vertical, 'is-dragging': dragging }"
    :style="rootStyle"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerCancel"
    @click="onClick"
  >
    <div
      ref="track"
      class="jm-swipe__track"
      :style="trackStyle"
      @transitionend="onTransitionEnd"
    >
      <template v-for="(node, i) in slides" :key="`${i}-${node.key ?? 'slide'}`">
        <div class="jm-swipe__slide">
          <SlideRenderer :vnode="node" />
        </div>
      </template>
    </div>

    <div
      v-if="showIndicators && count > 1"
      class="jm-swipe__indicators"
      :class="`jm-swipe__indicators--${indicatorPosition}`"
    >
      <span
        v-for="n in count"
        :key="n"
        class="jm-swipe__dot"
        :class="{ 'is-active': n - 1 === current }"
        @click.stop="goTo(n - 1)"
      />
    </div>
  </div>
</template>

<style>
.jm-swipe {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: var(--jm-swipe-height, 160px);
  border-radius: var(--jm-swipe-radius, 0);
  background: var(--jm-bg-input);
  font-family: var(--jm-font-family);
  /* 横向轮播只接管横向手势，纵向滚动仍交给页面 */
  touch-action: pan-y;
  -webkit-tap-highlight-color: transparent;
}

.jm-swipe--vertical {
  touch-action: pan-x;
}

.jm-swipe__track {
  display: flex;
  width: 100%;
  height: 100%;
  will-change: transform;
}

.jm-swipe--vertical .jm-swipe__track {
  flex-direction: column;
}

.jm-swipe__slide {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.jm-swipe.is-dragging {
  cursor: grabbing;
}

/* 指示点 */
.jm-swipe__indicators {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 var(--jm-space-3);
  pointer-events: none;
}

.jm-swipe__indicators--bottom {
  bottom: 10px;
}

.jm-swipe__indicators--top {
  top: 10px;
}

.jm-swipe__dot {
  position: relative;
  width: 6px;
  height: 6px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-swipe-dot-color, rgba(255, 255, 255, 0.6));
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.25);
  transition:
    width var(--jm-motion-transition-duration, 200ms) var(--jm-ease-out, ease-out),
    background-color var(--jm-motion-transition-duration, 200ms) var(--jm-ease-out, ease-out);
  cursor: pointer;
  pointer-events: auto;
}

/* 6px 的点太难点：透明扩大热区，不影响视觉与布局 */
.jm-swipe__dot::after {
  content: '';
  position: absolute;
  inset: -7px;
}

.jm-swipe__dot.is-active {
  width: 14px;
  background: var(--jm-swipe-dot-active-color, #fff);
}
</style>
