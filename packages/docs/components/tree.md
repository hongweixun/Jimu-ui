---
title: Tree 树形控件
description: 多层级数据的展开与选择，支持复选框父子联动、懒加载、搜索高亮与键盘操作。
---

# Tree 树形控件

课件目录、知识点树、组织架构……都是「一层套一层」的数据。Tree 把展开状态、缩进层级、勾选联动、键盘导航都接住了，只留一份 `data` 给你。

## 基础用法

<DemoBlock src="/demos/tree/basic.vue" title="课程目录：选中高亮 + 层级连接线" desc="data 是嵌套结构，label 显示文案、value 是唯一值；extra 放在行尾显示时长、题数这类补充信息。点整行选中并展开，点箭头只展开。" />

```vue
<jm-tree
  v-model="selected"
  v-model:expanded-values="expanded"
  :data="tree"
  show-line
  @node-click="onNodeClick"
/>
```

`show-line` 会画出层级连接线，树的层级越深越容易看清从属关系；不需要就关掉，只留纯缩进。

## 复选与父子联动

`checkable` 打开复选框。默认父子联动：勾上父节点等于勾上整棵子树，子节点只勾一部分时父节点显示半选。

<DemoBlock src="/demos/tree/checkable.vue" title="知识点勾选：父节点全选由子节点决定" desc="勾选结果通过 check 事件或 v-model:checked-values 拿到；info.halfCheckedValues 是当前所有半选节点，用来做「已选 N 项」之外的提示。" />

```vue
<jm-tree
  :data="tree"
  checkable
  :checked-values="checked"
  @check="(values, info) => { checked = values; half = info.halfCheckedValues }"
/>
```

联动规则值得记一下：

- **父节点状态是算出来的**，不靠外部维护。子节点全部选中 → 父节点全选；部分选中 → 父节点半选；全不选 → 未选。
- **禁用的子节点不参与联动**，点父节点不会把禁用的子项一起勾上。
- `check-strictly` 关掉联动，父子各自独立，适合「权限分配」这类必须逐项确认的场景。

## 异步加载

课程目录动辄几百节，一次拿全量不现实。传 `load-data` 后在展开时才请求子节点，加载期间箭头位置显示转圈。

<DemoBlock src="/demos/tree/lazy.vue" title="展开才加载：0.8 秒模拟一次请求" desc="返回的数组会挂到该节点下；同一个节点只会请求一次，收起再展开走缓存。根节点标 isLeaf 可以省掉「请求完发现是空的」。" />

```vue
<jm-tree :data="tree" :load-data="loadData" :filter="keyword" show-line />

<script setup lang="ts">
async function loadData(node: TreeNode) {
  const res = await fetch(`/api/chapters?parent=${node.value}`)
  return (await res.json()).map((c) => ({ label: c.title, value: c.id }))
}
</script>
```

注意：搜索只作用于**已经加载**的数据。懒加载 + 全量搜索需要服务端配合，前端搜不到还没请求过的节点。

## 搜索过滤

传 `filter` 关键字后，只保留命中的节点及其祖先，命中片段用红色标出，且自动展开整条路径。

<DemoBlock src="/demos/tree/lazy.vue" title="搜索已加载节点：命中路径自动展开" desc="同一个 demo：在搜索框输入「插槽」或「环境」，树会裁掉不相关的分支。清空关键字后回到原来的展开状态。" />

## 键盘操作

树是 `role="tree"`，每个节点是 `role="treeitem"`，整棵树只占一个 Tab 停靠点。

| 按键 | 行为 |
| --- | --- |
| `↓` / `↑` | 上下移动焦点 |
| `→` | 收起时展开当前节点，已展开则进入第一个子节点 |
| `←` | 展开时收起当前节点，已收起则回到父节点 |
| `Home` / `End` | 第一个 / 最后一个可见节点 |
| `Enter` | 选中（`checkable` 时为勾选） |
| `Space` | 同 `Enter` |

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| data | 树数据 | `TreeNode[]` | `[]` |
| model-value / v-model | 选中节点的值 | `string \| number` | — |
| expanded-values / v-model:expanded-values | 受控的展开值集合 | `(string \| number)[]` | — |
| default-expanded-values | 初始展开的节点 | `(string \| number)[]` | `[]` |
| default-expand-all | 初始展开全部 | `boolean` | `false` |
| accordion | 展开一个节点时收起同级其他节点 | `boolean` | `false` |
| checkable | 显示复选框 | `boolean` | `false` |
| check-strictly | 勾选不与父子联动 | `boolean` | `false` |
| checked-values / v-model:checked-values | 受控的勾选值集合 | `(string \| number)[]` | — |
| default-checked-values | 初始勾选的节点 | `(string \| number)[]` | `[]` |
| selectable | 节点可选中 | `boolean` | `true` |
| expand-on-click-node | 点整行同时展开 / 收起 | `boolean` | `true` |
| indent | 每层缩进（px） | `number` | `20` |
| show-line | 显示层级连接线 | `boolean` | `false` |
| empty-text | 空数据文案 | `string` | `暂无数据` |
| disabled | 整体禁用 | `boolean` | `false` |
| filter | 搜索关键字 | `string` | — |
| load-data | 异步加载子节点 | `(node: TreeNode) => Promise<TreeNode[]>` | — |

### TreeNode

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| label | 显示文案 | `string` |
| value | 唯一值 | `string \| number` |
| children | 子节点 | `TreeNode[]` |
| disabled | 该节点禁用 | `boolean` |
| extra | 行尾补充信息 | `string` |
| icon | 节点前图标（内置图标名） | `string` |
| isLeaf | 标记叶子节点，跳过异步加载 | `boolean` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:model-value | 选中变化 | `value` |
| node-click | 点击节点 | `node` |
| check | 勾选变化 | `(values, info)`，`info` 含 `node` / `checked` / `halfCheckedValues` |
| expand | 展开变化 | `(values, info)`，`info` 含 `node` / `expanded` |
| update:expanded-values | 展开集合变化 | `values` |
| update:checked-values | 勾选集合变化 | `values` |

### Methods

通过 ref 调用：

| 方法 | 说明 |
| --- | --- |
| expandAll() | 展开全部 |
| collapseAll() | 收起全部 |
| setCheckedValues(values) | 设置勾选（父节点会自动补全子树） |
| getCheckedValues() | 读取所有全选节点 |
| getHalfCheckedValues() | 读取所有半选节点 |
| toggleExpand(node) | 切换某个节点的展开状态 |

### Slots

| 插槽 | 说明 | 作用域 |
| --- | --- | --- |
| default | 节点右侧追加内容（徽标、操作按钮） | `{ node, level, expanded }` |
| empty | 空数据 | — |

## 使用建议

- **勾选状态别自己算**。父节点是否全选由子节点推导，只要维护 `checked-values` 里的叶子值就行；传父节点的值进来，Tree 会自动补全整棵子树。
- **层级很深时限制缩进**。`indent` 保持 20px 左右，超过 4 层建议直接改成搜索 + 平铺列表，手机屏幕横着走不下。
- **懒加载的节点也要能搜索**：给根节点标 `isLeaf: false` 保证箭头出现；需要全量搜索时把关键字交给后端，用返回的命中路径重建一份临时树。
