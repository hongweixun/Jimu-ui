---
title: Drag 拖拽
description: 让任意元素可以自由拖拽，支持方向限制、边缘吸附、范围约束，Pointer 事件鼠标触摸通用。
---

# Drag 拖拽

让任意元素（悬浮操作球、可拖动的角标、排序手柄等）可以按住拖动。内部用 Pointer 事件实现，鼠标、触摸、触控笔统一支持；按住拖动与单击通过位移阈值区分，拖动过的松手不会触发 click。

## 基本使用

<DemoBlock src="/demos/drag/basic.vue" title="拖拽、方向限制、吸附、重置" desc="按住拖动；direction 限制方向；attraction 松手吸附到最近的边；ref.reset() 重置位置。" />

```vue
<jm-drag target="#stage" style="left: 40px; top: 30px">
  <jm-fab />
</jm-drag>
```

## 拖拽方向

`direction` 限制可拖动的轴向：`x`（只能横向）、`y`（只能纵向）、`xy`（默认，自由拖）。

## 边缘吸附

`attraction` 让元素在松手后吸附到最近的边：`x` 吸附左右、`y` 吸附上下、`xy` 双向。常见用法是「悬浮球贴边停靠」：

```vue
<jm-drag attraction="x" style="left: 40px; top: 60px">
  <jm-icon name="customer-service" />
</jm-drag>
```

## 拖拽范围

`boundary` 设置元素到视口（或 `target` 容器）四边的最小留白，元素始终留在范围内：

```vue
<jm-drag :boundary="{ top: 80, bottom: 80, left: 12, right: 12 }">
  <jm-button type="primary">拖拽区域</jm-button>
</jm-drag>
```

## 约束在容器内

默认相对**视口**拖动（fixed 定位）。传 `target` 选择器后改为在容器内绝对定位拖拽，跟随容器滚动，适合面板、抽屉内部的可拖动元素。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| direction | 拖拽方向，可选 `x` `y` `xy` | `string` | `'xy'` |
| attraction | 吸附方向，可选 `x` `y` `xy`，不传则停在松手位置 | `string` | - |
| disabled | 禁用拖拽 | `boolean` | `false` |
| boundary | 距视口/容器四边的留白 | `{ top?, bottom?, left?, right? }` | `{}` |
| zIndex | 拖拽元素层级 | `number \| string` | `90` |
| teleport | 挂载位置，`false` 原地渲染 | `string \| false` | `false` |
| target | 约束容器选择器，传入后在容器内拖拽 | `string \| false` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| click | 单击（未拖动）时触发；拖动过的松手不会触发 | `event: Event` |

### 方法

| 方法 | 说明 |
| --- | --- |
| reset | 重置到初始位置 |
| resize | 容器尺寸变化后调用，把元素拉回合法范围（窗口 resize 自动触发） |

::: warning 初始位置
拖拽元素是 fixed/absolute 定位，必须通过 `style="left: ...; top: ..."` 给初始位置；`reset()` 会回到这个初始位置。
:::
