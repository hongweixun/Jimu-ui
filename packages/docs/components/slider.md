---
title: Slider 滑块
description: 单值或区间拖动选择，支持步长、刻度对齐、气泡提示与键盘操作。
---

# Slider 滑块

价格区间、难度系数、音量这类「连续值」用滑块比输入框顺手。`jm-slider` 同时支持单滑块和双滑块，点轨道可直接跳转，不用非得按住按钮。

## 基础用法

<DemoBlock src="/demos/slider/basic.vue" title="单值、双滑块、步长、禁用、自定义颜色与气泡" desc="modelValue 传数组自动进入双滑块模式；show-tooltip 常显数值气泡。" />

## 单值与区间

```vue
<jm-slider v-model="age" :min="1" :max="100" />

<jm-slider v-model="price" range :min="0" :max="1000" :step="10" show-tooltip />
```

传数组即区间；也可显式写 `range` 强制双滑块。区间两端会互相约束：左滑块不会越过右滑块，留白由 `minGap` 控制。

## 步长与精度

`step` 可以是小数（如 `0.1`），组件按 `step` 的小数位数做四舍五入，避免出现 `0.30000000000000004`。

## 拖动与点击

- 按住按钮拖动：实时预览，松开派发 `change`；
- 点击轨道：跳到点击位置（双滑块时移动较近的那个）；
- 键盘：聚焦后 `←/→` 走一步，`PageUp/PageDown` 走十步，`Home/End` 到两端。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前值，数组为区间 | `number \| [number, number]` | `0` |
| range | 强制双滑块 | `boolean` | `false` |
| min / max | 取值范围 | `number` | `0` / `100` |
| step | 步长，支持小数 | `number` | `1` |
| minGap | 双滑块最小间隔 | `number` | `0` |
| disabled | 禁用 | `boolean` | `false` |
| barHeight | 轨道高度 | `number \| string` | `4` |
| buttonSize | 滑块直径 | `number \| string` | `20` |
| activeColor | 已选轨道颜色 | `string` | 主色 |
| inactiveColor | 轨道底色 | `string` | `--jm-bg-input` |
| showTooltip | 常显数值气泡 | `boolean` | `false` |
| format | 气泡文案格式化 | `(v: number) => string` | — |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 值变化 | `number \| [number, number]` |
| change | 拖动结束/键盘调整 | `number \| [number, number]` |
| drag-start | 开始拖动 | — |
| drag-end | 结束拖动 | — |

### 无障碍

滑块节点带 `role="slider"`、`aria-valuenow/min/max` 与 `tabindex`，禁用时 `tabindex=-1` 且 `aria-disabled=true`。
