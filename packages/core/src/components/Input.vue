<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, ref, useId, watch } from 'vue'
import { toCssSize } from '../utils'
import { FORM_ITEM_KEY, FORM_KEY } from './form-context'

defineOptions({ name: 'JmInput' })

const props = withDefaults(
  defineProps<{
    modelValue?: string | number
    /** 'textarea' 时渲染多行文本域 */
    type?: string
    placeholder?: string
    /**
     * 标签。labelPlacement 默认 'float'：聚焦或有值后标签上浮；
     * 'top'：标签固定显示在输入框上方；
     * 'left'：标签固定在左侧（Vant Field 行式排版，配合 variant="plain" + 外部卡片使用）。
     */
    label?: string
    /** 标签位置：浮动 / 固定在上方 / 固定在左侧 */
    labelPlacement?: 'float' | 'top' | 'left'
    /** label-placement="left" 时标签列宽 */
    labelWidth?: number | string    /** 左侧模式下 label 后是否追加冒号 */
    colon?: boolean
    /** 必填：label 前显示红色星号 */
    required?: boolean
    size?: 'small' | 'medium' | 'large'
    /** 四种外观：描边 / 灰底 / 下划线 / 无边框透明（Vant Field 行式排版用） */
    variant?: 'outline' | 'filled' | 'underlined' | 'plain'
    radius?: number | string
    clearable?: boolean
    disabled?: boolean
    readonly?: boolean
    /** 校验失败态：描边、标签、placeholder 与光标转红 */
    error?: boolean
    /** 错误提示文案，显示在输入框下方（为 Form 校验预留）；plain 外观时渲染在输入行内、紧贴输入内容 */
    errorMessage?: string
    /** 错误提示文案对齐：左 / 中 / 右；不传时默认跟随 align */
    errorAlign?: 'left' | 'center' | 'right'
    /** 错误提示文案颜色（覆盖默认 danger 色） */
    errorColor?: string
    maxlength?: number
    showWordLimit?: boolean
    /** 文字对齐方向（浮动标签在 center 下保持靠左） */
    align?: 'left' | 'center' | 'right'
    inputmode?: 'text' | 'numeric' | 'decimal' | 'tel' | 'email' | 'search' | 'url'
    autocomplete?: string
    /** ---------- textarea 模式 ---------- */
    /** 内容撑开高度（textarea 专用） */
    autosize?: boolean
    /** textarea 行数（非 autosize 时按此定高） */
    rows?: number
    /** autosize 时的最大高度，数字按 px */
    maxHeight?: number | string
    /** ---------- 固定前缀（如 +86） ---------- */
    /** 带分隔竖线的固定前缀文案；要放图标或组件用 #prefix 插槽 */
    prefixText?: string
    /** ---------- 验证码按钮 ---------- */
    /** 输入框内嵌「获取验证码」按钮 */
    code?: boolean
    codeText?: string
    /**
     * 按钮形状。'auto'（默认）：跟随输入框自身圆角，输入框是胶囊按钮就是胶囊；
     * 'pill' / 'square'：强制胶囊 / 方形。
     */
    codeShape?: 'auto' | 'pill' | 'square'
    /** 按钮样式：'button' 实心按钮 / 'text' 纯文字链接 */
    codeType?: 'button' | 'text'
    /** 倒计时秒数，点击后自动进入倒计时并禁用 */
    codeDuration?: number
  }>(),
  {
    type: 'text',
    labelPlacement: 'float',
    size: 'medium',
    variant: 'outline',
    align: 'left',
    rows: 3,
    codeText: '获取验证码',
    codeShape: 'auto',
    codeType: 'button',
    codeDuration: 60,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
  clear: []
  enter: [value: string]
  /** 点击验证码按钮（点击后组件内部自动开始倒计时并禁用按钮） */
  send: []
}>()

const inputId = useId()
const focused = ref(false)
const inputRef = ref<HTMLInputElement | HTMLTextAreaElement>()

/* ---------- 与 Form / FormItem 联动 ----------
 * 放在 FormItem 里时自动接管校验状态：红框、报错文案、必填星号都由 FormItem 喂进来，
 * 同时把 blur / input 上报给 FormItem 触发对应时机的校验。单独使用时这些 computed 恒为原 props。 */
const formItem = inject(FORM_ITEM_KEY, null)
const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || formItem?.disabled.value || false)

