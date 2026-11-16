---
title: Table 表格
description: 移动端简版表格：列定义驱动、横向滚动 + 固定首列、粘性表头、自定义单元格。
---

# Table 表格

手机屏幕放不下六列数据，但有些内容——成绩单、对账单、规格参数——不排成表根本看不清。Table 只做移动端真正用得到的几件事：横向滚动、首列固定、表头吸顶、单元格自定义，不做排序筛选分页（那些交给外部控件）。

## 基础用法

<DemoBlock src="/demos/table/basic.vue" title="订单列表：金额右对齐，状态用 Tag" desc="columns 决定列顺序与宽度，data 是普通对象数组。金额这类数字列把 align 设为 right 让小数点对齐，个位数和五位数看起来才整齐。" />

```vue
<jm-table
  :columns="columns"
  :data="rows"
  row-key="id"
  stripe
  clickable
  max-height="260"
  @row-click="openOrder"
>
  <template #cell-status="{ value }">
    <jm-tag size="small" :type="value === '已完成' ? 'success' : 'warning'">
      {{ value }}
    </jm-tag>
  </template>
</jm-table>
```

```ts
const columns = [
  { key: 'id', title: '订单号', width: 128, fixed: 'left' },
  { key: 'title', title: '商品', minWidth: 130, ellipsis: true },
  { key: 'amount', title: '金额', width: 88, align: 'right', formatter: (v) => `¥${Number(v).toFixed(2)}` },
  { key: 'status', title: '状态', width: 76, align: 'center' },
]
```

## 固定首列与横向滚动

<DemoBlock src="/demos/table/wide.vue" title="成绩单：七列数据，首列不跟着滚" desc="列宽合计超过容器宽度时整表横向滚动，「学生」这一列 sticky 在左边 —— 滑到最右边也还知道在看谁的成绩。点按钮可以清空数据看空态。" />

```vue
<jm-table :columns="columns" :data="rows" row-key="id" bordered sticky-header max-height="240" />
```

只给第一列写 `fixed: 'left'` 就够了。手机屏幕宽 375 的时候，固定列建议控制在 90~120px，太宽会把可滚动区域挤没。

`max-height` 配合 `sticky-header`：表体在容器内滚动，表头吸顶。数据超过一屏时这个组合几乎是必须的，否则滚到第三屏就忘了列是什么。

## 单元格自定义

三种方式，按复杂度从上到下：

**1. formatter** —— 只改文本，不碰 DOM：

```ts
{ key: 'amount', title: '金额', formatter: (v, row, index) => `${row.type === 'refund' ? '-' : ''}¥${v}` }
```

**2. 具名插槽** —— 插槽名是 `cell-{key}`，作用域里有 `row` / `value` / `index` / `column`：

```vue
<template #cell-status="{ value }">
  <jm-tag :type="value === '已完成' ? 'success' : 'warning'">{{ value }}</jm-tag>
</template>
```

**3. 行点击 + 单元格点击**：

```vue
<jm-table
  :columns="columns"
  :data="rows"
  clickable
  @row-click="(row, index) => open(row)"
  @cell-click="({ row, column, value }) => copy(value)"
/>
```

## 空数据

```vue
<jm-table :columns="columns" :data="[]" empty-text="本学期还没有成绩记录" />
```

也可以换整个空态区域：`<template #empty><jm-empty description="暂无成绩" /></template>`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| columns | 列定义 | `TableColumn[]` | `[]` |
| data | 行数据 | `Record<string, any>[]` | `[]` |
| row-key | 行唯一键字段名 | `string` | 用下标 |
| stripe | 斑马纹 | `boolean` | `false` |
| bordered | 单元格竖线 | `boolean` | `false` |
| max-height | 最大高度，超出后表体滚动 | `number \| string` | — |
| sticky-header | 表头吸顶 | `boolean` | `false` |
| empty-text | 空数据文案 | `string` | `暂无数据` |
| clickable | 行可点击（指针 + 键盘 Enter） | `boolean` | `false` |

### TableColumn

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| key | 取值字段，同时用于插槽名 | `string` |
| title | 表头文案 | `string` |
| width | 列宽（数字按 px），不传按内容自适应 | `number \| string` |
| minWidth | 最小列宽 | `number \| string` |
| align | 对齐 | `'left' \| 'center' \| 'right'` |
| fixed | 固定在左侧 | `'left'` |
| ellipsis | 单行省略（需同时给 width） | `boolean` |
| formatter | 文本格式化 | `(value, row, index) => string` |
| className | 表头附加类名 | `string` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| row-click | 点击行 | `(row, index)` |
| cell-click | 点击单元格 | `{ row, column, value, index }` |

### Slots

| 插槽 | 说明 | 作用域 |
| --- | --- | --- |
| `cell-{key}` | 自定义某个单元格 | `{ row, value, index, column }` |
| empty | 空数据 | — |

## 什么时候别用表格

- **只有两三个字段**：用 Cell 或 Card 列表，信息密度更低但更好读。
- **需要排序、筛选、分页**：Table 不管这些，配 `Pagination` 和外部筛选控件自己拼；数据量大时更建议下拉刷新 + 分页加载。
- **每条记录字段差异大**（有的三行有的八行）：用 Descriptions 或卡片，表格的整齐反而会浪费空间。
- **纯展示、不可交互**：也要注意别为了「对齐」把文字塞成两行缩写，手机上宁可少一列。
