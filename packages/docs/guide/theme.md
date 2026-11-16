# 主题与令牌

Jimu UI 的所有视觉都来自 CSS 变量，分三层：

| 层级 | 举例 | 谁来改 |
| --- | --- | --- |
| 原始层 primitive | `--jm-blue-500: #00a0e9` | 基本不动 |
| 语义层 semantic | `--jm-color-primary: var(--jm-blue-500)` | 换品牌色改这里 |
| 组件层 component | `--jm-button-radius: var(--jm-radius)` | 组件属性或外部覆盖 |

组件只引用语义层，所以换肤、换品牌色、适配适老，都不需要动组件代码。

## 品牌标识

Jimu UI 的标识是「三块积木拼成的 J」（mark-02-j-assembly），主色 `#5B5BD6`，与界面主色 `#00A0E9` 各司其职：标识用积木紫表达「拼装」，界面交互用品牌蓝。

<img src="/logo.svg" alt="Jimu UI 标识" width="96" style="margin: 12px 0;" />

使用规范：

| 场景 | 用法 |
| --- | --- |
| 页面 / 应用标识 | 直接引用 SVG：`<img src="logo.svg" alt="Jimu UI" />`，最小可用尺寸 24px |
| 单色场景 | 整体用 `currentColor` 或品牌色，不建议拆开重配色 |
| 间距 | 标识四周留白 ≥ 标识高度的 1/4，不与文字挤在一起 |
| 变形 | 可整体旋转 ±8° 以内表达「积木正在拼装」，但不拉伸、不换每块积木的相对位置 |

```html
<!-- HTML 引用 -->
<img src="/logo.svg" width="24" height="24" alt="Jimu UI" />

<!-- 或内联后用 CSS 控色 -->
<svg viewBox="0 0 64 64" fill="currentColor" class="jimu-mark">…</svg>
```

## 控件高度

移动端主控件高度统一为 **44px**（食指热区下限），由 `--jm-control-height-*` 三档控制，Button、Input、Search、Dialog 按钮等全部读同一组令牌，混排在同一屏时高度天然对齐：

| 档位 | 令牌 | 默认值 | 用在哪 |
| --- | --- | --- | --- |
| 小 | `--jm-control-height-sm` | 30px | 标签栏内的筛选按钮、Toast 文字按钮、tag 大图标旁的紧凑操作 |
| 中（默认） | `--jm-control-height-md` | 44px | Button、Input、Search、Dialog 填充按钮 —— **页面主控件一律用这档** |
| 大 | `--jm-control-height-lg` | 52px | 首屏大按钮（登录、提交订单）、整宽 CTA |

适老模式会把 `--jm-size-scale` 提到 1.12，三档同步变高，业务代码不用改。

<DemoBlock src="/demos/guide/control-height.vue" title="控件高度对齐" desc="Button、Input、Search 默认都是中档 44px，同一行混排不需要任何对齐 hack；整宽 CTA 与首屏大按钮升到大档 52px。" />

## 换主色

主色是 `#00A0E9`，其余颜色按同一明度曲线推导。要换成别的品牌色，只改这几行：

```css
:root {
  --jm-color-primary: #00a0e9;
  --jm-color-primary-hover: #0087c6;
  --jm-color-primary-active: #006ea3;
  --jm-color-primary-light: #e7f6fd;
  --jm-color-primary-border: #c4ebfb;
  --jm-color-primary-text: #0087c6;
}
```

| 用途 | 令牌 |
| --- | --- |
| 实心按钮、选中态、进度条 | `--jm-color-primary` |
| 按下 / hover | `--jm-color-primary-hover` |
| 激活 | `--jm-color-primary-active` |
| 浅色底（ghost 按钮、标签底） | `--jm-color-primary-light` |
| 描边（标签、输入框） | `--jm-color-primary-border` |
| 深色底上的文字 / 图标 | `--jm-color-primary-text` |

功能色同理：`--jm-color-success` `--jm-color-warning` `--jm-color-danger` `--jm-color-info`，每个都有 `-hover` `-active` `-light` `-border` `-contrast`。

::: tip 填充色上的文字用 -contrast
警告色是亮橙，白字会糊。所以实心按钮的文字色读的是 `--jm-color-warning-contrast`（深棕），不要硬写 `#fff`。
:::

## 日夜切换

三种方式，任选：

```ts
// 1. 代码控制（会同时设置 data-theme 与 .dark）
import { useAppearance } from 'jimu-ui'
const { isDark, setTheme, toggleTheme } = useAppearance()

setTheme('dark') // 'light' | 'dark' | 'auto'
toggleTheme()
```

```html
<!-- 2. 直接改属性 -->
<html data-theme="dark"></html>
```

```css
/* 3. 跟随系统（auto 模式下已内置，也可自己写媒体查询） */
@media (prefers-color-scheme: dark) {
  :root {
    --jm-color-primary-light: rgba(0, 160, 233, 0.16);
  }
}
```

夜间皮肤只重写语义层（见 `dark.css`）。注意一条规则：**实心填充色在夜间不往浅调**，否则白字对比度会掉；需要亮色文字时走 `--jm-color-primary-text`。

## 适老模式

```html
<html data-elder="true"></html>
```

```ts
const { setElder } = useAppearance()
setElder(true)
```

它做的事情只有四件：

1. `--jm-font-scale: 1.28`，所有字号按 `calc(px * var(--jm-font-scale))` 放大
2. `--jm-size-scale: 1.12`，控件高度、单元格高度同步变高
3. 正文行高 1.5 → 1.75，次要文字加深两档
4. 动效放慢一档（仍可用 `data-motion="off"` 全关）

因为是变量驱动，传入组件内部的文字（比如 `props.message`）也会一起变大，不需要另做一套组件。

## 全局调圆角与字号

```css
:root {
  --jm-radius: 12px; /* 所有组件默认圆角，等价于 --jm-radius-lg */
  --jm-font-scale: 1.1; /* 整体放大 10% */
  --jm-size-scale: 1.05; /* 控件高度 */
}
```

单个组件用属性覆盖，优先级更高：

```vue
<jm-button :radius="0">方角按钮</jm-button>
<jm-button radius="50%">胶囊按钮</jm-button>
<jm-input :radius="14" />
<jm-cell-group :radius="16" />
```

## 组件级变量覆盖

每个组件都暴露了自己的局部变量，可以直接在外部覆盖，需要的话再配合 `:deep()`：

```css
/* 只改这一处的按钮 */
.my-cta {
  --jm-button-radius: 4px;
}
```

```vue
<jm-button class="my-cta" type="primary">立即报名</jm-button>
```

常用局部变量：

| 组件 | 变量 |
| --- | --- |
| Button | `--jm-button-radius` |
| Input | `--jm-input-radius` |
| Tag | `--jm-tag-radius`、`--jm-tag-text` |
| Cell | `--jm-cell-radius`、`--jm-cell-bg` |
| CellGroup | `--jm-cell-group-radius`、`--jm-cell-group-bg` |
| Popup | `--jm-popup-radius` |
| Dialog | `--jm-dialog-radius` |
| Switch | `--jm-switch-active`、`--jm-switch-inactive` |
| Checkbox | `--jm-checkbox-active` |
| Radio | `--jm-radio-active` |
| Tabs | `--jm-tabs-color`、`--jm-tabs-radius` |

## 自定义颜色

按钮、标签支持直接传色值，浅底和描边会自动按 12% / 40% 透明度派生：

```vue
<jm-button color="#7C4DFF">紫色按钮</jm-button>
<jm-tag color="#FF6B00" plain>橙色标签</jm-tag>
```
