---
title: Tag 标签
description: 状态标记与轻量分类，5 种语义色、实心与浅底两种视觉。
---

# Tag 标签

用来标记状态（待支付、已批改）或分类（直播、回放）。高度 20–30px，字号 11–13px。

## 基础用法

<DemoBlock src="/demos/tag/basic.vue" title="类型、形态与尺寸" desc="plain 是浅底方案，密排列表里比实心更耐看；round 与 radius 都能改形状。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 语义色 | `'default' \| 'primary' \| 'success' \| 'warning' \| 'danger'` | `'primary'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| plain | 浅底样式 | `boolean` | `false` |
| round | 胶囊圆角 | `boolean` | `false` |
| closable | 显示关闭按钮 | `boolean` | `false` |
| color | 自定义颜色 | `string` | — |
| text-color | 自定义文字色 | `string` | — |
| radius | 圆角 | `number \| string` | `var(--jm-radius-sm)` |

### 事件

| 事件名 | 说明 |
| --- | --- |
| close | 点击关闭按钮 |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-tag-radius` | 圆角 |
| `--jm-tag-text` | 文字色（浅底模式下单独控制） |

::: warning 长文案会撑破布局
Tag 是 `inline-flex` + `white-space: nowrap`，超长文案不会自动换行。列表里建议限制在 4 个字以内，或者外面套一层 `max-width` 加省略。
:::
