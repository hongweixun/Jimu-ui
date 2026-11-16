---
title: Grid 宫格
description: 把入口、功能按等分网格铺开，支持正方形、细线、角标与图标在左。
---

# Grid 宫格

移动端首页的「九宫格 / 四宫格」入口。基于 CSS Grid，等分由 `columns` 决定，格子尺寸随容器自适应，不写死宽度。

## 基础用法

<DemoBlock src="/demos/grid/basic.vue" title="四列入口、正方形宫格、图标在左" desc="columns 控制每行列数；square 让每格变正方形；border 画细线；direction=column 时图标在左、文字在右。" />

## 点击事件

`jm-grid` 与 `jm-grid-item` 都会派发 `click`，参数是该项下标。要接住下标，`GridItem` 需要知道自己是第几个：

- 默认按**挂载顺序**自动领号（`v-for` 直接渲染即可）；
- 列表会增删、或顺序不固定时，显式传 `:index` 更稳妥。

```vue
<jm-grid :columns="4" clickable @click="(i) => go(i)">
  <jm-grid-item v-for="(it, i) in list" :key="it.id" :text="it.text" :index="i" />
</jm-grid>
```

## 角标

`badge` 显示数字角标，`dot` 显示纯红点（`dot` 优先）。需要更复杂的角标时用 `icon` 插槽自行组合 `jm-badge`。

## API

### Grid Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| columns | 每行列数，非法值按 1 处理并告警 | `number` | `4` |
| gutter | 格子间距（数字按 px） | `number \| string` | `0` |
| border | 显示格子间细线 | `boolean` | `false` |
| center | 内容水平居中 | `boolean` | `true` |
| square | 每格强制正方形 | `boolean` | `false` |
| direction | `row` 图标在上，`column` 图标在左 | `'row' \| 'column'` | `'row'` |
| clickable | 整组可点击 | `boolean` | `false` |
| radius | 圆角（配合 background 做卡片） | `number \| string` | — |
| background | 背景色 | `string` | — |

### Grid Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击某一格 | `index: number` |

### GridItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| text | 文字 | `string` | — |
| icon | 图标（SVG 的 path `d`） | `string` | — |
| icon-size | 图标尺寸 | `number \| string` | `28px` |
| badge | 数字角标 | `number \| string` | — |
| dot | 小红点 | `boolean` | `false` |
| index | 下标，不传则自动领号 | `number` | — |
| clickable | 单项覆盖 Grid 的可点击设置 | `boolean` | 跟随 Grid |

### GridItem Slots

| 名称 | 说明 |
| --- | --- |
| icon | 自定义图标，替代 `icon` 属性 |
| text | 自定义文字内容 |
| default | 追加在文字下方的自定义内容 |
