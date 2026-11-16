---
title: Stepper 步进器
description: 数量增减，支持步长、范围、小数、禁输入，可与 Form 联动校验。
---

# Stepper 步进器

数量的增减输入。加减按钮到边界自动禁用并压淡；输入框允许输入过程的中间态（清空、打半截），失焦时统一收敛（clamp + 整数取整 + 小数对齐步长精度，避开 `0.1 + 0.2` 的浮点尾巴）。

## 基础用法

<DemoBlock src="/demos/stepper/basic.vue" title="范围、步长、小数、禁用与表单联动" desc="min / max / step 控制取值；integer 关掉后支持小数；disable-input 只允许点按钮；放进 FormItem 可触发 min/max 校验。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前值 | `number` | `1` |
| min | 最小值 | `number` | `1` |
| max | 最大值 | `number` | `Infinity` |
| step | 步长 | `number` | `1` |
| integer | 只允许整数 | `boolean` | `true` |
| disabled | 整体禁用 | `boolean` | `false` |
| disable-input | 禁止手动输入，只能点按钮 | `boolean` | `false` |
| input-width | 输入框宽度（数字按 px） | `number \| string` | `32px` |
| button-size | 按钮边长（数字按 px） | `number \| string` | `28px` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue / change | 值变化（被 clamp 收敛成相同值时不触发） | `value` |
| over-limit | 点击按钮后超出 min / max（值不变） | `'minus' \| 'plus'` |
| blur | 输入框失焦（已收敛到合法值） | `event` |

### Slots

无。图标为内置 SVG。

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-stepper-input-width` | 输入框宽度 | `32px * size-scale` |
| `--jm-stepper-button-size` | 按钮边长 | `28px * size-scale` |

::: tip 与 Form 联动
放进 `FormItem` 并声明 `min` / `max` / `validator` 规则后，点按钮或失焦都会触发 `change` / `blur` 时机校验，超范围会像 Input 一样呈现报错文案。
:::
