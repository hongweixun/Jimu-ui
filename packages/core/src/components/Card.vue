<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'
import { vRipple } from '../utils/ripple'

defineOptions({ name: 'JmCard' })

const props = withDefaults(
  defineProps<{
    title?: string
    /** 标题下面的一行说明 */
    desc?: string
    /** 封面图地址 */
    thumb?: string
    /** 封面在上方（图文卡片）还是左侧（列表卡片） */
    thumbPosition?: 'top' | 'left'
    /** 封面宽高比，top 布局是宽/高，left 布局是宽/高都生效；不传时 top 用 16/9、left 用 1 */
    thumbRatio?: number | string
    thumbFit?: 'cover' | 'contain'
    /** 右上角附加文案，如「3 分钟前」 */
    extra?: string
    /** 价格，数字会格式化成 ¥ 千分位两位小数，字符串原样输出 */
    price?: number | string
    /** 划线原价 */
    originPrice?: number | string
    /** 标题下方的标签 */
    tags?: string[]
    /** 描边 */
    bordered?: boolean
    shadow?: 'always' | 'hover' | 'never'
    round?: boolean | number | string
    clickable?: boolean
    /** 点击水波纹，默认跟随 clickable */
    ripple?: boolean
    /** 封面懒加载 */
    lazy?: boolean
  }>(),
  {
    thumbPosition: 'top',
    thumbFit: 'cover',
    bordered: true,
    shadow: 'never',
    round: true,
    lazy: true,
  },
)

const emit = defineEmits<{ click: [event: MouseEvent] }>()

const hasRipple = computed(() => props.ripple ?? props.clickable)
const rippleBinding = computed(() => ({ disabled: !hasRipple.value }))

const ratio = computed(() => {
  if (props.thumbRatio === undefined || props.thumbRatio === '') {
    return props.thumbPosition === 'left' ? 1 : 16 / 9
  }
  const n = typeof props.thumbRatio === 'string' ? Number(props.thumbRatio) : props.thumbRatio
  if (!Number.isFinite(n) || n <= 0) return props.thumbPosition === 'left' ? 1 : 16 / 9
  return n
})

const classes = computed(() => [
  `jm-card--${props.thumbPosition}`,
  `jm-card--shadow-${props.shadow}`,
  {
    'is-bordered': props.bordered,
    'is-clickable': props.clickable,
    'has-thumb': !!props.thumb,
  },
])

const styles = computed(() => {
  const s: Record<string, string> = {}
  // round 传 true 表示用默认圆角，不能丢给 toCssSize（会得到 "true" 这种非法值）
  if (props.round !== undefined && props.round !== true) {
    const r = props.round === false ? '0px' : toCssSize(props.round)
    if (r) s['--jm-card-radius'] = r
  }
  // 用 padding-top 撑出比例，比 aspect-ratio 更兼容老 WebView
  if (props.thumbPosition === 'top' && props.thumb) s['--jm-card-thumb-ratio'] = `${(1 / ratio.value) * 100}%`
  if (props.thumbPosition === 'left' && props.thumb) s['--jm-card-thumb-ratio'] = `${(1 / ratio.value) * 100}%`
  return s
})

function formatPrice(v: number | string | undefined) {
  if (v === undefined || v === '') return ''
  if (typeof v === 'string') return v
  const [int, dec] = Math.abs(v).toFixed(2).split('.')
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return `¥${v < 0 ? '-' : ''}${grouped}.${dec}`
}

function onClick(e: MouseEvent) {
  if (!props.clickable) return
  emit('click', e)
}

function onKeydown(e: KeyboardEvent) {
  if (!props.clickable) return
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()
    emit('click', e as unknown as MouseEvent)
  }
}
</script>

<template>
  <div
    class="jm-card"
    :class="classes"
    :style="styles"
    v-ripple="rippleBinding"
    :role="clickable ? 'button' : undefined"
    :tabindex="clickable ? 0 : undefined"
    @click="onClick"
    @keydown="onKeydown"
  >
    <div v-if="thumb || $slots.thumb" class="jm-card__thumb">
      <slot name="thumb">
        <img
          class="jm-card__img"
          :src="thumb"
          :loading="lazy ? 'lazy' : 'eager'"
          :style="{ objectFit: thumbFit }"
          alt=""
          draggable="false"
        />
      </slot>
    </div>

    <div class="jm-card__main">
      <div v-if="title || desc || extra || $slots.title || $slots.extra" class="jm-card__header">
        <div class="jm-card__heading">
          <div v-if="title || $slots.title" class="jm-card__title">
            <slot name="title">{{ title }}</slot>
          </div>
          <div v-if="desc" class="jm-card__desc">{{ desc }}</div>
        </div>
        <div v-if="extra || $slots.extra" class="jm-card__extra">
          <slot name="extra">{{ extra }}</slot>
        </div>
      </div>

      <div v-if="tags && tags.length" class="jm-card__tags">
        <span v-for="t in tags" :key="t" class="jm-card__tag">{{ t }}</span>
      </div>

      <div v-if="price !== undefined || originPrice !== undefined" class="jm-card__price">
        <span v-if="price !== undefined" class="jm-card__price-now">{{ formatPrice(price) }}</span>
        <span v-if="originPrice !== undefined" class="jm-card__price-origin">{{ formatPrice(originPrice) }}</span>
      </div>

      <div v-if="$slots.default" class="jm-card__body">
        <slot />
      </div>
    </div>

    <div v-if="$slots.footer" class="jm-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style>
