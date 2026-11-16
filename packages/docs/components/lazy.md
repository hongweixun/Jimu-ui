---
title: Lazy 懒加载指令
description: 图片进入视口才加载：首屏只请求看得见的图，提前 200px 预加载不露白。
---

# Lazy 懒加载指令

课程列表一页 30 张封面图，用户实际只看前 5 张——剩下 25 张的请求、解码、内存全是白付的。`v-lazy` 让元素**滚进视口才真正加载**：首屏请求数从 30 降到 5，弱网下的首屏时间立竿见影。

默认**提前 200px 预加载**（`rootMargin: '200px'`）：用户滚到的时候图已经在了，不会看到加载过程；加载完成前宿主保持透明占位，图到了淡入，不跳布局。

## 图片懒加载

<DemoBlock src="/demos/lazy/basic.vue" title="课程列表 + 评论区" desc="图片滚进视口才设置 src；评论区用 onVisible 回调，滚到才加载内容。" />

```vue
<template>
  <div v-for="c in courses" :key="c.id" class="course-card">
    <img v-lazy="{ src: c.src, onLoad: () => (c.loaded = true) }" alt="" />
  </div>

  <!-- 通用：进入视口时回调，内容自行接管 -->
  <div v-lazy="{ onVisible: loadComments }">评论区</div>
</template>

<script setup>
import { vLazy } from 'jimu-ui'
</script>
```

## 选项

| 选项 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `src` | `string` | — | 图片地址；`img` 设 `src`，其他元素设 `background-image` |
| `onLoad` | `() => void` | — | 真实图片加载完成（淡入后） |
| `onError` | `(event) => void` | — | 加载失败，宿主会带上 `jm-lazy-error` class 供自定义兜底 |
| `onVisible` | `() => void` | — | 进入视口回调（通用懒加载入口，与 `src` 可同时用） |
| `margin` | `string` | `'200px'` | 提前量，同 IntersectionObserver 的 `rootMargin` |
| `threshold` | `number` | `0` | 相交比例阈值 |
| `root` | `Element \| null` | `null` | 观察的滚动容器，默认视口 |
| `once` | `boolean` | `true` | 只触发一次 |

值的两种形态：

| 写法 | 含义 |
| --- | --- |
| `v-lazy="'https://…'"` | 等价于 `{ src: 'https://…' }` |
| `v-lazy="{ src, onVisible, margin }"` | 完整配置 |

::: tip 为什么默认 once 而不是"进出都算"
懒加载和曝光埋点 95% 只关心"第一次进入"。图片加载期间如果布局抖动，元素可能短暂离开视口——once 模式进入过就算加载过，不会因为抖动反复重置。需要"每次进入都触发"（比如多屏轮播的曝光统计）显式传 `once: false`。
:::

## 加载状态

| 状态 | 宿主元素表现 |
| --- | --- |
| 未进入视口 | `opacity: 0`（透明占位，不抽走 DOM，布局不跳） |
| 加载成功 | 淡入（`jm-lazy-visible`），300ms 过渡 |
| 加载失败 | 淡入 + `jm-lazy-error` class，供宿主自定义兜底图 |

```vue
<template>
  <img v-lazy="src" :class="{ 'broken': $el?.classList.contains('jm-lazy-error') }" />
</template>
```

更实用的兜底是直接监听 `onError` 换一张占位图：

```vue
<template>
  <img v-lazy="{ src, onError: () => (src = fallback) }" alt="" />
</template>
```

## 底层

指令内部使用 [`useIntersection`](/components/composables)——需要"进入视口"语义但不是图片的场景（滚动加载评论、曝光埋点、入场动画）直接用组合式函数。
