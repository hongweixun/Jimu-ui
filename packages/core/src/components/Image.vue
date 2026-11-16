<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmImage' })

const props = withDefaults(
  defineProps<{
    src?: string
    alt?: string
    /** 宽度；数字按 px */
    width?: number | string
    /** 高度；数字按 px */
    height?: number | string
    /** 填充方式，同 CSS object-fit */
    fit?: 'fill' | 'contain' | 'cover' | 'none' | 'scale-down'
    /** 圆角；round 为 true 时优先做圆形 */
    radius?: number | string
    /** 圆形（头像场景） */
    round?: boolean
    /** 进入视口再加载 */
    lazy?: boolean
    /** 加载中占位 */
    showLoading?: boolean
    /** 加载失败占位 */
    showError?: boolean
    loadingText?: string
    errorText?: string
    /** 加载完成后淡入 */
    fade?: boolean
    /** 块级占满父宽 */
    block?: boolean
    /** 图片本身可点击（放大预览等由外部处理） */
    clickable?: boolean
  }>(),
  {
    fit: 'cover',
    lazy: false,
    showLoading: true,
    showError: true,
    loadingText: '',
    errorText: '加载失败',
    fade: true,
    block: false,
  },
)

const emit = defineEmits<{
  load: [event: Event]
  error: [event: Event]
  click: [event: MouseEvent]
}>()

type Status = 'loading' | 'loaded' | 'error'

const status = ref<Status>('loading')
const visible = ref(!props.lazy)
const root = ref<HTMLElement | null>(null)

/* 懒加载：只在接近视口时才真正写入 src，省流量 */
let observer: IntersectionObserver | null = null

function observe() {
  if (!props.lazy || visible.value || !root.value || typeof IntersectionObserver === 'undefined') {
    visible.value = true
    return
  }
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        visible.value = true
        disconnect()
      }
    },
    { rootMargin: '50px' },
  )
  observer.observe(root.value)
}

function disconnect() {
  observer?.disconnect()
  observer = null
}

onMounted(observe)
onBeforeUnmount(disconnect)

watch(
  () => props.src,
  () => {
    status.value = 'loading'
    if (props.lazy && !visible.value) observe()
  },
)

const showImg = computed(() => visible.value && !!props.src && status.value !== 'error')

const styles = computed(() => {
  const s: Record<string, string> = {}
  const w = toCssSize(props.width)
  const h = toCssSize(props.height)
  if (w) s.width = w
  if (h) s.height = h
  if (props.round) s['--jm-image-radius'] = '50%'
  else {
    const r = toCssSize(props.radius)
    if (r) s['--jm-image-radius'] = r
  }
  if (props.block && !w) s.width = '100%'
  return s
})

const imgStyle = computed(() => ({ objectFit: props.fit }))

function onLoad(e: Event) {
  status.value = 'loaded'
  emit('load', e)
}

function onError(e: Event) {
  status.value = 'error'
  emit('error', e)
  /* 懒加载场景下有些图片在写入 src 前就判定失败，这里断开观察避免反复触发 */
  disconnect()
}

function onClick(e: MouseEvent) {
  emit('click', e)
}
</script>

<template>
  <div
    ref="root"
    class="jm-image"
    :class="{ 'is-block': block, 'is-clickable': clickable, 'is-round': round }"
    :style="styles"
    @click="onClick"
  >
    <img
      v-if="showImg"
      class="jm-image__img"
      :class="{ 'is-fade': fade, 'is-loaded': status === 'loaded' }"
      :src="src"
      :alt="alt"
      :style="imgStyle"
      draggable="false"
      @load="onLoad"
      @error="onError"
    />

    <div v-if="status === 'loading' && showLoading && showImg" class="jm-image__loading">
      <slot name="loading">
        <span class="jm-image__spinner" aria-hidden="true" />
        <span v-if="loadingText" class="jm-image__tip">{{ loadingText }}</span>
      </slot>
    </div>

    <div v-if="status === 'error' && showError" class="jm-image__error">
      <slot name="error">
        <jm-icon class="jm-image__error-icon" name="image" size="28px" :stroke-width="1.5" />
        <span v-if="errorText" class="jm-image__tip">{{ errorText }}</span>
      </slot>
    </div>
  </div>
</template>

<style>
.jm-image {
  position: relative;
  display: inline-block;
  overflow: hidden;
  max-width: 100%;
  border-radius: var(--jm-image-radius, 0);
  background: var(--jm-bg-input);
  font-family: var(--jm-font-family);
  vertical-align: middle;
  /* 未显式指定宽高时给个兜底比例，避免占位图标把布局撑成一条线 */
  aspect-ratio: var(--jm-image-ratio, auto);
}

.jm-image.is-block {
  display: block;
  width: 100%;
}

.jm-image.is-round {
  border-radius: 50%;
}

.jm-image.is-clickable {
  cursor: zoom-in;
}

.jm-image__img {
  display: block;
  width: 100%;
  height: 100%;
  transition: opacity var(--jm-motion-fade, 200ms) var(--jm-ease-out, ease-out);
}

.jm-image__img.is-fade {
  opacity: 0;
}

.jm-image__img.is-fade.is-loaded {
  opacity: 1;
}

.jm-image__loading,
.jm-image__error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: var(--jm-space-2);
  background: var(--jm-bg-input);
  color: var(--jm-text-color-4);
  font-size: var(--jm-font-size-xs);
  text-align: center;
}

.jm-image__error-icon {
  width: 28px;
  height: 28px;
}

.jm-image__tip {
  line-height: 1.3;
}

/* 加载指示：细环旋转，比其他地方的小一号，避免抢镜 */
.jm-image__spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--jm-border-color-2);
  border-top-color: var(--jm-color-primary);
  border-radius: 50%;
  animation: jm-image-spin 800ms linear infinite;
}

@keyframes jm-image-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .jm-image__spinner {
    animation-duration: 2400ms;
  }
  .jm-image__img {
    transition: none;
  }
}
</style>
