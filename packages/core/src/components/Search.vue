<script setup lang="ts">
import { computed, inject, ref } from 'vue'
import JmIcon from './Icon.vue'
import { FORM_KEY } from './form-context'

defineOptions({ name: 'JmSearch' })

const props = withDefaults(
  defineProps<{
    modelValue?: string
    placeholder?: string
    /** 圆形（默认，适合移动端）或方形 */
    shape?: 'round' | 'square'
    size?: 'small' | 'medium' | 'large'
    disabled?: boolean
    readonly?: boolean
    clearable?: boolean
    showCancel?: boolean
    cancelText?: string
    maxlength?: number
    autofocus?: boolean
    /** 输入框底色 */
    background?: string
    align?: 'left' | 'center'
  }>(),
  {
    modelValue: '',
    placeholder: '搜索',
    shape: 'round',
    size: 'medium',
    clearable: true,
    showCancel: false,
    cancelText: '取消',
    align: 'left',
  },
)

const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || false)

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: [value: string]
  clear: []
  cancel: []
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}>()

const inputRef = ref<HTMLInputElement | null>(null)
const focused = ref(false)

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.background) s['--jm-search-bg'] = props.background
  return s
})

const showClear = computed(
  () => props.clearable && !disabled.value && !props.readonly && !!props.modelValue,
)

function onInput(e: Event) {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}

function onClear() {
  emit('update:modelValue', '')
  emit('clear')
  inputRef.value?.focus()
}

function onFocus(e: FocusEvent) {
  focused.value = true
  emit('focus', e)
}

function onBlur(e: FocusEvent) {
  focused.value = false
  emit('blur', e)
}

function onEnter() {
  inputRef.value?.blur()
  emit('search', props.modelValue ?? '')
}

function onCancel() {
  emit('update:modelValue', '')
  emit('cancel')
  inputRef.value?.blur()
}
</script>

<template>
  <div class="jm-search" :class="[`jm-search--${size}`, `jm-search--${shape}`]" :style="styles">
    <div
      class="jm-search__field"
      :class="{
        'is-focused': focused,
        'is-disabled': disabled,
        'is-center': align === 'center',
      }"
    >
      <span class="jm-search__icon" aria-hidden="true">
        <slot name="left-icon">
          <jm-icon name="search" size="18px" :stroke-width="2" />
        </slot>
      </span>

      <input
        ref="inputRef"
        class="jm-search__input"
        type="search"
        inputmode="search"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :maxlength="maxlength"
        :autofocus="autofocus"
        enterkeyhint="search"
        @input="onInput"
        @focus="onFocus"
        @blur="onBlur"
        @keydown.enter.prevent="onEnter"
      />

      <span
        v-if="showClear"
        class="jm-search__clear"
        role="button"
        tabindex="0"
        aria-label="清空"
        @click="onClear"
        @keydown.enter="onClear"
      >
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <circle cx="12" cy="12" r="9" opacity="0.35" />
          <path
            d="M9 9l6 6M15 9l-6 6"
            stroke="var(--jm-bg-container)"
            stroke-width="1.8"
            stroke-linecap="round"
          />
        </svg>
      </span>

      <slot name="right-icon" />
    </div>

    <button v-if="showCancel" class="jm-search__cancel" type="button" @click="onCancel">
      {{ cancelText }}
    </button>
  </div>
</template>

<style>
.jm-search {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
  font-family: var(--jm-font-family);
  --jm-search-height: var(--jm-control-height-md);
}

.jm-search--small {
  --jm-search-height: var(--jm-control-height-sm);
}

.jm-search--large {
  --jm-search-height: var(--jm-control-height-lg);
}

.jm-search__field {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1 1 auto;
  min-width: 0;
  height: var(--jm-search-height);
  padding: 0 10px;
  background: var(--jm-search-bg, var(--jm-bg-input));
  border: var(--jm-border-width) solid transparent;
  border-radius: var(--jm-radius);
  transition: var(--jm-motion-surface);
}

.jm-search--round .jm-search__field {
  border-radius: var(--jm-radius-round);
}

.jm-search__field:focus-within {
  border-color: var(--jm-color-primary);
  background: var(--jm-bg-container);
}

.jm-search__field.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.jm-search__icon {
  display: flex;
  flex: 0 0 auto;
  width: 18px;
  height: 18px;
  color: var(--jm-text-color-3);
}

.jm-search__icon svg {
  width: 100%;
  height: 100%;
}

.jm-search__input {
  flex: 1 1 auto;
  min-width: 0;
  height: 100%;
  padding: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--jm-text-color);
  font-family: inherit;
  /* 锁 16px 起步：小于 16px 时 iOS 聚焦会自动放大页面 */
  font-size: max(16px, var(--jm-font-size-md));
  line-height: normal;
  -webkit-appearance: none;
  appearance: none;
}

.jm-search--small .jm-search__input,
.jm-search--large .jm-search__input {
  font-size: max(16px, var(--jm-font-size-md));
}

.jm-search__field.is-center .jm-search__input {
  text-align: center;
}

.jm-search__input::placeholder {
  color: var(--jm-text-color-4);
}

/* 去掉 iOS/Safari 原生 search 装饰 */
.jm-search__input::-webkit-search-decoration,
.jm-search__input::-webkit-search-cancel-button,
.jm-search__input::-webkit-search-results-button {
  -webkit-appearance: none;
  display: none;
}

.jm-search__clear {
  display: flex;
  flex: 0 0 auto;
  width: 18px;
  height: 18px;
  color: var(--jm-text-color-4);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-search__clear:active {
  opacity: 0.6;
}

.jm-search__clear svg {
  width: 100%;
  height: 100%;
}

.jm-search__cancel {
  flex: 0 0 auto;
  height: var(--jm-search-height);
  padding: 0 4px;
  border: 0;
  background: transparent;
  color: var(--jm-color-primary-text);
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-search__cancel:active {
  opacity: 0.6;
}
</style>
