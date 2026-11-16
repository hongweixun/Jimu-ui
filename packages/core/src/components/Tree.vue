<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
import JmIcon from './Icon.vue'
import type { TreeCheckInfo, TreeCheckState, TreeNode } from './tree-context'

defineOptions({ name: 'JmTree' })

const props = withDefaults(
  defineProps<{
    /** 树数据 */
    data?: TreeNode[]
    /** 选中节点的值（单选） */
    modelValue?: string | number
    /** 受控展开的节点值集合 */
    expandedValues?: (string | number)[]
    defaultExpandedValues?: (string | number)[]
    defaultExpandAll?: boolean
    /** 展开一个节点时收起同级其他节点 */
    accordion?: boolean
    /** 显示复选框，父子联动 */
    checkable?: boolean
    /** 勾选不与父子联动（各自独立） */
    checkStrictly?: boolean
    /** 受控勾选值集合 */
    checkedValues?: (string | number)[]
    defaultCheckedValues?: (string | number)[]
    selectable?: boolean
    /** 点击整行同时展开 / 收起 */
    expandOnClickNode?: boolean
    /** 每层缩进 */
    indent?: number
    /** 显示层级连接线 */
    showLine?: boolean
    emptyText?: string
    /** 整体禁用 */
    disabled?: boolean
    /** 搜索关键字：只保留命中节点及其祖先，并全部展开 */
    filter?: string
    /** 异步加载子节点，返回的节点会挂到该节点下 */
    loadData?: (node: TreeNode) => Promise<TreeNode[]>
  }>(),
  {
    data: () => [],
    defaultExpandedValues: () => [],
    defaultCheckedValues: () => [],
    selectable: true,
    expandOnClickNode: true,
    indent: 20,
    emptyText: '暂无数据',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  'update:expandedValues': [values: (string | number)[]]
  'update:checkedValues': [values: (string | number)[]]
  'node-click': [node: TreeNode]
  check: [values: (string | number)[], info: TreeCheckInfo]
  expand: [values: (string | number)[], info: { node: TreeNode; expanded: boolean }]
}>()

const keyOf = (node: TreeNode) => String(node.value)

/** 懒加载拿到的子节点，覆盖 node.children */
const extraChildren = reactive(new Map<string, TreeNode[]>())
const loadedKeys = reactive(new Set<string>())
const loadingKeys = reactive(new Set<string>())

const indentPx = computed(() => `${props.indent}px`)

const innerExpanded = ref<Set<string>>(new Set())
const innerChecked = ref<Set<string>>(new Set())

const expandedControlled = computed(() => props.expandedValues !== undefined)
const checkedControlled = computed(() => props.checkedValues !== undefined)

const expandedSet = computed<Set<string>>(() =>
  props.expandedValues ? new Set(props.expandedValues.map(String)) : innerExpanded.value,
)
const checkedSet = computed<Set<string>>(() =>
  props.checkedValues ? new Set(props.checkedValues.map(String)) : innerChecked.value,
)

const selectedKey = computed(() =>
  props.modelValue === undefined || props.modelValue === '' ? '' : String(props.modelValue),
)

function childrenOf(node: TreeNode): TreeNode[] {
  return extraChildren.get(keyOf(node)) ?? node.children ?? []
}

function canLoad(node: TreeNode) {
  return !!props.loadData && !loadedKeys.has(keyOf(node)) && node.isLeaf !== true
}

function hasChildrenOf(node: TreeNode) {
  return childrenOf(node).length > 0 || canLoad(node)
}

/** 值 → 节点 / 父节点，供联动与键盘导航用 */
const nodeIndex = computed(() => {
  const map = new Map<string, { node: TreeNode; parentKey: string | null }>()
  const walk = (nodes: TreeNode[], parentKey: string | null) => {
    nodes.forEach((node) => {
      const key = keyOf(node)
      if (map.has(key)) return
      map.set(key, { node, parentKey })
      walk(childrenOf(node), key)
    })
  }
  walk(props.data, null)
  return map
})

/* ---------------- 搜索过滤 ---------------- */

const keyword = computed(() => (props.filter ?? '').trim())
const isFiltering = computed(() => keyword.value !== '')

/** 命中节点 + 其所有祖先，其余整枝隐藏 */
const matchedKeys = computed<Set<string> | null>(() => {
  const q = keyword.value.toLowerCase()
  if (!q) return null
  const keep = new Set<string>()
  const walk = (nodes: TreeNode[]): boolean => {
    let hit = false
    nodes.forEach((node) => {
      const childHit = walk(childrenOf(node))
      const selfHit = String(node.label).toLowerCase().includes(q)
      if (selfHit || childHit) {
        keep.add(keyOf(node))
        hit = true
      }
    })
    return hit
  }
  walk(props.data)
  return keep
})

interface FlatNode {
  key: string
  node: TreeNode
  level: number
  parentKey: string | null
  hasChildren: boolean
  expanded: boolean
  loading: boolean
  disabled: boolean
  isLast: boolean
  state: TreeCheckState
}

const flatNodes = computed<FlatNode[]>(() => {
  const out: FlatNode[] = []
  const keep = matchedKeys.value
  const filtering = isFiltering.value
  const walk = (nodes: TreeNode[], level: number, parentKey: string | null) => {
    nodes.forEach((node, i) => {
      const key = keyOf(node)
      if (keep && !keep.has(key)) return
      const kids = childrenOf(node)
      const open = filtering ? true : expandedSet.value.has(key)
      out.push({
        key,
        node,
        level,
        parentKey,
        hasChildren: kids.length > 0 || canLoad(node),
        expanded: open,
        loading: loadingKeys.has(key),
        disabled: !!node.disabled || props.disabled,
        isLast: i === nodes.length - 1,
        state: stateWith(node, checkedSet.value),
      })
      if (open && kids.length) walk(kids, level + 1, key)
    })
  }
  walk(props.data, 0, null)
  return out
})

/* ---------------- 勾选状态 ---------------- */

function stateWith(node: TreeNode, set: Set<string>): TreeCheckState {
  const key = keyOf(node)
  if (props.checkStrictly) return set.has(key) ? 'checked' : 'unchecked'
  const kids = childrenOf(node)
  if (!kids.length) return set.has(key) ? 'checked' : 'unchecked'
  const states = kids.map((k) => stateWith(k, set))
  if (states.every((s) => s === 'checked')) return 'checked'
  if (states.some((s) => s !== 'unchecked')) return 'indeterminate'
  return 'unchecked'
}

function valuesFromSet(set: Set<string>) {
  const out: (string | number)[] = []
  nodeIndex.value.forEach((entry, key) => {
    if (set.has(key) && stateWith(entry.node, set) === 'checked') out.push(entry.node.value)
  })
  return out
}

function halfValuesFromSet(set: Set<string>) {
  const out: (string | number)[] = []
  nodeIndex.value.forEach((entry, key) => {
    if (stateWith(entry.node, set) === 'indeterminate') out.push(entry.node.value)
  })
  return out
}

/** 把一棵子树整体选中 / 取消（跳过禁用节点） */
function applySubtree(node: TreeNode, checked: boolean, set: Set<string>) {
  const key = keyOf(node)
  if (node.disabled && !props.disabled) return
  if (checked) set.add(key)
  else set.delete(key)
  childrenOf(node).forEach((child) => applySubtree(child, checked, set))
}

/** 自底向上把父节点状态对齐子节点（DFS 倒序即后序） */
function reconcile(set: Set<string>) {
  const entries = [...nodeIndex.value.entries()].reverse()
  entries.forEach(([key, entry]) => {
    const kids = childrenOf(entry.node)
    if (!kids.length) return
    const all = kids.every((k) => stateWith(k, set) === 'checked')
    if (all) set.add(key)
    else set.delete(key)
  })
}

function commitChecked(set: Set<string>) {
  if (!checkedControlled.value) innerChecked.value = set
  emit('update:checkedValues', valuesFromSet(set))
}

function toggleCheck(node: TreeNode) {
  if (props.disabled || node.disabled) return
  const set = new Set(checkedSet.value)
  const next = stateWith(node, set) !== 'checked'
  applySubtree(node, next, set)
  if (!props.checkStrictly) reconcile(set)
  commitChecked(set)
  emit('check', valuesFromSet(set), {
    node,
    checked: next,
    halfCheckedValues: halfValuesFromSet(set),
  })
}

/* ---------------- 展开 ---------------- */

function commitExpanded(set: Set<string>) {
  if (!expandedControlled.value) innerExpanded.value = set
  emit('update:expandedValues', [...set].map((k) => nodeIndex.value.get(k)?.node.value ?? k))
}

function siblingsOf(key: string): TreeNode[] {
  const entry = nodeIndex.value.get(key)
  if (!entry) return props.data
  if (!entry.parentKey) return props.data
  const parent = nodeIndex.value.get(entry.parentKey)
  return parent ? childrenOf(parent.node) : props.data
}

async function toggleExpand(node: TreeNode) {
  const key = keyOf(node)
  const open = expandedSet.value.has(key)
  if (open) {
    const next = new Set(expandedSet.value)
    next.delete(key)
    commitExpanded(next)
    emit('expand', [...next].map((k) => nodeIndex.value.get(k)?.node.value ?? k), {
      node,
      expanded: false,
    })
    return
  }
  if (!hasChildrenOf(node)) return

  if (childrenOf(node).length === 0 && canLoad(node)) {
    if (loadingKeys.has(key)) return
    loadingKeys.add(key)
    try {
      const kids = (await props.loadData?.(node)) ?? []
      extraChildren.set(key, kids)
      loadedKeys.add(key)
    } finally {
      loadingKeys.delete(key)
    }
  }

  const next = new Set(expandedSet.value)
  if (props.accordion) {
    siblingsOf(key).forEach((sibling) => {
      if (keyOf(sibling) !== key) next.delete(keyOf(sibling))
    })
  }
  next.add(key)
  commitExpanded(next)
  emit('expand', [...next].map((k) => nodeIndex.value.get(k)?.node.value ?? k), {
    node,
    expanded: true,
  })
}

/* ---------------- 选中与点击 ---------------- */

function selectNode(node: TreeNode) {
  if (props.disabled || node.disabled || !props.selectable) return
  emit('update:modelValue', node.value)
  emit('node-click', node)
}

function onNodeClick(item: FlatNode, event: MouseEvent) {
  if (item.disabled) return
  activeKey.value = item.key
  selectNode(item.node)
  if (item.hasChildren && props.expandOnClickNode) {
    event.preventDefault()
    toggleExpand(item.node)
  }
}

function onArrowClick(item: FlatNode) {
  if (item.disabled) return
  toggleExpand(item.node)
}

function onCheckClick(item: FlatNode) {
  if (item.disabled) return
  toggleCheck(item.node)
}

/* ---------------- 键盘导航 ---------------- */

const activeKey = ref('')
const nodeRefs = new Map<string, HTMLElement>()

function setNodeRef(el: unknown, key: string) {
  if (el) nodeRefs.set(key, el as HTMLElement)
  else nodeRefs.delete(key)
}

function focusAt(index: number) {
  const list = flatNodes.value
  if (!list.length) return
  const next = list[Math.min(Math.max(0, index), list.length - 1)]
  if (!next) return
  activeKey.value = next.key
  nextTick(() => nodeRefs.get(next.key)?.focus())
}

function onNodeKeydown(e: KeyboardEvent, item: FlatNode) {
  const list = flatNodes.value
  const index = list.findIndex((n) => n.key === item.key)
  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      focusAt(index + 1)
      break
    case 'ArrowUp':
      e.preventDefault()
      focusAt(index - 1)
      break
    case 'ArrowRight':
      e.preventDefault()
      if (item.hasChildren && !item.expanded) toggleExpand(item.node)
      else if (item.hasChildren) focusAt(index + 1)
      break
    case 'ArrowLeft':
      e.preventDefault()
      if (item.hasChildren && item.expanded) toggleExpand(item.node)
      else if (item.parentKey) focusAt(list.findIndex((n) => n.key === item.parentKey))
      break
    case 'Home':
      e.preventDefault()
      focusAt(0)
      break
    case 'End':
      e.preventDefault()
      focusAt(list.length - 1)
      break
    case 'Enter':
    case ' ':
      e.preventDefault()
      if (props.checkable) toggleCheck(item.node)
      else selectNode(item.node)
      break
    default:
      break
  }
}

