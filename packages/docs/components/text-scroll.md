---
title: TextScroll 滚动文本
description: 单行文本超出容器宽度时自动横向无缝滚动，放得下就静止——商品名、标题等任意位置的溢出播放。
---

# TextScroll 滚动文本

文字超出可视范围又不想省略号截断时，让它**自己滚动播放**：内容宽度超过容器就横向无缝循环滚动，刚好放得下就静止显示。组件本身不带样式，可以放进卡片标题、Cell、Flex 行等任何布局。

和 [NoticeBar](/components/notice-bar) 的分工：NoticeBar 是**通知栏**（自带喇叭图标、主题色背景），TextScroll 是**裸文本滚动**，外观完全跟随上下文。

## 基础用法

<DemoBlock src="/demos/text-scroll/basic.vue" title="超长滚动 / 放得下静止 / 速度调节" desc="第二行文本较短，静止显示；speed 越大滚得越快。" />

```vue
<template>
  <jm-text-scroll text="iPhone 17 Pro Max 256GB 沙漠色钛金属 全网通 5G 手机 国行原封全新正品" />
  <jm-text-scroll text="库存充足" />
</template>
```

## 插槽与复杂内容

默认插槽同样参与溢出测量，可以放富文本：

```vue
<template>
  <jm-text-scroll :speed="60">
    <b>新品首发</b>
    <span style="color: var(--jm-color-primary)"> · 前 100 名立减 300 元</span>
  </jm-text-scroll>
</template>
```

## 暂停交互

- 桌面端鼠标悬停时暂停滚动（`animation-play-state: paused`），移开继续；
- 移动端不暂停（手指按住时 CSS `:active` 也不会误触发暂停，保证滑动流畅）。

## 无障碍与动效降级

- `data-motion="off"` 或系统开启「减弱动态效果」时，不滚动、退回单行省略；完整文本仍在 DOM 与无障碍树中可读。
- 滚动速度用 `speed`（px/s）控制，一轮时长按内容实测宽度计算，长文本不会飞速掠过。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| text | 滚动文本（不传用默认插槽） | `string` | — |
| speed | 滚动速度 px/s | `number` | `40` |
| gap | 无缝衔接处（结尾与开头之间）的留白 px | `number` | `32` |

### 插槽

| 名称 | 说明 |
| --- | --- |
| default | 滚动内容，与 `text` 二选一 |

### 实例方法

| 方法 | 说明 |
| --- | --- |
| measure() | 内容或容器尺寸变化后手动触发一次重测（正常情况下 ResizeObserver 自动完成） |
