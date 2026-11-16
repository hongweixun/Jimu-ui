<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Picker from './Picker.vue'
import type { PickerColumnInput, PickerConfirmPayload } from './picker-context'
import type {
  DatePickerConfirmPayload,
  DatePickerFormatter,
  DatePickerType,
  DatePickerUnit,
} from './date-picker-context'

defineOptions({ name: 'JmDatePicker' })

const props = withDefaults(
  defineProps<{
    /** 各列选中的值，如 ['2024','05','12'] */
    modelValue?: string[]
    type?: DatePickerType
    title?: string
    minDate?: Date
    maxDate?: Date
    /** 自定义每列文案 */
    formatter?: DatePickerFormatter
    confirmButtonText?: string
    cancelButtonText?: string
    itemHeight?: number
    visibleCount?: number
  }>(),
  {
    type: 'date',
    title: '选择日期',
    minDate: () => new Date(2000, 0, 1),
    maxDate: () => new Date(2030, 11, 31),
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    itemHeight: 44,
    visibleCount: 5,
  },
)

const emit = defineEmits<{
  'update:modelValue': [values: string[]]
  change: [payload: DatePickerConfirmPayload]
  confirm: [payload: DatePickerConfirmPayload]
  cancel: []
}>()

interface Parts {
  year: number
  month: number
  day: number
  hour: number
  minute: number
}

const pad2 = (n: number) => String(n).padStart(2, '0')
const dayCount = (year: number, month: number) => new Date(year, month, 0).getDate()
const startOfDay = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime()

/** 列顺序由类型决定，后面所有换算都按这个顺序取值 */
const units = computed<DatePickerUnit[]>(() => {
  switch (props.type) {
    case 'time':
      return ['hour', 'minute']
    case 'year-month':
      return ['year', 'month']
    case 'datetime':
      return ['year', 'month', 'day', 'hour', 'minute']
    default:
      return ['year', 'month', 'day']
  }
})

/** 未选值时落在「今天」，超出范围则收敛到边界 */
function fallbackDate(): Date {
  const now = new Date()
  const min = props.minDate.getTime()
  const max = props.maxDate.getTime()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime()
  if (today < startOfDay(props.minDate)) return new Date(min)
  if (today > startOfDay(props.maxDate)) return new Date(max)
  return now
}

function toParts(list: string[]): Parts {
  const fb = fallbackDate()
  const p: Parts = {
    year: fb.getFullYear(),
    month: fb.getMonth() + 1,
    day: fb.getDate(),
    hour: 0,
    minute: 0,
  }
  units.value.forEach((unit, i) => {
    const raw = list[i]
    if (raw === undefined || raw === '') return
    const n = Number(raw)
    if (!Number.isNaN(n)) p[unit] = n
  })
  return p
}

const values = ref<string[]>([])

/** 日期越界/空值都收敛一次，避免出现 2 月 31 日这种状态 */
function normalize(input: string[] | undefined): string[] {
  const fb = fallbackDate()
  const base: Parts = {
    year: fb.getFullYear(),
    month: fb.getMonth() + 1,
    day: fb.getDate(),
    hour: 0,
    minute: 0,
  }
  const list = units.value.map((unit, i) => {
    const raw = input?.[i]
    const n = raw === undefined || raw === '' ? NaN : Number(raw)
    return Number.isNaN(n) ? base[unit] : n
  })
  const p = toParts(list.map(String))
  const out = units.value.map((unit, i) => {
    const n = list[i]
    if (unit === 'day') {
      const max = dayCount(p.year, p.month)
      return pad2(Math.min(Math.max(1, n), max))
    }
    return unit === 'year' ? String(n) : pad2(n)
  })
  return out
}

watch(
  () => props.modelValue,
  (v) => {
    values.value = normalize(Array.isArray(v) ? v : [])
  },
  { immediate: true, deep: true },
)

// 类型切换后列数变了，重新收敛
watch(units, () => {
  values.value = normalize(values.value)
})

const selected = computed<Parts>(() => toParts(values.value))

