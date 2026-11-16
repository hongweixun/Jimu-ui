<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmPullRefresh' })

const props = withDefaults(
  defineProps<{
    /** 是否处于加载中（v-model） */
    modelValue?: boolean
    /** 禁用下拉 */
    disabled?: boolean
    /** 触发刷新的下拉距离，数字按 px */
    headHeight?: number
    pullingText?: string
    loosingText?: string
    loadingText?: string
    successText?: string
    /** "刷新成功"停留时长 */
    successDuration?: number
    /** 回弹动画时长 */
    animationDuration?: number
  }>(),
  {
    modelValue: false,
    disabled: false,
    headHeight: 50,
    pullingText: '下拉刷新',
    loosingText: '释放刷新',
    loadingText: '加载中...',
    successText: '刷新成功',
    successDuration: 500,
    animationDuration: 300,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  refresh: []
  change: [status: Status]
}>()

type Status = 'normal' | 'pulling' | 'loosing' | 'loading' | 'success'

const status = ref<Status>('normal')
const distance = ref(0)
const duration = ref(0)

const headHeightPx = computed(() => Number(props.headHeight) || 50)

const text = computed(() => {
  switch (status.value) {
    case 'loosing':
      return props.loosingText
    case 'loading':
      return props.loadingText
    case 'success':
      return props.successText
    default:
      return props.pullingText
  }
})

const trackStyle = computed(() => ({
  transform: `translate3d(0, ${distance.value}px, 0)`,
  transition: duration.value ? `transform ${duration.value}ms cubic-bezier(0.22, 0.61, 0.36, 1)` : 'none',
}))

function setStatus(s: Status) {
  if (status.value === s) return
  status.value = s
  emit('change', s)
}

/* 找到真正可滚动的祖先：只有它已经滚到顶部时，下拉才应该被我们接管 */
function getScrollParent(el: HTMLElement | null): HTMLElement | null {
  let node = el?.parentElement ?? null
  while (node) {
    const style = getComputedStyle(node)
    if (/(auto|scroll|overlay)/.test(style.overflowY) && node.scrollHeight > node.clientHeight) {
      return node
    }
    node = node.parentElement
  }
  return null
}

const root = ref<HTMLElement | null>(null)

let startY = 0
let startX = 0
let pulling = false
let axis: 'x' | 'y' | null = null

function atTop() {
  const scroller = getScrollParent(root.value)
  if (scroller) return scroller.scrollTop <= 0
  return (window.scrollY || document.documentElement.scrollTop) <= 0
}

function onPointerDown(e: PointerEvent) {
  if (props.disabled || props.modelValue || status.value === 'loading') return
  if (e.pointerType === 'mouse' && e.button !== 0) return
  if (!atTop()) return
  pulling = true
  axis = null
  startY = e.clientY
  startX = e.clientX
  duration.value = 0
  try {
    ;(e.currentTarget as HTMLElement)?.setPointerCapture?.(e.pointerId)
  } catch {
    /* 合成事件或指针已释放时捕获会失败，忽略即可 */
  }
}

function onPointerMove(e: PointerEvent) {
  if (!pulling) return
  const dy = e.clientY - startY
  const dx = e.clientX - startX

  if (!axis) {
    if (Math.abs(dy) < 5 && Math.abs(dx) < 5) return
    axis = Math.abs(dy) > Math.abs(dx) ? 'y' : 'x'
    if (axis === 'x') {
      pulling = false
      return
    }
  }

  if (dy <= 0) {
    // 往上推：取消下拉，同时把控制权交回滚动容器
    distance.value = 0
    setStatus('normal')
    if (dy < -6) pulling = false
    return
  }

  // 阻尼：越拉越沉，但始终比手指慢一截
  const damped = Math.min(dy * 0.55, headHeightPx.value * 1.8)
  distance.value = damped
  setStatus(damped >= headHeightPx.value ? 'loosing' : 'pulling')
}

function onPointerUp() {
  if (!pulling) return
  pulling = false

  if (status.value === 'loosing') {
    duration.value = props.animationDuration
    distance.value = headHeightPx.value
    setStatus('loading')
    emit('update:modelValue', true)
    emit('refresh')
    return
  }

  duration.value = props.animationDuration
  distance.value = 0
  setStatus('normal')
}

function onPointerCancel() {
  pulling = false
  duration.value = props.animationDuration
  distance.value = 0
  setStatus('normal')
}

/* 外部结束加载：先展示一小段"刷新成功"，再回弹 */
let successTimer: ReturnType<typeof setTimeout> | undefined

watch(
  () => props.modelValue,
  async (v) => {
    if (v) {
      duration.value = props.animationDuration
      distance.value = headHeightPx.value
      setStatus('loading')
      return
    }
    if (status.value !== 'loading') return
    setStatus('success')
    await nextTick()
    successTimer = setTimeout(() => {
      duration.value = props.animationDuration
      distance.value = 0
      setTimeout(() => setStatus('normal'), props.animationDuration)
    }, props.successDuration)
  },
)

onBeforeUnmount(() => {
  if (successTimer) clearTimeout(successTimer)
})

defineExpose({ distance, status })
</script>

<template>
  <div
    ref="root"
    class="jm-pull-refresh"
    :style="{ '--jm-pull-head-height': toCssSize(headHeight) }"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerCancel"
  >
    <div class="jm-pull-refresh__track" :style="trackStyle">
      <div class="jm-pull-refresh__head" :class="`is-${status}`">
        <span v-if="status === 'loading'" class="jm-pull-refresh__spinner" aria-hidden="true" />
        <jm-icon
          v-else-if="status === 'success'"
          class="jm-pull-refresh__icon"
          name="check"
          size="16px"
          :stroke-width="2"
        />
        <jm-icon
          v-else
          class="jm-pull-refresh__icon jm-pull-refresh__arrow"
          :class="{ 'is-flip': status === 'loosing' }"
          name="arrow-down"
          size="16px"
          :stroke-width="1.8"
        />
        <span class="jm-pull-refresh__text">{{ text }}</span>
      </div>
      <slot />
    </div>
  </div>
</template>

<style>
.jm-pull-refresh {
  position: relative;
  overflow: hidden;
  font-family: var(--jm-font-family);
  /* 滚动仍交给浏览器：只有"已到顶部"时才接管手势，此时原生滚动本来就无处可去。
     这里只挡住 iOS / Chrome 的整页回弹，避免和下拉刷新抢同一个手势。 */
  overscroll-behavior-y: contain;
}

.jm-pull-refresh__track {
  will-change: transform;
}

.jm-pull-refresh__head {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(var(--jm-pull-head-height, 50px) * -1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: var(--jm-pull-head-height, 50px);
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  pointer-events: none;
}

.jm-pull-refresh__icon {
  width: 16px;
  height: 16px;
  color: var(--jm-text-color-4);
  transition: transform var(--jm-motion-transition-duration, 200ms) var(--jm-ease-out, ease-out);
}

.jm-pull-refresh__arrow.is-flip {
  transform: rotate(180deg);
  color: var(--jm-color-primary);
}

.jm-pull-refresh__head.is-success .jm-pull-refresh__icon {
  color: var(--jm-color-success);
}

.jm-pull-refresh__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--jm-border-color-2);
  border-top-color: var(--jm-color-primary);
  border-radius: 50%;
  animation: jm-pull-refresh-spin 800ms linear infinite;
}

@keyframes jm-pull-refresh-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .jm-pull-refresh__spinner {
    animation-duration: 2400ms;
  }
  .jm-pull-refresh__track {
    transition: none !important;
  }
}
</style>
