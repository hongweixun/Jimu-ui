<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import JmIcon from './Icon.vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmBackTop' })

const props = withDefaults(
  defineProps<{
    /** 滚动容器：CSS 选择器或元素本身；不传则监听 window */
    target?: string | HTMLElement | null
    /** 滚动超过这个距离才出现 */
    visibilityHeight?: number
    /** 距侧边 / 底部的距离 */
    offset?: number | string
    bottom?: number | string
    icon?: string
    /** 图标下方的文字 */
    text?: string
    zIndex?: number
    /** 回到顶部的动画时长；0 表示瞬间跳回（关闭动效时自动为 0） */
    duration?: number
    /** 绝对定位在父容器内（演示框、局部滚动区），不贴浏览器视口 */
    inline?: boolean
  }>(),
  {
    visibilityHeight: 200,
    offset: 16,
    bottom: 40,
    icon: 'chevron-up',
    zIndex: 800,
    duration: 300,
  },
)

const emit = defineEmits<{ click: [event: MouseEvent] }>()

const visible = ref(false)
const scroller = ref<HTMLElement | Window | null>(null)

function resolveTarget(): HTMLElement | Window | null {
  if (typeof window === 'undefined') return null
  const t = props.target
  if (!t) return window
  if (typeof t === 'string') return document.querySelector<HTMLElement>(t) ?? window
  return t
}

function getTop(): number {
  const el = scroller.value
  if (!el) return 0
  if (el === window) {
    return window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0
  }
  return (el as HTMLElement).scrollTop
}

function onScroll() {
  visible.value = getTop() > props.visibilityHeight
}

function bind() {
  const el = scroller.value
  if (!el) return
  el.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
}

function unbind() {
  const el = scroller.value
  if (!el) return
  el.removeEventListener('scroll', onScroll)
}

onMounted(async () => {
  // 模板 ref 在父组件挂载阶段才赋值，等一拍再解析，避免首次绑定拿到空
  await nextTick()
  scroller.value = resolveTarget()
  bind()
})

onBeforeUnmount(unbind)

watch(
  () => props.target,
  async () => {
    unbind()
    await nextTick()
    scroller.value = resolveTarget()
    bind()
  },
)

function scrollToTop() {
  const el = scroller.value
  if (!el) return
  const motionOff =
    typeof document !== 'undefined' && document.documentElement.dataset.motion === 'off'
  const behavior: ScrollBehavior = props.duration > 0 && !motionOff ? 'smooth' : 'auto'
  if (el === window) window.scrollTo({ top: 0, behavior })
  else (el as HTMLElement).scrollTo({ top: 0, behavior })
}

function onClick(e: MouseEvent) {
  scrollToTop()
  emit('click', e)
}

const styles = computed(() => {
  const s: Record<string, string> = { zIndex: String(props.zIndex) }
  const o = toCssSize(props.offset)
  if (o) s.right = o
  const b = toCssSize(props.bottom)
  if (b) s.bottom = props.inline ? b : `calc(${b} + env(safe-area-inset-bottom, 0px))`
  return s
})
</script>

<template>
  <Transition name="jm-backtop-fade">
    <button
      v-if="visible"
      type="button"
      class="jm-backtop"
      :class="{ 'is-inline': inline, 'has-text': text }"
      :style="styles"
      aria-label="回到顶部"
      @click="onClick"
    >
      <jm-icon :name="icon" size="20px" :stroke-width="2.2" />
      <span v-if="text" class="jm-backtop__text">{{ text }}</span>
    </button>
  </Transition>
</template>

<style>
.jm-backtop {
  position: fixed;
  right: 16px;
  bottom: calc(40px + env(safe-area-inset-bottom, 0px));
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  width: 40px;
  height: 40px;
  padding: 0;
  box-sizing: border-box;
  border: 0;
  border-radius: 50%;
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color-2);
  box-shadow: var(--jm-shadow-2);
  cursor: pointer;
  font-family: var(--jm-font-family);
  -webkit-tap-highlight-color: transparent;
  transition: transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-backtop.has-text {
  width: auto;
  min-width: 48px;
  height: auto;
  min-height: 48px;
  padding: 6px 10px;
  border-radius: var(--jm-radius-lg);
}

.jm-backtop.is-inline {
  position: absolute;
}

.jm-backtop__text {
  font-size: 10px;
  line-height: 1.2;
  white-space: nowrap;
}

.jm-backtop:active {
  transform: scale(0.92);
}

.jm-backtop:focus-visible {
  outline: none;
  box-shadow:
    var(--jm-shadow-2),
    0 0 0 3px var(--jm-ring-color);
}

.jm-backtop-fade-enter-active,
.jm-backtop-fade-leave-active {
  transition:
    opacity var(--jm-duration-2) var(--jm-motion-enter-ease),
    transform var(--jm-duration-3) var(--jm-motion-spring-ease);
}

.jm-backtop-fade-leave-active {
  transition:
    opacity 150ms var(--jm-motion-exit-ease),
    transform 150ms var(--jm-motion-exit-ease);
}

.jm-backtop-fade-enter-from,
.jm-backtop-fade-leave-to {
  opacity: 0;
  transform: translateY(8px) scale(0.8);
}

[data-motion='off'] .jm-backtop-fade-enter-active,
[data-motion='off'] .jm-backtop-fade-leave-active {
  transition: opacity 120ms linear;
}

[data-motion='off'] .jm-backtop-fade-enter-from,
[data-motion='off'] .jm-backtop-fade-leave-to {
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-backtop-fade-enter-active,
  .jm-backtop-fade-leave-active {
    transition: opacity 120ms linear;
  }

  .jm-backtop-fade-enter-from,
  .jm-backtop-fade-leave-to {
    transform: none;
  }
}
</style>
