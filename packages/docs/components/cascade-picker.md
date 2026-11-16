---
title: CascadePicker 级联选择
description: 省市区这类多级联动选择，选上层自动重建下层。
---

# CascadePicker 级联选择

`Picker` 的联动版：选项是一棵树，选完省之后，市、区两列**按新数据重建**。相比自己维护 `columns`，它把「改上层 → 下层回到第一项」这条规则固化了下来。

## 基础用法

<DemoBlock src="/demos/cascade-picker/basic.vue" title="省市区三级联动" desc="options 是嵌套结构，children 即下一级；v-model 是各级的值数组，长度即已选层级。" />

## 联动的语义

- 改动第 N 级 → 只保留前 N 级的选择，第 N+1 级回到第一项；
- `v-model` 传入的路径会按值逐级匹配，匹配不到的那一级停止，后面的值被丢弃；
- 叶子节点没有 `children`，列数就到此为止，所以一棵树里不同分支的深度可以不一样（两级、三级混用）。

::: tip 数据量大时按需加载
如果下一级要请求接口，先只传当前能拿到的层级，在 `@change` 里拿到新路径后请求子级，再把带 `children` 的 `options` 传回来——组件监听 `options` 变化并重新按路径定位。
:::

## 与 Picker 的关系

CascadePicker 内部就是 `Picker`：列、滚轮、吸附、禁用项跳过全部复用，只是 `columns` 由数据树 + 当前路径算出来。因此工具栏插槽暂未透出；需要自定义确认按钮时直接用 `Picker` 自行组装。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 各级选中的值 | `(string \| number)[]` | — |
| options | 级联数据树 | `CascadeOption[]` | `[]` |
| title | 标题 | `string` | — |
| confirm-button-text | 确认文案 | `string` | `'确认'` |
| cancel-button-text | 取消文案 | `string` | `'取消'` |
| show-toolbar | 显示顶部操作栏 | `boolean` | `true` |
| item-height | 每项高度 | `number` | `44` |
| visible-count | 可见项数 | `number` | `5` |

```ts
interface CascadeOption {
  text: string
  value: string | number
  disabled?: boolean
  children?: CascadeOption[]
}
```

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选择变化 | `values: (string \| number)[]` |
| change | 某列滚动结束 | `{ selectedValues, selectedOptions, selectedIndexes }` |
| confirm | 点击确认 | 同上 |
| cancel | 点击取消 | — |