const isError = computed(() => props.error || formItem?.state.value === 'error')
const messageText = computed(() => props.errorMessage ?? formItem?.message.value ?? '')
const isRequired = computed(() => props.required || !!formItem?.required.value)

onMounted(() => {
  /* 告知 FormItem：文案由 Input 自己排（plain 进框内、其余在框下），别再重复渲染 */
  formItem?.claimErrorDisplay()
})

const text = computed(() => (props.modelValue === undefined || props.modelValue === null ? '' : String(props.modelValue)))
const length = computed(() => text.value.length)
const showClear = computed(() => props.clearable && !disabled.value && !props.readonly && text.value.length > 0)

const isTextarea = computed(() => props.type === 'textarea')

/** label 固定在顶部 */
const labelTop = computed(() => !!props.label && props.labelPlacement === 'top')
/** label 固定在左侧（Vant Field 行式排版，textarea 不支持） */
const labelLeft = computed(() => !!props.label && props.labelPlacement === 'left' && !isTextarea.value)
/** 错误文案对齐：未配置时跟随输入框文字对齐 */
const effectiveErrorAlign = computed(() => props.errorAlign ?? props.align)
/** plain 外观无边框，错误文案直接渲染进盒内、紧跟输入内容（Vant Field 行排版习惯）；其余外观放框下方 */
const errorInside = computed(() => props.variant === 'plain')
/** 有 label 才启用浮动；textarea 与 top/left 不参与浮动 */
const floating = computed(() => !!props.label && !isTextarea.value && props.labelPlacement === 'float')
/** 浮起条件：聚焦或有内容。跟 Varlet 一致——只看"是否被激活"，不看长度是否为零 */
const raised = computed(() => floating.value && (focused.value || text.value.length > 0))

/** 浮起后原生 placeholder 才出现，否则会和没浮起的 label 叠在一起 */
const nativePlaceholder = computed(() => {
  if (!floating.value) return props.placeholder
  return raised.value ? props.placeholder : undefined
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-input-radius'] = r
  const mh = toCssSize(props.maxHeight)
  if (mh) s['--jm-input-textarea-max-height'] = mh
  const lw = toCssSize(props.labelWidth)
  if (lw) s['--jm-input-label-width'] = lw
  s['--jm-input-error-align'] = effectiveErrorAlign.value
  if (props.errorColor) s['--jm-input-error-color'] = props.errorColor
  return s
})

/* ---------- textarea 自适应高度 ----------
 * 全程命令式：height 置 auto 读 scrollHeight 再同帧写回 px。
 * 中间态在同一帧内完成、不经 Vue 响应式补丁，所以既不会塌陷也不会闪烁。 */
function resizeArea() {
  const el = inputRef.value as HTMLTextAreaElement | undefined
  if (!isTextarea.value || !props.autosize || !el) return
  el.style.height = 'auto'
  el.style.height = `${el.scrollHeight}px`
}

watch(() => [props.modelValue, props.autosize] as const, () => resizeArea(), { flush: 'post' })
onMounted(resizeArea)

/* ---------- 验证码倒计时 ---------- */
const counting = ref(false)
const remaining = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

function startCountdown(seconds = props.codeDuration) {
  stopCountdown()
  counting.value = true
  remaining.value = seconds
  timer = setInterval(() => {
    remaining.value -= 1
    if (remaining.value <= 0) stopCountdown()
  }, 1000)
}

function stopCountdown() {
  if (timer) clearInterval(timer)
  timer = undefined
  counting.value = false
  remaining.value = 0
}

