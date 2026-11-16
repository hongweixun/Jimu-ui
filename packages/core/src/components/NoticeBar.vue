<script setup lang="ts">
import { computed } from 'vue'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmNoticeBar' })

const props = withDefaults(
  defineProps<{
    text?: string
    /** link 右侧显示箭头且整条可点；closeable 显示关闭按钮 */
    mode?: 'link' | 'closeable' | ''
    /** 左侧喇叭图标 */
    leftIcon?: boolean
    /** 跑马灯；关掉后单行省略或换行 */
    scrollable?: boolean
    /** 允许换行（多行展示），优先级高于 scrollable */
    wrapable?: boolean
    /** 滚动速度，px/s，仅在支持测量的浏览器上作为动画时长参考 */
    speed?: number
    color?: string
    background?: string
    /** 自定义右侧图标 */
    rightIcon?: string
  }>(),
  {
    mode: '',
    leftIcon: true,
    scrollable: true,
    wrapable: false,
    speed: 50,
  },
)

const emit = defineEmits<{ close: []; click: [event: MouseEvent] }>()

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.color) s['--jm-notice-color'] = props.color
  if (props.background) s['--jm-notice-bg'] = props.background
  return s
})

/**
 * 不做文字宽度测量（SSR 安全），用文字长度估算时长：
 * 短词约 6s 走完一轮，长句按比例加长，避免长文本飞速掠过。
 */
const duration = computed(() => {
  const len = (props.text ?? '').length || 10
  const base = Math.max(6, (len * 0.55 * 50) / Math.max(20, props.speed))
  return `${Math.round(base)}s`
})

const scrolling = computed(() => props.scrollable && !props.wrapable)

function onClose() {
  emit('close')
}
</script>

<template>
  <div
    class="jm-noticebar"
    :class="{ 'is-scrolling': scrolling, 'is-wrapable': wrapable, 'is-link': mode === 'link' }"
    :style="styles"
    role="alert"
  >
    <span v-if="leftIcon" class="jm-noticebar__icon" aria-hidden="true">
      <jm-icon name="horn" size="16px" :stroke-width="1.8" />
    </span>

    <div class="jm-noticebar__wrap" @click="emit('click', $event)">
      <div v-if="scrolling" class="jm-noticebar__track" :style="{ animationDuration: duration }">
        <span class="jm-noticebar__text"><slot>{{ text }}</slot></span>
        <span class="jm-noticebar__text" aria-hidden="true"><slot>{{ text }}</slot></span>
      </div>
      <div v-else class="jm-noticebar__static">
        <slot>{{ text }}</slot>
      </div>
    </div>

    <span
      v-if="mode === 'closeable'"
      class="jm-noticebar__close"
      role="button"
      tabindex="0"
      aria-label="关闭"
      @click.stop="onClose"
      @keydown.enter="onClose"
    >
      <jm-icon name="close" size="16px" :stroke-width="2" />
    </span>

    <span v-else-if="mode === 'link'" class="jm-noticebar__arrow" aria-hidden="true">
      <jm-icon name="chevron-right" size="16px" :stroke-width="2" />
    </span>
  </div>
</template>

<style>
.jm-noticebar {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
  /* 防止 max-content 的跑马灯把 flex/grid 祖先的固有宽度撑爆 */
  min-width: 0;
  max-width: 100%;
  min-height: calc(40px * var(--jm-size-scale));
  padding: 9px var(--jm-space-3);
  box-sizing: border-box;
  background: var(--jm-notice-bg, var(--jm-color-primary-light));
  color: var(--jm-notice-color, var(--jm-color-primary-text));
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  line-height: var(--jm-line-height);
}

.jm-noticebar.is-link {
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-noticebar.is-link:active {
  opacity: 0.8;
}

.jm-noticebar__icon {
  display: flex;
  flex: 0 0 auto;
  width: 16px;
  height: 16px;
}

.jm-noticebar__icon svg {
  width: 100%;
  height: 100%;
}

.jm-noticebar__wrap {
  /* flex-basis 用 0 而不是 auto：auto 会把跑马灯 max-content 宽度
     当作固有尺寸向上传播，撑破手机模拟框/页面布局 */
  flex: 1 1 0%;
  min-width: 0;
  overflow: hidden;
}

.jm-noticebar__static {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-noticebar.is-wrapable .jm-noticebar__static {
  white-space: normal;
  word-break: break-word;
}

.jm-noticebar__track {
  display: flex;
  width: max-content;
  animation: jm-noticebar-marquee linear infinite;
  will-change: transform;
}

.jm-noticebar__text {
  flex: 0 0 auto;
  padding-right: 40px;
  white-space: nowrap;
}

@keyframes jm-noticebar-marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

/* 关动效：停跑马灯，退回单行省略（文案完整内容仍可从 DOM / 无障碍树读到） */
[data-motion='off'] .jm-noticebar__track {
  animation: none;
  transform: none;
  width: 100%;
}

[data-motion='off'] .jm-noticebar__text {
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 0;
}

[data-motion='off'] .jm-noticebar__text + .jm-noticebar__text {
  display: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-noticebar__track {
    animation: none;
    transform: none;
    width: 100%;
  }

  .jm-noticebar__text {
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 0;
  }

  .jm-noticebar__text + .jm-noticebar__text {
    display: none;
  }
}

.jm-noticebar__close,
.jm-noticebar__arrow {
  display: flex;
  flex: 0 0 auto;
  width: 16px;
  height: 16px;
  color: currentColor;
  opacity: 0.65;
}

.jm-noticebar__close {
  cursor: pointer;
  padding: 4px;
  margin: -4px;
  box-sizing: content-box;
}

.jm-noticebar__close svg,
.jm-noticebar__arrow svg {
  width: 100%;
  height: 100%;
}
</style>
