---
title: PullRefresh 下拉刷新
description: 到顶下拉触发刷新，带阻尼、释放提示与刷新成功反馈。
---

# PullRefresh 下拉刷新

只在**滚动容器已经到顶部**时接管手势，其余情况把纵向滚动完全交给浏览器——下拉刷新最容易踩的坑就是"整个列表突然不能滚了"。

## 基础用法

<DemoBlock src="/demos/pull-refresh/basic.vue" title="下拉刷新与禁用" desc="v-model 绑定 loading；refresh 事件里发起请求，结束后把 loading 置回 false。" />

## 状态流转

```
normal ──下拉→ pulling ──超过阈值→ loosing ──松手→ loading ──loading=false→ success ──500ms→ normal
```

- **阻尼**：位移 = 手指位移 × 0.55，最多拉到头高的 1.8 倍，越拉越沉；
- **成功提示**：`loading` 从 `true` 变 `false` 后先显示「刷新成功」停留 `success-duration`，再回弹归零；
- **中途上推**：还没松手就往上推，状态立刻回到 `normal`，手感上不会"卡在半空"。

## 与滚动容器的关系

组件向上找最近的可滚动祖先（`overflow-y: auto/scroll` 且内容溢出），判断它是否 `scrollTop <= 0`；找不到祖先就看整页滚动位置。所以既可以放在整页最外层，也可以放在固定高度的滚动盒子里。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 是否加载中 | `boolean` | `false` |
| disabled | 禁用下拉 | `boolean` | `false` |
| head-height | 触发刷新的下拉距离（px） | `number` | `50` |
| pulling-text | 下拉中文案 | `string` | `'下拉刷新'` |
| loosing-text | 释放文案 | `string` | `'释放刷新'` |
| loading-text | 加载中文案 | `string` | `'加载中...'` |
| success-text | 成功文案 | `string` | `'刷新成功'` |
| success-duration | 成功文案停留时长（ms） | `number` | `500` |
| animation-duration | 回弹动画时长（ms） | `number` | `300` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 加载状态变化 | `value: boolean` |
| refresh | 触发刷新（此时 modelValue 已置 true） | — |
| change | 状态变化 | `'normal' \| 'pulling' \| 'loosing' \| 'loading' \| 'success'` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 可下拉的内容 |
