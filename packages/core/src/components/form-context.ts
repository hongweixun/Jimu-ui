import type { ComputedRef, InjectionKey } from 'vue'

/** 校验触发时机 */
export type FormValidateTrigger = 'blur' | 'change'
/** 校验状态：'' 未校验 / 'error' 失败 / 'success' 通过 */
export type FormValidateState = '' | 'error' | 'success'

/** 单条校验规则（同时支持内置规则与自定义 validator） */
export interface FormRule {
  /** 必填 */
  required?: boolean
  /** 失败时的文案；不传用内置中文提示 */
  message?: string
  /** 触发时机，不传则失焦与输入都触发 */
  trigger?: FormValidateTrigger | FormValidateTrigger[]
  /** 正则校验 */
  pattern?: RegExp
  /** 类型校验 */
  type?: 'string' | 'number' | 'integer' | 'boolean' | 'array' | 'email' | 'tel' | 'url' | 'date'
  /** 最小长度（字符串/数组）或最小值（数字） */
  min?: number
  /** 最大长度或最大值 */
  max?: number
  /** 固定长度 */
  len?: number
  /** 允许纯空格（默认把纯空格视为空值） */
  whitespace?: boolean
  /** 自定义校验：返回 true / '' 视为通过，返回 false 用默认文案，返回字符串作为文案；支持异步 */
  validator?: (
    value: unknown,
    rule: FormRule,
    model: Record<string, unknown>,
  ) => boolean | string | Promise<boolean | string>
}

/** 表单实例对单个字段的操作句柄 */
export interface FormFieldHandle {
  name?: string
  /** 校验该字段，返回是否通过 */
  validate: (trigger?: FormValidateTrigger) => Promise<boolean>
  /** 当前错误文案（无错为空串） */
  getMessage: () => string
  clearValidate: () => void
  resetField: () => void
  el?: HTMLElement | null
}

export interface FormContext {
  model: Record<string, any>
  rules?: Record<string, FormRule[]>
  /** 是否展示报错文案 */
  showError: ComputedRef<boolean>
  /** 整表禁用：内部所有控件继承 */
  disabled: ComputedRef<boolean>
  /**
   * 表单级校验时机（vant 的 validate-trigger）：只约束「未声明 trigger 的规则」。
   * 规则自己声明了 trigger 就以声明为准。
   */
  validateTrigger: ComputedRef<FormValidateTrigger[]>
  registerField: (field: FormFieldHandle) => void
  unregisterField: (field: FormFieldHandle) => void
}

export const FORM_KEY: InjectionKey<FormContext> = Symbol('jm-form')

/** FormItem 向内部控件（Input 等）暴露的校验上下文 */
export interface FormItemContext {
  name?: string
  state: ComputedRef<FormValidateState>
  /** 已按 show-error 过滤：关闭展示时为空串，但 state 仍为 error（红框保留） */
  message: ComputedRef<string>
  required: ComputedRef<boolean>
  /** 单字段禁用：与 Form 的整表禁用叠加 */
  disabled: ComputedRef<boolean>
  /** 控件接管报错文案的渲染（Input 会把文案排进自己的框内/框下），FormItem 不再重复渲染 */
  claimErrorDisplay: () => void
  onBlur: () => void
  onChange: () => void
}

export const FORM_ITEM_KEY: InjectionKey<FormItemContext> = Symbol('jm-form-item')

/* ------------------------------------------------------------------ */
/* 取值 / 赋值：支持 'a.b.c' 形式的路径                                  */
/* ------------------------------------------------------------------ */

export function getValueByPath(obj: Record<string, any> | undefined, path?: string): unknown {
  if (!obj || !path) return undefined
  if (!path.includes('.')) return obj[path]
  return path.split('.').reduce<any>((acc, key) => (acc === undefined || acc === null ? undefined : acc[key]), obj)
}

export function setValueByPath(obj: Record<string, any> | undefined, path: string | undefined, value: unknown) {
  if (!obj || !path) return
  if (!path.includes('.')) {
    obj[path] = value
    return
  }
  const keys = path.split('.')
  const last = keys.pop() as string
  let target: any = obj
  for (const key of keys) {
    if (target[key] === undefined || target[key] === null) target[key] = {}
    target = target[key]
  }
  target[last] = value
}

/* ------------------------------------------------------------------ */
/* 空值判定                                                             */
/* ------------------------------------------------------------------ */

