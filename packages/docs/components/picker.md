---
title: Picker 选择器
description: 多列滚轮选择，带吸附、阻尼、禁用项跳过与字段映射。
---

# Picker 选择器

底部滚轮选择器，通常与 `Popup` 组合成「选择日期 / 选择城市」。列内部自己实现滚动与吸附，不走原生滚动——这样才能精确控制停靠行、边界阻尼和禁用项跳过。

## 基础用法

<DemoBlock src="/demos/picker/basic.vue" title="日期三列、单列城市、年级班级、内嵌使用" desc="columns 是二维数组；columns-field-names 做字段映射；visible-count / item-height 控制滚轮高度与行高。" />

## 列的滚动行为

| 场景 | 行为 |
| --- | --- |
| 拖动松手 | 按位移吸附到最近一行；快速轻扫（> 0.5px/ms）多走一格 |
| 拖到首尾继续拉 | 位移打 0.35 折，能感到边界但不会拖飞 |
| 点击选项 | 立即吸附到该行 |
| 桌面滚轮 | 支持，滚一格换一项（方便在文档里演示） |
| 禁用项 | 落点命中 `disabled` 时向两侧找最近的可用项 |

## 值的同步

- 传 `v-model` 时是受控的：`change` 时同步派发 `update:modelValue`；
- 未传时组件内部维护选中值，也能正常滚动（适合纯展示）；
- 列数变化或外部塞进来的值不在选项里时，会**静默回落到该列第一个可用项**，不会报错也不会留空。

::: tip 日期列变化后请重算天数
月份切换会改变天数，示例里用 `computed` 根据「年 + 月」重新生成日期列。组件检测到第 3 列不再包含原值时，会自动落到最近可用值。
:::

## 尚未支持

级联选择（一个列的选择改变下一列的选项集合）没有内置。需要时用 `computed` 重新计算 `columns` 传入即可，列数不变时行为与内置联动一致。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 选中的值，顺序对应各列 | `(string \| number)[]` | — |
| columns | 多列选项；元素可为字符串/数字或对象 | `PickerColumnInput[]` | — |
| title | 标题 | `string` | — |
| confirm-button-text | 确认文案 | `string` | `'确认'` |
| cancel-button-text | 取消文案 | `string` | `'取消'` |
| show-toolbar | 显示顶部操作栏 | `boolean` | `true` |
| columns-field-names | 对象选项字段映射 `{ text, value, disabled }` | `object` | `{}` |
| item-height | 每项高度（px） | `number` | `44` |
| visible-count | 可见项数（奇数效果最好） | `number` | `5` |
| height | 整体高度，不传按 `item-height × visible-count` | `number \| string` | — |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选中值变化 | `values: (string \| number)[]` |
| change | 任一列滚动结束 | `{ selectedValues, selectedOptions, selectedIndexes }` |
| confirm | 点击确认 | 同上 |
| cancel | 点击取消 | — |

### Slots

| 名称 | 说明 |
| --- | --- |
| title | 自定义标题 |
| cancel | 自定义取消按钮 |
| confirm | 自定义确认按钮 |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-picker-item-height` | 每项高度 | `44px` |
| `--jm-picker-column-height` | 滚轮可视高度 | `item-height × visible-count` |
