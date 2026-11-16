<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Picker from './Picker.vue'
import type { CascadeOption, PickerConfirmPayload, PickerOption } from './picker-context'

defineOptions({ name: 'JmCascadePicker' })

const props = withDefaults(
  defineProps<{
    /** 级联选项树 */
    options?: CascadeOption[]
    /** 各级选中的值，长度即已选层级 */
    modelValue?: (string | number)[]
    title?: string
    confirmButtonText?: string
    cancelButtonText?: string
    showToolbar?: boolean
    itemHeight?: number
    visibleCount?: number
  }>(),
  {
    options: () => [],
    title: '',
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    showToolbar: true,
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

/** 每一级的选中下标；层级深度由数据决定，改上层会把下层重置 */
const path = ref<number[]>([])

/* ---------------- 按 path 拼出各列 ---------------- */
const columns = computed<PickerOption[][]>(() => {
  const cols: PickerOption[][] = []
  let nodes = props.options ?? []
  let level = 0
  while (nodes.length) {
    cols.push(nodes.map((n) => ({ text: n.text, value: n.value, disabled: n.disabled })))
    nodes = nodes[path.value[level] ?? 0]?.children ?? []
    level += 1
  }
  return cols
})

const values = computed<(string | number)[]>(() =>
  columns.value
    .map((col, i) => col[path.value[i] ?? 0]?.value)
    .filter((v): v is string | number => v !== undefined),
)

const selectedOptions = computed<PickerOption[]>(() => {
  const list: PickerOption[] = []
  let nodes = props.options ?? []
  for (let i = 0; i < columns.value.length; i += 1) {
    const node = nodes[path.value[i] ?? 0]
    if (!node) break
    list.push({ text: node.text, value: node.value, disabled: node.disabled })
    nodes = node.children ?? []
  }
  return list
})

function payload(): PickerConfirmPayload {
  return {
    selectedValues: [...values.value],
    selectedOptions: selectedOptions.value,
    selectedIndexes: path.value.slice(),
  }
}

/* ---------------- 外部值 → path ---------------- */
function syncFromValue() {
  const target = props.modelValue
  if (!Array.isArray(target) || target.length === 0) {
    path.value = []
    return
  }
  const next: number[] = []
  let nodes = props.options ?? []
  for (const v of target) {
    const idx = nodes.findIndex((n) => n.value === v)
    if (idx < 0) break
    next.push(idx)
    nodes = nodes[idx]?.children ?? []
  }
  path.value = next
}

watch(() => props.modelValue, syncFromValue, { immediate: true, deep: true })
watch(() => props.options, syncFromValue, { deep: true })

/* ---------------- 用户滚动某一列 ---------------- */
function onChange(p: PickerConfirmPayload) {
  const idxs = p.selectedIndexes
  const changed = idxs.findIndex((v, i) => v !== (path.value[i] ?? 0))
  if (changed === -1) return

  // 只保留到变化的那一级：下层的值随新数据失效，回到第一项
  path.value = idxs.slice(0, changed + 1)
  emit('update:modelValue', values.value)
  emit('change', payload())
}

function onConfirm() {
  emit('update:modelValue', values.value)
  emit('confirm', payload())
}

function onCancel() {
  emit('cancel')
}

defineExpose({ path, values, confirm: onConfirm })
</script>

<template>
  <Picker
    :columns="columns"
    :model-value="values"
    :title="title"
    :confirm-button-text="confirmButtonText"
    :cancel-button-text="cancelButtonText"
    :show-toolbar="showToolbar"
    :item-height="itemHeight"
    :visible-count="visibleCount"
    @change="onChange"
    @confirm="onConfirm"
    @cancel="onCancel"
  />
</template>
