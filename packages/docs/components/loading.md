---
title: Loading 加载
description: 四种加载指示器，可内联可整页。
---

# Loading 加载

四种类型：`circular` 圆弧、`spinner` 细弧、`dots` 三点、`pulse` 双环脉冲。

## 基础用法

<DemoBlock src="/demos/loading/basic.vue" title="类型、尺寸与文字" desc="size 传数字按 px，传字符串原样透传；vertical 让动画在上、文字在下，适合整页加载。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 类型 | `'circular' \| 'spinner' \| 'dots' \| 'pulse'` | `'circular'` |
| size | 尺寸 | `number \| string` | `24` |
| color | 颜色 | `string` | `var(--jm-color-primary)` |
| text | 说明文字 | `string` | — |
| vertical | 垂直排列 | `boolean` | `false` |

::: tip 关闭动效后还转吗
圆弧始终旋转——它是"系统还在工作"的唯一信号，属于 WCAG 允许的必要动效。但 `dots` 的跳动和 `pulse` 的扩散会停下来，因为那是装饰。
:::

::: warning 超过 1 秒就该给文字
只有转圈没有文案，用户不知道在等什么。超过 800ms 的等待，配合 `text` 说明当前在做什么（"正在上传讲义…"）。
:::
