---
title: Badge 徽标
description: 数字或小红点提示，可包裹按钮、图标，也可独立使用。
---

# Badge 徽标

两种用法：包住一个元素（角标），或者自己单独站着一个数字。

## 基础用法

<DemoBlock src="/demos/badge/basic.vue" title="角标与独立徽标" desc="内容超过 max 自动显示 99+，dot 模式只显示小红点。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| content | 显示内容 | `string \| number` | — |
| dot | 小红点模式 | `boolean` | `false` |
| max | 数字上限，超出显示 `max+` | `number` | `99` |
| color | 背景色 | `string` | `var(--jm-color-danger)` |
| show-zero | 内容为 0 时是否显示 | `boolean` | `false` |
| show | 是否显示 | `boolean` | `true` |
| offset | 位置微调 `[x, y]` | `[number, number]` | — |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 被包裹的元素，不传则独立显示 |
| content | 自定义徽标内容（可放图标） |

::: tip 徽标的白边从哪来
角标带 1.5px 的白色描边（`box-shadow: 0 0 0 1.5px var(--jm-bg-container)`），是为了压在深色图标上时依然能看出边界。深色模式下这条边自动变成深色底。
:::
