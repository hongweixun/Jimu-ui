<script setup lang="ts">
import { computed, inject, ref, watch } from 'vue'
import JmButton from './Button.vue'
import JmIcon from './Icon.vue'
import JmSearch from './Search.vue'
import { FORM_KEY } from './form-context'
import type { TransferItem } from './transfer-context'

defineOptions({ name: 'JmTransfer' })

const props = withDefaults(
  defineProps<{
    /** 全部可选数据 */
    data?: TransferItem[]
    /** 右侧已选的值 */
    modelValue?: (string | number)[]
    /** 左右两侧标题 */
    titles?: [string, string]
    /** 面板内搜索 */
    searchable?: boolean
    /** 每个列表的可视高度 */
    height?: string
    disabled?: boolean
    /** 左侧为空时的文案 */
    emptyText?: string
  }>(),
  {
    data: () => [],
    titles: () => ['可选', '已选'],
    searchable: true,
    height: '220px',
    emptyText: '没有可选项',
  },
)

const emit = defineEmits<{
  'update:modelValue': [values: (string | number)[]]
  change: [values: (string | number)[], info: { direction: 'to-right' | 'to-left'; moved: (string | number)[] }]
}>()

const form = inject(FORM_KEY, null)
const isDisabled = computed(() => props.disabled || !!form?.disabled.value)

const innerValues = ref<(string | number)[]>([...(props.modelValue ?? [])])
watch(
  () => props.modelValue,
  (v) => {
    if (v) innerValues.value = [...v]
  },
)

const values = computed<(string | number)[]>(() => props.modelValue ?? innerValues.value)

const leftKeyword = ref('')
const rightKeyword = ref('')
const leftChecked = ref(new Set<string>())
const rightChecked = ref(new Set<string>())

const keyOf = (v: string | number) => String(v)

const leftAll = computed(() => props.data.filter((d) => !values.value.some((v) => keyOf(v) === keyOf(d.value))))
const rightAll = computed(() =>
  values.value
    .map((v) => props.data.find((d) => keyOf(d.value) === keyOf(v)))
    .filter((d): d is TransferItem => !!d),
)

function match(item: TransferItem, keyword: string) {
  const q = keyword.trim().toLowerCase()
  if (!q) return true
  return item.label.toLowerCase().includes(q) || (item.desc ?? '').toLowerCase().includes(q)
}

const leftList = computed(() => leftAll.value.filter((d) => match(d, leftKeyword.value)))
const rightList = computed(() => rightAll.value.filter((d) => match(d, rightKeyword.value)))

/** 可勾选的项（禁用项不参与全选计算） */
const leftSelectable = computed(() => leftList.value.filter((d) => !d.disabled))
const rightSelectable = computed(() => rightList.value.filter((d) => !d.disabled))

const leftAllChecked = computed(
  () => leftSelectable.value.length > 0 && leftSelectable.value.every((d) => leftChecked.value.has(keyOf(d.value))),
)
const leftIndeterminate = computed(
  () => !leftAllChecked.value && leftSelectable.value.some((d) => leftChecked.value.has(keyOf(d.value))),
)
const rightAllChecked = computed(
  () => rightSelectable.value.length > 0 && rightSelectable.value.every((d) => rightChecked.value.has(keyOf(d.value))),
)
const rightIndeterminate = computed(
  () => !rightAllChecked.value && rightSelectable.value.some((d) => rightChecked.value.has(keyOf(d.value))),
)

const leftCheckedCount = computed(
  () => leftList.value.filter((d) => leftChecked.value.has(keyOf(d.value)) && !d.disabled).length,
)
const rightCheckedCount = computed(
  () => rightList.value.filter((d) => rightChecked.value.has(keyOf(d.value)) && !d.disabled).length,
)

function toggle(side: 'left' | 'right', item: TransferItem) {
  if (isDisabled.value || item.disabled) return
  const ref_ = side === 'left' ? leftChecked : rightChecked
  const key = keyOf(item.value)
  const next = new Set(ref_.value)
  if (next.has(key)) next.delete(key)
  else next.add(key)
  ref_.value = next
}

function toggleAll(side: 'left' | 'right') {
  if (isDisabled.value) return
  if (side === 'left') {
    const next = new Set(leftChecked.value)
    if (leftAllChecked.value) leftSelectable.value.forEach((d) => next.delete(keyOf(d.value)))
    else leftSelectable.value.forEach((d) => next.add(keyOf(d.value)))
    leftChecked.value = next
  } else {
    const next = new Set(rightChecked.value)
    if (rightAllChecked.value) rightSelectable.value.forEach((d) => next.delete(keyOf(d.value)))
    else rightSelectable.value.forEach((d) => next.add(keyOf(d.value)))
    rightChecked.value = next
  }
}

