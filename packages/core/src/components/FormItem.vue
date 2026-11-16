<script setup lang="ts">
import { computed, inject, nextTick, onBeforeUnmount, onMounted, provide, ref } from 'vue'
import { toCssSize } from '../utils'
import {
  FORM_ITEM_KEY,
  FORM_KEY,
  getValueByPath,
  ruleMatchesTrigger,
  rulesRequired,
  runRules,
  setValueByPath,
  type FormItemContext,
  type FormRule,
  type FormValidateState,
  type FormValidateTrigger,
} from './form-context'

defineOptions({ name: 'JmFormItem' })

const props = withDefaults(
  defineProps<{
    /** 关联 model 的字段名，支持 'a.b' 路径；不传则该 FormItem 不参与校验 */
    name?: string
    /** 行标签；不传则 FormItem 只作纯校验容器，视觉交给插槽里的组件 */
    label?: string
    /** 该字段的校验规则，会与 Form 上的同名规则叠加（item 优先） */
    rules?: FormRule[]
    /** 必填红星；不传则根据规则里的 required 自动推导 */
    required?: boolean
    /** 标签后追加冒号 */
    colon?: boolean
    /** 标签列宽，数字按 px */
    labelWidth?: number | string
    /** 标签位置：左 / 右 / 上 */
    labelAlign?: 'left' | 'right' | 'top'
    /** 是否展示报错文案，不传则跟随 Form 的 show-error */
    showError?: boolean
    /** 单字段禁用，与 Form 的整表禁用叠加 */
    disabled?: boolean
    /** 外部直接指定报错文案（优先级最高，置空即清除） */
    errorMessage?: string
    /** 报错文案对齐，不传默认左对齐（有 label 时与值列对齐） */
    errorAlign?: 'left' | 'center' | 'right'
    /** 报错文案颜色 */
    errorColor?: string
    /** 外部接管校验状态 */
    validateStatus?: FormValidateState
  }>(),
  /* required / showError 显式给 undefined：Boolean 类型 prop 缺省时会被 Vue 转成 false，
     那样就没法区分「没传」和「传了 false」，也就没法做自动推导与继承 */
  { labelAlign: 'left', required: undefined, showError: undefined, disabled: undefined },
)

const form = inject(FORM_KEY, null)

const rootRef = ref<HTMLElement>()
const innerState = ref<FormValidateState>('')
const innerMessage = ref('')
/** 被内部控件（Input 等）接管错误展示时置真，FormItem 不再重复渲染文案 */
const fieldClaimed = ref(false)

const rules = computed<FormRule[]>(() => {
  const own = props.rules ?? []
  const fromForm = props.name ? form?.rules?.[props.name] ?? [] : []
  return [...own, ...fromForm]
})

const required = computed(() => !!props.required || rulesRequired(rules.value))

const showErrorMessage = computed(() => props.showError ?? form?.showError.value ?? true)

/** 单字段禁用：与 Form 的整表禁用叠加 */
const isDisabled = computed(() => props.disabled === true || (form?.disabled.value ?? false))

const state = computed<FormValidateState>(() => {
  if (props.validateStatus !== undefined) return props.validateStatus
  if (props.errorMessage) return 'error'
  return innerState.value
})

const message = computed(() => {
  if (props.errorMessage) return props.errorMessage
  return showErrorMessage.value ? innerMessage.value : ''
})

/** 有 label 才是「一整行」：加左右内边距、错误文案缩进到值列 */
const hasLabel = computed(() => !!props.label)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const w = toCssSize(props.labelWidth)
  if (w) s['--jm-form-label-width'] = w
  if (props.errorColor) s['--jm-form-error-color'] = props.errorColor
  if (props.errorAlign) s['--jm-form-error-align'] = props.errorAlign
  return s
})

const classes = computed(() => [
  `jm-form-item--label-${props.labelAlign}`,
  {
    'has-label': hasLabel.value,
    'is-error': state.value === 'error',
    'is-success': state.value === 'success',
    'is-disabled': isDisabled.value,
  },
])

/* ---------------- 校验 ---------------- */

async function validate(trigger?: FormValidateTrigger): Promise<boolean> {
  if (!props.name || !form) {
    /* 没有 name 时不参与校验，外部手动指定 error-message 仍可展示 */
    return !props.errorMessage
  }

  const all = rules.value
  if (!all.length) {
    innerState.value = ''
    innerMessage.value = ''
    return true
  }

  let list = trigger ? all.filter((r) => ruleMatchesTrigger(r, trigger)) : all
  /* 已处于错误态时，输入过程中用全量规则复检：用户改对了就立刻恢复，不用等失焦 */
  if (trigger === 'change' && innerState.value === 'error') list = all
  if (!list.length) return innerState.value !== 'error'

  const value = getValueByPath(form.model, props.name)
  const label = props.label || props.name
  const msg = await runRules(value, list, form.model, label)

  innerMessage.value = msg
  innerState.value = msg ? 'error' : 'success'
  return !msg
}

function clearValidate() {
  innerState.value = ''
  innerMessage.value = ''
}

/* 重置：回到首次挂载时的值 */
let initialValue: unknown
function resetField() {
  if (!form || !props.name) return
  setValueByPath(form.model, props.name, initialValue)
  clearValidate()
}

