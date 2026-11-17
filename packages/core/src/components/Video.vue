<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmVideo' })

const props = withDefaults(
  defineProps<{
    /** 视频地址，也可用默认插槽放 <source> */
    src?: string
    /** 封面图 */
    poster?: string
    /** 宽高比，数字按 px 高度、字符串原样（'16 / 9'、'4 / 3' 都可以） */
    aspectRatio?: number | string
    /** 进入视口自动播放（浏览器要求自动播放必须 muted，组件会自动带上） */
    playInView?: boolean
    /** 离开视口自动暂停；playInView 打开时默认跟随开启 */
    pauseOffView?: boolean
    /** 页面切到后台时暂停 */
    pauseOnHidden?: boolean
    /** 显示原生控制条；playInView 静音轮播场景常关掉 */
    controls?: boolean
    loop?: boolean
    /** 静音；playInView 自动播放时强制为 true（浏览器策略） */
    muted?: boolean
    objectFit?: 'cover' | 'contain' | 'fill'
    /** 预加载策略；懒加载默认 none，进视口才真正开始拉数据 */
    preload?: 'none' | 'metadata' | 'auto'
    /** 加载成功前显示的骨架背景色 */
    background?: string
    radius?: number | string
    playbackRate?: number
    disabled?: boolean
  }>(),
  {
    aspectRatio: '16 / 9',
    playInView: false,
    pauseOffView: undefined,
    pauseOnHidden: true,
    controls: true,
    loop: false,
    muted: false,
    objectFit: 'contain',
    preload: 'none',
    background: '#000',
    radius: 0,
    playbackRate: 1,
  },
)

const emit = defineEmits<{
  play: []
  pause: []
  ended: []
  /** 节流到 500ms 一次的进度回调，别拿它做逐帧驱动 */
  timeupdate: [currentTime: number, duration: number]
  loadedmetadata: [duration: number]
  error: [event: Event]
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
const rootRef = ref<HTMLElement | null>(null)
const inView = ref(false)
const loaded = ref(false)

const pauseOffView = computed(() => props.pauseOffView ?? props.playInView)
const effectiveMuted = computed(() => props.muted || props.playInView)

const rootStyle = computed(() => {
  const s: Record<string, string> = {}
  /* 数字宽高比（1.777）不能带 px，字符串（'16 / 9'）原样给 aspect-ratio */
  s['--jm-video-ratio'] =
    typeof props.aspectRatio === 'number' ? String(props.aspectRatio) : props.aspectRatio || '16 / 9'
  const r = toCssSize(props.radius)
  if (r) s['--jm-video-radius'] = r
  if (props.background) s['--jm-video-bg'] = props.background
  s['--jm-video-fit'] = props.objectFit
  return s
})

/* ---------------- 播放控制 ---------------- */

let userPaused = false

function safePlay() {
  const el = videoRef.value
  if (!el || props.disabled) return
  if (el.paused) {
    el.play().catch(() => {
      /* 自动播放被浏览器策略拦截时静默失败，等用户手动点 */
    })
  }
}

function pause() {
  videoRef.value?.pause()
}

/** 视口进出：进自动播、出自动停，是页面不卡的关键——
    列表里几十个视频同时播是卡顿的主要来源 */
function applyViewPlayback() {
  if (props.playInView && inView.value && !userPaused) safePlay()
  if (pauseOffView.value && !inView.value) pause()
}

function onVideoPlay() {
  userPaused = false
  emit('play')
}

function onVideoPause() {
  emit('pause')
}

function onVideoEnded() {
  emit('ended')
}

/* timeupdate 每秒能触发几十次，节流到 500ms，回调里做重活也不会拖累渲染 */
let lastEmit = 0
function onTimeUpdate() {
  const el = videoRef.value
  if (!el) return
  const now = Date.now()
  if (now - lastEmit < 500) return
  lastEmit = now
  emit('timeupdate', el.currentTime, el.duration || 0)
}

function onLoadedMetadata() {
  const el = videoRef.value
  if (el) emit('loadedmetadata', el.duration || 0)
}

function onError(e: Event) {
  emit('error', e)
}

/* ---------------- IntersectionObserver ---------------- */

let io: IntersectionObserver | undefined

function setupObserver() {
  if (typeof IntersectionObserver === 'undefined' || !rootRef.value) return
  io?.disconnect()
  io = new IntersectionObserver(
    (entries) => {
      inView.value = entries[0]?.isIntersecting ?? false
      applyViewPlayback()
    },
    { rootMargin: '80px' },
  )
  io.observe(rootRef.value)
}

/* 页面切后台时暂停，回前台仅在视口内且 playInView 时恢复 */
function onVisibilityChange() {
  if (typeof document === 'undefined') return
  if (document.hidden) pause()
  else applyViewPlayback()
}

watch(
  () => [props.playInView, props.pauseOffView],
  () => {
    setupObserver()
    applyViewPlayback()
  },
)

watch(
  () => props.playbackRate,
  (rate) => {
    if (videoRef.value && rate) videoRef.value.playbackRate = rate
  },
)

onMounted(() => {
  setupObserver()
  if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', onVisibilityChange)
  }
  if (videoRef.value && props.playbackRate) videoRef.value.playbackRate = props.playbackRate
})

onBeforeUnmount(() => {
  io?.disconnect()
  io = undefined
  if (typeof document !== 'undefined') {
    document.removeEventListener('visibilitychange', onVisibilityChange)
  }
  pause()
})

function onClickVideo() {
  /* 没有控制条时点击切换播放，轮播海报场景的兜底手势 */
  if (props.controls || props.disabled) return
  const el = videoRef.value
  if (!el) return
  if (el.paused) safePlay()
  else {
    userPaused = true
    pause()
  }
}

defineExpose({
  play: () => {
    userPaused = false
    safePlay()
  },
  pause,
  /** 原生 video 元素，做自定义控制条时直接拿 */
  el: videoRef,
})
</script>

<template>
  <div ref="rootRef" class="jm-video" :style="rootStyle" @click="onClickVideo">
    <video
      v-if="src"
      ref="videoRef"
      class="jm-video__el"
      :src="src"
      :poster="poster"
      :controls="controls && !disabled"
      :loop="loop"
      :muted="effectiveMuted"
      :preload="preload"
      :playsinline="true"
      :webkit-playsinline="true"
      :aria-label="'视频播放器'"
      @play="onVideoPlay"
      @pause="onVideoPause"
      @ended="onVideoEnded"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="
        (e) => {
          loaded = true
          onLoadedMetadata()
        }
      "
      @canplay="loaded = true"
      @error="onError"
    >
      <slot />
    </video>
    <slot v-else name="source" />

    <span v-if="!loaded" class="jm-video__placeholder" aria-hidden="true">
      <span v-if="poster" class="jm-video__poster" :style="{ backgroundImage: `url(${poster})` }" />
    </span>
  </div>
</template>

<style>
.jm-video {
  position: relative;
  width: 100%;
  aspect-ratio: var(--jm-video-ratio, 16 / 9);
  border-radius: var(--jm-video-radius, 0);
  overflow: hidden;
  background: var(--jm-video-bg, #000);
  font-family: var(--jm-font-family);
}

.jm-video__el {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: var(--jm-video-fit, contain);
  background: transparent;
}

.jm-video__placeholder {
  position: absolute;
  inset: 0;
  display: block;
  pointer-events: none;
}

.jm-video__poster {
  position: absolute;
  inset: 0;
  display: block;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
