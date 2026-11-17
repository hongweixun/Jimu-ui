<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmPopover' })

const props = withDefaults(
  defineProps<{
    show?: boolean
    /** 气泡内容，也可用 default 插槽 */
    content?: string
    /** click：点触发器开合；manual：完全受控 */
    trigger?: 'click' | 'manual'
    placement?: 'top' | 'bottom' | 'left' | 'right'
    /** 贴着触发器的那条边怎么对齐（左右方向忽略） */
    align?: 'start' | 'center' | 'end'
    /** dark：深色底白字（默认）；light：白底描边 */
    theme?: 'dark' | 'light'
    /** 与触发器的距离 */
    offset?: number
    arrow?: boolean
    disabled?: boolean
    /** 点面板外部关闭 */
    closeOnClickOutside?: boolean
    /** 点面板内容后关闭（放按钮时通常打开） */
    closeOnClickContent?: boolean
    /** 面板最大宽度，默认不限制 */
    maxWidth?: number | string
    /** 层级，默认 1200 */
    zIndex?: number
  }>(),
  {
    show: undefined,
    trigger: 'click',
    placement: 'top',
    align: 'center',
    theme: 'dark',
    offset: 8,
    arrow: true,
    closeOnClickOutside: true,
    closeOnClickContent: false,
    zIndex: 1200,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  open: []
  close: []
}>()

const root = ref<HTMLElement | null>(null)

/* 未受控时用内部状态：传了 show 就走受控，行为完全由使用方决定 */
const innerVisible = ref(false)
const visible = computed({
  get: () => (props.show === undefined ? innerVisible.value : props.show),
  set: (v: boolean) => {
    innerVisible.value = v
    emit('update:show', v)
    if (v) emit('open')
    else emit('close')
  },
})

function toggle() {
  if (props.disabled || props.trigger === 'manual') return
  visible.value = !visible.value
}

function close() {
  if (!visible.value) return
  visible.value = false
}

function onDocPointerDown(e: PointerEvent) {
  if (!props.closeOnClickOutside) return
  const el = root.value
  if (el && e.target instanceof Node && el.contains(e.target)) return
  close()
}

function onPanelClick() {
  if (props.closeOnClickContent) close()
}

watch(
  () => visible.value,
  (v) => {
    if (typeof document === 'undefined') return
    if (v) document.addEventListener('pointerdown', onDocPointerDown, true)
    else document.removeEventListener('pointerdown', onDocPointerDown, true)
  },
)

onBeforeUnmount(() => {
  if (typeof document !== 'undefined') {
    document.removeEventListener('pointerdown', onDocPointerDown, true)
  }
})

const panelStyle = computed(() => {
  const s: Record<string, string> = {
    zIndex: String(props.zIndex),
  }
  const gap = toCssSize(props.offset)
  if (gap) s['--jm-popover-offset'] = gap
  const max = toCssSize(props.maxWidth)
  if (max) s.maxWidth = max
  /* 视口回移量：渲染后测量面板，越界部分用 margin 拉回来 */
  s['--jm-popover-shift-x'] = `${shiftX.value}px`
  s['--jm-popover-shift-y'] = `${shiftY.value}px`
  /* 箭头位置（相对面板的 px 坐标）：回移后跟随触发器 */
  if (arrowX.value !== null) s['--jm-popover-arrow-cx'] = `${arrowX.value}px`
  if (arrowY.value !== null) s['--jm-popover-arrow-cy'] = `${arrowY.value}px`
  return s
})

/* ---------------- 视口边界自适应 ---------------- */
/* 面板按触发器定位后可能伸出屏幕（居中 + 长文案时最常见）。
   渲染完成后量一次实际位置，把超出部分用 margin 平移回来，
   文案太长时先被 maxWidth 约束换行，再配合平移保证完整可见。 */
const panelRef = ref<HTMLElement | null>(null)
const shiftX = ref(0)
const shiftY = ref(0)
/* 箭头中心相对面板的 px 坐标（null = 用 CSS 默认定位） */
const arrowX = ref<number | null>(null)
const arrowY = ref<number | null>(null)

/* 箭头跟随触发器：面板被回移后，居中/贴边的默认箭头会偏离触发器，
   按触发器中心重新定位（限制在面板安全区内，避免顶到圆角外） */
function syncArrow(r: DOMRect, dx: number, dy: number) {
  const host = root.value
  if (!props.arrow || !host) return
  const tr = host.getBoundingClientRect()
  if (props.placement === 'top' || props.placement === 'bottom') {
    const cx = tr.left + tr.width / 2 - (r.left + dx)
    const min = Math.min(12, r.width / 2)
    const max = Math.max(r.width - 12, r.width / 2)
    arrowX.value = Math.round(Math.min(max, Math.max(min, cx)))
    arrowY.value = null
  } else {
    const cy = tr.top + tr.height / 2 - (r.top + dy)
    const min = Math.min(12, r.height / 2)
    const max = Math.max(r.height - 12, r.height / 2)
    arrowY.value = Math.round(Math.min(max, Math.max(min, cy)))
    arrowX.value = null
  }
}

function clampToViewport() {
  const el = panelRef.value
  const host = root.value
  if (!el || !host || typeof document === 'undefined') return
  if (!el.offsetWidth && !el.offsetHeight) return
  /* 用 getBoundingClientRect 拿真实视觉位置（含 translateX(-50%) 等定位 transform），
     但进场动画的 scale 会污染 rect——临时禁用动画测完再恢复 */
  const prevAnim = el.style.animation
  el.style.animation = 'none'
  const r = el.getBoundingClientRect()
  el.style.animation = prevAnim
  const left = r.left
  const top = r.top
  const right = r.right
  const bottom = r.bottom
  /* 可用区域 = 视口 ∩ 最近的滚动/裁剪容器（手机模拟框、弹层内部等场景），
     没有裁剪容器时就是视口本身 */
  const vw = document.documentElement.clientWidth
  const vh = document.documentElement.clientHeight
  const pad = 8
  let boxL = pad
  let boxT = pad
  let boxR = vw - pad
  let boxB = vh - pad
  let node: HTMLElement | null = host.parentElement
  while (node && node !== document.body) {
    const st = getComputedStyle(node)
    const clipped = /(auto|hidden|clip|scroll)/.test(st.overflowX + st.overflowY)
    if (clipped) {
      const cr = node.getBoundingClientRect()
      if (cr.width > 0 && cr.height > 0) {
        boxL = Math.max(boxL, cr.left)
        boxT = Math.max(boxT, cr.top)
        boxR = Math.min(boxR, cr.right)
        boxB = Math.min(boxB, cr.bottom)
      }
    }
    node = node.parentElement
  }
  if (boxR - boxL < 40 || boxB - boxT < 40) return /* 裁剪容器过小，回移没有意义 */
  /* 增量累加而不是绝对覆盖：测量值已包含之前应用的 margin，
     直接赋绝对值会在复测时把上一次的偏移抵消掉 */
  const prevX = shiftX.value
  const prevY = shiftY.value
  shiftX.value += Math.round(left < boxL ? boxL - left : right > boxR ? boxR - right : 0)
  shiftY.value += Math.round(top < boxT ? boxT - top : bottom > boxB ? boxB - bottom : 0)
  syncArrow(r, shiftX.value - prevX, shiftY.value - prevY)
}

watch(
  () => visible.value,
  (v) => {
    if (typeof document === 'undefined') return
    if (v) {
      /* 先归零再测，避免上一次的偏移量污染这次的测量结果 */
      shiftX.value = 0
      shiftY.value = 0
      nextTick(() => {
        requestAnimationFrame(clampToViewport)
        /* 字体异步加载会改变面板宽度（translateX(-50%) 随之漂移），
           动画结束后再复测一次；公式是绝对修正，重复执行幂等 */
        setTimeout(clampToViewport, 250)
      })
    } else {
      shiftX.value = 0
      shiftY.value = 0
      arrowX.value = null
      arrowY.value = null
    }
  },
)
</script>

<template>
  <span
    ref="root"
    class="jm-popover"
    :class="[`is-${placement}`, `is-align-${align}`, { 'is-open': visible }]"
  >
    <span class="jm-popover__reference" @click="toggle">
      <slot name="reference" />
    </span>

    <Transition name="jm-popover-zoom">
      <div
        v-if="visible"
        ref="panelRef"
        class="jm-popover__panel"
        :class="`is-${theme}`"
        :style="panelStyle"
        role="tooltip"
      >
        <span v-if="arrow" class="jm-popover__arrow" aria-hidden="true" />
        <div class="jm-popover__inner" @click="onPanelClick">
          <slot>{{ content }}</slot>
        </div>
      </div>
    </Transition>
  </span>
</template>

<style>
.jm-popover {
  --jm-popover-offset: 8px;
  position: relative;
  display: inline-flex;
  vertical-align: middle;
  max-width: 100%;
  font-family: var(--jm-font-family);
}

.jm-popover__reference {
  display: inline-flex;
  max-width: 100%;
}

.jm-popover__panel {
  position: absolute;
  z-index: 1200;
  box-sizing: border-box;
  /* 绝对定位的面板默认 shrink-to-fit，可用宽度会被包含块掐得很窄，
     长文案会被挤成一列竖排字；显式给 max-content 才按内容自然排 */
  width: max-content;
  /* 没传 maxWidth 时的兜底：太长的文案仍然折行，不撑出屏幕 */
  max-width: min(86vw, 320px);
  padding: 10px 14px;
  border-radius: var(--jm-radius-md);
  font-size: var(--jm-font-size-sm);
  line-height: 1.5;
  word-break: break-word;
  /* 视口回移：渲染后测量越界量写入，margin 不与定位 transform 冲突 */
  margin-left: var(--jm-popover-shift-x, 0px);
  margin-top: var(--jm-popover-shift-y, 0px);
  animation: none;
}

.jm-popover__panel.is-dark {
  background: rgba(16, 21, 26, 0.92);
  color: #fff;
  box-shadow: var(--jm-shadow-2);
}

.jm-popover__panel.is-light {
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  border: 1px solid var(--jm-border-color);
  box-shadow: var(--jm-shadow-2);
}

/* 四个方向：面板贴住触发器，偏移量由 --jm-popover-offset 控制 */
.jm-popover.is-top .jm-popover__panel {
  bottom: calc(100% + var(--jm-popover-offset));
}

.jm-popover.is-bottom .jm-popover__panel {
  top: calc(100% + var(--jm-popover-offset));
}

.jm-popover.is-left .jm-popover__panel {
  right: calc(100% + var(--jm-popover-offset));
  top: 50%;
  transform: translateY(-50%);
}

.jm-popover.is-right .jm-popover__panel {
  left: calc(100% + var(--jm-popover-offset));
  top: 50%;
  transform: translateY(-50%);
}

/* 水平对齐：左右方向忽略 align，上下方向按 start/center/end 贴边 */
.jm-popover.is-align-center .jm-popover__panel {
  left: 50%;
  transform: translateX(-50%);
}

.jm-popover.is-align-start .jm-popover__panel {
  left: 0;
}

.jm-popover.is-align-end .jm-popover__panel {
  right: 0;
}

.jm-popover.is-left .jm-popover__panel,
.jm-popover.is-right .jm-popover__panel {
  left: auto;
  right: auto;
  /* 左右方向垂直居中：重申 transform，防止被 is-align-center 的 translateX 覆盖 */
  transform: translateY(-50%);
}

.jm-popover.is-right .jm-popover__panel {
  left: calc(100% + var(--jm-popover-offset));
}

.jm-popover.is-left .jm-popover__panel {
  right: calc(100% + var(--jm-popover-offset));
}

.jm-popover__inner {
  position: relative;
}

/* 箭头：一个小方块旋转 45°，只露一个尖角朝向触发器 */
.jm-popover__arrow {
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
  border: 0;
  border-radius: 1px;
  pointer-events: none;
}

.jm-popover.is-top .jm-popover__arrow {
  bottom: -3.5px;
  transform: rotate(45deg);
}

.jm-popover.is-bottom .jm-popover__arrow {
  top: -3.5px;
  transform: rotate(45deg);
}

/* 上下方向：箭头水平位置由面板注入的 --jm-popover-arrow-cx 控制
   （打开后 JS 按触发器中心计算，回移时跟随；未注入时居中兜底） */
.jm-popover.is-top .jm-popover__arrow,
.jm-popover.is-bottom .jm-popover__arrow {
  left: var(--jm-popover-arrow-cx, 50%);
  right: auto;
  margin-left: -4px;
}

/* 左右方向：箭头垂直位置由 --jm-popover-arrow-cy 控制 */
.jm-popover.is-left .jm-popover__arrow {
  right: -3.5px;
  top: var(--jm-popover-arrow-cy, 50%);
  transform: translateY(-50%) rotate(45deg);
}

.jm-popover.is-right .jm-popover__arrow {
  left: -3.5px;
  top: var(--jm-popover-arrow-cy, 50%);
  transform: translateY(-50%) rotate(45deg);
}

.jm-popover.is-left .jm-popover__arrow,
.jm-popover.is-right .jm-popover__arrow {
  left: auto;
  right: auto;
  margin-left: 0;
}

.jm-popover.is-right .jm-popover__arrow {
  left: -3.5px;
}

.jm-popover.is-left .jm-popover__arrow {
  right: -3.5px;
}

/* 进出场：从贴边的那一角展开，比整体缩放更「长在触发点上」 */
.jm-popover-zoom-enter-active {
  transition:
    opacity var(--jm-duration-2) var(--jm-motion-enter-ease),
    transform var(--jm-duration-3) var(--jm-motion-enter-ease);
  will-change: transform, opacity;
}

.jm-popover-zoom-leave-active {
  transition:
    opacity 130ms var(--jm-motion-exit-ease),
    transform 130ms var(--jm-motion-exit-ease);
}

.jm-popover.is-top .jm-popover-zoom-enter-from,
.jm-popover.is-top .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateY(4px) scale(0.92);
}

