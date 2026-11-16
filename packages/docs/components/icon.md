---
title: Icon 图标
description: 一套 24×24 的描边图标，按名字引用，大小跟随字号，业务可自行注册。
---

# Icon 图标

移动端大量场景需要小图标：列表箭头、状态提示、入口图标。组件库内置一套 24×24 描边图标（`stroke: currentColor`），统一由 `jm-icon` 渲染，避免各组件各写一份内联 SVG。

## 基础用法

<DemoBlock src="/demos/icon/basic.vue" title="尺寸、颜色、旋转与内置图标清单" desc="size 默认 1em，跟着父级字号走；颜色默认继承文字色，配合 currentColor 可直接换主题色。" />

## 尺寸与颜色

```vue
<jm-icon name="star-fill" :size="20" color="#FFB300" />
<jm-icon name="graduation-cap" :size="28" color="var(--jm-color-primary)" />
```

`size` 传数字按 px，传字符串则原样使用（`'1.2rem'`、`'24px'` 都可以）。默认 `1em` 的好处是：字号变了图标跟着变，不用一处处改。

## 旋转

- `spin`：持续旋转，用于 loading 类图标；
- `rotate`：固定角度，数字按 `deg`。

```vue
<jm-icon name="loading" spin />
<jm-icon name="chevron-right" :rotate="180" />
```

## 注册自定义图标

业务图标不必等组件库更新，注册一次就能按名字用：

```ts
import { registerIcon } from 'jimu-ui'

registerIcon('school', 'M3 9.6L12 5l9 4.6-9 4.6z')          // 单个 path
registerIcon('logo', ['M4 4h16v16H4z', 'M8 8h8v8H8z'])        // 多段 path
registerIcon('badge', { paths: ['...'], filled: true })        // 实心图标
```

`filled: true` 的图标用 `fill: currentColor` 绘制，适合星标、播放键这类实心造型。

## 未注册的名字

`name` 找不到时只在控制台告警一次，并渲染一个 `1em` 的透明占位，**不会让布局塌掉**。所以灰度期漏配图标时页面还能用。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 图标名，支持别名（如 `arrow` → `chevron-right`） | `string` | — |
| size | 尺寸，数字按 px | `number \| string` | `1em` |
| color | 颜色，默认继承 `currentColor` | `string` | — |
| spin | 持续旋转 | `boolean` | `false` |
| rotate | 固定旋转角度，数字按 deg | `number \| string` | — |
| strokeWidth | 描边粗细（实心图标无效） | `number` | `1.8` |
| label | 无障碍标签；不传视为纯装饰 | `string` | — |

### 工具函数

| 方法 | 说明 |
| --- | --- |
| `registerIcon(name, def)` | 注册/覆盖图标，`def` 可为 path 字符串、字符串数组或 `{ paths, filled, viewBox }` |
| `hasIcon(name)` | 是否已注册 |
| `iconNames()` | 全部图标名（做图标选择器用） |
| `icons` | 图标表本身，只读遍历用 |

### 内置图标分组

| 分组 | 图标 |
| --- | --- |
| 方向 | `chevron-left` `chevron-right` `chevron-up` `chevron-down` `arrow-left` `arrow-right` `arrow-up` `arrow-down` `arrow-up-left` |
| 操作 | `check` `close` `plus` `minus` `search` `more-horizontal` `more-vertical` `refresh` `loading` |
| 状态 | `check-circle` `close-circle` `warning` `info` `star` `star-fill` `heart` `heart-fill` `eye` `eye-close` `lock` `unlock` |
| 业务 | `user` `users` `phone` `mail` `location` `calendar` `clock` `home` `setting` `bell` `camera` `image` `file` `book` `graduation-cap` |
| 更多 | `download` `upload` `trash` `edit` `filter` `sort` `cart` `gift` `wallet` `qr-code` `share` `link` `scan` `mic` `play` `pause` `volume` `wifi` `sun` `moon` `lightning` |
