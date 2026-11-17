<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import { FORM_ITEM_KEY, FORM_KEY } from './form-context'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmRate' })

const props = withDefaults(
  defineProps<{
    modelValue?: number
    count?: number
    /** 星星尺寸，数字按 px */
    size?: number | string
    gutter?: number
    activeColor?: string
    voidColor?: string
    allowHalf?: boolean
    /** 再次点击当前值可清零 */
    allowClear?: boolean
    readonly?: boolean
    disabled?: boolean
    /** 只读时在右侧显示分数 */
    showText?: boolean
  }>(),
  {
    modelValue: 0,
    count: 5,
    size: 24,
    gutter: 4,
    allowHalf: false,
    allowClear: true,
    readonly: false,
    disabled: false,
    showText: false,
  },
)

/* 放在 FormItem 里时，点选后立刻按 change 时机校验 */
const formItem = inject(FORM_ITEM_KEY, null)
const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || formItem?.disabled.value || false)


const emit = defineEmits<{
  'update:modelValue': [value: number]
  change: [value: number]
}>()

const hoverValue = ref<number | null>(null)
const interactive = computed(() => !props.readonly && !disabled.value)
const display = computed(() => hoverValue.value ?? props.modelValue)

const styles = computed(() => {
  const s: Record<string, string> = {
    '--jm-rate-size': toCssSize(props.size) ?? '24px',
    '--jm-rate-gutter': `${props.gutter}px`,
  }
  if (props.activeColor) s['--jm-rate-active'] = props.activeColor
  if (props.voidColor) s['--jm-rate-void'] = props.voidColor
  return s
})

function fillPercent(index: number) {
  const v = display.value
  if (v >= index + 1) return 100
  if (v >= index + 0.5) return 50
  return 0
}

function pick(value: number) {
  if (!interactive.value) return
  let next = value
  if (props.allowClear && props.modelValue === value) next = 0
  emit('update:modelValue', next)
  emit('change', next)
  formItem?.onChange()
}

function onHover(value: number) {
  if (!interactive.value) return
  hoverValue.value = value
}

function onLeave() {
  hoverValue.value = null
}

function onKeydown(e: KeyboardEvent) {
  if (!interactive.value) return
  const step = props.allowHalf ? 0.5 : 1
  if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
    e.preventDefault()
    const next = Math.min(props.count, props.modelValue + step)
    emit('update:modelValue', next)
    emit('change', next)
    formItem?.onChange()
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
    e.preventDefault()
    const next = Math.max(0, props.modelValue - step)
    emit('update:modelValue', next)
    emit('change', next)
    formItem?.onChange()
  }
}
</script>

<template>
  <div
    class="jm-rate"
    :class="{ 'is-readonly': !interactive, 'is-disabled': disabled }"
    :style="styles"
    role="slider"
    :tabindex="interactive ? 0 : undefined"
    :aria-label="'评分'"
    :aria-valuemin="0"
    :aria-valuemax="count"
    :aria-valuenow="modelValue"
    :aria-readonly="!interactive || undefined"
    @mouseleave="onLeave"
    @keydown="onKeydown"
  >
    <span v-for="i in count" :key="i" class="jm-rate__item">
      <span class="jm-rate__star">
        <svg class="jm-rate__void" viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M12 2.6l2.86 5.98 6.54.86-4.79 4.6 1.2 6.5L12 17.5l-5.81 3.04 1.2-6.5-4.79-4.6 6.54-.86L12 2.6z"
            fill="currentColor"
          />
        </svg>
        <span class="jm-rate__fill" :style="{ width: `${fillPercent(i - 1)}%` }">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M12 2.6l2.86 5.98 6.54.86-4.79 4.6 1.2 6.5L12 17.5l-5.81 3.04 1.2-6.5-4.79-4.6 6.54-.86L12 2.6z"
              fill="currentColor"
            />
          </svg>
        </span>
        <template v-if="interactive">
          <span
            v-if="allowHalf"
            class="jm-rate__hit jm-rate__hit--half"
            @click="pick(i - 0.5)"
            @mouseenter="onHover(i - 0.5)"
          />
          <span class="jm-rate__hit" @click="pick(i)" @mouseenter="onHover(i)" />
        </template>
      </span>
    </span>

    <span v-if="showText" class="jm-rate__text">{{ modelValue }}</span>
  </div>
</template>

<style>
.jm-rate {
  display: inline-flex;
  align-items: center;
  gap: var(--jm-rate-gutter, 4px);
  font-family: var(--jm-font-family);
  outline: none;
  -webkit-tap-highlight-color: transparent;
}

.jm-rate:focus-visible {
  box-shadow: 0 0 0 3px var(--jm-ring-color);
  border-radius: var(--jm-radius-sm);
}

.jm-rate__item {
  display: inline-flex;
}

.jm-rate__star {
  position: relative;
  display: inline-flex;
  width: var(--jm-rate-size, 24px);
  height: var(--jm-rate-size, 24px);
  color: var(--jm-rate-void, var(--jm-gray-300));
}

.jm-rate__void,
.jm-rate__fill svg {
  width: 100%;
  height: 100%;
  display: block;
}

.jm-rate__fill {
  position: absolute;
  inset: 0 auto 0 0;
  overflow: hidden;
  color: var(--jm-rate-active, var(--jm-color-warning));
  transition: width var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-rate__fill svg {
  width: var(--jm-rate-size, 24px);
  height: var(--jm-rate-size, 24px);
}

.jm-rate.is-disabled .jm-rate__star {
  opacity: 0.45;
}

.jm-rate:not(.is-readonly) .jm-rate__star {
  cursor: pointer;
}

.jm-rate__hit {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  border-radius: var(--jm-radius-xs);
}

.jm-rate__hit--half {
  right: auto;
  left: 0;
  width: 50%;
  /* 半星热区必须压在整星热区之上：整星热区 100% 宽且 DOM 顺序靠后，
     不抬层级的话左半边的点击永远落不到半星上 */
  z-index: 1;
}

.jm-rate__text {
  margin-left: var(--jm-space-1);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
  font-variant-numeric: tabular-nums;
}

/* 触屏放大点击热区，避免小数点级别的手势需要精确点中 */
@media (hover: none) {
  .jm-rate__hit {
    height: 120%;
    top: -10%;
  }
}

[data-motion='off'] .jm-rate__fill {
  transition: none;
}
</style>