function label(unit: DatePickerUnit, value: string): string {
  if (props.formatter) return props.formatter(unit, value)
  // datetime 五列宽度有限（每列约 70px），默认不带「年/月」后缀，避免截断
  const bare = props.type === 'datetime'
  if (bare) return value
  switch (unit) {
    case 'year':
      return `${value}年`
    case 'month':
      return `${value}月`
    case 'day':
      return `${value}日`
    case 'hour':
      return `${value}时`
    default:
      return `${value}分`
  }
}

/** 日期部分是否越界 */
function dateDisabled(year: number, month: number, day: number): boolean {
  const t = new Date(year, month - 1, day).getTime()
  return t < startOfDay(props.minDate) || t > startOfDay(props.maxDate)
}

/** 时分是否越界：只在日期已是边界当天时才需要判断 */
function timeDisabled(hour: number, minute: number): boolean {
  const p = selected.value
  const t = new Date(p.year, p.month - 1, p.day, hour, minute).getTime()
  return t < props.minDate.getTime() || t > props.maxDate.getTime()
}

function columnOf(unit: DatePickerUnit) {
  const p = selected.value
  const items: { value: string; disabled?: boolean }[] = []
  const push = (value: string, disabled = false) => items.push({ value, disabled })

  if (unit === 'year') {
    for (let y = props.minDate.getFullYear(); y <= props.maxDate.getFullYear(); y++) {
      push(String(y))
    }
  } else if (unit === 'month') {
    for (let m = 1; m <= 12; m++) {
      // 只在边界年份禁用越界月份；日同理
      const first = new Date(p.year, m - 1, 1).getTime()
      const last = new Date(p.year, m, 0).getTime()
      push(pad2(m), last < startOfDay(props.minDate) || first > startOfDay(props.maxDate))
    }
  } else if (unit === 'day') {
    const total = dayCount(p.year, p.month)
    for (let d = 1; d <= total; d++) {
      push(pad2(d), dateDisabled(p.year, p.month, d))
    }
  } else if (unit === 'hour') {
    for (let h = 0; h < 24; h++) {
      push(pad2(h), props.type === 'datetime' && timeDisabled(h, p.minute))
    }
  } else {
    for (let m = 0; m < 60; m++) {
      push(pad2(m), props.type === 'datetime' && timeDisabled(p.hour, m))
    }
  }

  return items.map((o) => ({
    value: o.value,
    text: label(unit, o.value),
    disabled: o.disabled,
  }))
}

const columns = computed<PickerColumnInput[]>(() => units.value.map(columnOf))

function payloadOf(list: string[]): DatePickerConfirmPayload {
  const p = toParts(list)
  return {
    selectedValues: [...list],
    selectedDate: new Date(p.year, p.month - 1, p.day, p.hour, p.minute),
  }
}

function onChange(p: PickerConfirmPayload) {
  const next = normalize(p.selectedValues as string[])
  values.value = next
  emit('update:modelValue', next)
  emit('change', payloadOf(next))
}

function onConfirm(p: PickerConfirmPayload) {
  const next = normalize(p.selectedValues as string[])
  values.value = next
  emit('update:modelValue', next)
  emit('confirm', payloadOf(next))
}

const picker = ref<InstanceType<typeof Picker> | null>(null)

defineExpose({
  /** 以当前值触发一次确认（外部按钮常用） */
  confirm: () => picker.value?.confirm(),
  cancel: () => picker.value?.cancel(),
  values,
})
</script>

<template>
  <div class="jm-date-picker">
    <Picker
      ref="picker"
      :columns="columns"
      :model-value="values"
      :title="title"
      :confirm-button-text="confirmButtonText"
      :cancel-button-text="cancelButtonText"
      :item-height="itemHeight"
      :visible-count="visibleCount"
      @change="onChange"
      @confirm="onConfirm"
      @cancel="emit('cancel')"
    />
  </div>
</template>

<style>
.jm-date-picker {
  font-family: var(--jm-font-family);
  background: var(--jm-bg-elevated);
}
</style>
