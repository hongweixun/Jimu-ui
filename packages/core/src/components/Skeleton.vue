<script setup lang="ts">
import { computed, useSlots } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmSkeleton' })

const props = withDefaults(
  defineProps<{
    /** 为 true 显示骨架，为 false 显示默认插槽内容 */
    loading?: boolean
    avatar?: boolean
    avatarSize?: number | string
    avatarShape?: 'circle' | 'square'
    title?: boolean
    /** 段落行数 */
    rows?: number
    /** 单行宽度；传数组可逐行指定 */
    rowWidth?: number | string | (number | string)[]
    /** 最后一行收窄，视觉上更像文本 */
    lastRowWidth?: number | string
    /** 标题行宽度；数字按 px */
    titleWidth?: number | string
    /** 动效形态：shine 扫光 / breath 透明度呼吸 */
    animation?: 'shine' | 'breath'
    animate?: boolean
    /** 圆角块 */
    round?: boolean
  }>(),
  {
    loading: true,
    avatar: false,
    avatarSize: 48,
    avatarShape: 'circle',
    title: true,
    rows: 3,
    lastRowWidth: '58%',
    animation: 'shine',
    animate: true,
    round: false,
  },
)

const avatarStyle = computed(() => ({
  width: toCssSize(props.avatarSize) ?? '48px',
  height: toCssSize(props.avatarSize) ?? '48px',
}))

const rowList = computed(() => {
  const total = Math.max(0, props.rows)
  const widths: (number | string)[] = []
  for (let i = 0; i < total; i++) {
    if (Array.isArray(props.rowWidth)) {
      widths.push(props.rowWidth[i] ?? props.rowWidth[props.rowWidth.length - 1] ?? '100%')
    } else if (props.rowWidth !== undefined) {
      widths.push(props.rowWidth)
    } else {
      // 最后一行收窄，其余满宽
      widths.push(i === total - 1 && total > 1 ? props.lastRowWidth : '100%')
    }
  }
  return widths.map((w) => ({ width: toCssSize(w) ?? '100%' }))
})

const titleStyle = computed(() =>
  props.titleWidth === undefined ? undefined : { width: toCssSize(props.titleWidth) ?? '40%' },
)

const hasTemplate = computed(() => Boolean(useSlots().template))
const isBreath = computed(() => props.animate && props.animation === 'breath')
const isShine = computed(() => props.animate && props.animation === 'shine')
</script>

<template>
  <div
    v-if="loading"
    class="jm-skeleton"
    :class="{ 'is-shine': isShine, 'is-breath': isBreath, 'is-round': round }"
  >
    <!-- 自定义排版：优先用 #template 里的骨架子组件 -->
    <slot v-if="hasTemplate" name="template" />
    <template v-else>
      <div
        v-if="avatar"
        class="jm-skeleton__avatar jm-skeleton__block"
        :class="`is-${avatarShape}`"
        :style="avatarStyle"
      />
      <div class="jm-skeleton__content">
        <div v-if="title" class="jm-skeleton__title jm-skeleton__block" :style="titleStyle" />
        <div
          v-for="(row, i) in rowList"
          :key="i"
          class="jm-skeleton__row jm-skeleton__block"
          :style="row"
        />
      </div>
    </template>
  </div>
  <slot v-else />
</template>

<style>
.jm-skeleton {
  display: flex;
  align-items: flex-start;
  gap: var(--jm-space-3);
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-skeleton__content {
  flex: 1 1 auto;
  min-width: 0;
  padding-top: 2px;
}

/* #template 自定义排版：段落子组件撑满剩余空间 */
.jm-skeleton__paragraph {
  flex: 1 1 auto;
  min-width: 0;
}

.jm-skeleton__block {
  position: relative;
  overflow: hidden;
  background: var(--jm-bg-input);
  border-radius: var(--jm-radius-sm);
}

.jm-skeleton.is-round .jm-skeleton__block {
  border-radius: var(--jm-radius-round);
}

.jm-skeleton__avatar {
  flex: 0 0 auto;
}

.jm-skeleton__avatar.is-circle {
  border-radius: 50%;
}

.jm-skeleton__avatar.is-square {
  border-radius: var(--jm-radius-md);
}

.jm-skeleton__title {
  width: 40%;
  height: calc(14px * var(--jm-font-scale));
  margin-bottom: var(--jm-space-3);
  border-radius: var(--jm-radius-sm);
}

.jm-skeleton__row {
  height: calc(12px * var(--jm-font-scale));
  margin-bottom: var(--jm-space-2);
}

.jm-skeleton__row:last-child {
  margin-bottom: 0;
}

/* 扫光：装饰性动效，关闭动效时完全停掉 */
.jm-skeleton.is-shine .jm-skeleton__block::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--jm-bg-hover) 45%,
    rgba(255, 255, 255, 0.16) 55%,
    transparent 100%
  );
  animation: jm-skeleton-shine 1.5s var(--jm-motion-transition-ease) infinite;
}

/* 呼吸：整块透明度起伏，低端机比扫光更省 */
.jm-skeleton.is-breath .jm-skeleton__block {
  animation: jm-skeleton-breath 1.8s ease-in-out infinite;
}

@keyframes jm-skeleton-shine {
  to {
    transform: translateX(100%);
  }
}

@keyframes jm-skeleton-breath {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.45;
  }
}

[data-motion='off'] .jm-skeleton.is-shine .jm-skeleton__block::after,
[data-motion='off'] .jm-skeleton.is-breath .jm-skeleton__block {
  animation: none;
  display: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-skeleton.is-shine .jm-skeleton__block::after,
  .jm-skeleton.is-breath .jm-skeleton__block {
    animation: none;
    display: none;
  }
}
</style>
