<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

defineOptions({ name: 'JmTextScroll' })

const props = withDefaults(
  defineProps<{
    /** 滚动文本；不传时用默认插槽（插槽内容同样参与溢出测量） */
    text?: string
    /** 滚动速度 px/s（单份内容宽度 / speed = 一轮时长） */
    speed?: number
    /** 无缝衔接处（结尾与开头之间）的留白 px */
    gap?: number
  }>(),
  {
    text: '',
    speed: 40,
    gap: 32,
  },
)

const wrap = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)
/** 内容宽度是否超过容器：超过才滚动，否则静止（SSR 首帧按不滚渲染） */
const overflow = ref(false)
/** 一轮滚动时长（秒），按内容实测宽度 / 速度计算 */
const duration = ref(10)

let ro: ResizeObserver | null = null

function measure() {
  if (!track.value || !wrap.value) return
  const cs = getComputedStyle(track.value)
  const gapPx = parseFloat(cs.paddingRight) || props.gap
  // track 是两份内容拼接（各带 gap），单份宽度 = 总宽/2
  const contentWidth = track.value.scrollWidth / 2
  overflow.value = contentWidth > wrap.value.clientWidth + 1
  if (overflow.value) {
    duration.value = Math.max(3, contentWidth / Math.max(10, props.speed))
  }
}

onMounted(() => {
  measure()
  if (typeof ResizeObserver !== 'undefined') {
    ro = new ResizeObserver(measure)
    if (wrap.value) ro.observe(wrap.value)
    if (track.value) ro.observe(track.value)
  } else if (typeof window !== 'undefined') {
    window.addEventListener('resize', measure)
  }
})

onBeforeUnmount(() => {
  ro?.disconnect()
  if (typeof window !== 'undefined') window.removeEventListener('resize', measure)
})

watch(
  () => props.text,
  () => requestAnimationFrame(measure),
)

defineExpose({ /** 内容或容器尺寸变化后可手动触发一次重测 */
  measure })
</script>

<template>
  <div ref="wrap" class="jm-text-scroll">
    <div
      ref="track"
      class="jm-text-scroll__track"
      :class="{ 'is-scrolling': overflow }"
      :style="{ '--jm-text-scroll-gap': `${gap}px`, animationDuration: `${duration}s` }"
    >
      <span class="jm-text-scroll__content"><slot>{{ text }}</slot></span>
      <span v-if="overflow" class="jm-text-scroll__content" aria-hidden="true">
        <slot>{{ text }}</slot>
      </span>
    </div>
  </div>
</template>

<style>
.jm-text-scroll {
  overflow: hidden;
  min-width: 0;
  max-width: 100%;
  font-family: var(--jm-font-family);
  line-height: inherit;
}

.jm-text-scroll__track {
  display: flex;
  width: max-content;
  will-change: transform;
}

.jm-text-scroll__track.is-scrolling {
  animation: jm-text-scroll linear infinite;
}

/* 桌面端悬停暂停，方便看清/选中内容 */
@media (hover: hover) {
  .jm-text-scroll__track.is-scrolling:hover {
    animation-play-state: paused;
  }
}

.jm-text-scroll__content {
  flex: 0 0 auto;
  padding-right: var(--jm-text-scroll-gap, 32px);
  white-space: nowrap;
}

@keyframes jm-text-scroll {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

/* 动效关闭：退回单行省略（完整内容仍在 DOM / 无障碍树里） */
[data-motion='off'] .jm-text-scroll__track.is-scrolling {
  animation: none;
  width: 100%;
}

[data-motion='off'] .jm-text-scroll__content {
  overflow: hidden;
  text-overflow: ellipsis;
}

[data-motion='off'] .jm-text-scroll__content + .jm-text-scroll__content {
  display: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-text-scroll__track.is-scrolling {
    animation: none;
    width: 100%;
  }

  .jm-text-scroll__content {
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .jm-text-scroll__content + .jm-text-scroll__content {
    display: none;
  }
}
</style>
