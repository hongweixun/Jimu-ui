---
title: Sticky 粘性布局
description: "内容滚过时吸顶：原生 position: sticky 实现，不监听滚动、不打破文档流。"
---

# Sticky 粘性布局

包裹需要吸顶的内容（Tabs、NavBar、索引栏等），当滚动容器滚过组件位置时钉在顶部。用原生 `position: sticky` 实现：不监听 scroll 事件、不克隆节点、不打破文档流，嵌套滚动容器（如弹窗内）同样直接生效。

## 基础用法

配合 Tabs 使用，滚动长内容时标签栏吸顶（见 [Tabs 标签页](/components/tabs) 的置顶演示）：

```html
<jm-sticky :offset-top="0">
  <jm-tabs v-model="active" animated swipeable>…</jm-tabs>
</jm-sticky>
```

吸顶偏移：吸顶后距滚动容器顶部留出距离（如给 NavBar 让位）：

```html
<jm-sticky :offset-top="44">
  <jm-tabs v-model="active">…</jm-tabs>
</jm-sticky>
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| offset-top | 吸顶后距滚动容器顶部的偏移，数字按 px | `number \| string` | `0` |
| z-index | 吸顶层的 z-index | `number \| string` | `99` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 需要吸顶的内容 |

::: tip sticky 生效条件
`position: sticky` 相对**最近的滚动容器**生效，且容器内需要有足够的内容高度；若父级存在 `overflow: hidden` 等裁剪声明，会限制 sticky 的作用范围，请保证滚动链路上没有裁剪容器。
:::

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-sticky-top` | 吸顶偏移（由 `offset-top` 换算） |
| `--jm-sticky-z` | 吸顶层 z-index（由 `z-index` 换算） |
