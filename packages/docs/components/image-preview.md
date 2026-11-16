---
title: ImagePreview 图片预览
description: 全屏看图，左右滑动切换，支持组件式与函数式两种调用。
---

# ImagePreview 图片预览

点击缩略图后铺满屏幕看图。组件版用 `v-model:show`，函数版 `showImagePreview()` 一行调起、不占模板；两者共用同一套手势与样式。

## 基础用法

<DemoBlock src="/demos/image-preview/basic.vue" title="组件式与函数式" desc="images 为图片地址数组，start-position 决定从第几张开始；图片上双击或双指捏合可以放大看细节，函数式可传 target 把预览限制在某个容器内。" />

## 两种调用方式

**组件式**：适合预览状态需要跟业务状态绑定的场景（比如相册页）。

```vue
<jm-image-preview v-model:show="show" :images="list" :start-position="index" />
```

**函数式**：适合散落在列表里的「点我看大图」，不用为每次点击维护状态。

```ts
import { showImagePreview } from 'jimu-ui'

showImagePreview({ images: list, startPosition: 2, onChange: (i) => console.log(i) })
```

函数式会挂一个宿主节点：默认挂到 `body`，传了 `target` 就挂到目标容器里（文档示例用它把预览限制在手机框内）。

## 手势与关闭

| 场景 | 行为 |
| --- | --- |
| 左右滑动（未放大） | 位移超过 20%（最多 70px）或速度 > 0.4px/ms 切换 |
| 首尾继续滑 | 打 0.35 折阻尼，不会拖出空白 |
| 双击 | 放大到 `double-tap-scale`（默认 2.5 倍），再双击回到 1 倍 |
| 双指捏合 | 以两指中点为焦点缩放，范围 1 ~ `max-scale`（默认 4），超过上限有阻尼 |
| 放大后单指拖动 | 平移看细节，到边界停住；此时左右滑动不再翻页 |
| 点空白 / 点图片 | 由 `close-on-click-mask` / `close-on-click-image` 控制，默认点空白关闭 |

几个手感的细节：

- **单击关闭会等 280ms**：要留出时间接第二下，否则双击放大永远等不到第二下。双击会取消这次关闭。
- **放大状态下单击不关闭**：手上有放大倍率时，单击是"看细节"而不是"退出"，避免看到一半误触退出。
- **翻页自动复位**：切到下一张时缩放与位移归零，不会把上一张的倍率带过去。
- **缩放与翻页共用一个手势轴**：倍率回到 1 之前，横向拖动归平移；回到 1 之后才重新交给翻页，两者不会互相抢。

## 键盘操作

桌面浏览器与带外接键盘的平板上，预览是一个完整的模态层：

| 按键 | 行为 |
| --- | --- |
| `←` / `→` | 上一张 / 下一张（到头停住，不循环） |
| `Home` / `End` | 第一张 / 最后一张 |
| `+` / `-` | 以视口中心放大 / 缩小 |
| `0` | 缩放复位 |
| `Esc` | 关闭 |

打开时焦点移进预览容器，关闭后还给打开它的元素（相册格子、缩略图按钮）。索引变化会通过 `aria-live="polite"` 播报「第 3 张，共 9 张」，读屏用户也能感知翻页。

## 已知限制

- 图片在 `object-fit: contain` 下留出的空白区域也参与平移判定，极端比例的长图在放大后水平方向可能"多拖一点"。这是用容器尺寸近似图片尺寸的取舍，换取任何比例的图片都能立即响应。
- 缩放态下没有做「拖到边缘继续拖就翻页」的接力（Vant 有），需要先双击/捏合回到 1 倍再滑。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:show | 是否显示 | `boolean` | `false` |
| images | 图片地址数组 | `string[]` | `[]` |
| start-position | 打开时停留的下标 | `number` | `0` |
| show-index | 显示 `2 / 5` 计数 | `boolean` | `true` |
| closeable | 右上角关闭按钮 | `boolean` | `true` |
| close-on-click-mask | 点空白处关闭 | `boolean` | `true` |
| close-on-click-image | 点图片关闭 | `boolean` | `false` |
| teleport | 挂载目标；`false` 就地渲染 | `boolean \| string \| Element` | `true` |
| z-index | 层级 | `number` | `2200` |
| mask-color | 蒙层背景色 | `string` | `rgba(0,0,0,.92)` |
| zoomable | 开启双击 / 双指缩放 | `boolean` | `true` |
| max-scale | 最大放大倍数 | `number` | `4` |
| double-tap-scale | 双击放大到的倍数 | `number` | `2.5` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:show | 显示状态变化 | `value: boolean` |
| change | 切换到另一张 | `index: number` |
| close | 关闭 | — |
| zoom | 缩放倍率变化（双击、捏合、回弹、复位都会触发） | `scale: number` |

### 函数式

```ts
showImagePreview(options: ImagePreviewOptions): void
closeImagePreview(): void
```

`ImagePreviewOptions` 在 Props 基础上增加 `target?: HTMLElement | null`、`onChange?(index)`、`onZoom?(scale)`、`onClose?()`。
