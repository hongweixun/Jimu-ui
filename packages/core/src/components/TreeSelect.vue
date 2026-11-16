<script setup lang="ts">
import { computed, inject, ref, watch } from 'vue'
import JmIcon from './Icon.vue'
import JmPopup from './Popup.vue'
import JmSearch from './Search.vue'
import JmTree from './Tree.vue'
import { FORM_KEY } from './form-context'
import type { TreeNode } from './tree-context'

defineOptions({ name: 'JmTreeSelect' })

const props = withDefaults(
  defineProps<{
    /** 树数据 */
    data?: TreeNode[]
    /** 选中的节点值 */
    modelValue?: string | number
    /** 触发器左侧文案 */
    label?: string
    /** 未选中时的占位文案 */
    placeholder?: string
    /** 弹层标题 */
    title?: string
    /** 路径分隔符 */
    separator?: string
    /** 可清空 */
    clearable?: boolean
    /** 弹层内搜索 */
    searchable?: boolean
    /** 选中后自动关闭 */
    closeOnSelect?: boolean
    disabled?: boolean
    readonly?: boolean
    /** 展开全部节点（默认只展开到已选项） */
    expandAll?: boolean
    /** 弹层高度 */
    height?: string
    teleport?: boolean | string | Element
    zIndex?: number
  }>(),
  {
    data: () => [],
    placeholder: '请选择',
    title: '请选择',
    separator: ' / ',
    clearable: true,
    searchable: true,
    closeOnSelect: true,
    height: '62vh',
    teleport: true,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  change: [value: string | number, node: TreeNode | null]
  open: []
  close: []
}>()

const form = inject(FORM_KEY, null)
const isDisabled = computed(() => props.disabled || !!form?.disabled.value)
const isReadonly = computed(() => props.readonly)

const show = ref(false)
const keyword = ref('')
const panelExpanded = ref<(string | number)[]>([])

/** 从根到选中节点的完整路径，用来显示「第一章 / 1.2 节」并展开祖先 */
const selectedPath = computed<TreeNode[]>(() => {
  const target = props.modelValue
  if (target === undefined || target === '') return []
  const path: TreeNode[] = []
  const walk = (nodes: TreeNode[], trail: TreeNode[]): boolean => {
    for (const node of nodes) {
      const next = [...trail, node]
      if (String(node.value) === String(target)) {
        path.push(...next)
        return true
      }
      if (node.children && walk(node.children, next)) return true
    }
    return false
  }
  walk(props.data, [])
  return path
})

const valueText = computed(() => selectedPath.value.map((n) => n.label).join(props.separator))
const hasValue = computed(() => selectedPath.value.length > 0)

function openPanel() {
  if (isDisabled.value || isReadonly.value) return
  keyword.value = ''
  panelExpanded.value = props.expandAll
    ? []
    : selectedPath.value.slice(0, -1).map((n) => n.value)
  show.value = true
  emit('open')
}

function closePanel() {
  show.value = false
  keyword.value = ''
  emit('close')
}

/** Popup 只会向外抛 false（点遮罩 / 关闭按钮），打开一律走 openPanel */
function onShowChange(v: boolean) {
  if (!v) closePanel()
}

function onNodeClick(node: TreeNode) {
  emit('update:modelValue', node.value)
  emit('change', node.value, node)
  if (props.closeOnSelect) closePanel()
}

function clear(e: MouseEvent) {
  e.stopPropagation()
  if (isDisabled.value || isReadonly.value) return
  emit('update:modelValue', '')
  emit('change', '', null)
}

/** 搜索时把命中路径全部展开，清空后回到「只展开已选路径」 */
watch(keyword, (v) => {
  if (v) return
  panelExpanded.value = props.expandAll ? [] : selectedPath.value.slice(0, -1).map((n) => n.value)
})

watch(
  () => props.modelValue,
  () => {
    if (show.value && !props.expandAll) {
      panelExpanded.value = selectedPath.value.slice(0, -1).map((n) => n.value)
    }
  },
)

defineExpose({ open: openPanel, close: closePanel })
</script>

<template>
  <div class="jm-tree-select" :class="{ 'is-disabled': isDisabled }">
    <button
      type="button"
      class="jm-tree-select__trigger"
      role="combobox"
      aria-haspopup="tree"
      :aria-expanded="show"
      :disabled="isDisabled"
      @click="openPanel"
    >
      <span v-if="label" class="jm-tree-select__label">{{ label }}</span>
      <span class="jm-tree-select__value" :class="{ 'is-placeholder': !hasValue }">
        {{ hasValue ? valueText : placeholder }}
      </span>
      <span
        v-if="clearable && hasValue && !isDisabled"
        class="jm-tree-select__clear"
        role="button"
        tabindex="-1"
        aria-label="清除选择"
        @click="clear"
      >
        <jm-icon name="close-circle" size="16px" />
      </span>
      <jm-icon v-else class="jm-tree-select__arrow" name="chevron-right" size="16px" />

      <span v-if="isReadonly" class="jm-tree-select__mask" aria-hidden="true" />
    </button>

    <jm-popup
      :show="show"
      position="bottom"
      round
      :teleport="teleport"
      :z-index="zIndex"
      @update:show="onShowChange"
    >
      <div class="jm-tree-select__panel" :style="{ height }">
        <div class="jm-tree-select__header">
          <span class="jm-tree-select__title">{{ title }}</span>
          <button type="button" class="jm-tree-select__close" aria-label="关闭" @click="closePanel">
            <jm-icon name="close" size="18px" />
          </button>
        </div>

        <div v-if="searchable" class="jm-tree-select__search">
          <jm-search
            v-model="keyword"
            size="small"
            placeholder="搜索节点"
            :show-cancel="false"
          />
        </div>

        <div class="jm-tree-select__body">
          <jm-tree
            :data="data"
            :model-value="modelValue"
            :expanded-values="panelExpanded"
            :filter="keyword"
            show-line
            empty-text="没有匹配的节点"
            @update:expanded-values="panelExpanded = $event"
            @node-click="onNodeClick"
          />
        </div>
      </div>
    </jm-popup>
  </div>
</template>

<style scoped>
.jm-tree-select {
  box-sizing: border-box;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

.jm-tree-select__trigger {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
  width: 100%;
  min-height: 48px;
  padding: 10px 14px;
  border: 1px solid var(--jm-border-color);
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-container);
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  text-align: left;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-tree-select__trigger:active {
  background: var(--jm-bg-active);
}

.jm-tree-select__label {
  flex: none;
  color: var(--jm-text-color-2);
}

.jm-tree-select__value {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-tree-select__value.is-placeholder {
  color: var(--jm-text-color-4);
}

.jm-tree-select__clear {
  display: inline-flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  color: var(--jm-text-color-4);
}

.jm-tree-select__arrow {
  flex: none;
  color: var(--jm-text-color-4);
  opacity: 0.7;
}

.jm-tree-select__mask {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: var(--jm-bg-container);
  opacity: 0.35;
}

.jm-tree-select.is-disabled .jm-tree-select__trigger {
  color: var(--jm-text-color-4);
  background: var(--jm-bg-disabled);
  cursor: not-allowed;
}

.jm-tree-select__panel {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  min-height: 240px;
  padding-bottom: var(--jm-safe-bottom);
  background: var(--jm-bg-elevated);
}

.jm-tree-select__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: none;
  padding: 14px 16px 8px;
}

.jm-tree-select__title {
  font-size: var(--jm-font-size-lg);
  font-weight: var(--jm-font-weight-medium);
}

.jm-tree-select__close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: var(--jm-radius-round);
  background: transparent;
  color: var(--jm-text-color-3);
  cursor: pointer;
}

.jm-tree-select__search {
  flex: none;
  padding: 0 16px 8px;
}

.jm-tree-select__body {
  flex: 1;
  min-height: 0;
  padding: 0 12px 12px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

.jm-tree-select__trigger:focus-visible {
  outline: var(--jm-focus-ring-width, 2px) solid var(--jm-focus-ring-color, #00a0e9);
  outline-offset: var(--jm-focus-ring-offset, 2px);
}
</style>