/* ---------------- 初始化 ---------------- */

function collectAllKeys(nodes: TreeNode[], out: string[] = []) {
  nodes.forEach((node) => {
    out.push(keyOf(node))
    collectAllKeys(childrenOf(node), out)
  })
  return out
}

function setCheckedValues(values: (string | number)[]) {
  const set = new Set<string>()
  values.forEach((value) => {
    const entry = nodeIndex.value.get(String(value))
    if (entry) applySubtree(entry.node, true, set)
  })
  if (!props.checkStrictly) reconcile(set)
  commitChecked(set)
}

function expandAll() {
  commitExpanded(new Set(collectAllKeys(props.data)))
}

function collapseAll() {
  commitExpanded(new Set())
}

defineExpose({
  expandAll,
  collapseAll,
  setCheckedValues,
  getCheckedValues: () => valuesFromSet(checkedSet.value),
  getHalfCheckedValues: () => halfValuesFromSet(checkedSet.value),
  toggleExpand,
})

/** 初始展开状态 */
function initExpanded() {
  if (expandedControlled.value) return
  if (props.defaultExpandAll) {
    innerExpanded.value = new Set(collectAllKeys(props.data))
    return
  }
  innerExpanded.value = new Set(props.defaultExpandedValues.map(String))
}

/** 外部传入的勾选值要向下补全整棵子树（父被选中＝子全部选中） */
function initChecked() {
  const seed = props.checkedValues ?? props.defaultCheckedValues
  if (!seed.length) return
  const set = new Set<string>()
  seed.forEach((value) => {
    const entry = nodeIndex.value.get(String(value))
    if (entry) applySubtree(entry.node, true, set)
  })
  if (!props.checkStrictly) reconcile(set)
  if (!checkedControlled.value) innerChecked.value = set
  else emit('update:checkedValues', valuesFromSet(set))
}

