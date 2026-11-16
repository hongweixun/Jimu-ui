<script setup lang="ts">
import { computed, provide } from 'vue'
import { toCssSize } from '../utils'
import {
  FORM_KEY,
  type FormContext,
  type FormFieldHandle,
  type FormRule,
  type FormValidateTrigger,
} from './form-context'

defineOptions({ name: 'JmForm' })

const props = withDefaults(
  defineProps<{
    /** 表单数据对象，字段通过 FormItem 的 name 关联到这里 */
    model: Record<string, any>
    /** 全局校验规则，键为字段 name（可与 FormItem 的 rules 叠加） */
    rules?: Record<string, FormRule[]>
    /** 字段标签列宽，FormItem 共用；数字按 px */
    labelWidth?: number | string
    /** 是否展示校验失败文案（关掉后仍保留红框状态） */
    showError?: boolean
    /** 校验失败时自动把第一个出错的字段滚动到视野中间 */
    scrollToError?: boolean
    /** 整表禁用：内部所有表单控件（Input/Switch/Stepper 等）继承 */
    disabled?: boolean
  }>(),
  { showError: true, scrollToError: false, disabled: undefined },
)

const emit = defineEmits<{
  /** 校验通过后提交 */
  submit: [model: Record<string, any>]
  /** 校验失败 */
  failed: [info: { errors: Array<{ name?: string; message: string }> }]
  /** 每次校验结束（通过与否都触发） */
  validate: [passed: boolean]
}>()

const showError = computed(() => props.showError)
const isDisabled = computed(() => props.disabled === true)

/* 字段注册表：用数组保持挂载顺序，校验结果顺序与视觉顺序一致 */
const fields: FormFieldHandle[] = []
/** 最近一次校验的错误清单，供 failed 事件使用 */
let lastErrors: Array<{ name?: string; message: string }> = []

function registerField(field: FormFieldHandle) {
  if (!field.name || fields.includes(field)) return
  fields.push(field)
}

function unregisterField(field: FormFieldHandle) {
  const i = fields.indexOf(field)
  if (i > -1) fields.splice(i, 1)
}

provide<FormContext>(FORM_KEY, {
  get model() {
    return props.model
  },
  get rules() {
    return props.rules
  },
  showError,
  disabled: isDisabled,
  registerField,
  unregisterField,
})

function scrollTo(el: HTMLElement | null | undefined) {
  if (!el || typeof el.scrollIntoView !== 'function') return
  el.scrollIntoView({ block: 'center', behavior: 'smooth' })
}

/** 校验全部字段；返回是否通过，不 reject，调用方不用包 try/catch */
async function validate(): Promise<boolean> {
  let firstFailed: FormFieldHandle | undefined
  const errors: Array<{ name?: string; message: string }> = []
  /* 顺序执行：字段常有异步校验，并发也没问题，但串行能保证「首个错误」与视觉顺序一致 */
  for (const field of fields) {
    const ok = await field.validate()
    if (!ok) {
      if (!firstFailed) firstFailed = field
      errors.push({ name: field.name, message: field.getMessage() })
    }
  }
  lastErrors = errors
  const passed = errors.length === 0
  emit('validate', passed)
  if (!passed && props.scrollToError) scrollTo(firstFailed?.el)
  return passed
}

/** 校验指定字段（不传则全部） */
async function validateField(name?: string | string[]): Promise<boolean> {
  const names = name === undefined ? undefined : Array.isArray(name) ? name : [name]
  const targets = names ? fields.filter((f) => f.name && names.includes(f.name)) : [...fields]
  const results = await Promise.all(targets.map((f) => f.validate()))
  return results.every(Boolean)
}

/** 清空校验状态（不恢复数据） */
function clearValidate(name?: string | string[]) {
  const names = name === undefined ? undefined : Array.isArray(name) ? name : [name]
  fields
    .filter((f) => !names || (f.name && names.includes(f.name)))
    .forEach((f) => f.clearValidate())
}

/** 重置指定字段的数据到初始值并清空校验（不传则全部） */
function resetFields(name?: string | string[]) {
  const names = name === undefined ? undefined : Array.isArray(name) ? name : [name]
  fields
    .filter((f) => !names || (f.name && names.includes(f.name)))
    .forEach((f) => f.resetField())
}

/** 手动滚动到指定字段 */
function scrollToField(name: string) {
  scrollTo(fields.find((f) => f.name === name)?.el)
}

async function onSubmit(e: Event) {
  e.preventDefault()
  const passed = await validate()
  if (passed) emit('submit', props.model)
  else emit('failed', { errors: lastErrors })
}

defineExpose({ validate, validateField, clearValidate, resetFields, scrollToField })

const styles = computed(() => {
  const s: Record<string, string> = {}
  const lw = toCssSize(props.labelWidth)
  if (lw) s['--jm-form-label-width'] = lw
  return s
})
</script>

<template>
  <form class="jm-form" :style="styles" @submit="onSubmit">
    <slot />
  </form>
</template>

<style>
/**
 * Form
 * ---------------------------------------------------------------------------
 * 只负责「数据 + 规则 + 提交」，视觉交给 FormItem 与内部控件：
 *   - 有 label 的 FormItem 是一整行（label 列 + 值 + 错误文案）
 *   - 无 label 的 FormItem 只是校验容器，样式完全交给插槽里的组件（如自带 label 的 Input）
 */
.jm-form {
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}
</style>
