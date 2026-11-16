---
title: Button 按钮
description: 触发操作的基础组件，6 种语义色 × 4 种形态 × 3 种尺寸，圆角可自由设置。
---

# Button 按钮

触发一个操作。移动端最重要的交互元素，触控高度最低 `30px`，默认 `44px`，适老模式下自动抬高。

## 基础用法

<DemoBlock src="/demos/button/type.vue" title="语义类型" desc="type 决定语义色，default 是描边白底，用于次要操作。" />

## 样式形态

`variant` 提供四种形态。同一个 `type` 换 `variant` 就能适配不同层级的视觉权重。

<DemoBlock src="/demos/button/variant.vue" title="四种形态" desc="solid 实心 / outline 描边 / ghost 浅底 / text 纯文字。同层级页面里，一个实心按钮就够，其余用 ghost 或 text。" />

## 尺寸与圆角

<DemoBlock src="/demos/button/size.vue" title="尺寸、胶囊与圆角" desc="round 一键胶囊，radius 传数字按 px 处理、传字符串原样透传，两者同时传以 radius 为准。移动端主按钮推荐 round + size medium（44px）。" />

## 状态与自定义颜色

<DemoBlock src="/demos/button/state.vue" title="加载、禁用、图标与自定义色" desc="传 color 时，浅底和描边会按 12%/40% 透明度自动派生，不用自己配三个色。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 语义类型 | `'default' \| 'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'` | `'default'` |
| variant | 形态 | `'solid' \| 'outline' \| 'ghost' \| 'text'` | `'solid'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| radius | 圆角 | `number \| string` | `var(--jm-radius)` |
| round | 胶囊形态（`radius` 显式传值时以 `radius` 为准） | `boolean` | `false` |
| block | 是否撑满一行 | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| loading | 加载中（自动禁用点击） | `boolean` | `false` |
| ripple | 点击水波纹 | `boolean` | `true` |
| color | 自定义主色 | `string` | — |
| native-type | 原生 type | `'button' \| 'submit' \| 'reset'` | `'button'` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击（禁用/加载时不触发） | `MouseEvent` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 按钮文字 |
| icon | 左侧图标，加载时自动隐藏 |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-button-radius` | 圆角，等价于 `radius` 属性 |
| `--jm-button-press-overlay` | 按压时底色加深的程度，默认 `0.12`（0~1） |
| `--jm-button-press-scale` | 按压缩放比例，默认 `1` 即不缩放；设成 `0.97` 可恢复 iOS 式回弹 |

::: tip 按钮的点击反馈：水波纹 + 轻微压暗
按下时会从指尖扩散一圈水波（参照 Varlet UI），同时底色压暗 6% 作为"瞬时回应"——水波需要 200ms 才铺满，压暗负责那 200ms 里的即时感。`ripple="false"` 可关掉水波纹，此时压暗回到 12%。
:::

::: tip 按下时为什么不做缩放
早期实现是按下整体 `scale(0.96)`，实际在真机上会看到**文字像在跳动**：缩放会把文字一起缩放，字形需要重新栅格化，小字号在高 DPR 屏上对齐点变化，观感就是"字号忽大忽小"。

现在改成**覆盖层压暗**：一层纯色薄幕落在文字下方，100ms 内渐显，按钮的宽高、文字位置、字形都不发生任何变化，白字也不会因为叠加而变灰。悬停同样只改底色，不用 `opacity` 淡化整块——交互过程中文字亮度恒定，就不会有"闪一下"的感觉。

如果确实喜欢缩放回弹的手感，可以局部开回来：

```css
.my-btn { --jm-button-press-scale: 0.97; }
```
:::
