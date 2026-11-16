---
title: TreeSelect 树选择器
description: 层级数据的选择器：输入框式触发器 + 弹层内的树，显示完整路径、支持搜索与清空。
---

# TreeSelect 树选择器

选分类、选知识点、选部门——数据是层级的，但界面上只能放一个输入框。TreeSelect 把 Tree 塞进底部弹层，触发器上显示从根到叶子的完整路径，选完立刻回填。

## 基础用法

<DemoBlock src="/demos/tree-select/basic.vue" title="知识点选择：触发器显示完整路径" desc="触发器显示「数学 / 函数 / 二次函数」这样的路径，比只显示叶子名更容易确认选中的是哪一层。弹层打开时自动展开到已选项。" />

```vue
<jm-tree-select
  v-model="value"
  :data="data"
  label="知识点"
  title="选择知识点"
/>
```

弹层里的树是完整的 Tree：点整行选中，有子节点时同时展开；选中后弹层自动关闭（`close-on-select` 可关）。

## 搜索与清空

弹层顶部默认带搜索框，输入关键字时只保留命中节点及其祖先，命中片段标红。

```vue
<jm-tree-select v-model="value" :data="data" searchable :clearable="true" />
```

- `searchable` 默认开。数据量小、层级浅时可以关掉，弹层会更紧凑。
- `clearable` 在触发器右侧显示清除按钮，点它把值置为空字符串并触发一次 `change`。
- `expand-all` 让弹层一打开就展开全部节点，适合「总共就两三层」的轻量场景。

## 禁用与只读

```vue
<jm-tree-select :data="data" model-value="english-1" disabled label="已锁定" />
```

`disabled` 会在触发器上盖一层半透明遮罩并且不可点击；`readonly` 保留正常外观，只是不展开弹层（适合「展示但不可改」的详情页）。在 `JmForm` 里整表禁用时，TreeSelect 会自动继承。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| data | 树数据，同 Tree | `TreeNode[]` | `[]` |
| model-value / v-model | 选中的节点值 | `string \| number` | — |
| label | 触发器左侧文案 | `string` | — |
| placeholder | 未选中时的占位文案 | `string` | `请选择` |
| title | 弹层标题 | `string` | `请选择` |
| separator | 路径分隔符 | `string` | ` / ` |
| clearable | 显示清除按钮 | `boolean` | `true` |
| searchable | 弹层内显示搜索框 | `boolean` | `true` |
| close-on-select | 选中后关闭弹层 | `boolean` | `true` |
| expand-all | 打开时展开全部节点 | `boolean` | `false` |
| height | 弹层高度 | `string` | `62vh` |
| disabled | 禁用 | `boolean` | `false` |
| readonly | 只读（不展开） | `boolean` | `false` |
| teleport | 弹层挂载位置 | `boolean \| string \| Element` | `true` |
| z-index | 弹层层级 | `number` | — |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:model-value | 选中变化 | `value` |
| change | 选中变化（清除也会触发，`node` 为 `null`） | `(value, node)` |
| open / close | 弹层打开 / 关闭 | — |

### Methods

| 方法 | 说明 |
| --- | --- |
| open() | 打开弹层 |
| close() | 关闭弹层 |

## 和 Tree 怎么选

| 场景 | 用哪个 |
| --- | --- |
| 页面里直接铺开的一棵树（目录、章节列表） | Tree |
| 表单里一格位置，需要收起 / 展开 | TreeSelect |
| 需要多选、需要看到半选状态 | Tree（`checkable`）+ 自己包一层弹层 |
| 只需要选一层，但数据是树 | CascadePicker |

TreeSelect 目前只做单选。要选多个节点时用 Tree 的 `checkable` 放进 Popup，触发器和 TreeSelect 长得一样，区别只是回填 `array`。
