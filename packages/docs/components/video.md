---
title: Video 视频播放器
description: 视频播放组件，懒加载 + 进视口自动播放 + 离屏自动暂停，多视频列表不卡顿。
---

# Video 视频播放器

为「页面里嵌视频」设计的播放器：默认 `preload="none"` 懒加载，滚动到附近才开始拉数据；`playInView` 让视频**进视口自动播、离屏自动停**，页面切后台也会统一暂停——避免列表里几十个视频同时在播把页面拖卡。

## 基础用法

<DemoBlock src="/demos/video/basic.vue" title="封面 + 控制条、静音自动播放轮播" desc="基础播放器带 16:9 封面与原生控制条；playInView 场景滚动出屏幕即暂停，进度回调 500ms 节流。" />

## 用法

```html
<!-- 基础：封面 + 控制条 -->
<jm-video :src="url" :poster="poster" :radius="12" />

<!-- 静音自动播放（滚动轮播），无控制条，离屏自动暂停 -->
<jm-video :src="url" :poster="poster" play-in-view :controls="false" loop />
```

## 性能设计

| 机制 | 说明 |
| --- | --- |
| `preload="none"`（默认） | 不进视口不拉流量，长列表首屏零视频流量 |
| IntersectionObserver | 只在视口内（含 80px 预载边距）触发播放判断，进出视口无需监听 scroll |
| `play-in-view` + 离屏暂停 | 一屏多个视频时只有可见的在播，划走即停 |
| 页面隐藏暂停 | 切后台 / 锁屏统一暂停，回来按视口状态恢复 |
| `timeupdate` 节流 | 原生每秒可触发几十次，组件节流到 500ms 再回调，回调里做重活也不拖渲染 |
| 自动播放强制 muted | 浏览器策略要求自动播放必须静音，`play-in-view` 时组件自动带上，播放被拦截时静默降级为用户手动播 |

## API

### Video Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| src | 视频地址 | `string` | — |
| poster | 封面图 | `string` | — |
| aspect-ratio | 宽高比，数字按比例值，字符串原样 | `number \| string` | `'16 / 9'` |
| play-in-view | 进视口自动播放（强制静音） | `boolean` | `false` |
| pause-off-view | 离开视口自动暂停；不传跟随 `play-in-view` | `boolean` | — |
| pause-on-hidden | 页面切后台时暂停 | `boolean` | `true` |
| controls | 显示原生控制条 | `boolean` | `true` |
| loop | 循环播放 | `boolean` | `false` |
| muted | 静音 | `boolean` | `false` |
| object-fit | 视频适配方式 | `'cover' \| 'contain' \| 'fill'` | `'contain'` |
| preload | 预加载策略 | `'none' \| 'metadata' \| 'auto'` | `'none'` |
| background | 加载前背景色 | `string` | `'#000'` |
| radius | 圆角 | `number \| string` | `0` |
| playback-rate | 倍速 | `number` | `1` |
| disabled | 禁用 | `boolean` | `false` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| play / pause / ended | 播放状态变化 | — |
| timeupdate | 进度（500ms 节流） | `(currentTime, duration)` |
| loadedmetadata | 元数据加载完成（拿到时长） | `duration` |
| error | 加载或播放出错 | `Event` |

### 方法 / 插槽

| 名称 | 说明 |
| --- | --- |
| `play()` / `pause()` | 通过 ref 手动播放暂停 |
| `el` | 原生 `<video>` 元素，自定义控制条时直接操作 |
| default（video 内）/ `#source` | 放 `<source>` 标签多清晰度源 |
