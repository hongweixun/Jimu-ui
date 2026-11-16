<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { GRID_KEY } from './grid-context'

defineOptions({ name: 'JmGridItem' })

const props = withDefaults(
  defineProps<{
    /** 文字（也可用 text 插槽） */
    text?: string
    /** 图标：SVG 的 path d 值；复杂图标用 icon 插槽 */
    icon?: string
    /** 图标尺寸 */
    iconSize?: number | string
    /** 角标内容 */
    badge?: string | number
    /** 小红点（无数字） */
    dot?: boolean
    /** 下标；不传则按挂载顺序自动领取 */
    index?: number
    /** 单项覆盖 Grid 的 clickable */
    clickable?: boolean
  }>(),
  {
    // 显式 undefined 才能绕过 Vue 对布尔 prop 的缺省转换（absent → false），
    // 保住「未传 → 跟随 Grid」的继承链
    clickable: undefined,
  },
)

const grid = inject(GRID_KEY, null)

const emit = defineEmits<{ click: [index: number] }>()

/* 优先用显式 index，否则向 Grid 领取顺序号 */
const autoIndex = ref(0)
onMounted(() => {
  if (props.index === undefined && grid) autoIndex.value = grid.claimIndex()
})

const idx = computed(() => (props.index !== undefined ? props.index : autoIndex.value))

const isClickable = computed(() => props.clickable ?? grid?.clickable.value ?? false)
const direction = computed(() => grid?.direction.value ?? 'row')
const square = computed(() => grid?.square.value ?? false)
const centered = computed(() => grid?.center.value ?? true)
const hasBorder = computed(() => grid?.border.value ?? false)

const iconStyle = computed(() =>
  props.iconSize === undefined
    ? undefined
    : { fontSize: typeof props.iconSize === 'number' ? `${props.iconSize}px` : props.iconSize },
)

function onClick() {
  if (!isClickable.value) return
  grid?.onItemClick(idx.value)
  emit('click', idx.value)
}
</script>

<template>
  <div
    class="jm-grid__item"
    :class="[
      `jm-grid__item--${direction}`,
      {
        'is-clickable': isClickable,
        'is-square': square,
        'is-centered': centered,
        'has-border': hasBorder,
      },
    ]"
    :role="isClickable ? 'button' : undefined"
    :tabindex="isClickable ? 0 : undefined"
    @click="onClick"
    @keydown.enter="onClick"
  >
    <div class="jm-grid__inner">
      <div v-if="$slots.icon || icon" class="jm-grid__icon" :style="iconStyle">
        <slot name="icon">
          <svg v-if="icon" viewBox="0 0 24 24" aria-hidden="true">
            <path :d="icon" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </slot>
        <span v-if="dot" class="jm-grid__dot" />
        <span v-else-if="badge !== undefined && badge !== ''" class="jm-grid__badge">{{ badge }}</span>
      </div>

      <div v-if="text || $slots.text" class="jm-grid__text">
        <slot name="text">{{ text }}</slot>
      </div>

      <slot />
    </div>
  </div>
</template>

<style>
.jm-grid__item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  padding: var(--jm-space-3) var(--jm-space-2);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  line-height: 1.3;
  color: var(--jm-text-color);
  text-align: center;
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
  -webkit-tap-highlight-color: transparent;
}

.jm-grid__item.is-square {
  aspect-ratio: 1 / 1;
}

.jm-grid__item--column {
  justify-content: flex-start;
  text-align: left;
}

.jm-grid__inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 0;
  max-width: 100%;
}

.jm-grid__item--column .jm-grid__inner {
  flex-direction: row;
  align-items: center;
  gap: var(--jm-space-3);
}

.jm-grid__item.is-square .jm-grid__inner {
  justify-content: center;
}

/* 图标 */
.jm-grid__icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 28px;
  height: 28px;
  font-size: 28px;
  color: var(--jm-text-color-2);
}

.jm-grid__icon > svg {
  width: 1em;
  height: 1em;
}

.jm-grid__text {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--jm-text-color-2);
}

/* 角标 */
.jm-grid__badge {
  position: absolute;
  top: -4px;
  right: -8px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-danger);
  color: var(--jm-color-danger-contrast);
  font-size: 11px;
  line-height: 16px;
  font-variant-numeric: tabular-nums;
  text-align: center;
  box-sizing: border-box;
}

.jm-grid__dot {
  position: absolute;
  top: 0;
  right: -2px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--jm-color-danger);
}

/* 细线：只画右、下，靠容器 overflow:hidden 裁掉最外圈 */
.jm-grid__item.has-border::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 1px;
  height: 100%;
  background: var(--jm-border-color);
  transform: scaleX(0.5);
  transform-origin: right;
}

.jm-grid__item.has-border::before {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 1px;
  background: var(--jm-border-color);
  transform: scaleY(0.5);
  transform-origin: bottom;
}

/* 交互 */
.jm-grid__item.is-clickable {
  cursor: pointer;
}

.jm-grid__item.is-clickable:active {
  background: var(--jm-bg-active);
}

@media (hover: hover) {
  .jm-grid__item.is-clickable:hover {
    background: var(--jm-bg-hover);
  }
}

.jm-grid__item.is-clickable:focus-visible {
  outline: 2px solid var(--jm-color-primary);
  outline-offset: -2px;
}
</style>
