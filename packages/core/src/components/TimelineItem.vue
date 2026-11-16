<script setup lang="ts">
import { computed, inject } from 'vue'
import { TIMELINE_KEY, type TimelineType } from './timeline-context'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmTimelineItem' })

const props = withDefaults(
  defineProps<{
    /** 左侧时间文字 */
    time?: string
    title?: string
    /** 正文内容（也可用默认插槽） */
    content?: string
    /** 语义色，决定圆点颜色 */
    type?: TimelineType
    /** 自定义圆点颜色（优先于 type） */
    color?: string
    /** 空心圆点 */
    hollow?: boolean
    /** 圆点内图标，传入后圆点自动放大到 20px */
    icon?: string
    /** 高亮当前节点 */
    active?: boolean
    /** 不显示该节点向下的连线 */
    hideLine?: boolean
    /** 单个节点的圆点直径（px） */
    dotSize?: number
  }>(),
  { type: 'default', hollow: false, active: false, hideLine: false },
)

const ctx = inject(TIMELINE_KEY, null)

const classes = computed(() => [
  `jm-timeline-item--${props.type}`,
  {
    'has-time': Boolean(props.time),
    'has-icon': Boolean(props.icon),
    'is-active': props.active,
    'is-hollow': props.hollow,
    'is-dashed': ctx?.lineStyle === 'dashed',
  },
])

const dotStyle = computed<Record<string, string>>(() => {
  const s: Record<string, string> = {}
  if (props.color) s['--jm-timeline-dot-color'] = props.color
  if (props.dotSize) s['--jm-timeline-dot-size'] = `${props.dotSize}px`
  return s
})
</script>

<template>
  <div class="jm-timeline-item" :class="classes" :style="dotStyle">
    <div v-if="time || $slots.time" class="jm-timeline-item__time">
      <slot name="time">{{ time }}</slot>
    </div>

    <div class="jm-timeline-item__rail">
      <span class="jm-timeline-item__dot" :class="{ 'is-custom': $slots.dot }" aria-hidden="true">
        <slot name="dot">
          <jm-icon v-if="icon" :name="icon" :size="13" :stroke-width="2.6" />
        </slot>
      </span>
      <span v-if="!hideLine" class="jm-timeline-item__line" aria-hidden="true" />
    </div>

    <div class="jm-timeline-item__body">
      <div v-if="title || $slots.title" class="jm-timeline-item__title">
        <slot name="title">{{ title }}</slot>
      </div>
      <div v-if="content || $slots.default" class="jm-timeline-item__content">
        <slot>{{ content }}</slot>
      </div>
    </div>
  </div>
</template>

<style>
.jm-timeline-item {
  position: relative;
  display: grid;
  grid-template-columns: 20px minmax(0, 1fr);
  column-gap: 12px;
  padding-bottom: var(--jm-timeline-gap, 18px);
}

.jm-timeline-item.has-time {
  grid-template-columns: var(--jm-timeline-time-width, 60px) 20px minmax(0, 1fr);
  column-gap: 10px;
}

.jm-timeline-item:last-child {
  padding-bottom: 0;
}

.jm-timeline-item:last-child .jm-timeline-item__line {
  display: none;
}

.jm-timeline-item__time {
  padding-top: 1px;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-xs);
  line-height: var(--jm-line-height);
  text-align: right;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.jm-timeline-item__rail {
  position: relative;
  display: flex;
  justify-content: center;
  align-self: stretch;
  padding-top: 5px;
}

.jm-timeline-item__dot {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  width: var(--jm-timeline-dot-size, 10px);
  height: var(--jm-timeline-dot-size, 10px);
  border-radius: 50%;
  background: var(--jm-timeline-dot-color, var(--jm-text-color-4));
  color: #fff;
  flex: none;
  transition:
    box-shadow var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-timeline-item.has-icon {
  --jm-timeline-dot-size: 20px;
}

/* 自定义圆点（头像 / 图片）：不限制尺寸、不画底色 */
.jm-timeline-item__dot.is-custom {
  width: auto;
  height: auto;
  background: none;
}

.jm-timeline-item__line {
  position: absolute;
  top: calc(var(--jm-timeline-dot-size, 10px) + 8px);
  /* 多伸 6px 顶到下一行圆点的上内边距，视觉上连线不断口 */
  bottom: calc(-1 * (var(--jm-timeline-gap, 18px) + 6px));
  left: 50%;
  width: 2px;
  margin-left: -1px;
  border-radius: 1px;
  background: var(--jm-timeline-line);
}

.jm-timeline-item.is-dashed .jm-timeline-item__line {
  background: none;
  background-image: linear-gradient(
    to bottom,
    var(--jm-timeline-line) 0,
    var(--jm-timeline-line) 4px,
    transparent 4px,
    transparent 8px
  );
  background-size: 2px 8px;
}

.jm-timeline-item.is-hollow .jm-timeline-item__dot {
  background: var(--jm-bg-elevated);
  border: 2px solid var(--jm-timeline-dot-color, var(--jm-text-color-4));
}

.jm-timeline-item__body {
  min-width: 0;
}

.jm-timeline-item__title {
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.45;
  word-break: break-word;
}

.jm-timeline-item__content {
  margin-top: 3px;
  color: var(--jm-text-color-2);
  font-size: var(--jm-font-size-sm);
  line-height: var(--jm-line-height);
  word-break: break-word;
}

/* 语义色：只改圆点与连线起点颜色，文字仍按内容层级 */
.jm-timeline-item--primary {
  --jm-timeline-dot-color: var(--jm-color-primary);
}

.jm-timeline-item--success {
  --jm-timeline-dot-color: var(--jm-color-success);
}

.jm-timeline-item--warning {
  --jm-timeline-dot-color: var(--jm-color-warning);
}

.jm-timeline-item--danger {
  --jm-timeline-dot-color: var(--jm-color-danger);
}

.jm-timeline-item--info {
  --jm-timeline-dot-color: var(--jm-color-info);
}

.jm-timeline-item.is-active .jm-timeline-item__dot {
  box-shadow: 0 0 0 4px var(--jm-color-primary-light);
}

.jm-timeline-item.is-active .jm-timeline-item__title {
  color: var(--jm-color-primary);
}
</style>
