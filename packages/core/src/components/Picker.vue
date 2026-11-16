<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import PickerColumn from './PickerColumn.vue'
import type {
  PickerColumnInput,
  PickerConfirmPayload,
  PickerFieldNames,
  PickerOption,
} from './picker-context'

defineOptions({ name: 'JmPicker' })

const props = withDefaults(
  defineProps<{
    /** 多列选项：[[...], [...]]；元素可以是字符串/数字或对象 */
    columns: PickerColumnInput[]
    /** 选中的值，顺序对应各列 */
    modelValue?: (string | number)[]
    title?: string
    confirmButtonText?: string
    cancelButtonText?: string
    /** 顶部操作栏 */
    showToolbar?: boolean
    /** 对象选项的字段映射 */
    columnsFieldNames?: PickerFieldNames
    /** 每项高度 */
    itemHeight?: number
    /** 可见项数（奇数效果最好） */
    visibleCount?: number
    /** 整体高度（不传则按 itemHeight * visibleCount 计算） */
    height?: number | string
  }>(),
  {
    title: '',
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    showToolbar: true,
    columnsFieldNames: () => ({}),
    itemHeight: 44,
    visibleCount: 5,
  },
)

const emit = defineEmits<{
  'update:modelValue': [values: (string | number)[]]
  change: [payload: PickerConfirmPayload]
  confirm: [payload: PickerConfirmPayload]
  cancel: []
}>()

/* ---------------- 选项归一化 ---------------- */
const textField = computed(() => props.columnsFieldNames?.text ?? 'text')
const valueField = computed(() => props.columnsFieldNames?.value ?? 'value')
const disabledField = computed(() => props.columnsFieldNames?.disabled ?? 'disabled')

function normalizeOption(input: PickerColumnInput[number]): PickerOption {
  if (input === null || input === undefined) return { text: '', value: '' }
  if (typeof input === 'object') {
    const raw = input as unknown as Record<string, unknown>
    const value = (raw[valueField.value] ?? '') as string | number
    return {
      text: String(raw[textField.value] ?? value),
      value,
      disabled: Boolean(raw[disabledField.value]),
    }
  }
  return { text: String(input), value: input }
}

const normalizedColumns = computed<PickerOption[][]>(() => {
  const cols = Array.isArray(props.columns) ? props.columns : []
  if (!cols.length) return []
  // 容错：直接传一维选项数组时按单列处理
  const first = cols[0] as unknown
  const safe = Array.isArray(first) ? cols : [cols as unknown as PickerColumnInput]
  return (safe as PickerColumnInput[]).map((col) =>
    (Array.isArray(col) ? col : []).map(normalizeOption),
  )
})

/* ---------------- 选中值 ---------------- */
const values = ref<(string | number)[]>([])

watch(
  () => props.modelValue,
  (v) => {
    if (Array.isArray(v)) values.value = [...v]
  },
  { immediate: true, deep: true },
)

/** 未指定的列默认落在第一个可用项上 */
function fillMissing() {
  const next = [...values.value]
  normalizedColumns.value.forEach((col, i) => {
    const exists = col.some((o) => o.value === next[i])
    if (!exists) {
      const firstEnabled = col.find((o) => !o.disabled) ?? col[0]
      if (firstEnabled) next[i] = firstEnabled.value
    }
  })
  values.value = next
}

onMounted(fillMissing)

watch(normalizedColumns, () => nextTick(fillMissing))

const indexes = computed<number[]>(() =>
  normalizedColumns.value.map((col, i) => {
    const idx = col.findIndex((o) => o.value === values.value[i])
    return idx >= 0 ? idx : 0
  }),
)

const selectedOptions = computed<PickerOption[]>(() =>
  normalizedColumns.value.map((col, i) => col[indexes.value[i]] ?? { text: '', value: '' }),
)

function payload(): PickerConfirmPayload {
  return {
    selectedValues: [...values.value],
    selectedOptions: selectedOptions.value,
    selectedIndexes: [...indexes.value],
  }
}