function onSendCode() {
  if (counting.value || disabled.value) return
  startCountdown()
  emit('send')
}

onBeforeUnmount(stopCountdown)

/** 倒计时固定两位数（08s），按钮宽度不跳动 */
const codeLabel = computed(() => (counting.value ? `${String(remaining.value).padStart(2, '0')}s` : props.codeText))

function onInput(e: Event) {
  const v = (e.target as HTMLInputElement | HTMLTextAreaElement).value
  emit('update:modelValue', v)
  resizeArea()
  formItem?.onChange()
}

function onFocus(e: FocusEvent) {
  focused.value = true
  emit('focus', e)
}

function onBlur(e: FocusEvent) {
  focused.value = false
  emit('blur', e)
  formItem?.onBlur()
}

function onClear() {
  emit('update:modelValue', '')
  emit('clear')
  inputRef.value?.focus()
  formItem?.onChange()
}

function focus() {
  inputRef.value?.focus()
}

function blur() {
  inputRef.value?.blur()
}

defineExpose({ focus, blur, inputRef, startCountdown, stopCountdown })
</script>

<template>
  <div class="jm-input" :style="styles">
    <div
      class="jm-input__box"
      :class="[
        `jm-input--${size}`,
        `jm-input--${variant}`,
        `jm-input--align-${align}`,
        {
          'jm-input--textarea': isTextarea,
          'jm-input--label-top': labelTop,
          'jm-input--label-left': labelLeft,
          'is-focused': focused,
          'is-disabled': disabled,
          'is-readonly': readonly,
          'is-error': isError,
          'is-floating': floating,
          'is-raised': raised,
          'is-code': code,
          'has-error-message': !!messageText,
        },
      ]"
      @click="inputRef?.focus()"
    >
      <!-- label 在顶部：plain 行卡片里即 Vant 的 label-align="top"（顶部对齐），星号/冒号同样生效 -->
      <label v-if="labelTop" class="jm-input__label-top" :for="inputId">
        <i v-if="isRequired" class="jm-input__required" aria-hidden="true">*</i>
        <span class="jm-input__label-text">{{ label }}{{ colon ? '：' : '' }}</span>
      </label>

      <span v-if="$slots['left-icon']" class="jm-input__left-icon"><slot name="left-icon" /></span>

      <!-- label 在左侧：Vant Field 行式排版 -->
      <label v-if="labelLeft" class="jm-input__label-left" :for="inputId">
        <i v-if="isRequired" class="jm-input__required" aria-hidden="true">*</i>
        <span class="jm-input__label-text">{{ label }}{{ colon ? '：' : '' }}</span>
      </label>

      <span v-if="prefixText" class="jm-input__fixed-prefix">{{ prefixText }}</span>

      <span v-if="$slots.prefix" class="jm-input__prefix"><slot name="prefix" /></span>

      <div class="jm-input__field">
        <textarea
          v-if="isTextarea"
          :id="inputId"
          ref="inputRef"
          class="jm-input__inner jm-input__inner--area"
          :value="text"
          :placeholder="nativePlaceholder"
          :disabled="disabled"
          :readonly="readonly"
          :maxlength="maxlength"
          :rows="autosize ? 1 : rows"
          :aria-label="label || placeholder"
          @input="onInput"
          @focus="onFocus"
          @blur="onBlur"
        />
        <input
          v-else
          :id="inputId"
          ref="inputRef"
          class="jm-input__inner"
          :type="type"
          :value="text"
          :placeholder="nativePlaceholder"
          :disabled="disabled"
          :readonly="readonly"
          :maxlength="maxlength"
          :inputmode="inputmode"
          :autocomplete="autocomplete"
          :aria-label="label || placeholder"
          @input="onInput"
          @focus="onFocus"
          @blur="onBlur"
          @keydown.enter="emit('enter', text)"
        />

        <label v-if="floating" class="jm-input__label" :for="inputId">{{ label }}</label>
      </div>

      <!-- 字数统计：textarea 覆盖在框内右下角，单行输入框在框内右侧 -->
      <span
        v-if="showWordLimit && maxlength"
        class="jm-input__count"
        :class="{ 'jm-input__count--area': isTextarea }"
      >{{ length }}/{{ maxlength }}</span>

      <button
        v-if="showClear"
        type="button"
        class="jm-input__clear"
        aria-label="清空"
        @click.stop="onClear"
      >
        <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
          <circle cx="8" cy="8" r="8" fill="currentColor" />
          <path
            d="M5.5 5.5l5 5M10.5 5.5l-5 5"
            stroke="var(--jm-bg-container)"
            stroke-width="1.6"
            stroke-linecap="round"
          />
        </svg>
      </button>

      <span v-if="$slots.suffix" class="jm-input__suffix"><slot name="suffix" /></span>

      <!-- 验证码按钮：嵌在输入框内，点击后自动倒计时禁用 -->
      <button
        v-if="code"
        type="button"
        class="jm-input__code"
        :class="[`jm-input__code--${codeShape}`, `jm-input__code--type-${codeType}`]"
        :disabled="disabled || counting"
        :aria-label="counting ? `${remaining}秒后可重发` : codeText"
        @click.stop="onSendCode"
      >
        {{ codeLabel }}
      </button>

      <!-- 聚焦时从中心展开的高亮线：下划线外观的签名动效，其余外观不用 -->
      <i v-if="variant === 'underlined'" class="jm-input__line" aria-hidden="true" />

      <!-- 错误提示（plain 外观）：无边框盒直接把文案排进输入行内，紧贴输入内容下方 -->
      <div
        v-if="messageText && errorInside"
        class="jm-input__error-message jm-input__error-message--inside"
        :class="{ 'jm-input__error-message--indent': labelLeft }"
      >{{ messageText }}</div>
    </div>

    <!-- 错误提示（其余外观）：显示在输入框下方（行排版时缩进到值列） -->
    <div
      v-if="messageText && !errorInside"
      class="jm-input__error-message"
      :class="{ 'jm-input__error-message--indent': labelLeft }"
    >{{ messageText }}</div>
  </div>
