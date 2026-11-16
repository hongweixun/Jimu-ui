---
title: Circle 环形进度
description: 学习进度、正确率、打卡完成度，支持渐变、逆时针与中心自定义内容。
---

# Circle 环形进度

`jm-circle` 用 SVG 描边画环，`stroke-dashoffset` 控制进度。比 `jm-progress` 更适合「一个数字 + 一圈进度」的场景。

## 基础用法

<DemoBlock src="/demos/circle/basic.vue" title="单色、渐变、自定义中心、尺寸" desc="改 percentage 会按增量比例补间，不会整圈乱跳。" />

```vue
<jm-circle :percentage="66" :size="100" />
<jm-circle :percentage="66" :size="100" color="#1D9E75" :stroke-width="6" />
```

## 渐变色

```vue
<jm-circle
  :percentage="70"
  :color="[
    { color: '#00A0E9', percentage: 0 },
    { color: '#1D9E75', percentage: 1 },
  ]"
/>
```

色标的 `percentage` 是 0~1 的比例。渐变的跟随行为是「整条渐变固定在环上」，进度越多露出的色带越长——与 Vant 一致。

## 中心内容

默认显示百分比，`text` 换成文案，或直接用插槽：

```vue
<jm-circle :percentage="70" :size="120">
  <div class="center">
    <strong>42/60</strong>
    <span>答对题数</span>
  </div>
</jm-circle>
```

插槽内容会自动居中，字号由组件根据 `size` 换算（约 18%），也可以在插槽里自己控制。

## 动画节奏

`speed` 是「走完 100% 所需毫秒数」，实际时长按本次变化量折算：

```ts
duration = speed * |next - prev| / 100
```

所以从 0 到 100 是 `speed`，从 60 到 70 只有 `speed / 10`，小幅更新不会拖沓。用 `stroke-linecap="butt"` 可以关掉圆头。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| percentage | 进度 0~100，越界自动收敛 | `number` | `0` |
| size | 直径，数字按 px | `number \| string` | `100` |
| strokeWidth | 环宽 | `number` | `8` |
| color | 单色或渐变色标 | `string \| { color, percentage }[]` | 主色 |
| layerColor | 底环颜色 | `string` | `--jm-border-color-2` |
| fill | 圆内填充色 | `string` | `none` |
| speed | 走完 100% 的时长（ms） | `number` | `1000` |
| text | 中心文案 | `string` | 百分比 |
| textColor | 中心文字颜色 | `string` | `--jm-text-color` |
| clockwise | 顺时针增长 | `boolean` | `true` |
| strokeLinecap | 线端样式 | `'round' \| 'square' \| 'butt'` | `'round'` |

### Slots

| 插槽 | 说明 |
| --- | --- |
| default | 中心内容 |

::: tip 与 Progress 的分工
横向进度条（课程完成度、上传进度）用 `jm-progress`；需要「一个数字套一圈」时用 `jm-circle`。两者都只做展示，不处理交互。
:::
