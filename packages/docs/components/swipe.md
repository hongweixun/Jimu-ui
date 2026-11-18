---
title: Swipe 轮播
description: 手势拖动、自动播放、循环无缝、纵向轮播与指示点。
---

# Swipe 轮播

广告位、通知条、图片走廊。手势用 Pointer Events 实现，鼠标与触摸同一套逻辑；循环靠**首尾克隆页**做到无缝，不在切换瞬间闪一下。

## 基础用法

<DemoBlock src="/demos/swipe/basic.vue" title="循环自动播放、非循环回弹、纵向通知" desc="autoplay 传毫秒数（0/false 关闭）；loop 无缝循环；vertical 纵向；indicator-* 控制指示点颜色。" />

## 手势细节

| 场景 | 行为 |
| --- | --- |
| 纵向滚动页面 | 手指先动 5px 判定方向，纵向手势直接放行，轮播不抢 |
| 拖到两端（非循环） | 位移打 0.35 折的阻尼，能感到「到头了」但拖不走 |
| 松手判定 | 位移超过屏宽 25%（最多 80px）**或**速度超过 0.35px/ms 才翻页 |
| 自动播放 | 手指按下立即暂停，抬起后重新计时 |
| 点击 | 拖动过的这一次不派发 `click`，避免「滑一下就误点」 |

## 循环原理

`loop` 开启时，轨道渲染成 `[最后一张, ...真实项, 第一张]`。从最后一张继续往后翻，实际是滑到克隆的第一张；`transitionend` 之后在**关掉过渡**的状态下瞬间归位到真实第一张，人眼看不到跳变。

因此：循环模式下首尾两张会被渲染两次，**不要在 slide 里放有状态或有副作用的组件**（视频、埋点上报等），否则会重复实例化。

## 高度

轮播必须有确定高度，否则无法计算位移。默认 `160px`，按设计稿传 `height` 即可；图文卡片建议用固定比例（如 `height="180"`）而不是 `auto`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| autoplay | 自动播放间隔（ms），0/false 关闭 | `number \| boolean` | `0` |
| duration | 切换动画时长（ms） | `number` | `400` |
| initial-swipe | 初始下标 | `number` | `0` |
| loop | 无缝循环 | `boolean` | `false` |
| vertical | 纵向轮播 | `boolean` | `false` |
| touchable | 允许手势拖动 | `boolean` | `true` |
| show-indicators | 显示指示点 | `boolean` | `true` |
| indicator-position | 指示点位置 | `'bottom' \| 'top'` | `'bottom'` |
| indicator-color | 指示点颜色 | `string` | 白色半透明 |
| indicator-active-color | 选中指示点颜色 | `string` | `#fff` |

指示点**可点击直接跳转到对应页**，透明扩大了点击热区（视觉仍 6px），手指不好点的问题一并处理；翻页会正常派发 `change`。
| height | 容器高度（数字按 px） | `number \| string` | `160px` |
| radius | 容器圆角 | `number \| string` | — |
| threshold-speed | 手势判定速度（px/ms） | `number` | `0.35` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 当前页变化 | `index: number` |
| click | 点击当前页（拖动不触发） | `index: number` |

### 实例方法

| 方法 | 说明 |
| --- | --- |
| next() | 下一页 |
| prev() | 上一页 |
| goTo(index) | 跳到指定页 |
| resize() | 容器尺寸变化后重算（ResizeObserver 已自动处理，一般不用调） |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 轮播内容，每个直接子节点成为一页 |