function onColumnChange(columnIndex: number, optionIndex: number) {
  const opt = normalizedColumns.value[columnIndex]?.[optionIndex]
  if (!opt) return
  const next = [...values.value]
  next[columnIndex] = opt.value
  values.value = next
  emit('update:modelValue', next)
  emit('change', payload())
}

function onConfirm() {
  emit('update:modelValue', [...values.value])
  emit('confirm', payload())
}

function onCancel() {
  emit('cancel')
}

const columnsStyle = computed(() => {
  const s: Record<string, string> = {}
  const h = toCssSize(props.height) ?? `${props.itemHeight * props.visibleCount}px`
  s['--jm-picker-column-height'] = h
  s['--jm-picker-item-height'] = `${props.itemHeight}px`
  return s
})

defineExpose({ indexes, values, confirm: onConfirm, cancel: onCancel })
</script>

<template>
  <div class="jm-picker">
    <div v-if="showToolbar" class="jm-picker__toolbar">
      <slot name="cancel">
        <button type="button" class="jm-picker__action" @click="onCancel">
          {{ cancelButtonText }}
        </button>
      </slot>

      <div class="jm-picker__title">
        <slot name="title">{{ title }}</slot>
      </div>

      <slot name="confirm">
        <button type="button" class="jm-picker__action is-confirm" @click="onConfirm">
          {{ confirmButtonText }}
        </button>
      </slot>
    </div>

    <div class="jm-picker__columns" :style="columnsStyle">
      <!-- 用遮罩（mask）做上下渐隐：不依赖背景色，明暗主题通用 -->
      <div class="jm-picker__columns-mask">
        <PickerColumn
          v-for="(col, ci) in normalizedColumns"
          :key="ci"
          :options="col"
          :index="indexes[ci] ?? 0"
          :item-height="itemHeight"
          :visible-count="visibleCount"
          @update:index="(i) => onColumnChange(ci, i)"
        />
      </div>
      <!-- 中间选中带：两条细线标出"停在这行" -->
      <div class="jm-picker__indicator" aria-hidden="true" />
    </div>
  </div>
</template>

<style>
.jm-picker {
  --jm-picker-item-height: 44px;
  display: flex;
  flex-direction: column;
  background: var(--jm-bg-elevated);
  font-family: var(--jm-font-family);
  user-select: none;
}

.jm-picker__toolbar {
  position: relative;
  display: flex;
  align-items: center;
  height: 48px;
  padding: 0 var(--jm-space-2);
  border-bottom: 1px solid var(--jm-border-color);
}

.jm-picker__title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-picker__action {
  flex: 0 0 auto;
  min-width: 56px;
  height: 36px;
  padding: 0 var(--jm-space-3);
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: transparent;
  color: var(--jm-text-color-2);
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  cursor: pointer;
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-picker__action:active {
  background: var(--jm-bg-active);
}

.jm-picker__action.is-confirm {
  color: var(--jm-color-primary);
  font-weight: var(--jm-font-weight-medium);
}

.jm-picker__action:focus-visible {
  outline: 2px solid var(--jm-color-primary);
  outline-offset: -2px;
}

.jm-picker__columns {
  position: relative;
  display: flex;
  height: var(--jm-picker-column-height, 220px);
  padding: 0 var(--jm-space-2);
}

.jm-picker__columns-mask {
  display: flex;
  width: 100%;
  -webkit-mask-image: linear-gradient(
    180deg,
    transparent 0,
    #000 26%,
    #000 74%,
    transparent 100%
  );
  mask-image: linear-gradient(180deg, transparent 0, #000 26%, #000 74%, transparent 100%);
}

/* 选中带：中间一行上下各一条细线，比整块底色更轻 */
.jm-picker__indicator {
  position: absolute;
  left: var(--jm-space-2);
  right: var(--jm-space-2);
  top: 50%;
  height: var(--jm-picker-item-height, 44px);
  margin-top: calc(var(--jm-picker-item-height, 44px) / -2);
  border-top: 1px solid var(--jm-border-color);
  border-bottom: 1px solid var(--jm-border-color);
  pointer-events: none;
}

/* 上下渐隐遮罩：让滚出视区的选项淡出而不是硬切 */
</style>
