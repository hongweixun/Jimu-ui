---
title: Divider 分割线
description: 内容分隔，支持带文案、虚线、细线与行内竖线。
---

# Divider 分割线

分隔内容区块，默认颜色 `--jm-border-color`，间距 `16px`。

## 基础用法

<DemoBlock src="/demos/divider/basic.vue" title="各种形态" desc="带文案时自动变成左右两条线夹住文字；position 控制文字位置。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| vertical | 行内竖线 | `boolean` | `false` |
| dashed | 虚线 | `boolean` | `false` |
| position | 文案位置（仅横向且有文案时生效） | `'left' \| 'center' \| 'right'` | `'center'` |
| hairline | 只留 1px（用 `scaleY(.5)` 实现） | `boolean` | `false` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 分割线中间的文字 |

::: tip 竖线只在行内用
`vertical` 会渲染成 `inline-block` 的 1px 竖线，必须和文字在同一行（比如 `<span>课程</span><jm-divider vertical /><span>讲义</span>`）。放在块级容器里不会撑高。
:::
