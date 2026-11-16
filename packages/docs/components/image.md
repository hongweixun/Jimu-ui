---
title: Image 图片
description: 图片占位、失败兜底、懒加载与淡入，圆角圆形一并支持。
---

# Image 图片

在原生 `<img>` 外面包了一层状态机：**加载中 / 成功 / 失败**。移动端弱网下最容易被忽略的是「图还没回来时的高度塌陷」——所以未指定宽高时用 `aspect-ratio` 兜底，而不是让占位图标把布局压成一条线。

## 基础用法

<DemoBlock src="/demos/image/basic.vue" title="占位、fit、失败兜底、懒加载" desc="loading / error 都有默认占位与对应插槽；lazy 进入视口前不写 src；fade 让加载完成后淡入。" />

## 懒加载

`lazy` 内部用 `IntersectionObserver` 实现，提前 50px 开始加载。列表里的图片务必打开，长列表一次请求几百张图会直接把首屏拖慢。

::: tip 与浏览器原生 loading="lazy" 的区别
原生 `loading="lazy"` 的触发距离由浏览器决定（Chrome 约为 1250px），不可控；组件内实现可以精确控制提前量，也方便做统一的占位样式。
:::

## 圆形头像

`round` 会把圆角固定成 50%，并忽略 `radius`。头像场景建议同时固定 `width` / `height`，否则圆形会变成椭圆。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| src | 图片地址 | `string` | — |
| alt | 替代文本 | `string` | — |
| width | 宽度（数字按 px） | `number \| string` | — |
| height | 高度（数字按 px） | `number \| string` | — |
| fit | 填充方式 | `'fill' \| 'contain' \| 'cover' \| 'none' \| 'scale-down'` | `'cover'` |
| radius | 圆角 | `number \| string` | — |
| round | 圆形 | `boolean` | `false` |
| lazy | 进入视口再加载 | `boolean` | `false` |
| show-loading | 显示加载占位 | `boolean` | `true` |
| show-error | 显示失败占位 | `boolean` | `true` |
| loading-text | 加载文案 | `string` | — |
| error-text | 失败文案 | `string` | `'加载失败'` |
| fade | 加载完成淡入 | `boolean` | `true` |
| block | 块级、占满父宽 | `boolean` | `false` |
| clickable | 可点击（放大预览等外部处理） | `boolean` | `false` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| load | 图片加载完成 | `event: Event` |
| error | 加载失败 | `event: Event` |
| click | 点击 | `event: MouseEvent` |

### Slots

| 名称 | 说明 |
| --- | --- |
| loading | 自定义加载占位 |
| error | 自定义失败占位 |
