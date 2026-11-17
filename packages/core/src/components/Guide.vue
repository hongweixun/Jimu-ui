<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'

defineOptions({ name: 'JmGuide' })

export interface GuideStep {
  /** 目标元素：选择器、元素引用或取值函数 */
  element: string | HTMLElement | (() => HTMLElement | null)
  title?: string
  content: string
  /** 气泡相对目标的位置；center 表示不指向目标，直接居中弹窗 */
  placement?: 'top' | 'bottom' | 'left' | 'right' | 'center'
  /** popover 气泡 / dialog 居中弹窗 */
  mode?: 'popover' | 'dialog'
  /** 高亮区域向四周外扩的像素（默认 0） */
  highlightPadding?: number
  /** 自定义按钮文案（默认 跳过 / 上一步 / 下一步·完成） */
  skipText?: string
  prevText?: string
  nextText?: string
}

const props = withDefaults(
  defineProps<{
    steps: GuideStep[]
    /** 当前步骤索引；-1 或超出范围表示关闭 */
    current: number
    zIndex?: number
    /** 是否显示遮罩挖孔 */
    mask?: boolean
  }>(),
  {
    zIndex: 2100,
    mask: true,
  },
)

const emit = defineEmits<{
  'update:current': [index: number]
  change: [index: number]
  skip: []
  finish: []
}>()

const targetRect = ref<{ left: number; top: number; right: number; bottom: number } | null>(null)
const bubbleStyle = ref<Record<string, string>>({})

const step = computed(() => (props.current >= 0 && props.current < props.steps.length ? props.steps[props.current] : null))
const open = computed(() => !!step.value)

const padding = computed(() => step.value?.highlightPadding ?? 0)

function resolveElement(el: GuideStep['element']): HTMLElement | null {
  if (!el) return null
  if (typeof el === 'string') return document.querySelector<HTMLElement>(el)
  if (typeof el === 'function') return el()
  return el
}

function measure() {
  const s = step.value
  /* dialog 模式不指向具体元素：不测量、不挖孔，整屏遮罩 */
  if (!s || s.mode === 'dialog' || typeof document === 'undefined') {
    targetRect.value = null
    return
  }
  // 先把目标滚到可见
  const el = resolveElement(s.element)
  if (!el) {
    targetRect.value = null
    return
  }
  el.scrollIntoView({ block: 'center', behavior: 'smooth' })
  requestAnimationFrame(() => {
    const r = el.getBoundingClientRect()
    const p = padding.value
    targetRect.value = {
      left: Math.max(0, r.left - p),
      top: Math.max(0, r.top - p),
      right: Math.min(document.documentElement.clientWidth, r.right + p),
      bottom: Math.min(document.documentElement.clientHeight, r.bottom + p),
    }
    positionBubble()
  })
}

function positionBubble() {
  const s = step.value
  const r = targetRect.value
  if (!s || !r || typeof document === 'undefined') return
  const placement = s.placement ?? 'bottom'
  if (s.mode === 'dialog' || placement === 'center') {
    bubbleStyle.value = { position: 'fixed', left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }
    return
  }
  const vw = document.documentElement.clientWidth
  const vh = document.documentElement.clientHeight
  const pad = 12
  /* 气泡宽度先给一个估值，定位后按实际尺寸再校正一次 */
  const w = Math.min(bubbleEl.value?.offsetWidth || 260, vw - pad * 2)
  const h = bubbleEl.value?.offsetHeight || 120
  const style: Record<string, string> = { position: 'fixed', maxWidth: `${vw - pad * 2}px` }
  if (placement === 'top' || placement === 'bottom') {
    let left = (r.left + r.right) / 2 - w / 2
    left = Math.min(Math.max(pad, left), vw - pad - w)
    style.left = `${Math.round(left)}px`
    if (placement === 'top') style.top = `${Math.round(Math.max(pad, r.top - h - 10))}px`
    else style.top = `${Math.round(Math.min(vh - pad - h, r.bottom + 10))}px`
  } else {
    const top = Math.min(Math.max(pad, (r.top + r.bottom) / 2 - h / 2), vh - pad - h)
    style.top = `${Math.round(top)}px`
    if (placement === 'left') {
      const left = r.left - w - 10
      style.left = `${Math.round(Math.max(pad, left))}px`
    } else {
      const left = r.right + 10
      style.left = `${Math.round(Math.min(vw - pad - w, left))}px`
    }
  }
  bubbleStyle.value = style
}

const bubbleEl = ref<HTMLElement | null>(null)

watch(
  () => props.current,
  () => {
    nextTick(measure)
  },
  { immediate: true },
)

watch(bubbleEl, (el) => {
  if (el) positionBubble()
})

/* 滚动 / 尺寸变化时重算 */
function onScroll() {
  measure()
}
function onResize() {
  measure()
}
watch(open, (v) => {
  if (typeof window === 'undefined') return
  if (v) {
    window.addEventListener('scroll', onScroll, true)
    window.addEventListener('resize', onResize)
  } else {
    window.removeEventListener('scroll', onScroll, true)
    window.removeEventListener('resize', onResize)
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', onScroll, true)
    window.removeEventListener('resize', onResize)
  }
})

function goTo(index: number) {
  const clamped = Math.min(Math.max(index, -1), props.steps.length - 1)
  emit('update:current', clamped)
  emit('change', clamped)
  if (clamped === props.steps.length - 1 && index >= props.steps.length) emit('finish')
}

function next() {
  if (props.current >= props.steps.length - 1) {
    emit('update:current', -1)
    emit('finish')
  } else {
    goTo(props.current + 1)
  }
}

function prev() {
  goTo(props.current - 1)
}

function skip() {
  emit('update:current', -1)
  emit('skip')
  emit('finish')
}

