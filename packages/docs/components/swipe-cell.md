---
title: SwipeCell 滑动单元格
description: 左滑或右滑露出操作按钮，用于列表里的删除、归档、标记等高频操作。
---

# SwipeCell 滑动单元格

移动端列表的「左滑删除」几乎是标配。`jm-swipe-cell` 用 Pointer Events 实现，鼠标和手指都能拖；横向手势自己接管，纵向滚动照常交给页面。

## 基础用法

<DemoBlock src="/demos/swipe-cell/basic.vue" title="左滑删除、双侧按钮、编程控制、禁用" desc="按钮放进 left/right 插槽，宽度由内容自然撑开，也可用 left-width/right-width 固定。" />

## 插槽决定按钮

```vue
<jm-swipe-cell>
  <jm-cell title="作业批改提醒" label="32 份待批改" />
  <template #right>
    <button class="danger" @click="remove">删除</button>
    <button @click="archive">归档</button>
  </template>
</jm-swipe-cell>
```

- 按钮**从右往左**排列，最右侧是「删除」这类破坏性操作；
- 没有对应的插槽，该方向就拖不动（带阻尼反馈，不是硬顶）；
- 按钮样式完全由业务决定，组件只负责「露出」。

## 交互细节

| 行为 | 处理方式 |
| --- | --- |
| 手势方向判定 | 位移超过 6px 才判定，横向优先；判为纵向立即交还页面滚动 |
| 打开阈值 | 拖过按钮宽度的 40%（`threshold`），或甩动速度超过 0.35px/ms |
| 多单元格 | 默认打开一个时自动收起其他（`auto-close-others`） |
| 点击空白 | 全局 `pointerdown` 监听，点外部收起 |
| 滑动后的误触 | 滑动结束会吞掉一次 `click`，不会连带触发列表项跳转 |
| 已打开时点内容 | 先收起，不派发 `click` |

## 编程控制

```vue
<jm-swipe-cell ref="cellRef" open-side="right">
  ...
</jm-swipe-cell>
```

通过 ref 调用 `open('left' | 'right')`、`close()`、`toggle(side)`，`open-side` 可以在挂载时直接展开。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| disabled | 禁用滑动 | `boolean` | `false` |
| leftWidth | 左侧按钮总宽（不传按内容测量） | `number \| string` | — |
| rightWidth | 右侧按钮总宽（不传按内容测量） | `number \| string` | — |
| threshold | 打开阈值，占按钮宽度比例 | `number` | `0.4` |
| autoCloseOthers | 打开时收起其他单元格 | `boolean` | `true` |
| openSide | 初始打开方向 | `'left' \| 'right' \| null` | `null` |
| closeOnAction | 点击按钮后自动收起 | `boolean` | `false` |
| beforeClose | 收起前钩子，返回 false / reject 则不收起 | `({ side, action, event }) => boolean \| Promise<boolean>` | — |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| open | 展开 | `side: 'left' \| 'right'` |
| close | 收起 | — |
| click | 点击内容区（未发生滑动时） | `MouseEvent` |
| action | 点击了左右侧按钮 | `(side, event)` |

## 操作前二次确认

删除这类不可逆操作，点按钮到真的收起之间应该问一句。`beforeClose` 返回 Promise 时，按钮进入 loading 且不会重复触发，确认后才收起：

<DemoBlock src="/demos/swipe-cell/before-close.vue" title="删除前确认" desc="需要配合 close-on-action 使用，否则组件不接管点击后的收起动作。" />

```vue
<jm-swipe-cell close-on-action :before-close="beforeClose">
  <jm-cell title="期末成绩单" />
  <template #right>
    <button :data-id="row.id">删除</button>
  </template>
</jm-swipe-cell>
```

```ts
function beforeClose({ side, action, event }) {
  const id = Number(action.dataset.id)   // 按钮自己能带上下文
  return new Promise<boolean>((resolve) => showConfirm(resolve))
}
```

- `close-on-action`（默认 `false`）：组件替你接管「点按钮 → 收起」，老项目不传就维持原来的「业务自己调 `close()`」。
- `beforeClose` 返回 `false` 或 reject → 保持展开；返回 `true` / 不返回 → 收起。
- 异步期间被点的那个按钮加 `opacity: .65` 且不可再次点击。
- 无论是否开启 `closeOnAction`，点击都会先发 `action` 事件，埋点用得上。

## Slots

| 名称 | 说明 |
| --- | --- |
| default | 单元格内容 |
| left | 右滑露出的按钮 |
| right | 左滑露出的按钮 |

### Expose

| 方法 | 说明 |
| --- | --- |
| `open(side)` | 展开指定方向 |
| `close()` | 收起 |
| `toggle(side)` | 切换 |
| `offset` | 当前位移（px，正数向右） |