.jm-popover.is-bottom .jm-popover-zoom-enter-from,
.jm-popover.is-bottom .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.92);
}

.jm-popover.is-align-center.is-top .jm-popover-zoom-enter-from,
.jm-popover.is-align-center.is-top .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(4px) scale(0.92);
}

.jm-popover.is-align-center.is-bottom .jm-popover-zoom-enter-from,
.jm-popover.is-align-center.is-bottom .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-4px) scale(0.92);
}

.jm-popover.is-left .jm-popover-zoom-enter-from,
.jm-popover.is-left .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(4px) scale(0.92);
}

.jm-popover.is-right .jm-popover-zoom-enter-from,
.jm-popover.is-right .jm-popover-zoom-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(-4px) scale(0.92);
}

[data-motion='off'] .jm-popover-zoom-enter-active,
[data-motion='off'] .jm-popover-zoom-leave-active {
  transition: opacity 120ms linear;
}

[data-motion='off'] .jm-popover-zoom-enter-from,
[data-motion='off'] .jm-popover-zoom-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .jm-popover-zoom-enter-active,
  .jm-popover-zoom-leave-active {
    transition: opacity 120ms linear;
  }

  .jm-popover-zoom-enter-from,
  .jm-popover-zoom-leave-to {
    opacity: 0;
  }
}
</style>