function commit(next: (string | number)[], direction: 'to-right' | 'to-left', moved: (string | number)[]) {
  innerValues.value = next
  emit('update:modelValue', next)
  emit('change', next, { direction, moved })
}

function moveToRight() {
  if (isDisabled.value || !leftCheckedCount.value) return
  const moved = leftList.value.filter((d) => leftChecked.value.has(keyOf(d.value)) && !d.disabled).map((d) => d.value)
  // 顺序跟随原数据，避免先加进来的排到最后
  const next = props.data
    .filter((d) => values.value.some((v) => keyOf(v) === keyOf(d.value)) || moved.some((m) => keyOf(m) === keyOf(d.value)))
    .map((d) => d.value)
  leftChecked.value = new Set()
  commit(next, 'to-right', moved)
}

function moveToLeft() {
  if (isDisabled.value || !rightCheckedCount.value) return
  const moved = rightList.value.filter((d) => rightChecked.value.has(keyOf(d.value)) && !d.disabled).map((d) => d.value)
  const next = values.value.filter((v) => !moved.some((m) => keyOf(m) === keyOf(v)))
  rightChecked.value = new Set()
  commit(next, 'to-left', moved)
}

/** 数据变化后清掉已经不存在或已移走的勾选，避免「看不见的勾选」被一起移动 */
watch(
  [leftList, rightList],
  () => {
    const leftKeys = new Set(leftList.value.map((d) => keyOf(d.value)))
    const rightKeys = new Set(rightList.value.map((d) => keyOf(d.value)))
    const l = new Set([...leftChecked.value].filter((k) => leftKeys.has(k)))
    const r = new Set([...rightChecked.value].filter((k) => rightKeys.has(k)))
    if (l.size !== leftChecked.value.size) leftChecked.value = l
    if (r.size !== rightChecked.value.size) rightChecked.value = r
  },
  { deep: false },
)
</script>

<template>
  <div class="jm-transfer" :class="{ 'is-disabled': isDisabled }">
    <!-- 可选面板 -->
    <section class="jm-transfer__panel" aria-label="可选列表">
      <header class="jm-transfer__head">
        <span class="jm-transfer__title">{{ titles[0] }}</span>
        <span class="jm-transfer__count">{{ leftAll.length }} 项</span>
        <button
          type="button"
          class="jm-transfer__all"
          :disabled="isDisabled || !leftSelectable.length"
          @click="toggleAll('left')"
        >
          <span
            class="jm-transfer__check"
            :class="{
              'is-checked': leftAllChecked,
              'is-indeterminate': leftIndeterminate,
            }"
            aria-hidden="true"
          >
            <jm-icon v-if="leftAllChecked" name="check" size="11px" :stroke-width="3" />
            <i v-else-if="leftIndeterminate" />
          </span>
          <span>全选</span>
        </button>
      </header>

      <div v-if="searchable" class="jm-transfer__search">
        <jm-search v-model="leftKeyword" size="small" placeholder="搜索" :show-cancel="false" />
      </div>

      <ul class="jm-transfer__list" :style="{ height }" role="listbox" aria-multiselectable="true">
        <li
          v-for="item in leftList"
          :key="item.value"
          class="jm-transfer__item"
          :class="{ 'is-checked': leftChecked.has(String(item.value)), 'is-disabled': item.disabled }"
          role="option"
          :aria-selected="leftChecked.has(String(item.value))"
          :aria-disabled="item.disabled || undefined"
          @click="toggle('left', item)"
        >
          <span
            class="jm-transfer__check"
            :class="{ 'is-checked': leftChecked.has(String(item.value)) }"
            role="checkbox"
            :aria-checked="leftChecked.has(String(item.value))"
          >
            <jm-icon
              v-if="leftChecked.has(String(item.value))"
              name="check"
              size="11px"
              :stroke-width="3"
            />
          </span>
          <span class="jm-transfer__text">
            <span class="jm-transfer__label">{{ item.label }}</span>
            <span v-if="item.desc" class="jm-transfer__desc">{{ item.desc }}</span>
          </span>
        </li>
        <li v-if="!leftList.length" class="jm-transfer__empty">
          {{ leftAll.length ? '没有匹配项' : emptyText }}
        </li>
      </ul>
    </section>

    <!-- 操作 -->
    <div class="jm-transfer__actions">
      <span class="jm-transfer__hint">
        已选 {{ values.length }} / {{ data.length }}
      </span>
      <div class="jm-transfer__btns">
        <jm-button
          size="small"
          variant="outline"
          :disabled="isDisabled || !rightCheckedCount"
          @click="moveToLeft"
        >
          <jm-icon name="arrow-up" size="14px" />
          移除{{ rightCheckedCount ? ` ${rightCheckedCount}` : '' }}
        </jm-button>
        <jm-button size="small" :disabled="isDisabled || !leftCheckedCount" @click="moveToRight">
          <jm-icon name="arrow-down" size="14px" />
          添加{{ leftCheckedCount ? ` ${leftCheckedCount}` : '' }}
        </jm-button>
      </div>
    </div>

    <!-- 已选面板 -->
    <section class="jm-transfer__panel" aria-label="已选列表">
      <header class="jm-transfer__head">
        <span class="jm-transfer__title">{{ titles[1] }}</span>
        <span class="jm-transfer__count">{{ rightAll.length }} 项</span>
        <button
          type="button"
          class="jm-transfer__all"
          :disabled="isDisabled || !rightSelectable.length"
          @click="toggleAll('right')"
        >
          <span
            class="jm-transfer__check"
            :class="{
              'is-checked': rightAllChecked,
              'is-indeterminate': rightIndeterminate,
            }"
            aria-hidden="true"
          >
            <jm-icon v-if="rightAllChecked" name="check" size="11px" :stroke-width="3" />
            <i v-else-if="rightIndeterminate" />
          </span>
          <span>全选</span>
        </button>
      </header>

      <div v-if="searchable" class="jm-transfer__search">
        <jm-search v-model="rightKeyword" size="small" placeholder="搜索已选" :show-cancel="false" />
      </div>

      <ul class="jm-transfer__list" :style="{ height }" role="listbox" aria-multiselectable="true">
        <li
          v-for="item in rightList"
          :key="item.value"
          class="jm-transfer__item"
          :class="{ 'is-checked': rightChecked.has(String(item.value)), 'is-disabled': item.disabled }"
          role="option"
          :aria-selected="rightChecked.has(String(item.value))"
          :aria-disabled="item.disabled || undefined"
          @click="toggle('right', item)"
        >
          <span
            class="jm-transfer__check"
            :class="{ 'is-checked': rightChecked.has(String(item.value)) }"
            role="checkbox"
            :aria-checked="rightChecked.has(String(item.value))"
          >
            <jm-icon
              v-if="rightChecked.has(String(item.value))"
              name="check"
              size="11px"
              :stroke-width="3"
            />
          </span>
          <span class="jm-transfer__text">
            <span class="jm-transfer__label">{{ item.label }}</span>
            <span v-if="item.desc" class="jm-transfer__desc">{{ item.desc }}</span>
          </span>
        </li>
        <li v-if="!rightList.length" class="jm-transfer__empty">
          {{ rightKeyword ? '没有匹配项' : '还没有选择' }}
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.jm-transfer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-sizing: border-box;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

