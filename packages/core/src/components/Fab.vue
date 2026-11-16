<script setup lang="ts">
import { computed } from 'vue'
import JmIcon from './Icon.vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmFab' })

const props = withDefaults(
  defineProps<{
    /** 图标名，见 jm-icon */
    icon?: string
    /** 图标右侧的文字，传了就变成胶囊按钮 */
    text?: string
    /** 贴在屏幕哪一侧 */
    position?: 'right' | 'left'
    /** 距底部的距离；默认避开底部安全区 */
    bottom?: number | string
    /** 距侧边的距离 */
    offset?: number | string
    /** 直径（无文字时） */
    size?: number | string
    /** 底色，默认主色 */
    color?: string
    /** 图标与文字的颜色 */
    textColor?: string
    /** 受控激活态：可用来做「展开菜单」的喇叭 */
    active?: boolean
    activeIcon?: string
    zIndex?: number
    /** false 时跟着父容器定位（演示框里用） */
    teleport?: boolean
    /** 绝对定位在父容器内，不贴浏览器视口 */
    inline?: boolean
  }>(),
  {
    icon: 'plus',
    position: 'right',
    bottom: 24,
    offset: 16,
    size: 48,
    active: undefined,
    activeIcon: 'close',
    zIndex: 900,
    teleport: true,
    inline: false,
  },
)

const emit = defineEmits<{
  click: [event: MouseEvent]
  'update:active': [value: boolean]
}>()

const isActive = computed(() => props.active === true)

const currentIcon = computed(() => (isActive.value ? props.activeIcon : props.icon))

const styles = computed(() => {
  const s: Record<string, string> = { zIndex: String(props.zIndex) }
  const b = toCssSize(props.bottom)
  if (b) s.bottom = `calc(${b} + env(safe-area-inset-bottom, 0px))`
  const o = toCssSize(props.offset)
  if (o) s[props.position] = o
  const size = toCssSize(props.size)
  if (size) s['--jm-fab-size'] = size
  if (props.color) s['--jm-fab-bg'] = props.color
  if (props.textColor) s['--jm-fab-color'] = props.textColor
  return s
})

function onClick(e: MouseEvent) {
  emit('click', e)
  if (props.active !== undefined) emit('update:active', !props.active)
}
</script>

<template>
  <Teleport to="body" :disabled="!teleport || inline">
    <button
      type="button"
      class="jm-fab"
      :class="[`is-${position}`, { 'is-text': text, 'is-active': isActive, 'is-inline': inline }]"
      :style="styles"
      @click="onClick"
    >
      <jm-icon :name="currentIcon" :size="text ? '18px' : '22px'" :stroke-width="2.1" />
      <span v-if="text" class="jm-fab__text">{{ text }}</span>
    </button>
  </Teleport>
</template>

<style>
.jm-fab {
  --jm-fab-size: 48px;
  --jm-fab-bg: var(--jm-color-primary);
  --jm-fab-color: #fff;
  position: fixed;
  right: 16px;
  bottom: calc(24px + env(safe-area-inset-bottom, 0px));
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-width: var(--jm-fab-size);
  height: var(--jm-fab-size);
  padding: 0;
  box-sizing: border-box;
  border: 0;
  border-radius: calc(var(--jm-fab-size) / 2);
  background: var(--jm-fab-bg);
  color: var(--jm-fab-color);
  box-shadow: var(--jm-shadow-3);
  cursor: pointer;
  font-family: var(--jm-font-family);
  -webkit-tap-highlight-color: transparent;
  transition:
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    box-shadow var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
  will-change: transform;
}

.jm-fab.is-text {
  padding: 0 18px;
}

.jm-fab.is-left {
  right: auto;
  left: 16px;
}

/* 演示框 / 局部容器内：绝对定位在最近的可定位祖先里 */
.jm-fab.is-inline {
  position: absolute;
}

.jm-fab__text {
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  white-space: nowrap;
}

/* 按下缩一点，松手回弹；不用 :active 缩放导致抖动 */
.jm-fab:active {
  transform: scale(0.94);
  box-shadow: var(--jm-shadow-2);
}

.jm-fab:focus-visible {
  outline: none;
  box-shadow:
    var(--jm-shadow-3),
    0 0 0 3px var(--jm-ring-color);
}

/* 激活态：底色压深一点点，配合 active-icon 切换成叉 */
.jm-fab.is-active {
  filter: brightness(1.05);
}

[data-motion='off'] .jm-fab {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-fab,
  .jm-fab.is-active :deep(svg) {
    transition: none;
  }
}
</style>
