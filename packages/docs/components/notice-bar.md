---
title: NoticeBar 通知栏
description: 顶部通告栏，支持跑马灯、可关闭、可点击与多行换行。
---

# NoticeBar 通知栏

系统公告、活动通知、异常提示。默认跑马灯滚动（长文案不会撑破布局），关掉动效时会自动退回单行省略，不会出现「文字卡在中间」的诡异状态。

## 基础用法

<DemoBlock src="/demos/notice-bar/basic.vue" title="跑马灯、关闭、点击与换行" desc="四条示例都可实际关闭；换成自定义配色时注意对比度。" />

## 用法

```vue
<template>
  <jm-notice-bar text="本周六课程调整到周日" mode="closeable" @close="visible = false" />
  <jm-notice-bar text="点击查看详情" mode="link" @click="goDetail" />
</template>
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| text | 文字内容 | `string` | — |
| mode | 右侧形态 | `'link' \| 'closeable' \| ''` | `''` |
| left-icon | 显示左侧喇叭 | `boolean` | `true` |
| scrollable | 跑马灯滚动 | `boolean` | `true` |
| wrapable | 允许换行（优先级高于 scrollable） | `boolean` | `false` |
| speed | 滚动速度参考值 px/s | `number` | `50` |
| color | 文字色 | `string` | `var(--jm-color-primary-text)` |
| background | 背景色 | `string` | `var(--jm-color-primary-light)` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| close | 点击关闭 | — |
| click | 点击文字区域 | `MouseEvent` |

### 插槽

| 名称 | 说明 |
| --- | --- |
| default | 自定义内容（可放图标、链接） |

::: tip 滚动时长是估算的，不是测量的
为了 SSR 安全，没有用 `getBoundingClientRect` 测文字宽度，而是按字符数估时长。中文按字宽、英文按字符宽差异很大，长英文句子会略快。真要精确可以在 `onMounted` 里测量后覆盖 `animation-duration`。
:::