.jm-transfer__panel {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
  border: 1px solid var(--jm-border-color);
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-container);
}

.jm-transfer__head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: none;
  padding: 10px 12px;
  border-bottom: 1px solid var(--jm-border-color);
  background: var(--jm-bg-input);
}

.jm-transfer__title {
  flex: none;
  font-weight: var(--jm-font-weight-medium);
}

.jm-transfer__count {
  flex: 1;
  min-width: 0;
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
}

.jm-transfer__all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex: none;
  padding: 4px 6px;
  border: none;
  border-radius: var(--jm-radius-sm);
  background: transparent;
  font-family: inherit;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
  cursor: pointer;
}

.jm-transfer__all:disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-transfer__search {
  flex: none;
  padding: 8px 12px 0;
}

.jm-transfer__list {
  box-sizing: border-box;
  margin: 0;
  padding: 4px 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
  list-style: none;
}

.jm-transfer__item {
  display: flex;
  align-items: center;
  gap: 10px;
  box-sizing: border-box;
  min-height: 44px;
  padding: 8px 12px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-transfer__item:active {
  background: var(--jm-bg-active);
}

.jm-transfer__item.is-checked {
  background: var(--jm-color-primary-light);
}

.jm-transfer__item.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-transfer__check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  box-sizing: border-box;
  width: 20px;
  height: 20px;
  border: 1.5px solid var(--jm-border-color-2);
  border-radius: 50%;
  background: var(--jm-bg-container);
  color: #fff;
  transition:
    background-color 0.16s ease,
    border-color 0.16s ease;
}

.jm-transfer__check.is-checked,
.jm-transfer__check.is-indeterminate {
  border-color: var(--jm-color-primary);
  background: var(--jm-color-primary);
}

.jm-transfer__check i {
  display: block;
  width: 9px;
  height: 2px;
  border-radius: 1px;
  background: #fff;
}

.jm-transfer__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.jm-transfer__label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-transfer__desc {
  overflow: hidden;
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-transfer__empty {
  padding: 28px 0;
  text-align: center;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.jm-transfer__actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 0 2px;
}

.jm-transfer__hint {
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
}

.jm-transfer__btns {
  display: flex;
  gap: 8px;
}

.jm-transfer.is-disabled {
  opacity: 0.6;
}

[data-motion='off'] .jm-transfer__check {
  transition: none;
}
</style>