</template>

<style>
/**
 * Input
 * ---------------------------------------------------------------------------
 * 结构：.jm-input（外层布局壳，承载 CSS 变量与框外元素）
 *      └ .jm-input__box（视觉盒：边框/背景/圆角都在这层）
 * 动效参照 Varlet 的 FieldDecorator，按移动端表单的实际用法收敛成三条：
 *   1. 标签上浮：280ms，从控件中心移到边框/顶部，同时缩到 0.75（origin: left）
 *   2. 下划线展开：300ms，从中心 scaleX(0) → scaleX(1)，1px 变 2px 不重排
 *   3. 颜色过渡：200ms，标签、光标、前后缀图标统一跟随聚焦色
 * 全部走语义层令牌，data-motion="off" 时瞬时到位。
 */
.jm-input {
  display: block;
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-input__box {
  --jm-input-height: var(--jm-control-height-md);
  --jm-input-pad-x: 12px;
  /* 浮起落点（相对控件顶边）：outline 骑在边框上，filled 落在框内，underlined 落到框外 */
  --jm-input-label-lift: calc(var(--jm-input-height) / 2 + 2px);

  position: relative;
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
  height: var(--jm-input-height);
  padding: 0 var(--jm-input-pad-x);
  border: var(--jm-border-width) solid var(--jm-border-color-2);
  border-radius: var(--jm-input-radius, var(--jm-radius));
  background: var(--jm-bg-container);
  cursor: text;
  transition: var(--jm-motion-surface);
}

.jm-input__field {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 0;
  height: 100%;
}

/* 输入框字号不允许低于 16px，否则 iOS Safari 聚焦时会自动放大整页 */
.jm-input__inner {
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--jm-text-color);
  caret-color: var(--jm-color-primary);
  font-family: inherit;
  font-size: max(16px, var(--jm-font-size-md));
  line-height: normal;
  -webkit-appearance: none;
  appearance: none;
  transition: color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-input__inner::placeholder {
  color: var(--jm-input-placeholder-color, var(--jm-text-color-4));
  font-size: var(--jm-input-placeholder-font-size, var(--jm-font-size-md));
  font-family: var(--jm-input-placeholder-font-family, inherit);
  font-weight: var(--jm-input-placeholder-font-weight, inherit);
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

/* ---------- textarea 模式 ---------- */
.jm-input--textarea {
  height: auto;
  min-height: var(--jm-input-height);
  padding: 10px var(--jm-input-pad-x);
}

.jm-input--textarea .jm-input__field {
  display: block;
  height: auto;
}

.jm-input__inner--area {
  display: block;
  height: auto;
  resize: none;
  line-height: 1.55;
  max-height: var(--jm-input-textarea-max-height, none);
  overflow-y: auto;
  transition: none;
}

/* ---------- label 固定在顶部（Vant Field 排版） ---------- */
.jm-input--label-top {
  height: auto;
  flex-direction: column;
  align-items: stretch;
  gap: 0;
  padding: 8px var(--jm-input-pad-x) 10px;
}

.jm-input__label-top {
  display: flex;
  align-items: center;
  padding-bottom: 2px;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  line-height: 1.4;
  cursor: text;
}

/* 顶部 label 字号比输入内容小，星号随 label 尺寸 */
.jm-input__label-top .jm-input__required {
  font-size: inherit;
}

.jm-input--label-top .jm-input__field {
  height: auto;
}

.jm-input--label-top .jm-input__inner {
  height: calc(var(--jm-input-height) - 20px);
}

.jm-input--label-top.jm-input--textarea .jm-input__inner {
  height: auto;
}

.jm-input--label-top.is-focused .jm-input__label-top {
  color: var(--jm-color-primary);
}

.jm-input--label-top.is-error .jm-input__label-top {
  color: var(--jm-color-danger);
}

/* ---------- label 固定在左侧（Vant Field 行式排版） ---------- */
.jm-input--label-left .jm-input__label-left {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  /* 固定 px：报错文案缩进也用同一变量，em 在不同字号元素上解析不一致会导致对不齐 */
  width: var(--jm-input-label-width, 96px);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  line-height: 1.4;
  cursor: text;
}

.jm-input__required {
  margin-right: 2px;
  color: var(--jm-color-danger);
  font-style: normal;
  font-family: var(--jm-font-family);
}

.jm-input__label-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-input__left-icon {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-lg);
  transition: var(--jm-motion-color);
}

/* ---------- 外观：无边框透明（Vant Field 行式排版用，配合外部卡片） ----------
 * 提高特异性写在后面：聚焦不出现整框描边，只有底部横线高亮 */
.jm-input__box.jm-input--plain {
  border-color: transparent;
  background: transparent;
}

.jm-input__box.jm-input--plain.is-focused {
  border-color: transparent;
  background: transparent;
}

/* ---------- 浮动标签 ---------- */
.jm-input__label {
  position: absolute;
  top: 50%;
  left: 0;
  max-width: 100%;
  margin-left: -2px;
  padding: 0 2px;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-md);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
  transform-origin: left center;
  transform: translateY(-50%);
  transition:
    transform 280ms var(--jm-motion-enter-ease),
    color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    background-color 120ms linear,
    font-size 280ms var(--jm-motion-enter-ease);
  will-change: transform;
}

