<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

defineOptions({ name: 'JmList' })

const props = withDefaults(
  defineProps<{
    /** 加载中（v-model:loading） */
    loading?: boolean
    /** 已加载全部 */
    finished?: boolean
    /** 加载失败（v-model:error） */
    error?: boolean
    loadingText?: string
    finishedText?: string
    errorText?: string
    /** 挂载后立即检查一次 */
    immediateCheck?: boolean
    /** 提前触发的距离（px） */
    offset?: number
    /** 触底加载 / 顶部加载 */
    direction?: 'down' | 'up'
    disabled?: boolean
  }>(),
  {
    loading: false,
    finished: false,
    error: false,
    loadingText: '加载中...',
    finishedText: '没有更多了',
    errorText: '加载失败，点击重试',
    immediateCheck: true,
    offset: 120,
    direction: 'down',
    disabled: false,
  },
)

const emit = defineEmits<{
  load: []
  'update:loading': [value: boolean]
  'update:error': [value: boolean]
  clickError: []
}>()

const sentinel = ref<HTMLElement | null>(null)

const canLoad = computed(
  () => !props.disabled && !props.loading && !props.finished && !props.error,
)

const showPlaceholder = computed(
  () => props.loading || props.finished || props.error,
)

let observer: IntersectionObserver | null = null

/** 触发一次加载检查：哨兵进入视口（含 offset 提前量）才发 load */
function check() {
  if (!sentinel.value || !canLoad.value) return
  const rect = sentinel.value.getBoundingClientRect()
  const vh = window.innerHeight || document.documentElement.clientHeight
  const near = props.direction === 'down' ? rect.top - props.offset <= vh : rect.bottom + props.offset >= 0
  if (near) emit('load')
}

function setupObserver() {
  if (typeof IntersectionObserver === 'undefined' || !sentinel.value) return
  observer?.disconnect()
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        emit('load')
      }
    },
    { rootMargin: `${props.offset}px 0px` },
  )
  observer.observe(sentinel.value)
}

onMounted(async () => {
  await nextTick()
  setupObserver()
  if (props.immediateCheck) check()
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
})

/* 加载结束（loading 由 true → false）后哨兵可能仍在视口内：
   IO 不会重复回调，需要主动补一次检查，否则列表会"卡住不再加载"。 */
watch(
  () => props.loading,
  async (v, old) => {
    if (old && !v) {
      await nextTick()
      check()
    }
  },
)

watch([() => props.finished, () => props.error], () => {
  if (canLoad.value) void nextTick().then(check)
})

function onErrorClick() {
  if (!props.error) return
  emit('update:error', false)
  emit('clickError')
  void nextTick().then(check)
}

defineExpose({ check })
</script>

<template>
  <div class="jm-list">
    <div v-if="direction === 'up' && showPlaceholder" class="jm-list__placeholder">
      <template v-if="loading">
        <span class="jm-list__spinner" aria-hidden="true" />
        <span>{{ loadingText }}</span>
      </template>
      <span v-else-if="error" class="jm-list__retry" @click="onErrorClick">{{ errorText }}</span>
      <span v-else>{{ finishedText }}</span>
    </div>

    <slot />

    <div ref="sentinel" class="jm-list__sentinel" aria-hidden="true" />

    <div v-if="direction === 'down' && showPlaceholder" class="jm-list__placeholder">
      <template v-if="loading">
        <span class="jm-list__spinner" aria-hidden="true" />
        <span>{{ loadingText }}</span>
      </template>
      <span v-else-if="error" class="jm-list__retry" @click="onErrorClick">{{ errorText }}</span>
      <span v-else>{{ finishedText }}</span>
    </div>
  </div>
</template>

<style>
.jm-list {
  font-family: var(--jm-font-family);
}

.jm-list__sentinel {
  width: 100%;
  height: 1px;
}

.jm-list__placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: var(--jm-space-4) 0;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  text-align: center;
}

.jm-list__retry {
  color: var(--jm-color-primary);
  cursor: pointer;
}

.jm-list__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--jm-border-color-2);
  border-top-color: var(--jm-color-primary);
  border-radius: 50%;
  animation: jm-list-spin 800ms linear infinite;
}

@keyframes jm-list-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .jm-list__spinner {
    animation-duration: 2400ms;
  }
}
</style>
