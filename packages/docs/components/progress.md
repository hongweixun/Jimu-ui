---
title: Progress 进度条
description: 展示任务进度，宽度过渡动画，颜色粗细文字可配。
---

# Progress 进度条

展示操作或任务的当前进度。进度变化只动 `width`（300ms 标准缓动），不引起重排；越界值自动收敛到 0~100 并在控制台告警。

## 基础用法

<DemoBlock src="/demos/progress/basic.vue" title="颜色、粗细、置灰与动画" desc="percentage 驱动；color / track-color / stroke-width 自定义；show-text 控制右侧百分比；inactive 置灰表示暂停态。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| percentage | 进度 0~100，越界自动收敛 | `number` | `0` |
| stroke-width | 轨道粗细（数字按 px） | `number \| string` | `6px` |
| color | 进度条颜色 | `string` | `var(--jm-color-primary)` |
| track-color | 轨道颜色 | `string` | `var(--jm-bg-input)` |
| show-text | 右侧显示百分比文字 | `boolean` | `true` |
| inactive | 置灰（暂停态） | `boolean` | `false` |

### Slots

无。

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-progress-height` | 轨道粗细 | `6px` |
| `--jm-progress-color` | 进度条颜色 | `var(--jm-color-primary)` |
| `--jm-progress-track-color` | 轨道颜色 | `var(--jm-bg-input)` |