.jm-input__box.is-raised .jm-input__label {
  /* scale 放在 translate 之后：平移量按原尺寸计算，不会被 0.75 缩掉 */
  transform: translateY(calc(-50% - var(--jm-input-label-lift))) scale(0.75);
  background: var(--jm-input-label-bg, var(--jm-bg-container));
  border-radius: 2px;
}

.jm-input__box.is-focused .jm-input__label {
  color: var(--jm-color-primary);
}

/* ---------- 固定前缀（如 +86） ---------- */
.jm-input__fixed-prefix {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  padding-right: 10px;
  border-right: 1px solid var(--jm-border-color);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  font-variant-numeric: tabular-nums;
  transition: var(--jm-motion-color);
}

/* ---------- 前后缀与计数器 ---------- */
.jm-input__prefix,
.jm-input__suffix {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-md);
  transition: var(--jm-motion-color);
}

.jm-input__box.is-focused .jm-input__prefix,
.jm-input__box.is-focused .jm-input__suffix {
  color: var(--jm-color-primary);
}

.jm-input__count {
  flex: 0 0 auto;
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-4);
  font-variant-numeric: tabular-nums;
}

/* textarea 的字数统计：覆盖在框内右下角，不挡光标与滚动 */
.jm-input__count--area {
  position: absolute;
  right: var(--jm-input-pad-x);
  bottom: 6px;
  line-height: 1.4;
  pointer-events: none;
  text-shadow: 0 0 3px var(--jm-bg-container), 0 0 3px var(--jm-bg-container);
}