initExpanded()
initChecked()

watch(() => props.data, () => {
  loadedKeys.clear()
  extraChildren.clear()
  initExpanded()
  if (!checkedControlled.value) initChecked()
})

watch(flatNodes, (list) => {
  if (!list.length) {
    activeKey.value = ''
    return
  }
  if (!list.some((n) => n.key === activeKey.value)) activeKey.value = list[0].key
}, { immediate: true })

/** 过滤时高亮命中片段 */
function labelParts(label: string) {
  const q = keyword.value
  if (!q) return [{ text: label, hit: false }]
  const lower = label.toLowerCase()
  const needle = q.toLowerCase()
  const parts: { text: string; hit: boolean }[] = []
  let from = 0
  let at = lower.indexOf(needle)
  while (at >= 0) {
    if (at > from) parts.push({ text: label.slice(from, at), hit: false })
    parts.push({ text: label.slice(at, at + needle.length), hit: true })
    from = at + needle.length
    at = lower.indexOf(needle, from)
  }
  if (from < label.length) parts.push({ text: label.slice(from), hit: false })
  return parts.length ? parts : [{ text: label, hit: false }]
}
</script>

<template>
  <div
    class="jm-tree"
    :class="{ 'is-line': showLine, 'is-disabled': disabled }"
    role="tree"
    :aria-multiselectable="checkable || undefined"
  >
    <div
      v-for="item in flatNodes"
      :key="item.key"
      :ref="(el) => setNodeRef(el, item.key)"
      class="jm-tree__node"
      :class="{
        'is-selected': item.key === selectedKey,
        'is-expanded': item.expanded,
        'is-disabled': item.disabled,
        'is-leaf': !item.hasChildren,
      }"
      role="treeitem"
      :aria-level="item.level + 1"
      :aria-expanded="item.hasChildren ? item.expanded : undefined"
      :aria-selected="item.key === selectedKey"
      :aria-disabled="item.disabled || undefined"
      :tabindex="item.key === activeKey ? 0 : -1"
      @click="onNodeClick(item, $event)"
      @keydown="onNodeKeydown($event, item)"
      @focus="activeKey = item.key"
    >
      <span class="jm-tree__indents" aria-hidden="true">
        <i
          v-for="n in item.level"
          :key="n"
          :class="{ 'is-last': n === item.level && item.isLast }"
        />
      </span>

      <span
        class="jm-tree__arrow"
        :class="{ 'is-open': item.expanded, 'is-loading': item.loading }"
        aria-hidden="true"
        @click.stop="onArrowClick(item)"
      >
        <jm-icon
          v-if="item.loading"
          name="loading"
          size="14px"
          class="jm-tree__spin"
        />
        <jm-icon
          v-else-if="item.hasChildren"
          name="chevron-right"
          size="14px"
          :stroke-width="2"
        />
      </span>

      <span
        v-if="checkable"
        class="jm-tree__check"
        :class="`is-${item.state}`"
        role="checkbox"
        :aria-checked="item.state === 'indeterminate' ? 'mixed' : item.state === 'checked'"
        :aria-disabled="item.disabled || undefined"
        @click.stop="onCheckClick(item)"
      >
        <jm-icon
          v-if="item.state === 'checked'"
          name="check"
          size="12px"
          :stroke-width="3"
        />
        <i v-else-if="item.state === 'indeterminate'" class="jm-tree__minus" />
      </span>

      <span v-if="item.node.icon" class="jm-tree__icon" aria-hidden="true">
        <jm-icon :name="item.node.icon" size="16px" />
      </span>

      <span class="jm-tree__label">
        <template v-for="(part, i) in labelParts(item.node.label)" :key="i">
          <mark v-if="part.hit" class="jm-tree__hit">{{ part.text }}</mark>
          <template v-else>{{ part.text }}</template>
        </template>
      </span>

      <span v-if="item.node.extra" class="jm-tree__extra">{{ item.node.extra }}</span>

      <span v-if="$slots.default" class="jm-tree__suffix">
        <slot :node="item.node" :level="item.level" :expanded="item.expanded" />
      </span>
    </div>

    <div v-if="!flatNodes.length" class="jm-tree__empty">
      <slot name="empty">{{ emptyText }}</slot>
    </div>
  </div>
