---
title: LongPress 长按指令
description: 长按隐藏操作：消息多选、卡片菜单、危险操作确认，移动超过阈值自动取消。
---

# LongPress 长按指令

移动端屏幕空间有限，低频操作（多选、删除、识别文字）不值得常驻一个按钮——**长按**是它们的标准入口：iOS 桌面长按图标出菜单、微信长按消息出多选，用户已经习惯"按住不动，等它出东西"。

`v-longpress` 统一用 pointer 事件实现，触屏 / 鼠标 / 手写笔一套代码；滑动超过 8px 视为滚动意图直接取消，列表里长按不会和"滑动列表"打架。

## 基础用法

<DemoBlock src="/demos/long-press/basic.vue" title="长按卡片" desc="按住 500ms 触发；onStart 做按压反馈，onEnd 区分触发完成与取消。" />

```vue
<template>
  <div
    v-longpress="{
      onLongPress: handleLongPress,
      onStart: () => (pressing = true),
      onEnd: () => (pressing = false),
    }"
    :class="{ 'is-pressing': pressing }"
  >
    长按我
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { vLongPress } from 'jimu-ui'

const pressing = ref(false)
function handleLongPress() {
  /* 长按后的动作：出菜单 / 进多选 / 确认删除 */
}
</script>
```

## 选项

| 选项 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `onLongPress` | `(event) => void` | 必填 | 长按触发回调，参数是原始 pointer/keyboard 事件 |
| `onStart` | `() => void` | — | 按下时回调，用来做按压反馈（加 class / 缩放） |
| `onEnd` | `(state) => void` | — | 结束回调，`'done'` 表示已触发，`'cancelled'` 表示被取消 |
| `duration` | `number` | `500` | 按住多久算长按（ms）；危险操作建议拉长到 800–1200ms |
| `moveTolerance` | `number` | `8` | 移动超过该距离（px）视为滑动，取消长按 |
| `disabled` | `boolean` | `false` | 禁用 |

::: tip 危险操作把 duration 拉长
"长按删除"用默认 500ms 和普通长按没有区分度，误触代价却高得多。把 `duration` 调到 1000ms 以上，长按本身就成了一道"你确定吗"的闸门——按的时间就是确认成本。
:::

## 取消的三种方式

| 用户行为 | 结果 |
| --- | --- |
| 提前松手（未到 duration） | 取消，**不会**触发宿主的 click 之外任何东西 |
| 手指移动超过 `moveTolerance` | 取消——滚动列表、滑动切换都不会误触 |
| 触发后松手 | 正常收尾；宿主如果同时监听了 click，需要自己判断是否忽略 |

## 键盘可达性

Enter / Space 按住超过 `duration` 同样触发，松开提前取消——与指针路径共用同一套计时，屏幕阅读器用户不缺入口。

## 与系统长按行为的冲突

宿主元素若有系统级长按行为（如 iOS 上长按 `<img>` 出"存储图像"），建议给宿主加：

```css
.lp-host {
  -webkit-touch-callout: none; /* 关掉 iOS 系统长按菜单 */
  user-select: none;
  -webkit-user-select: none;
}
```
