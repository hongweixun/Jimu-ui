---
title: BackTop 回到顶部
description: 滚动超过阈值后出现的回顶按钮，支持监听 window 或指定滚动容器。
---

# BackTop 回到顶部

长列表滚了一屏之后，用户想回到筛选条件或页面头部时，总要往上扒半天。回到顶部按钮就是为这个动作准备的：滚过阈值才出现，点一下平滑回去。

## 基础用法

<DemoBlock src="/demos/back-top/basic.vue" title="容器内滚动与带文字" desc="示例监听的是演示区里的滚动容器。" />

```vue
<div ref="scroller" class="list">…</div>
<jm-back-top :target="scroller" :visibility-height="200" />
```

不传 `target` 时监听 `window`，用于整页滚动；传 CSS 选择器或元素时跟随该容器的 `scrollTop`：

```vue
<jm-back-top target="#order-list" />
```

## 出现的时机

`visibility-height` 默认 200（约一屏多一点的 1/3）。实测下来 200~400 之间比较舒服：太小了刚滚一点就冒出来，太大会让人以为没有这个功能。

列表本身有「加载更多」时，注意不要把阈值设得比一屏还大，否则用户永远看不到它。

## 平滑回顶

`duration` 只用来决定是否开启浏览器原生的 `scroll-behavior: smooth`：

- `duration > 0`（默认 300）→ 平滑滚动；
- `duration = 0` → 瞬间跳回，适合数据量极大、滚动会卡的页面；
- 页面处于「关闭动效」模式（`data-motion="off"`）或系统 `prefers-reduced-motion` 时，组件会自动改成瞬间跳回。

## 局部定位

在弹窗、抽屉或演示框里用时，加 `inline`，按钮会变成 `position: absolute`，定位在最近的可定位祖先内，不会跑到浏览器视口右下角。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| target | 滚动容器，不传监听 window | `string \| HTMLElement` | - |
| visibilityHeight | 滚动超过多少才出现 | `number` | `200` |
| offset | 距右侧距离 | `number \| string` | `16` |
| bottom | 距底部距离 | `number \| string` | `40` |
| icon | 图标名 | `string` | `'chevron-up'` |
| text | 图标下方文字 | `string` | - |
| duration | 0 表示瞬间跳回 | `number` | `300` |
| zIndex | 层级 | `number` | `800` |
| inline | 绝对定位在父容器内 | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| click | 点击按钮 | `MouseEvent` |

## 性能

滚动监听是 `passive` 的，回调里只读一次 `scrollTop` 并写一个布尔值，不触发同步布局；`visible` 没变化时 Vue 不会重渲染。长期滚动的大列表也不会因此掉帧。
