---
title: VirtualList 虚拟列表
description: 长列表性能优化，只渲染可视区间；支持固定行高与动态行高。
---

# VirtualList 虚拟列表

上千行的列表一次性渲染会卡爆滚动。虚拟列表只渲染可视区前后各 `overscan` 行（默认 5 行），其余用高度占位——DOM 节点数恒定，滚动不再随数据量变重。

行高固定时用默认模式，滚动计算是纯算术，最省；聊天气泡、富文本评论这类**行高由内容决定**的列表，加一个 `dynamic` 让组件自己测量。

## 基础用法

<DemoBlock src="/demos/virtual-list/basic.vue" title="2000 行虚拟滚动与跳行" desc="只渲染可视区 ± overscan 行；scrollToIndex 可以直接跳到任意行，右上角实时显示当前首行。" />

## 用法

```vue
<template>
  <div style="height: 100vh">
    <jm-virtual-list :items="rows" :item-height="56">
      <template #item="{ item, index }">
        <div class="row">{{ index }}. {{ item.name }}</div>
      </template>
    </jm-virtual-list>
  </div>
</template>
```

- 不传 `height` 时组件撑满父容器，**父容器必须有确定高度**（flex 布局里用 `flex: 1; min-height: 0`）
- 固定行高模式下，行内容超过 `item-height` 会被裁切；行高不定的数据请打开 `dynamic`
- `item-key` 传字段名或函数，让 DOM 复用稳定；动态行高模式下已测量的高度也按 key 记，头部插入数据时高度不会错行

## 动态行高

数据来源不同（有的两行、有的六行，还夹着图片），固定行高只能全都按最大行撑开，很浪费。加 `dynamic` 后每行高度由内容决定，组件在渲染后逐行测量并更新位置：

<DemoBlock src="/demos/virtual-list/dynamic.vue" title="300 条聊天气泡，行高随内容变化" desc="item-height 退化为首屏估值；测量完成后内容总高会收敛到真实值。" />

```vue
<jm-virtual-list
  ref="listRef"
  :items="messages"
  dynamic
  :item-height="64"
  :estimated-item-height="64"
  item-key="id"
>
  <template #item="{ item }">
    <div class="bubble">{{ item.text }}</div>
  </template>
</jm-virtual-list>
```

三个细节决定了它好不好用：

- **估值只影响首屏**：`item-height` / `estimated-item-height` 是未测量行的占位高，量到真实高度后立刻替换。给一个「平均行高」比给「最大行高」更合适，滚动条长度不会一开始就很长。
- **滚动位置不跳**：如果视口上方某行被量出更高/更矮，后面的内容会整体位移。组件把这段增量补进 `scrollTop`，视觉上内容原地不动——否则一边往上滑一边自己被顶走，体验很糟。
- **宽度变化重新测量**：容器宽度变了会换行，旧高度全部失效。此时清空测量值按估值重排，再把可视行重测一遍（`ResizeObserver` 监听视口宽度）。

已知边界：行内图片未设尺寸时，图片加载完成会再次改变行高，视觉上会有一次跳动——给图片固定宽高比（或先占位）可以避免。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| items | 数据源 | `unknown[]` | — |
| item-height | 行高（px）；`dynamic` 下作为未测量行的估值 | `number` | `48` |
| dynamic | 动态行高：行高由内容决定，渲染后逐行测量 | `boolean` | `false` |
| estimated-item-height | 动态模式下未测量行的估值，优先于 `item-height` | `number` | `item-height` |
| overscan | 视口上下各多渲染几行 | `number` | `5` |
| height | 视口高度，不传撑满父容器 | `number \| string` | `100%` |
| item-key | 行 key：字段名或 `(item, index) => key` | `string \| function` | 索引 |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| scroll | 滚动（rAF 节流） | `offsetTop: number` |
| scroll-bottom | 滚到底部附近，可用来触发加载更多 | — |

### Slots

| 名称 | 说明 |
| --- | --- |
| item | 行内容，作用域 `{ item, index }` |

### Methods

| 方法 | 说明 |
| --- | --- |
| scrollToIndex(index, align?) | 定位到指定行，`align` 为 `'start'`（默认）/ `'center'` / `'end'` |
| scrollToBottom() | 滚到底部，适合聊天「跳到最新」 |
| refresh() | 清空已测量行高，按估值重新测量（数据整体替换、字号变化后调用） |
