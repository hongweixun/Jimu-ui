# 适老与无障碍

## 适老模式的边界

适老是"放大 + 加厚 + 放慢"，不是"简化功能"。所有组件共用同一份代码，只多一组变量：

- 字号基准 ×1.28，控件高度 ×1.12，触控区最小 52px
- 正文行高 1.75，次要文字整体加深两档，避免灰字看不清
- 边框颜色加深，解决浅色描边在高龄用户屏幕上"看不见"的问题
- 动效整体慢一档、位移距离砍三分之一（减少眩晕，详见[动效系统](/guide/motion#适老模式)）

```html
<html data-elder="true"></html>
```

局部使用也可以，只影响这个容器内的组件：

```html
<div data-elder="true">
  <jm-cell-group title="长辈模式预览">
    <jm-cell title="字号已经放大" value="1.28×" />
  </jm-cell-group>
</div>
```

## 关闭动效的三种方式

```html
<!-- 1. 全局开关，最常用 -->
<html data-motion="off"></html>
```

```ts
// 2. 代码控制
import { useAppearance } from 'jimu-ui'
const { setMotion } = useAppearance()
setMotion(false)
```

```html
<!-- 3. 只关闭某一块区域 -->
<div data-motion="off">
  <jm-button>这块区域没有动效</jm-button>
</div>
```

第三种能生效是因为时长变量沿 DOM 继承，组件读到的是 0ms。系统层面也做了兜底：用户开了「减少动态效果」时自动静止。开关的完整机制与"必要动效白名单"见[动效系统](/guide/motion#关掉动效)。

## 键盘与焦点

移动端也要能用键盘：教室一体机、外接键盘的平板、桌面浏览器预览，还有读屏软件用户。组件库这一层做三件事。

### 焦点环

键盘 Tab 到任何组件上都会出现一圈实心焦点环，鼠标 / 手指点按则不出现（`:focus-visible` 的语义）：

```css
--jm-focus-ring-color: var(--jm-color-primary); /* 换品牌色自动跟随 */
--jm-focus-ring-width: 2px;                     /* 适老模式 3px */
--jm-focus-ring-offset: 2px;
```

已经有自己焦点光晕的组件（Button、Checkbox、Radio、Rate、Segmented 等）不会叠两层；输入框仍用"边框变色"这一套，不加描边。

### 模态弹层的焦点陷阱

Dialog、Popup（`trap-focus`）、ActionSheet、ImagePreview 打开后会：

1. 把焦点移进弹层，Tab / Shift+Tab 在弹层内首尾循环，不会跑到背后的页面上
2. 按 `Esc` 关闭（Dialog 与 ActionSheet 默认开，Popup 需 `close-on-esc`）
3. 关闭后把焦点还给打开它的那个元素，键盘用户不用重新从头 Tab

叠了多个弹层时，`Esc` 只关最上面那层。

### 组件键盘速查

| 组件 | 按键 | 行为 |
| --- | --- | --- |
| Dialog / ActionSheet | `Esc` | 关闭（走 `beforeClose`，等同点取消） |
| Popup | `Esc` | 关闭（`close-on-esc` 开启时） |
| ImagePreview | `←` `→` | 上一张 / 下一张 |
| ImagePreview | `Home` `End` | 第一张 / 最后一张 |
| ImagePreview | `+` `-` `0` | 放大 / 缩小 / 缩放复位 |
| ImagePreview | `Esc` | 关闭 |
| Tabs / Segmented | `←` `→`（`↑` `↓`） | 切换到相邻标签，跳过禁用项 |
| Tabs / Segmented | `Home` `End` | 第一个 / 最后一个标签 |
| Cell（clickable） | `Enter` | 触发点击 |
| Rate | `←` `→` | 调整分值 |
| Switch / Stepper / Slider | 原生控件按键 | 由浏览器与系统提供 |

Tabs 与 Segmented 用 roving tabindex：整组标签对外只占一个 Tab 停靠点，进去之后用方向键横移。十个标签的页面不会让用户按十一次 Tab 才能穿过去。

## 无障碍要点

组件层已经处理的部分：

| 项 | 做法 |
| --- | --- |
| 键盘焦点 | 所有可点元素带 `:focus-visible` 焦点环，令牌见上 |
| 焦点管理 | 模态弹层焦点陷阱 + 关闭归还，`Esc` 关闭最上层 |
| 语义标签 | Switch 用 `role="switch"` + `aria-checked`；Tabs 用 `role="tablist"/"tab"/"tabpanel"`；Popup/Dialog 用 `role="dialog"` + `aria-modal` + `aria-labelledby` |
| 屏幕阅读器 | 纯图标按钮（关闭、清空）都有 `aria-label`；装饰性 SVG 一律 `aria-hidden="true"`；图片预览用 `aria-live` 播报「第 3 张，共 9 张」 |
| 触控尺寸 | 可点元素最小 44×44（适老 52），Cell 最小高度 48 |
| 对比度 | 正文 `--jm-text-color` 对背景 ≥ 7:1，次要文字 ≥ 4.5:1 |
| 高对比度 | 系统开启「增强对比度」时焦点环自动加粗到 3px |
| 动效 | 任意动效都能一键关停，不依赖动画传达信息 |

只给读屏软件的文案用 `.jm-visually-hidden` 包一层，不要用 `display: none`：

```html
<span class="jm-visually-hidden">当前选中第 3 项，共 9 项</span>
```

接入方需要自己保证的：

1. 每个页面有唯一的 `h1`，层级不跳
2. 图片有 `alt`，纯装饰留空
3. 表单错误提示用文字说明，不只用红色边框
4. 自定义弹层记得给 `aria-label` 或标题，别让读屏软件只念出"对话框"
