---
title: Layout 布局
description: 24 栅格的行列布局，配合 gutter 控制间距，适合表单、卡片、图文混排。
---

# Layout 布局

`jm-row` + `jm-col` 组成 24 栅格。与 [Grid 宫格](/components/grid) 的分工：Grid 是「等分入口」，Layout 是「自由比例的页面骨架」。

## 基础用法

<DemoBlock src="/demos/layout/basic.vue" title="24 栅格、横纵间距、偏移与分布" desc="gutter 传数字是横向间距，传 [横, 纵] 可同时控制行距；offset 以列宽为单位右移。" />

## 栅格换算

一行 24 份，`span=12` 即一半，`span=8` 即三分之一：

```vue
<jm-row :gutter="12">
  <jm-col :span="8">1/3</jm-col>
  <jm-col :span="16">2/3</jm-col>
</jm-row>
```

`offset` 也以列为单位，用于「只占一半、另一半留白」这类排版，比写 `justify: flex-end` 更好对齐其他行。

## 与 gutter 的关系

`gutter` 的实现是「Col 左右各一半内边距 + Row 负外边距抵消」，所以：

- 最左/最右的格子与父容器**边沿对齐**，不会多出空白；
- `gutter` 只在 Row 内生效，嵌套 Row 各算各的；
- 纵向间距用 `row-gap`，与横向互不影响。

## API

### Row Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| gutter | 列间距，`[横向, 纵向]` 可分别设置 | `number \| string \| [number \| string, number \| string]` | `0` |
| align | 交叉轴对齐 | `'top' \| 'middle' \| 'bottom' \| 'stretch'` | `top` |
| justify | 主轴分布 | `'start' \| 'center' \| 'end' \| 'between' \| 'around'` | `start` |
| wrap | 是否换行 | `boolean` | `true` |

### Col Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| span | 占多少列（1~24），越界自动收敛 | `number` | `24` |
| offset | 向右偏移列数 | `number` | `0` |
| order | 排序权重，数字小的在前 | `number` | `0` |

### Slots

| 组件 | 名称 | 说明 |
| --- | --- | --- |
| Row | default | 若干 `jm-col` |
| Col | default | 列内容 |
