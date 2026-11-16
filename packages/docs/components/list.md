---
title: List 列表加载
description: 滚动到哨兵位置自动加载下一页，内置加载中、加载完、失败重试三种状态。
---

# List 列表加载

用 `IntersectionObserver` 观察列表末尾的哨兵节点，比监听 `scroll` 事件便宜得多：不产生每帧计算，也不会因为滚动容器嵌套而算错。

## 基础用法

<DemoBlock src="/demos/list/basic.vue" title="触底加载、加载完、失败重试" desc="v-model:loading 控制加载中；v-model:error 控制失败态；finished 表示没有更多。" />

## 必须回写 loading

一次 `load` 只发一次。业务侧务必在请求结束后把 `loading` 置回 `false`，否则不会再触发下一次加载。

「请求太快、哨兵一直在视口里」是常见卡点：`loading` 由 `true → false` 时组件会**补一次检查**，所以数据填满屏幕后仍能继续往下加载，不会卡住。

## 失败重试

`error` 为 `true` 时底部显示失败文案，点击会：

1. 派发 `update:error(false)` 清除失败态；
2. 派发 `click-error` 供业务决定是否重新请求；
3. 自动补一次 `check()`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:loading | 加载中 | `boolean` | `false` |
| v-model:error | 加载失败 | `boolean` | `false` |
| finished | 已加载全部 | `boolean` | `false` |
| loading-text | 加载中文案 | `string` | `'加载中...'` |
| finished-text | 加载完文案 | `string` | `'没有更多了'` |
| error-text | 失败文案 | `string` | `'加载失败，点击重试'` |
| immediate-check | 挂载后立即检查一次 | `boolean` | `true` |
| offset | 提前触发的距离（px） | `number` | `120` |
| direction | 触底加载 / 顶部加载 | `'down' \| 'up'` | `'down'` |
| disabled | 禁用加载 | `boolean` | `false` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| load | 需要加载下一页 | — |
| update:loading | 加载状态变化 | `value: boolean` |
| update:error | 失败状态变化 | `value: boolean` |
| click-error | 点击失败文案 | — |

### 实例方法

| 方法 | 说明 |
| --- | --- |
| check() | 手动检查一次是否该加载（例如筛选条件变化后重新拉取） |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 列表内容 |
