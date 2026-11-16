<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import NumberKeyboard from './NumberKeyboard.vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmPasswordInput' })

const props = withDefaults(
  defineProps<{
    modelValue?: string
    /** 密码位数 */
    length?: number
    /** 格子间距，0 为连体样式 */
    gutter?: number | string
    /** 用圆点遮挡输入内容 */
    mask?: boolean
    /** 受控聚焦（v-model:focused） */
    focused?: boolean
    /** 使用内置数字键盘 */
    showKeyboard?: boolean
    /** 输满后自动收起键盘 */
    autoClose?: boolean
    /** 键盘标题 */
    keyboardTitle?: string
    zIndex?: number
    safeArea?: boolean
    /** 键盘挂载目标：false 就地渲染 */
    teleport?: boolean | string | Element
  }>(),
  {
    modelValue: '',
    length: 6,
    gutter: 0,
    mask: true,
    focused: undefined,
    showKeyboard: true,
    autoClose: false,
    zIndex: 1100,
    safeArea: true,
    teleport: true,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'update:focused': [value: boolean]
  input: [value: string]
  complete: [value: string]
  focus: []
  blur: []
}>()

const inner = ref(props.modelValue ?? '')

watch(
  () => props.modelValue,
  (v) => {
    const next = v ?? ''
    if (next !== inner.value) inner.value = next
  },
)

const isFocused = ref(!!props.focused)

// focused 传了才受控，不传时组件自己管
watch(
  () => props.focused,
  (v) => {
    if (typeof v === 'boolean' && v !== isFocused.value) isFocused.value = v
  },
)

watch(isFocused, (v) => {
  emit('update:focused', v)
  if (v) emit('focus')
  else emit('blur')
})

const keyboardVisible = computed(() => isFocused.value && props.showKeyboard)

function commit(next: string) {
  inner.value = next
  emit('update:modelValue', next)
  emit('input', next)
  if (next.length >= props.length) {
    emit('complete', next)
    if (props.autoClose) isFocused.value = false
  }
}

function onInput(key: string) {
  if (inner.value.length >= props.length) return
  commit(inner.value + key)
}

function onDelete() {
  if (!inner.value.length) return
  commit(inner.value.slice(0, -1))
}

function focus() {
  isFocused.value = true
}

function blur() {
  isFocused.value = false
}

function clear() {
  commit('')
}

/** 桌面端也能直接敲数字，省得只能点 */
function onKeydown(e: KeyboardEvent) {
  if (/^\d$/.test(e.key)) {
    e.preventDefault()
    isFocused.value = true
    onInput(e.key)
  } else if (e.key === 'Backspace') {
    e.preventDefault()
    onDelete()
  }
}

// v-for 遍历数组「值」，这里直接给 1 起的下标，模板里 i === inner.length + 1 才能对上
const cells = computed(() => Array.from({ length: Math.max(1, props.length) }, (_, i) => i + 1))
const gap = computed(() => toCssSize(props.gutter))
const hasGutter = computed(() => !!gap.value && gap.value !== '0px')

const rootStyle = computed(() => ({ '--jm-password-gutter': gap.value ?? '0px' }))

defineExpose({ focus, blur, clear })
</script>

<template>
  <div class="jm-password-input-wrap">
    <div
      class="jm-password-input"
      :class="{ 'is-focused': isFocused, 'has-gutter': hasGutter }"
      :style="rootStyle"
      role="textbox"
      tabindex="0"
      :aria-label="`密码输入，共 ${length} 位`"
      @click="focus"
      @keydown="onKeydown"
    >
      <div
        v-for="i in cells"
        :key="i"
        class="jm-password-input__cell"
        :class="{ 'is-active': isFocused && i === inner.length + 1 }"
      >
        <span v-if="i <= inner.length" class="jm-password-input__dot" :class="{ 'is-plain': !mask }">
          {{ mask ? '' : inner[i - 1] }}
        </span>
      </div>
    </div>

    <NumberKeyboard
      v-if="showKeyboard"
      :show="keyboardVisible"
      :title="keyboardTitle"
      :maxlength="length"
      :value="inner"
      :z-index="zIndex"
      :safe-area="safeArea"
      :teleport="teleport"
      @input="onInput"
      @delete="onDelete"
      @update:show="(v: boolean) => (!v ? blur() : focus())"
    />
  </div>
</template>

<style>
.jm-password-input {
  --jm-password-gutter: 0px;
  display: flex;
  align-items: stretch;
  font-family: var(--jm-font-family);
  cursor: text;
  user-select: none;
  -webkit-user-select: none;
}

.jm-password-input.has-gutter {
  gap: var(--jm-password-gutter);
}

.jm-password-input__cell {
  position: relative;
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  min-width: 0;
  height: 48px;
  border: 1px solid var(--jm-border-color);
  background: var(--jm-bg-container);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

/* 连体样式：相邻边框重叠，只留一条线 */
.jm-password-input:not(.has-gutter) .jm-password-input__cell + .jm-password-input__cell {
  margin-left: -1px;
}

.jm-password-input:not(.has-gutter) .jm-password-input__cell:first-child {
  border-top-left-radius: var(--jm-radius-md);
  border-bottom-left-radius: var(--jm-radius-md);
}

.jm-password-input:not(.has-gutter) .jm-password-input__cell:last-child {
  border-top-right-radius: var(--jm-radius-md);
  border-bottom-right-radius: var(--jm-radius-md);
}

.jm-password-input.has-gutter .jm-password-input__cell {
  border-radius: var(--jm-radius-md);
}

/* 当前待输入的格子：主色描边，一眼看出焦点在哪 */
.jm-password-input__cell.is-active {
  z-index: 1;
  border-color: var(--jm-color-primary);
  box-shadow: 0 0 0 1px var(--jm-color-primary-border);
}

.jm-password-input__dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--jm-text-color);
}

.jm-password-input__dot.is-plain {
  width: auto;
  height: auto;
  border-radius: 0;
  background: none;
  font-size: var(--jm-font-size-lg);
  font-weight: var(--jm-font-weight-medium);
}
</style>