</template>

<style scoped>
.jm-tree {
  --jm-tree-row-height: 44px;
  --jm-tree-indent: v-bind(indentPx);
  box-sizing: border-box;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  -webkit-tap-highlight-color: transparent;
}

.jm-tree__node {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  box-sizing: border-box;
  min-height: var(--jm-tree-row-height);
  padding-right: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.16s ease;
}

.jm-tree__node:hover {
  background: var(--jm-bg-hover);
}

.jm-tree__node:focus-visible {
  outline: var(--jm-focus-ring-width, 2px) solid var(--jm-focus-ring-color, #00a0e9);
  outline-offset: -2px;
}

.jm-tree__node.is-selected {
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary-text);
  font-weight: var(--jm-font-weight-medium);
}

.jm-tree__node.is-disabled {
  color: var(--jm-text-color-4);
  cursor: not-allowed;
}

.jm-tree__node.is-disabled:hover {
  background: transparent;
}

/* 缩进占位与连接线 */
.jm-tree__indents {
  display: flex;
  align-self: stretch;
  flex: none;
}

.jm-tree__indents i {
  position: relative;
  display: block;
  width: var(--jm-tree-indent);
  flex: none;
}

.is-line .jm-tree__indents i::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  border-left: 1px solid var(--jm-border-color);
}

