<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import Popup from './Popup.vue'
import Icon from './Icon.vue'

defineOptions({ name: 'JmNumberKeyboard' })

const props = withDefaults(
  defineProps<{
    /** 是否显示，配合 v-model:show */
    show?: boolean
    /** default：数字九宫格；custom：完全自定义按键 */
    theme?: 'default' | 'custom'
    title?: string
    /** 左下角辅助键：false 留空，字符串则作为按键内容 */
    extraKey?: boolean | string
    /** 右上角关闭按钮文案，传了才显示按钮 */
    closeButtonText?: string
    /** 数字键随机排列 */
    randomKeyOrder?: boolean
    /** 已输入内容，用于 maxlength 判断 */
    value?: string
    maxlength?: number
    /** 长按退格连续删除 */
    deleteRepeat?: boolean
    zIndex?: number
    safeArea?: boolean
    /** 挂载目标：false 就地渲染（手机模拟框内），默认 body */
    teleport?: boolean | string | Element
  }>(),
  {
    theme: 'default',
    extraKey: false,
    randomKeyOrder: false,
    value: '',
    maxlength: Number.MAX_SAFE_INTEGER,
    deleteRepeat: true,
    zIndex: 1100,
    safeArea: true,
    teleport: true,
  },
)

const emit = defineEmits<{
  'update:show': [value: boolean]
  input: [key: string]
  delete: []
  close: []
}>()

const digits = ref<string[]>(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

function shuffle() {
  const list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  if (!props.randomKeyOrder) {
    digits.value = list
    return
  }
  for (let i = list.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[list[i], list[j]] = [list[j], list[i]]
  }
  digits.value = list
}

watch(
  () => [props.randomKeyOrder, props.show] as const,
  () => shuffle(),
  { immediate: true },
)

const reachedLimit = computed(() => props.value.length >= props.maxlength)

function input(key: string) {
  if (reachedLimit.value) return
  emit('input', key)
}

const extraLabel = computed(() => {
  if (typeof props.extraKey === 'string') return props.extraKey
  return ''
})

function onExtra() {
  if (extraLabel.value) input(extraLabel.value)
}

/* 长按退格：460ms 后以 90ms 间隔连删，松手即停 */
let holdTimer: ReturnType<typeof setTimeout> | null = null
let repeatTimer: ReturnType<typeof setInterval> | null = null

function stopHold() {
  if (holdTimer) {
    clearTimeout(holdTimer)
    holdTimer = null
  }
  if (repeatTimer) {
    clearInterval(repeatTimer)
    repeatTimer = null
  }
}

function onDeleteDown(e: PointerEvent) {
  e.preventDefault()
  emit('delete')
  if (!props.deleteRepeat) return
  stopHold()
  holdTimer = setTimeout(() => {
    repeatTimer = setInterval(() => emit('delete'), 90)
  }, 460)
}

function close() {
  emit('update:show', false)
  emit('close')
}

onBeforeUnmount(stopHold)

defineExpose({ shuffle })
</script>

<template>
  <Popup
    :show="show"
    position="bottom"
    :mask="false"
    :lock="false"
    :safe-area="safeArea"
    :z-index="zIndex"
    :teleport="teleport"
    @update:show="(v: boolean) => emit('update:show', v)"
  >
    <div class="jm-number-keyboard" :class="`jm-number-keyboard--${theme}`" role="group" aria-label="数字键盘">
      <div v-if="title || closeButtonText" class="jm-number-keyboard__header">
        <span class="jm-number-keyboard__title">{{ title }}</span>
        <button v-if="closeButtonText" type="button" class="jm-number-keyboard__close" @click="close">
          {{ closeButtonText }}
        </button>
      </div>

      <div v-if="theme === 'custom'" class="jm-number-keyboard__custom">
        <slot :input="input" :delete="() => emit('delete')" :close="close" />
      </div>

      <div v-else class="jm-number-keyboard__grid">
        <button
          v-for="d in digits"
          :key="d"
          type="button"
          class="jm-number-keyboard__key"
          :class="{ 'is-disabled': reachedLimit }"
          @click="input(d)"
        >
          {{ d }}
        </button>

        <button
          type="button"
          class="jm-number-keyboard__key is-extra"
          :class="{ 'is-disabled': reachedLimit || !extraLabel }"
          @click="onExtra"
        >
          {{ extraLabel }}
        </button>

        <button
          type="button"
          class="jm-number-keyboard__key"
          :class="{ 'is-disabled': reachedLimit }"
          @click="input('0')"
        >
          0
        </button>

        <button
          type="button"
          class="jm-number-keyboard__key is-delete"
          aria-label="删除"
          @pointerdown="onDeleteDown"
          @pointerup="stopHold"
          @pointerleave="stopHold"
          @pointercancel="stopHold"
          @contextmenu.prevent
        >
          <Icon name="backspace" :size="22" />
        </button>
      </div>
    </div>
  </Popup>
</template>

<style>
.jm-number-keyboard {
  --jm-keyboard-gap: 6px;
  padding: var(--jm-keyboard-gap);
  padding-bottom: calc(var(--jm-keyboard-gap) + var(--jm-safe-bottom, 0px));
  background: var(--jm-bg-input);
  font-family: var(--jm-font-family);
  user-select: none;
  -webkit-user-select: none;
}

.jm-number-keyboard__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  padding: 0 var(--jm-space-2);
}

.jm-number-keyboard__title {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
}

.jm-number-keyboard__close {
  appearance: none;
  border: 0;
  background: none;
  padding: 4px 6px;
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  color: var(--jm-color-primary);
  cursor: pointer;
}

.jm-number-keyboard__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--jm-keyboard-gap);
}

.jm-number-keyboard__key {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  border: 0;
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-container);
  color: var(--jm-text-color);
  font-family: var(--jm-font-family-number), var(--jm-font-family);
  font-size: 24px;
  font-weight: var(--jm-font-weight-medium);
  line-height: 1;
  cursor: pointer;
  /* 按键按下的即时反馈，不等 click 往返 */
  transition: background-color 0.12s ease, transform 0.12s ease;
}

.jm-number-keyboard__key:active {
  background: var(--jm-bg-active);
  transform: scale(0.97);
}

.jm-number-keyboard__key.is-extra {
  font-size: 18px;
  color: var(--jm-text-color-2);
}

.jm-number-keyboard__key.is-delete {
  background: var(--jm-bg-input);
  color: var(--jm-text-color-2);
  transition: background-color 0.12s ease;
}

.jm-number-keyboard__key.is-delete:active {
  background: var(--jm-bg-active);
  transform: none;
}

.jm-number-keyboard__key.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-number-keyboard__custom {
  display: flex;
  flex-wrap: wrap;
  gap: var(--jm-keyboard-gap);
}

/* 自定义按键也复用同一套外观（全局样式里用子选择器，:slotted 只对 scoped 有效） */
.jm-number-keyboard__custom > * {
  flex: 1 1 30%;
}
</style>