const isFirst = computed(() => props.current <= 0)
const isLast = computed(() => props.current >= props.steps.length - 1)
</script>

<template>
  <Teleport to="body">
    <template v-if="open && step">
      <!-- 遮罩挖孔：4 块黑片拼出高亮区 -->
      <div class="jm-guide__mask" :style="{ zIndex }">
        <template v-if="mask && targetRect">
          <div class="jm-guide__shade" :style="{ left: 0, top: 0, right: 0, height: `${Math.max(0, targetRect.top)}px` }" />
          <div
            class="jm-guide__shade"
            :style="{ left: 0, top: `${targetRect.bottom}px`, right: 0, bottom: 0 }"
          />
          <div
            class="jm-guide__shade"
            :style="{ left: 0, top: `${targetRect.top}px`, width: `${Math.max(0, targetRect.left)}px`, height: `${Math.max(0, targetRect.bottom - targetRect.top)}px` }"
          />
          <div
            class="jm-guide__shade"
            :style="{ left: `${targetRect.right}px`, top: `${targetRect.top}px`, right: 0, height: `${Math.max(0, targetRect.bottom - targetRect.top)}px` }"
          />
          <!-- 高亮描边 -->
          <div
            class="jm-guide__highlight"
            :style="{
              left: `${targetRect.left}px`,
              top: `${targetRect.top}px`,
              width: `${targetRect.right - targetRect.left}px`,
              height: `${targetRect.bottom - targetRect.top}px`,
            }"
          />
        </template>
        <template v-else>
          <div class="jm-guide__shade" :style="{ left: 0, top: 0, right: 0, bottom: 0 }" />
        </template>
      </div>

      <!-- 气泡 / 弹窗 -->
      <div
        ref="bubbleEl"
        class="jm-guide__bubble"
        :class="[`is-${step.mode === 'dialog' || step.placement === 'center' ? 'dialog' : 'popover'}`, `is-${step.placement ?? 'bottom'}`]"
        :style="{ zIndex: zIndex + 1, ...bubbleStyle }"
        role="dialog"
        :aria-label="step.title || '引导'"
      >
        <span
          v-if="step.mode !== 'dialog' && step.placement !== 'center'"
          class="jm-guide__arrow"
          aria-hidden="true"
        />
        <div class="jm-guide__body">
          <div v-if="step.title" class="jm-guide__title">{{ step.title }}</div>
          <div class="jm-guide__content">{{ step.content }}</div>
        </div>
        <div class="jm-guide__footer">
          <span class="jm-guide__count">{{ current + 1 }}/{{ steps.length }}</span>
          <div class="jm-guide__actions">
            <button type="button" class="jm-guide__btn" @click="skip">{{ step.skipText || '跳过' }}</button>
            <button v-if="!isFirst" type="button" class="jm-guide__btn" @click="prev">{{ step.prevText || '上一步' }}</button>
            <button type="button" class="jm-guide__btn is-primary" @click="next">
              {{ isLast ? (step.nextText || '完成') : step.nextText || '下一步' }}
            </button>
          </div>
        </div>
      </div>
    </template>
  </Teleport>
</template>

<style>
.jm-guide__mask {
  position: fixed;
  inset: 0;
}

.jm-guide__shade {
  position: absolute;
  background: rgba(0, 0, 0, 0.55);
}

.jm-guide__highlight {
  position: absolute;
  box-sizing: border-box;
  border: 2px solid var(--jm-color-primary);
  border-radius: 6px;
  box-shadow: 0 0 0 4px rgba(0, 160, 233, 0.25);
  pointer-events: none;
}

.jm-guide__bubble {
  box-sizing: border-box;
  width: 260px;
  padding: 14px 14px 12px;
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  font-family: var(--jm-font-family);
  box-shadow: var(--jm-elevation-12);
  animation: jm-guide-pop var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

@keyframes jm-guide-pop {
  from {
    opacity: 0;
    transform: translateY(6px) scale(0.96);
  }
}

.jm-guide__bubble.is-dialog {
  transform: translate(-50%, -50%);
}

.jm-guide__bubble.is-dialog[style*='translate(-50%, -50%)'] {
  animation: jm-guide-dialog-pop var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

@keyframes jm-guide-dialog-pop {
  from {
    opacity: 0;
  }
}

.jm-guide__arrow {
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--jm-bg-elevated);
  transform: rotate(45deg);
}

.jm-guide__bubble.is-top .jm-guide__arrow {
  left: 50%;
  bottom: -5px;
  margin-left: -5px;
}

.jm-guide__bubble.is-bottom .jm-guide__arrow {
  left: 50%;
  top: -5px;
  margin-left: -5px;
}

.jm-guide__bubble.is-left .jm-guide__arrow {
  top: 50%;
  right: -5px;
  margin-top: -5px;
}

.jm-guide__bubble.is-right .jm-guide__arrow {
  top: 50%;
  left: -5px;
  margin-top: -5px;
}

.jm-guide__title {
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.4;
}

.jm-guide__content {
  margin-top: 4px;
  font-size: var(--jm-font-size-sm);
  line-height: 1.5;
  color: var(--jm-text-color-2);
  word-break: break-word;
}

.jm-guide__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.jm-guide__count {
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
  font-variant-numeric: tabular-nums;
}

.jm-guide__actions {
  display: flex;
  gap: 4px;
}

.jm-guide__btn {
  padding: 5px 10px;
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: none;
  color: var(--jm-text-color-2);
  font-family: inherit;
  font-size: var(--jm-font-size-sm);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-guide__btn.is-primary {
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
  font-weight: var(--jm-font-weight-medium);
}

.jm-guide__btn.is-primary:active {
  opacity: 0.85;
}

[data-motion='off'] .jm-guide__bubble {
  animation: none;
}
</style>
