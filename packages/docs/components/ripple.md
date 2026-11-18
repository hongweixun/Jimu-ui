---
title: Ripple 水波纹
description: 移动端点击反馈：从指尖扩散到整个元素的水波，Button / Cell / ActionSheet / Dialog 已内置。
---

# Ripple 水波纹

移动端点击最有效的反馈不是边框变色，而是**从指尖长出来的一圈水波**：它把"我点到了这里"这件事直接画在屏幕上，比任何颜色变化都精确。

Jimu UI 的水波纹参照 [Varlet UI](https://www.varletjs.com/) 的算法实现：半径取元素对角线的一半，保证扩散完成后必然盖满整个元素；起点是真实触点坐标，终点是元素中心。

## 基础用法

`v-ripple` 是一个指令，挂在任意元素上即可。宿主元素需要能裁剪溢出，指令在挂载时自动补上 `position: relative` 与 `overflow: hidden`。

<DemoBlock src="/demos/ripple/basic.vue" title="指令用法" desc="不传参数时水波颜色取 currentColor：深色按钮上是白波，浅色元素上是深色波。" />

```vue
<template>
  <div v-ripple @click="handleClick">点我试试</div>

  <div v-ripple="{ color: '#00A0E9' }">主色水波</div>
  <div v-ripple="{ centered: true }">从中心扩散</div>
  <div v-ripple="{ disabled: true }">关闭水波</div>
</template>
```

## 已经内置水波纹的组件

| 组件 | 说明 |
| --- | --- |
| [Button 按钮](/components/button) | 默认开启，`ripple="false"` 关闭 |
| [Cell 单元格](/components/cell) | `clickable` 时默认开启，可用 `ripple` 单独控制 |
| [ActionSheet 动作面板](/components/action-sheet) | 每个操作项与取消按钮 |
| [Dialog 对话框](/components/dialog) | 底部两个按钮 |

::: tip 和水波纹共存的"底色变化"做了减法
按钮里保留了一点点按压压暗（`--jm-button-press-overlay` 从 0.12 降到 0.06），因为水波要 200ms 才铺满，压暗负责"瞬时回应"；而 Cell / ActionSheet / Dialog 的 `:active` 底色被完全去掉——大面积元素上两层反馈叠在一起会显脏。
:::

## 为什么是这套参数

| 参数 | 值 | 理由 |
| --- | --- | --- |
| 直径 | `√(w² + h²)` | 对角线长度，从任意触点出发都能盖满元素，不会出现"波到一半没了" |
| 起点缩放 | `0.3` | 小按钮上不会先冒出一个大圆再缩回来 |
| 扩散 | `200ms` + `cubic-bezier(.68,.01,.62,.6)` | 起步极快、尾巴极长，手指离开时波纹还在走，像真的按下去了 |
| 淡出 | `140ms` linear | 比扩散短，退场不糊手 |
| 透明度 | `0.25` | 深色文字上用 0.25 是 Material 的经典值；Cell/ActionSheet 这类大面积元素降到 0.1~0.12 |

## 移动端的五个细节

1. **按下即有波**：`pointerdown` 当帧立即创建水波，没有延迟窗口——再快的轻点也能看到完整扩散。抬手时按最短停留 180ms 补足展示时长。
2. **轻微抖动不算滑动**：位移容差 12px，覆盖真机手指落地时的自然抖动；超过容差判定为滚动，波纹**快速淡出**（不硬删，不会闪断）。列表滚动不会满屏闪波。
3. **滚动接管立即收尾**：浏览器接管滚动（`pointercancel`）时波纹 90ms 内淡出，不会挂在按钮上。
4. **内核兼容**：不支持 PointerEvent 的老内核（部分 iOS WebView）自动降级到 touch / mouse 事件，行为一致。
5. **动效可关**：`data-motion="off"` 或系统 `prefers-reduced-motion` 下**根本不创建 DOM 节点**，不是靠动画时长归零糊过去。

## 自定义

```css
/* 全局：换水波颜色与浓度 */
:root {
  --jm-ripple-color: rgba(0, 160, 233, 0.6);
  --jm-ripple-opacity: 0.18;
  --jm-ripple-duration: 240ms;
}

/* 局部：某个区域里的水波更淡 */
.my-list {
  --jm-ripple-opacity: 0.08;
}
```

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| color | 水波颜色，不传用 `currentColor` | `string` | `currentColor` |
| centered | 忽略触点，固定从元素中心扩散 | `boolean` | `false` |
| disabled | 关闭水波 | `boolean` | `false` |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-ripple-color` | 水波颜色 | `currentColor` |
| `--jm-ripple-opacity` | 水波最终透明度 | `0.25` |
| `--jm-ripple-duration` | 扩散时长 | `200ms` |
| `--jm-ripple-fade-duration` | 淡出时长 | `140ms` |
| `--jm-ripple-ease` | 扩散曲线 | `cubic-bezier(.68,.01,.62,.6)` |