export function isEmptyValue(value: unknown, allowWhitespace = false): boolean {
  if (value === undefined || value === null) return true
  if (Array.isArray(value)) return value.length === 0
  if (typeof value === 'string') return allowWhitespace ? value.length === 0 : value.trim().length === 0
  return false
}

/* ------------------------------------------------------------------ */
/* 规则执行                                                             */
/* ------------------------------------------------------------------ */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const TEL_RE = /^\+?[\d\s-]{6,20}$/

const TYPE_MESSAGES: Record<string, string> = {
  email: '邮箱格式不正确',
  tel: '手机号格式不正确',
  url: '链接格式不正确',
  number: '必须是数字',
  integer: '必须是整数',
  array: '必须是数组',
  date: '日期格式不正确',
  boolean: '必须是布尔值',
  string: '必须是文本',
}

function checkType(value: unknown, type: NonNullable<FormRule['type']>): boolean {
  switch (type) {
    case 'string':
      return typeof value === 'string'
    case 'number':
      return typeof value === 'number' ? !Number.isNaN(value) : value !== '' && !Number.isNaN(Number(value))
    case 'integer':
      return Number.isInteger(Number(value))
    case 'boolean':
      return typeof value === 'boolean'
    case 'array':
      return Array.isArray(value)
    case 'email':
      return EMAIL_RE.test(String(value))
    case 'tel':
      return TEL_RE.test(String(value))
    case 'url':
      try {
        return !!new URL(String(value))
      } catch {
        return false
      }
    case 'date':
      return !Number.isNaN(new Date(String(value)).getTime())
    default:
      return true
  }
}

/** 量长度/大小：数组看 length、数字看值、其余看字符串长度 */
function measure(value: unknown) {
  if (Array.isArray(value)) return value.length
  if (typeof value === 'number') return value
  return String(value ?? '').length
}

async function runRule(value: unknown, rule: FormRule, model: Record<string, unknown>, label: string): Promise<string> {
  const allowWhitespace = rule.whitespace ?? false
  const empty = isEmptyValue(value, allowWhitespace)

  /* 必填 */
  if (rule.required && empty) {
    return rule.message || `请填写${label}`
  }

  /* 非必填且为空：跳过后续格式类校验，避免「空值报格式错」 */
  if (empty && !rule.validator) return ''

  /* 类型 */
  if (rule.type && !checkType(value, rule.type)) {
    return rule.message || `${label}${TYPE_MESSAGES[rule.type] ?? '格式不正确'}`
  }

  /* 正则 */
  if (rule.pattern && !rule.pattern.test(String(value ?? ''))) {
    return rule.message || `${label}格式不正确`
  }

  /* 长度 / 大小 */
  if (rule.len !== undefined && measure(value) !== rule.len) {
    return rule.message || `${label}长度必须为 ${rule.len}`
  }
  if (rule.min !== undefined && measure(value) < rule.min) {
    return rule.message || (typeof value === 'number' ? `${label}不能小于 ${rule.min}` : `${label}长度不能少于 ${rule.min}`)
  }
  if (rule.max !== undefined && measure(value) > rule.max) {
    return rule.message || (typeof value === 'number' ? `${label}不能大于 ${rule.max}` : `${label}长度不能超过 ${rule.max}`)
  }

  /* 自定义 */
  if (rule.validator) {
    const res = await rule.validator(value, rule, model)
    if (res === true || res === '') return ''
    if (typeof res === 'string') return res
    return rule.message || `${label}校验未通过`
  }

  return ''
}

/** 依次执行规则，返回第一条错误文案；'' 表示通过 */
export async function runRules(
  value: unknown,
  rules: FormRule[],
  model: Record<string, unknown>,
  label = '该项',
): Promise<string> {
  for (const rule of rules) {
    const msg = await runRule(value, rule, model, label)
    if (msg) return msg
  }
  return ''
}

/** 规则是否响应某个触发时机；未声明 trigger 的规则跟随表单级 validateTrigger（默认 blur+change） */
export function ruleMatchesTrigger(
  rule: FormRule,
  trigger: FormValidateTrigger,
  defaults: FormValidateTrigger[] = ['blur', 'change'],
): boolean {
  if (!rule.trigger) return defaults.includes(trigger)
  return Array.isArray(rule.trigger) ? rule.trigger.includes(trigger) : rule.trigger === trigger
}

/** 从规则里推导是否必填 */
export function rulesRequired(rules: FormRule[]): boolean {
  return rules.some((r) => r.required)
}