.is-line .jm-tree__indents i.is-last::before {
  bottom: 50%;
}

.is-line .jm-tree__indents i.is-last::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50%;
  border-top: 1px solid var(--jm-border-color);
}

.jm-tree__arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  width: 18px;
  height: 24px;
  color: var(--jm-text-color-3);
  transition: transform 0.2s ease;
}

.jm-tree__arrow.is-open {
  transform: rotate(90deg);
}

.jm-tree__spin {
  animation: jm-tree-spin 0.9s linear infinite;
}

@keyframes jm-tree-spin {
  to {
    transform: rotate(360deg);
  }
}

.jm-tree__check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  box-sizing: border-box;
  width: 20px;
  height: 20px;
  margin-right: 2px;
  border: 1.5px solid var(--jm-border-color-2);
  border-radius: 5px;
  background: var(--jm-bg-container);
  color: #fff;
  transition:
    background-color 0.16s ease,
    border-color 0.16s ease;
}

.jm-tree__check.is-checked,
.jm-tree__check.is-indeterminate {
  border-color: var(--jm-color-primary);
  background: var(--jm-color-primary);
}

.jm-tree__minus {
  display: block;
  width: 10px;
  height: 2px;
  border-radius: 1px;
  background: #fff;
}

.jm-tree__icon {
  display: inline-flex;
  flex: none;
  color: var(--jm-color-primary);
}

.jm-tree__label {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.jm-tree__hit {
  background: none;
  color: var(--jm-color-danger);
  font-weight: var(--jm-font-weight-medium);
}

.jm-tree__extra {
  flex: none;
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
}

.jm-tree__suffix {
  flex: none;
  display: inline-flex;
  align-items: center;
}

.jm-tree__empty {
  padding: 32px 0;
  text-align: center;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.jm-tree__node.is-disabled .jm-tree__check {
  opacity: 0.5;
}

[data-motion='off'] .jm-tree__arrow,
[data-motion='off'] .jm-tree__node {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-tree__arrow,
  .jm-tree__node {
    transition: none;
  }

  .jm-tree__spin {
    animation-duration: 2s;
  }
}
</style>
