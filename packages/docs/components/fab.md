---
title: Fab 悬浮按钮
description: 固定在屏幕一角的圆形主行动按钮，可带文字、可切换激活态。
---

# Fab 悬浮按钮

页面里只有一个「最重要的事」时，用悬浮按钮把它固定在拇指够得着的右下角：新建作业、发起咨询、回到客服。

一个页面最多放一个。两个以上的悬浮按钮会互相抢注意力，也会挡住内容。

## 基础用法

<DemoBlock src="/demos/fab/basic.vue" title="位置、文字与展开菜单" desc="示例用 inline 把按钮限制在演示区域内。" />

```vue
<jm-fab icon="plus" @click="onCreate" />

<!-- 带文字 → 自动变胶囊 -->
<jm-fab icon="edit" text="写作业" position="left" />

<!-- 激活态：图标切成叉号 -->
<jm-fab :active="open" icon="plus" active-icon="close" @click="open = !open" />
```

## 位置

| 属性 | 说明 |
| --- | --- |
| `position` | `right`（默认）/ `left` |
| `offset` | 距侧边距离，默认 16 |
| `bottom` | 距底部距离，默认 24；会自动叠加 `env(safe-area-inset-bottom)`，全面屏不压手势条 |

`size` 控制直径（默认 48，正好是移动端最小点击区的 1.5 倍），有 `text` 时宽度由内容撑开、高度仍由 `size` 决定。

## 展开菜单

悬浮按钮点开后变叉号，是最常见的交互。把 `active` 绑到弹层显隐上，`active-icon` 换成 `close` 即可，按钮自己不做弹层——用什么弹层由业务选：

```vue
<jm-fab :active="open" active-icon="close" @click="open = !open" />
<jm-popup v-model:show="open" position="bottom" round>…</jm-popup>
```

`active` 不传时是**非受控**的，点击只抛事件、不改图标，适合单纯「新建」的场景。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| icon | 图标名 | `string` | `'plus'` |
| text | 文字，传了变胶囊 | `string` | - |
| position | 靠哪一侧 | `'right' \| 'left'` | `'right'` |
| bottom | 距底部 | `number \| string` | `24` |
| offset | 距侧边 | `number \| string` | `16` |
| size | 直径 | `number \| string` | `48` |
| color | 底色 | `string` | 主色 |
| textColor | 图标/文字颜色 | `string` | `#fff` |
| active | 激活态（受控） | `boolean` | - |
| activeIcon | 激活态图标 | `string` | `'close'` |
| zIndex | 层级 | `number` | `900` |
| teleport | 挂到 body | `boolean` | `true` |
| inline | 绝对定位在父容器内 | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| click | 点击 | `MouseEvent` |
| update:active | 受控时请求切换激活态 | `boolean` |

## 层级建议

`zIndex` 默认 900，低于 Popup（1000+）与 Toast（2000+），所以弹层和提示一定能盖住它。如果页面上还有自绘的吸底操作栏，记得把 `zIndex` 调到操作栏之下，别让按钮浮在操作栏上面。