/* 错误提示文案：框外下方，对齐与颜色可配；默认与输入文字对齐（缩进 pad-x） */
.jm-input__error-message {
  margin-top: 4px;
  padding-left: var(--jm-input-pad-x, 12px);
  font-size: var(--jm-font-size-sm);
  line-height: 1.4;
  text-align: var(--jm-input-error-align, left);
  color: var(--jm-input-error-color, var(--jm-color-danger));
}

/* label 在左时，额外缩进整个标签列宽，与输入区对齐 */
.jm-input__error-message--indent {
  padding-left: calc(var(--jm-input-pad-x, 12px) + var(--jm-input-label-width, 96px) + var(--jm-space-2));
}

/* ---------- plain 外观的错误文案：排进盒内、紧跟输入内容（Vant Field 习惯） ----------
 * 盒子从固定高度改为内容撑高：上下补 10px 内边距（文案不再贴死行底分割线），
 * flex-wrap 让全宽文案换到输入内容下一行，row-gap 归零保证间距只有 2px */
.jm-input__box.jm-input--plain.has-error-message {
  height: auto;
  min-height: var(--jm-input-height);
  flex-wrap: wrap;
  row-gap: 0;
  padding-top: 10px;
  padding-bottom: 10px;
}

.jm-input__error-message--inside {
  flex: 0 0 auto;
  width: 100%;
  margin-top: 2px;
  padding-left: 0;
}

/* 盒内已自带 pad-x，label 在左时只需补标签列宽 */
.jm-input__error-message--inside.jm-input__error-message--indent {
  padding-left: calc(var(--jm-input-label-width, 96px) + var(--jm-space-2));
}

