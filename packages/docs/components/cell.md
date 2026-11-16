---
title: Cell 单元格
description: 列表的骨架，配合 CellGroup 组成卡片式分组。
---

# Cell 单元格

移动端最常见的布局单元：左边标题、右边内容、可带箭头。单行高度默认 `48px`，点击有底色反馈。

## 基础用法

<DemoBlock src="/demos/cell/basic.vue" title="个人中心" desc="右侧内容完全交给插槽，所以开关、头像、自定义标签都能直接塞进去。" />

## 分组与圆角

<DemoBlock src="/demos/cell/group.vue" title="CellGroup 分组" desc="inset 控制左右留白，radius 控制圆角，分割线由分组统一管理，不需要每行手写 border。" />

## API

### Cell Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 左侧标题 | `string` | — |
| label | 标题下方说明 | `string` | — |
| value | 右侧内容 | `string \| number` | — |
| is-link | 显示右箭头 | `boolean` | `false` |
| clickable | 可点击（带水波纹反馈） | `boolean` | `false` |
| ripple | 水波纹，默认跟随 `clickable` | `boolean` | 同 `clickable` |
| border | 单独使用时是否显示下边框 | `boolean` | `true` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| radius | 圆角 | `number \| string` | `0` |
| background | 背景色 | `string` | 透明 |
| align | 标题对齐 | `'left' \| 'right'` | `'left'` |

### CellGroup Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 分组标题 | `string` | — |
| inset | 卡片式（左右留白） | `boolean` | `true` |
| radius | 圆角 | `number \| string` | `var(--jm-radius)` |
| background | 分组底色 | `string` | `var(--jm-bg-container)` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 右侧内容（Cell） |
| icon | 左侧图标 |
| title | 自定义标题 |
| label | 自定义说明 |
| right | 箭头左侧的额外内容 |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-cell-radius` | 单元格圆角 |
| `--jm-cell-bg` | 单元格底色 |
| `--jm-cell-group-radius` | 分组圆角 |
| `--jm-cell-group-bg` | 分组底色 |

::: tip 分割线只在两行之间
放在 CellGroup 里时，Cell 自己的 `border` 会被接管，由分组的 `:not(:last-child)` 规则画线，所以最后一行永远不会有悬空的线。
:::
