---
title: ActionSheet 动作面板
description: 从底部升起的一组操作项，替代右键菜单；标题区可换色、贴图，整张面板也能铺背景。
---

# ActionSheet 动作面板

移动端替代右键菜单的标准做法。危险操作放最后一行并染红，是这行的共识。

标题区与整张面板的背景都做成了可配置的：颜色、渐变、图片三种给法，配色和字号用 prop 或 CSS 变量调，不用担心「只能长成一个样」。

## 基础用法

<DemoBlock src="/demos/action-sheet/basic.vue" title="标题、说明与取消按钮" desc="action 支持 subLabel、color、disabled、icon、loading；选中后默认自动关闭。closeable 开启右上角关闭图标。" />

## 自定义关闭图标

<DemoBlock src="/demos/action-sheet/custom-close.vue" title="两种给图标的姿势" desc="close-icon 传 SVG 的 path d 值，适合单路径图标；#close-icon 插槽整块替换，放 img、放组件都可以。条目图标走 action.icon，同样是 path。" />

## 标题区配色与字号

<DemoBlock src="/demos/action-sheet/header-style.vue" title="渐变标题区" desc="title-background 收任意 CSS background，渐变、纯色都能写；title-color 给文字、title-size 给字号（数字按 px）。" />

## 标题区背景图

<DemoBlock src="/demos/action-sheet/header-image.vue" title="贴一张图当标题底" desc="title-image 传图片地址（自动补 url()），高度用 --jm-action-sheet-header-min-height 加高，文字用 title-color 转白。" />

## 整张面板的背景

<DemoBlock src="/demos/action-sheet/panel-background.vue" title="背景图与渐变色" desc="background 铺任意 CSS background，background-image 铺图片，background-mask 在图片上加一层提亮/压暗保证可读。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | `false` |
| actions | 操作项 | `ActionSheetAction[]` | `[]` |
| title | 标题 | `string` | — |
| description | 说明 | `string` | — |
| cancel-text | 取消按钮文字，传空串则不显示 | `string` | `'取消'` |
| closeable | 显示右上角关闭图标 | `boolean` | `false` |
| close-icon | 关闭图标的 SVG path d 值 | `string` | 内置 × |
| round | 圆角 | `boolean` | `true` |
| close-on-click-action | 选中后自动关闭 | `boolean` | `true` |
| cancel-gap | 取消按钮与列表之间留一条灰色间隙（Vant 同款），默认紧贴 | `boolean` | `false` |
| teleport | 挂载目标：`false` 就地渲染，字符串按选择器、元素直接挂载 | `boolean \| string \| Element` | `true` |
| title-background | 标题区背景，任意 CSS background 值（颜色 / 渐变 / `url(...)`） | `string` | — |
| title-image | 标题区背景图，图片地址，自动补 `url()`；盖在 `title-background` 之上 | `string` | — |
| title-color | 标题文字颜色 | `string` | `var(--jm-text-color)` |
| title-size | 标题字号，数字按 px | `number \| string` | `var(--jm-font-size-md)` |
| background | 面板整体背景，任意 CSS background 值（颜色 / 渐变 / `url(...)`） | `string` | `var(--jm-bg-elevated)` |
| background-image | 面板整体背景图，图片地址，自动补 `url()` | `string` | — |
| background-size | 背景图尺寸 | `string` | `'cover'` |
| background-position | 背景图位置 | `string` | `'center'` |
| background-mask | 背景之上的蒙层：`0`~`1` 数字生成黑色遮罩，字符串当 background 值（可传渐变） | `string \| number` | — |
| close-on-esc | 按 `Esc` 关闭（等同点取消） | `boolean` | `true` |
| trap-focus | 焦点锁在面板内，关闭后归还触发元素 | `boolean` | `true` |

### ActionSheetAction

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| name | 唯一标识 | `string \| number` |
| label | 主文案 | `string` |
| subLabel | 副文案 | `string` |
| icon | 图标，SVG 的 path d 值 | `string` |
| color | 文字色，危险操作用 `var(--jm-color-danger)` | `string` |
| disabled | 禁用 | `boolean` |
| loading | 加载中 | `boolean` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:show | 显示状态变化 | `boolean` |
| select | 选中某一项 | `(action, index)` |
| cancel | 点击取消或关闭图标 | — |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 追加在条目列表末尾的自定义内容 |
| header | 自定义整个头部（覆盖 title / description） |
| description | 说明区追加内容 |
| close-icon | 整块替换关闭图标 |
| cancel | 自定义取消按钮内容 |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-action-sheet-max-height` | 面板最大高度（默认 `80vh`，超出时列表内部滚动） |
| `--jm-action-sheet-header-min-height` | 标题区最小高度（默认 `52px`，贴背景图时加高） |
| `--jm-action-sheet-title-size` | 标题字号 |
| `--jm-action-sheet-title-color` | 标题颜色 |
| `--jm-action-sheet-subtitle-color` | 说明文字颜色（深色背景时转白） |
| `--jm-action-sheet-close-color` | 关闭图标颜色 |
| `--jm-action-sheet-cancel-color` | 取消按钮文字颜色 |
| `--jm-action-sheet-header-border` | 分割线颜色，贴背景图时传 `transparent` 去掉 |
| `--jm-action-sheet-cancel-gap-height` | 间隙模式下灰隙高度（默认 `10px`） |
| `--jm-action-sheet-cancel-gap-bg` | 灰隙颜色（默认 `var(--jm-gray-100)`，浅了就调它） |

::: tip 深色或图片背景上的文字
条目文字用的是全局 `--jm-text-color`，深色面板上把它改成白色即可，`--jm-text-color-2` / `--jm-text-color-3` 一起改掉主副文案才统一。
:::

::: tip 安全区
底部安全区由内置的 Popup 处理（`safe-area` 默认开），iPhone 全面屏上不会贴着 Home 条。
:::