.jm-card {
  --jm-card-radius: var(--jm-radius-lg);
  --jm-card-bg: var(--jm-bg-elevated);
  --jm-card-padding: 14px;
  --jm-card-thumb-w: 96px;
  box-sizing: border-box;
  position: relative;
  display: block;
  overflow: hidden;
  border-radius: var(--jm-card-radius);
  background: var(--jm-card-bg);
  color: var(--jm-text-color);
  font-family: var(--jm-font-family);
  -webkit-tap-highlight-color: transparent;
  transition:
    transform var(--jm-duration-2) var(--jm-motion-enter-ease),
    box-shadow var(--jm-duration-2) var(--jm-motion-enter-ease);
}

.jm-card.is-bordered {
  border: 1px solid var(--jm-border-color);
}

.jm-card--shadow-always {
  border-color: transparent;
  box-shadow: var(--jm-shadow-2);
}

.jm-card--shadow-hover {
  border-color: transparent;
  box-shadow: var(--jm-shadow-1);
}

@media (hover: hover) {
  .jm-card--shadow-hover:hover {
    box-shadow: var(--jm-shadow-3);
  }
}

.jm-card.is-clickable {
  cursor: pointer;
}

.jm-card.is-clickable:active {
  transform: scale(0.988);
}

/* 封面：top 用 padding-top 撑比例，left 用固定宽度 + 自身比例 */
.jm-card__thumb {
  position: relative;
  overflow: hidden;
  background: var(--jm-bg-input, #f2f4f6);
}

.jm-card--top .jm-card__thumb {
  width: 100%;
  padding-top: var(--jm-card-thumb-ratio, 56.25%);
}

.jm-card--top .jm-card__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.jm-card--left {
  display: grid;
  grid-template-columns: var(--jm-card-thumb-w) minmax(0, 1fr);
  align-items: stretch;
  gap: 12px;
  padding: var(--jm-card-padding);
}

.jm-card--left .jm-card__thumb {
  width: var(--jm-card-thumb-w);
  align-self: start;
  border-radius: var(--jm-radius-md);
  padding-top: var(--jm-card-thumb-ratio, 100%);
}

.jm-card--left .jm-card__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* left 布局下 footer 横跨整行 */
.jm-card--left .jm-card__footer {
  grid-column: 1 / -1;
}

.jm-card--left .jm-card__main {
  min-width: 0;
  padding: 0;
}

.jm-card__main {
  box-sizing: border-box;
  padding: var(--jm-card-padding);
  min-width: 0;
}

.jm-card--top.has-thumb .jm-card__main {
  padding-top: 12px;
}

.jm-card__header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.jm-card__heading {
  flex: 1;
  min-width: 0;
}

.jm-card__title {
  font-size: var(--jm-font-size-md);
  font-weight: 600;
  line-height: 1.4;
  color: var(--jm-text-color);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.jm-card__desc {
  margin-top: 4px;
  font-size: var(--jm-font-size-sm);
  line-height: 1.5;
  color: var(--jm-text-color-2);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.jm-card__extra {
  flex: none;
  font-size: var(--jm-font-size-xs);
  line-height: 1.6;
  color: var(--jm-text-color-3, #8a9099);
}

.jm-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.jm-card__tag {
  padding: 2px 6px;
  border-radius: var(--jm-radius-sm);
  background: var(--jm-color-primary-light, rgba(0, 160, 233, 0.1));
  color: var(--jm-color-primary);
  font-size: var(--jm-font-size-xs);
  line-height: 1.4;
}

.jm-card__price {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-top: 8px;
}

.jm-card__price-now {
  font-size: var(--jm-font-size-lg);
  font-weight: 700;
  line-height: 1.3;
  color: var(--jm-card-price-color, var(--jm-color-danger, #f5222d));
}

.jm-card__price-origin {
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3, #8a9099);
  text-decoration: line-through;
}

.jm-card__body {
  margin-top: 8px;
  font-size: var(--jm-font-size-sm);
  line-height: 1.6;
  color: var(--jm-text-color-2);
}

.jm-card__body:first-child {
  margin-top: 0;
}

.jm-card__footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px var(--jm-card-padding);
  border-top: 1px solid var(--jm-border-color);
}

[data-motion='off'] .jm-card,
[data-motion='off'] .jm-card.is-clickable:active {
  transition: none;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-card,
  .jm-card.is-clickable:active {
    transition: none;
    transform: none;
  }
}
</style>
