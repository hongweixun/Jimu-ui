<script setup lang="ts">
import { computed, nextTick } from 'vue'
import JmIcon from './Icon.vue'
import type { SegmentedOption } from '../types'

defineOptions({ name: 'JmSegmented' })

const props = withDefaults(
  defineProps<{
    modelValue?: string | number
    options?: SegmentedOption[]
    disabled?: boolean
    /** 撑满父容器宽度（默认就是撑满，传 false 变 inline） */
    block?: boolean
    size?: 'small' | 'medium' | 'large'
    /** 选中项的文字颜色 */
    activeColor?: string
    /** 滑块底色 */
    indicatorColor?: string
  }>(),
  {
    options: () => [],
    block: true,
    size: 'medium',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  change: [value: string | number, index: number]
}>()

const activeIndex = computed(() =>
  props.options.findIndex((opt) => opt.value === props.modelValue),
)

const styles = computed(() => {
  const s: Record<string, string> = {
    '--jm-segmented-count': String(Math.max(props.options.length, 1)),
    '--jm-segmented-index': String(Math.max(activeIndex.value, 0)),
  }
  if (props.activeColor) s['--jm-segmented-active-color'] = props.activeColor
  if (props.indicatorColor) s['--jm-segmented-indicator-bg'] = props.indicatorColor
  return s
})

function isDisabled(opt: SegmentedOption): boolean {
  return !!(props.disabled || opt.disabled)
}

function select(opt: SegmentedOption, index: number) {
  if (isDisabled(opt) || opt.value === props.modelValue) return
  emit('update:modelValue', opt.value)
  emit('change', opt.value, index)
}

/* ---------- 键盘：整组只占一个 Tab 停靠点，方向键 / Home / End 切换 ---------- */
const itemEls: (HTMLElement | undefined)[] = []

function setItem(el: unknown, i: number) {
  itemEls[i] = (el as HTMLElement) || undefined
}

function onKeydown(e: KeyboardEvent) {
  const keys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End']
  if (props.disabled || !keys.includes(e.key)) return
  const n = props.options.length
  if (!n) return
  const cur = Math.max(activeIndex.value, 0)
  let next = -1
  if (e.key === 'Home') {
    next = props.options.findIndex((opt) => !isDisabled(opt))
  } else if (e.key === 'End') {
    for (let i = n - 1; i >= 0; i--) {
      if (!isDisabled(props.options[i])) {
        next = i
        break
      }
    }
  } else {
    const dir = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : -1
    for (let step = 1; step <= n; step++) {
      const i = (cur + dir * step + n * 2) % n
      if (!isDisabled(props.options[i])) {
        next = i
        break
      }
    }
  }
  if (next < 0) return
  e.preventDefault()
  select(props.options[next], next)
  nextTick(() => itemEls[next]?.focus())
}
</script>

<template>
  <div
    class="jm-segmented"
    :class="[`jm-segmented--${size}`, { 'is-block': block, 'is-disabled': disabled }]"
    :style="styles"
    role="tablist"
    @keydown="onKeydown"
  >
    <span
      v-if="activeIndex >= 0"
      class="jm-segmented__indicator"
      :class="{ 'is-muted': options[activeIndex]?.disabled }"
      aria-hidden="true"
    />
    <button
      v-for="(opt, i) in options"
      :key="opt.value"
      :ref="(el) => setItem(el, i)"
      type="button"
      role="tab"
      class="jm-segmented__item"
      :class="{ 'is-active': i === activeIndex, 'is-disabled': isDisabled(opt) }"
      :aria-selected="i === activeIndex"
      :tabindex="i === (activeIndex >= 0 ? activeIndex : 0) ? 0 : -1"
      :disabled="isDisabled(opt)"
      @click="select(opt, i)"
    >
      <jm-icon v-if="opt.icon" :name="opt.icon" size="14px" :stroke-width="2" />
      <span v-if="opt.label !== undefined" class="jm-segmented__label">{{ opt.label }}</span>
    </button>
  </div>
</template>

<style>
.jm-segmented {
  --jm-segmented-count: 2;
  --jm-segmented-index: 0;
  --jm-segmented-pad: 3px;
  --jm-segmented-height: 34px;
  position: relative;
  display: flex;
  box-sizing: border-box;
  height: var(--jm-segmented-height);
  padding: var(--jm-segmented-pad);
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-input);
  font-family: var(--jm-font-family);
  -webkit-tap-highlight-color: transparent;
}

.jm-segmented:not(.is-block) {
  display: inline-flex;
}

.jm-segmented--small {
  --jm-segmented-height: 28px;
  --jm-segmented-pad: 2px;
}

.jm-segmented--large {
  --jm-segmented-height: 40px;
  --jm-segmented-pad: 4px;
}

/* 滑块宽度 = 内容区宽度 / 段数，位移按段号整段平移 */
.jm-segmented__indicator {
  position: absolute;
  top: var(--jm-segmented-pad);
  bottom: var(--jm-segmented-pad);
  left: var(--jm-segmented-pad);
  width: calc((100% - var(--jm-segmented-pad) * 2) / var(--jm-segmented-count));
  border-radius: calc(var(--jm-radius-md) - var(--jm-segmented-pad));
  background: var(--jm-segmented-indicator-bg, var(--jm-bg-elevated));
  box-shadow: 0 1px 3px rgba(16, 21, 26, 0.12);
  transform: translateX(calc(var(--jm-segmented-index) * 100%));
  transition: transform var(--jm-motion-transition-duration) var(--jm-motion-spring-ease);
  will-change: transform;
}

.jm-segmented__indicator.is-muted {
  opacity: 0.6;
}

.jm-segmented__item {
  position: relative;
  z-index: 1;
  display: flex;
  flex: 1 1 0%;
  min-width: 0;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 100%;
  padding: 0 6px;
  border: 0;
  background: none;
  color: var(--jm-text-color-2);
  font-family: inherit;
  font-size: var(--jm-font-size-sm);
  line-height: 1;
  cursor: pointer;
  transition: color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
  -webkit-tap-highlight-color: transparent;
}

.jm-segmented__label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-segmented__item.is-active {
  color: var(--jm-segmented-active-color, var(--jm-color-primary));
  font-weight: var(--jm-font-weight-medium);
}

.jm-segmented__item.is-disabled {
  color: var(--jm-text-color-3);
  opacity: 0.55;
  cursor: not-allowed;
}

.jm-segmented__item:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--jm-ring-color);
  border-radius: var(--jm-radius-sm);
}

[data-motion='off'] .jm-segmented__indicator {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-segmented__indicator {
    transition: none;
  }
}
</style>
