---
title: Radio 单选框
description: 单选，圆形触控区带水波纹，选中后文字跟随主色。
---

# Radio 单选框

一组里只能选一个。选项超过 5 个、或者选项文案很长时，改用 ActionSheet 或 Picker 更合适。

视觉与触感参照 Varlet：

- 图标外再包一层**圆形触控区（action）**，点击时从这里散开水波纹，热区比图标本身大得多
- 文案保持常规深灰，**只有图标变色**（Varlet 同款）；想让文字一起变主色传 `label-color="active"`
- 左侧负外边距抵消触控区留白，图标与周围文字（如 Cell 文案）保持视觉对齐
- 选中圆点用弹簧曲线从 0 弹到 1，比图标硬切换更有确认感

## 基础用法

<DemoBlock src="/demos/radio/basic.vue" title="分组、竖排与样式" desc="点击选中项可以看到从图标散开的水波纹；dot='ring' 是空心环，视觉更轻；关闭动效后波纹不出现、圆点瞬时呈现。" />

## API

### Radio Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 选中值（单独使用时） | `string \| number` | — |
| value | 当前项取值 | `string \| number` | — |
| label | 文案 | `string` | — |
| disabled | 禁用 | `boolean` | `false` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| color | 选中色 | `string` | 继承分组或主题主色 |
| dot | 圆点样式 | `'solid' \| 'ring'` | `'solid'` |
| label-color | 选中后文字颜色：`'inherit'` 保持常规 / `'active'` 跟随主色 | `'active' \| 'inherit'` | `'inherit'` |
| ripple | 水波纹触感 | `boolean` | `true` |

### RadioGroup Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 选中值 | `string \| number` | — |
| disabled | 整组禁用 | `boolean` | `false` |
| color | 整组选中色 | `string` | — |
| direction | 排列方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| gap | 间距 | `number \| string` | `16px` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选中变化 | `string \| number` |
| change | 选中变化 | `string \| number` |

::: tip 分组不是必须的
单独用 `<jm-radio :model-value="x" value="a" />` 时要自己管状态。放进 `jm-radio-group` 后，子项只负责展示和触发，状态统一在父级，这样列表里几十个选项也不会各自为政。
:::

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-radio-size` | 图标直径（默认 24px） |
| `--jm-radio-action-padding` | 圆形触控区的内边距（默认 5px） |
| `--jm-radio-unchecked` | 未选中环的颜色（默认深灰，可调浅） |
| `--jm-radio-border` | 环的粗细（默认 1.5px，想要粗环设 `2px` 以上；图标为 SVG 绘制，随尺寸等比缩放） |
| `--jm-radio-border` | 环的粗细（默认 1.5px，想要粗环设 `2px` 以上；图标为 SVG 绘制，随尺寸等比缩放） |
| `--jm-radio-active` | 选中色（组件内自动写入） |
