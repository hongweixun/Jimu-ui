---
layout: doc
title: SafeBottom 安全区占位
---

# SafeBottom 安全区占位

iPhone 刘海屏 / Home Indicator 会遮住页面底部内容。`SafeBottom` 在需要的位置插入一个高度等于系统安全距离的占位块——真机上自动让位，PC 与大多数安卓设备 env 为 0、不占空间。

全局 CSS 变量 `--jm-safe-top / --jm-safe-bottom / --jm-safe-left / --jm-safe-right` 已在 tokens 中定义（`env(safe-area-inset-*)`），也可以直接使用；配套工具类见下文。

## 前置条件

页面 viewport meta 必须带 `viewport-fit=cover`，否则 iOS 上 env() 恒为 0：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
```

## 基础用法

<DemoBlock src="/demos/safe-area/basic.vue" title="列表末尾占位 + 底栏让位" desc="桌面浏览器 env 为 0，demo 用 min-height 兜底可视化占位效果。" />

```vue
<template>
  <!-- 滚动内容末尾：最后一条不被小黑条遮住 -->
  <div class="page-scroll">
    <ListItem v-for="i in list" :key="i.id" :item="i" />
    <JmSafeBottom />
  </div>

  <!-- fixed 底栏内部让位 -->
  <div class="my-tabbar jm-safe-pad-bottom">
    <TabItem />
  </div>
</template>

<script setup lang="ts">
import { SafeBottom } from 'jimu-ui'
</script>
```

## API

### SafeBottom Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| position | 占位哪一侧 | `'bottom'` / `'top'` | `'bottom'` |
| min-height | env 为 0 时的兜底高度，数字按 px | `number \| string` | — |
| background | 占位块背景色 | `string` | — |

### 工具类

| 类名 | 说明 |
| --- | --- |
| `.jm-safe-bottom` | 高度为底部安全距离的空占位（pointer-events: none） |
| `.jm-safe-top` | 高度为顶部安全距离的空占位 |
| `.jm-safe-pad-bottom` | 给 fixed 底栏补 `padding-bottom` |
| `.jm-safe-pad-x` | 补左右安全距离内边距 |

### 已内置安全区的组件

| 组件 | 方式 |
| --- | --- |
| Popup | `safe-area` prop（默认开启），底部弹层自动让位 |
| Tabbar | `safe-area-inset-bottom` prop（默认开启） |
| NumberKeyboard | `safe-area` prop 透传 Popup |
| Fab / BackTop / Notify | bottom 定位自动叠加 `env(safe-area-inset-bottom)` |
