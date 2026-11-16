---
title: Card 卡片
description: 图文容器，封面可放上方或左侧，内置标题、描述、标签、价格与页脚操作区。
---

# Card 卡片

列表里一条商品、一篇文章、一张订单，结构都是「图 + 标题 + 一行说明 + 价格/状态 + 操作」。每次手写这套 DOM 都要重新算间距、对齐封面比例，Card 把它固化成两个布局：

- `thumb-position="top"`：图文卡片，封面按比例撑开在上方，适合信息流、商品橱窗。
- `thumb-position="left"`：列表卡片，方形缩略图在左、文字在右，适合订单、消息、设置项。

## 基础用法

<DemoBlock src="/demos/card/basic.vue" title="图文卡片：封面、标签、价格与页脚" desc="价格传数字自动格式化（¥199.00、千分位），传字符串则原样输出；封面按 16:9 撑开，图片没加载完也不会跳动。" />

```vue
<jm-card
  title="零基础学 Vue 3 组合式 API"
  desc="从 setup 到 composable，用 12 个小项目把响应式吃透"
  :thumb="cover"
  :price="199"
  :origin-price="399"
  :tags="['共 24 讲', '可回放']"
  extra="1.2 万人学过"
  clickable
  shadow="always"
>
  <template #footer>
    <jm-button size="small" variant="outline">查看详情</jm-button>
    <jm-button size="small">立即报名</jm-button>
  </template>
</jm-card>
```

## 左侧封面（列表卡片）

`thumb-position="left"` 切成两栏：左边固定宽度的方形缩略图，右边文字区。`thumb-fit="contain"` 适合商品图这种不能被裁切的场景。

<DemoBlock src="/demos/card/list.vue" title="订单列表卡：左图、状态、页脚按钮" desc="extra 放「待收货 / 已完成」这类状态文案；页脚自带分割线，按钮上记得加 .stop 阻止冒泡，否则点按钮会连带触发整卡点击。" />

```vue
<jm-card
  title="青柠气泡水 × 6 瓶"
  desc="下单时间 11-16 14:02 · 顺丰配送"
  :thumb="img"
  :price="39.9"
  extra="待收货"
  thumb-position="left"
  clickable
  @click="openOrder"
>
  <template #footer>
    <jm-button size="small" variant="outline" @click.stop>查看物流</jm-button>
    <jm-button size="small" @click.stop="confirm">确认收货</jm-button>
  </template>
</jm-card>
```

## 封面比例

| 布局 | `thumb-ratio` 默认 | 说明 |
| --- | --- | --- |
| `top` | `16 / 9` | 传 `1` 得到正方形，传 `4 / 3` 得到 4:3 |
| `left` | `1` | 固定宽度 96px（`--jm-card-thumb-w` 可覆盖），高度按比例算 |

比例用 `padding-top` 撑开而不是 `aspect-ratio`，是为了兼容旧版 WebView——图片没加载出来时占位高度就已经是最终高度，列表不会因为图片陆续到达而抖动。

## 描边与阴影

| `shadow` | 效果 | 场景 |
| --- | --- | --- |
| `never`（默认） | 只有 1px 描边（`bordered` 控制） | 列表页，卡片多、要克制 |
| `always` | 无描边 + 常驻阴影 | 信息流、单品推荐 |
| `hover` | 默认浅阴影，悬停加深 | 桌面端可点卡片 |

`bordered` 与 `shadow` 是互斥视觉：开阴影时描边自动让位，避免「阴影 + 硬边」叠在一起的脏边。

## 可点击

`clickable` 会给整卡加 `role="button"`、`tabindex="0"`、回车/空格触发，以及按下时的轻微缩放反馈；`ripple` 默认跟随 `clickable`，想保留缩放但不要水波纹就显式传 `:ripple="false"`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 标题，最多两行省略 | `string` | - |
| desc | 标题下方的说明，最多两行省略 | `string` | - |
| thumb | 封面图地址 | `string` | - |
| thumb-position | 封面位置 | `'top' \| 'left'` | `'top'` |
| thumb-ratio | 封面宽高比 | `number \| string` | `16/9`（top）/ `1`（left） |
| thumb-fit | 封面填充方式 | `'cover' \| 'contain'` | `'cover'` |
| extra | 右上角附加文案（状态、时间） | `string` | - |
| price | 价格，数字格式化、字符串原样 | `number \| string` | - |
| origin-price | 划线原价 | `number \| string` | - |
| tags | 标题下方标签 | `string[]` | - |
| bordered | 1px 描边 | `boolean` | `true` |
| shadow | 阴影 | `'always' \| 'hover' \| 'never'` | `'never'` |
| round | 圆角，`false` 去圆角，数字按 px | `boolean \| number \| string` | `true` |
| clickable | 整卡可点 | `boolean` | `false` |
| ripple | 水波纹，默认跟随 clickable | `boolean` | - |
| lazy | 封面懒加载 | `boolean` | `true` |

### 事件

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| click | 点击卡片（`clickable` 时） | `event: MouseEvent` |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| thumb | 自定义封面（视频、轮播、角标） |
| title | 自定义标题 |
| extra | 自定义右上角 |
| default | 正文区 |
| footer | 页脚操作区，自带分割线与右对齐 |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-card-radius` | 圆角 | `--jm-radius-lg` |
| `--jm-card-padding` | 内边距 | `14px` |
| `--jm-card-thumb-w` | 左侧封面宽度 | `96px` |
| `--jm-card-price-color` | 价格颜色 | `--jm-color-danger` |

## 无障碍

`clickable` 时卡片带 `role="button"` 与键盘触发，焦点环沿用全局 `:focus-visible` 令牌。封面图是装饰性的（标题已表达信息），统一 `alt=""`；如果封面本身承载信息（例如无文字的图集），用 `#thumb` 插槽自己写 `<img alt="...">`。价格用真实文本渲染而非伪元素，读屏会读出「¥199.00」。