const handle = {
  get name() {
    return props.name
  },
  validate,
  getMessage: () => props.errorMessage || innerMessage.value,
  clearValidate,
  resetField,
  get el() {
    return rootRef.value ?? null
  },
}

onMounted(() => {
  if (!form) return
  if (props.name) {
    initialValue = getValueByPath(form.model, props.name)
    form.registerField(handle)
  }
})

onBeforeUnmount(() => form?.unregisterField(handle))

provide<FormItemContext>(FORM_ITEM_KEY, {
  get name() {
    return props.name
  },
  state,
  message,
  required,
  disabled: isDisabled,
  claimErrorDisplay: () => {
    fieldClaimed.value = true
  },
  onBlur: () => {
    /* 延后到渲染队列清空后再校验：父组件可能用内联对象绑定 model（:model="{ num: x }"），
       emit 同步链里读到的是旧对象，nextTick 后才是新值 */
    nextTick(() => validate('blur'))
  },
  onChange: () => {
    nextTick(() => validate('change'))
  },
})

/** 点击标签聚焦行内第一个原生控件 */
function focusField() {
  const el = rootRef.value?.querySelector<HTMLElement>('input, textarea, select')
  el?.focus()
}
</script>

<template>
  <div ref="rootRef" class="jm-form-item" :class="classes" :style="styles">
    <label v-if="hasLabel" class="jm-form-item__label" @click="focusField">
      <i v-if="required && labelAlign !== 'top'" class="jm-form-item__required" aria-hidden="true">*</i>
      <slot name="label">{{ label }}{{ colon ? '：' : '' }}</slot>
      <i v-if="required && labelAlign === 'top'" class="jm-form-item__required" aria-hidden="true">*</i>
    </label>

    <div class="jm-form-item__value">
      <slot />
    </div>

    <div v-if="$slots.right" class="jm-form-item__right"><slot name="right" /></div>

    <!-- 字段组件（Input 等）已接管时，文案由它自己渲染到框内/框下，这里不再重复 -->
    <div v-if="message && !fieldClaimed" class="jm-form-item__error">{{ message }}</div>
  </div>
</template>

<style>
/**
 * FormItem
 * ---------------------------------------------------------------------------
 * 两种用法：
 * 1) 带 label：整行布局（label 列 + 值 + #right），值右对齐，报错文案换行到下一行并缩进到值列；
 * 2) 不带 label：纯校验容器，不产生任何视觉（padding/背景/分割线都为 0），
 *    视觉完全由插槽内的组件负责（如自带 label 的 Input 行）。
 */
.jm-form-item {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0 var(--jm-space-2);
  width: 100%;
  box-sizing: border-box;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

/* 纯校验容器：不占额外空间 */
.jm-form-item:not(.has-label) {
  min-height: 0;
  padding: 0;
}

/* 整行模式 */
.jm-form-item.has-label {
  min-height: calc(var(--jm-form-item-height, 48px) * var(--jm-size-scale));
  padding: 0 var(--jm-form-pad-x, 12px);
}

.jm-form-item__label {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  width: var(--jm-form-label-width, 96px);
  color: var(--jm-text-color);
  line-height: 1.4;
  cursor: pointer;
}

.jm-form-item--label-right .jm-form-item__label {
  justify-content: flex-end;
  padding-right: 4px;
}

.jm-form-item__required {
  margin-right: 2px;
  color: var(--jm-color-danger);
  font-style: normal;
}

.jm-form-item__value {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  flex: 1;
  min-width: 0;
}

/* 有 label 时值区靠右，Switch / Rate 这类小控件自然贴边 */
.jm-form-item.has-label .jm-form-item__value {
  justify-content: flex-end;
}

.jm-form-item__right {
  display: inline-flex;
  align-items: center;
  gap: var(--jm-space-1);
  flex: 0 0 auto;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
}

/* 报错文案：换到下一行，缩进到值列 */
.jm-form-item__error {
  flex: 0 0 100%;
  width: 100%;
  margin-top: 4px;
  padding-left: calc(var(--jm-form-label-width, 96px) + var(--jm-space-2));
  font-size: var(--jm-font-size-sm);
  line-height: 1.4;
  text-align: var(--jm-form-error-align, left);
  color: var(--jm-form-error-color, var(--jm-color-danger));
}

.jm-form-item__error:first-child {
  padding-left: 0;
}

/* label 在右时，文案也跟着右对齐 */
.jm-form-item--label-right .jm-form-item__error {
  text-align: right;
}

/* ---------- label 在上 ---------- */
.jm-form-item--label-top.has-label {
  flex-direction: column;
  align-items: stretch;
  gap: 0;
  padding-top: 10px;
  padding-bottom: 10px;
}

.jm-form-item--label-top .jm-form-item__label {
  width: 100%;
  padding-bottom: 2px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.jm-form-item--label-top .jm-form-item__value {
  justify-content: flex-start;
}

.jm-form-item--label-top .jm-form-item__error {
  padding-left: 0;
}

/* ---------- 状态 ---------- */
.jm-form-item.is-error .jm-form-item__label {
  color: var(--jm-color-danger);
}

.jm-form-item.is-disabled .jm-form-item__label {
  color: var(--jm-text-color-4);
}
</style>