.jm-input__clear {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  padding: 2px;
  margin-right: -2px;
  border: 0;
  background: none;
  color: var(--jm-text-color-4);
  cursor: pointer;
  /* 出现时轻微弹一下：清空按钮是"凭空冒出来"的元素，硬切会有跳动感 */
  animation: jm-input-clear-in 160ms var(--jm-motion-enter-ease);
  transition: color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-input__clear:hover {
  color: var(--jm-text-color-3);
}

@keyframes jm-input-clear-in {
  from {
    opacity: 0;
    transform: scale(0.6);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ---------- 验证码按钮 ---------- */
.jm-input__code {
  flex: 0 0 auto;
  height: var(--jm-input-code-height, calc(32px * var(--jm-size-scale)));
  padding: 0 12px;
  border: 0;
  border-radius: var(--jm-input-code-radius, var(--jm-radius-sm));
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast, #fff);
  font-family: inherit;
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

/* auto：跟随输入框自身圆角——输入框是胶囊按钮才是胶囊 */
.jm-input__code--auto {
  border-radius: inherit;
}

.jm-input__code--pill {
  border-radius: var(--jm-radius-round);
}

.jm-input__code--square {
  border-radius: var(--jm-radius-sm);
}

/* 纯文字样式：无底色，主色文字链接 */
.jm-input__code--type-text {
  padding: 0 4px;
  border-radius: 0;
  background: transparent;
  color: var(--jm-color-primary);
}

.jm-input__code--type-text:disabled {
  color: var(--jm-text-color-4);
  opacity: 1;
}

.jm-input__code:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.jm-input--align-left .jm-input__inner {
  text-align: left;
}

.jm-input--align-center .jm-input__inner {
  text-align: center;
}

.jm-input--align-right .jm-input__inner {
  text-align: right;
}

.jm-input--align-right .jm-input__label {
  left: auto;
  right: 0;
  transform-origin: right center;
}

/* ---------- 聚焦 ---------- */
/* 只变色，不投影：移动端小屏幕上外圈光晕会显得脏，边框换色已经足够清晰 */
.jm-input__box.is-focused {
  border-color: var(--jm-color-primary);
}

/* ---------- 外观：灰底 ---------- */
.jm-input--filled {
  --jm-input-label-lift: calc(var(--jm-input-height) / 2 - 10px);
  border-color: transparent;
  background: var(--jm-bg-input);
}

.jm-input--filled .jm-input__label {
  --jm-input-label-bg: transparent;
}

.jm-input--filled.is-focused {
  background: var(--jm-bg-container);
  border-color: var(--jm-color-primary);
}

/* ---------- 外观：下划线 ---------- */
.jm-input--underlined {
  --jm-input-label-lift: calc(var(--jm-input-height) / 2 + 8px);
  padding-left: 0;
  padding-right: 0;
  border-width: 0 0 1px;
  border-radius: 0;
  background: transparent;
}

.jm-input--underlined .jm-input__label {
  --jm-input-label-bg: transparent;
}

.jm-input--underlined.is-focused {
  border-bottom-color: var(--jm-color-primary);
  box-shadow: none;
}

/* 关键帧式的高亮线：只做 transform，不动高度，所以不会挤动上方内容 */
.jm-input__line {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 2px;
  border-radius: 1px;
  background: var(--jm-color-primary);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 300ms var(--jm-ease-standard);
  pointer-events: none;
}

.jm-input__box.is-focused .jm-input__line {
  transform: scaleX(1);
}

/* ---------- 尺寸 ---------- */
.jm-input--small {
  --jm-input-height: var(--jm-control-height-sm);
  --jm-input-pad-x: 10px;
}

.jm-input--large {
  --jm-input-height: var(--jm-control-height-lg);
  --jm-input-pad-x: 14px;
}

/* ---------- 状态 ---------- */
.jm-input__box.is-disabled {
  cursor: not-allowed;
  background: var(--jm-bg-disabled);
  opacity: 0.6;
}

.jm-input__box.is-disabled .jm-input__inner {
  cursor: not-allowed;
}

.jm-input__box.is-readonly {
  background: var(--jm-bg-input);
}

.jm-input__box.is-error {
  border-color: var(--jm-color-danger);
}

.jm-input__box.is-error .jm-input__label,
.jm-input__box.is-error.is-focused .jm-input__label {
  color: var(--jm-color-danger);
}

.jm-input__box.is-error .jm-input__inner {
  caret-color: var(--jm-color-danger);
}

/* 错误态 placeholder 转红（Vant Field 的 error 展示习惯） */
.jm-input__box.is-error .jm-input__inner::placeholder {
  color: var(--jm-color-danger);
}

.jm-input__box.is-error .jm-input__line {
  background: var(--jm-color-danger);
}

/* plain 外观的状态覆盖：行式排版下保持透明，不出现灰底块；报错也不框起来，只用文字颜色表达 */
.jm-input__box.jm-input--plain.is-disabled,
.jm-input__box.jm-input--plain.is-readonly,
.jm-input__box.jm-input--plain.is-error {
  background: transparent;
  border-color: transparent;
}
</style>
