---
title: Watermark 水印
description: 讲义、试卷、截图防外传的平铺水印，支持文字、图片、旋转与透明度。
---

# Watermark 水印

用 canvas 画一块「单元格」，再交给 `background-repeat` 平铺——比 DOM 铺一堆文字轻得多，滚动时也不掉帧。

## 基础用法

<DemoBlock src="/demos/watermark/basic.vue" title="文字水印、多行、纯覆盖层" desc="水印层不接收指针事件，不影响选择、点击与滚动。" />

```vue
<jm-watermark text="金智安 · 内部资料" :opacity="0.12" :gap="[90, 66]" :rotate="-20">
  <div class="paper">…讲义内容…</div>
</jm-watermark>
```

## 两种用法

**包裹内容**（传插槽）：组件变成 `position: relative` 的容器，水印铺满整个内容区，随内容高度自适应。

**纯覆盖层**（不传插槽）：组件是 `position: absolute; inset: 0`，铺满**最近的定位祖先**，所以父容器必须有 `position: relative`。

**全屏**：`fullscreen` 改成 `position: fixed; inset: 0`，配合 `z-index` 压在最上层，适合「整站加水印」。

## 平铺与旋转

- `gap` 是单元格的间距 `[横, 纵]`，密度由它决定；水印越密越难裁剪，但越影响阅读；
- `rotate` 会先把内容旋转再计算外接矩形，保证旋转后不被裁掉；
- `fontSize` 同时影响单元格大小和文字大小；
- `offset` 整体偏移平铺起点，适合做「错行」效果。

## 图片水印

```vue
<jm-watermark image="/logo.png" text="内部资料" :opacity="0.1" />
```

图片与文字可同时存在（图片在上、文字在下）。注意跨域图片会污染画布，此时会静默降级为纯文字水印。

## 什么时候不管用

水印是**视觉威慑**，不是安全边界：

- 截图工具可以裁掉水印区域；
- 打印时可能不渲染背景图（浏览器默认不打印背景），需要业务侧加 `@media print`；
- 内容被程序化抓取时水印不参与文本。

真正防泄露还得靠权限、水印 + 审计日志组合。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| text | 文字水印，数组为多行 | `string \| string[]` | `''` |
| image | 图片水印地址 | `string` | - |
| opacity | 透明度 0~1 | `number` | `0.16` |
| gap | 间距 `[横, 纵]`，数字表示两者相同 | `number \| [number, number]` | `[80, 80]` |
| rotate | 旋转角度（deg） | `number` | `-22` |
| fontSize | 字号（px） | `number` | `14` |
| color | 文字颜色 | `string` | `#000000` |
| offset | 平铺起点偏移 | `[number, number]` | - |
| fullscreen | 固定全屏 | `boolean` | `false` |
| zIndex | 全屏时的层级 | `number` | `9` |

### Slots

| 插槽 | 说明 |
| --- | --- |
| default | 被保护的内容；不传则作为纯覆盖层 |
