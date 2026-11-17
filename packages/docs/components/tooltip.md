---
title: Tooltip 文字提示
description: 轻量气泡说明，支持鼠标悬停、键盘聚焦与移动端长按，空间不足自动翻转。
---

# Tooltip 文字提示

Tooltip 和 [Popover](/components/popover) 长得像，但用途完全不同：

| | Tooltip | Popover |
| --- | --- | --- |
| 内容 | 一句话说明 | 可以放按钮、表单 |
| 交互 | 不接收点击（`pointer-events: none`） | 可点、可输入 |
| 触发 | 悬停 / 聚焦 / 长按 | 点击 |
| 场景 | 解释图标含义、补充单位、说明为什么禁用 | 二次确认、筛选面板、操作菜单 |

一句话概括：**Tooltip 只负责「看懂」，Popover 负责「操作」**。需要用户在气泡里点东西，用 Popover。

## 基础用法

<DemoBlock src="/demos/tooltip/basic.vue" title="图标按钮说明、四个方向、长按与点击触发" desc="桌面端鼠标移上或键盘 Tab 到都会显示；移动端没有悬停，用 trigger=“longpress”。" />

```vue
<jm-tooltip content="刷新数据">
  <jm-button size="small" variant="outline"><jm-icon name="refresh" /></jm-button>
</jm-tooltip>

<jm-tooltip content="删除后不可恢复" theme="light" placement="top">
  <jm-button size="small" type="danger"><jm-icon name="trash" /></jm-button>
</jm-tooltip>
```

纯图标按钮没有文字，读屏和视觉用户都只能靠猜——给每个图标按钮配一句 `content` 是最低成本的可理解性提升。

## 三种触发方式

| `trigger` | 行为 | 适合 |
| --- | --- | --- |
| `hover`（默认） | 鼠标移入延迟 `show-delay`（120ms）出现，移出 60ms 后消失；键盘聚焦时立即出现 | 桌面端、文档、后台 |
| `longpress` | 长按 `longpress-duration`（450ms）出现，抬手后 `auto-hide-delay`（1.6s）自动消失；移动超 8px 视为滚动取消。**移动端用 touch 事件、PC 用鼠标按住**（应用打开在 PC 浏览器也能长按），两边自动适配不双触发 | 移动端 / PC |
| `click` | 点一下开、再点一下关 | 触屏与鼠标混用、需要停留阅读 |

用 `hover` 时最好也检查移动端：手机浏览器会把第一次点击当成 hover，导致「点一下只出现气泡、没触发按钮」的错觉。移动端项目建议统一改成 `longpress`。

## 自动翻转

气泡默认朝 `placement` 指定的方向展开，但**贴着屏幕边缘时会自动翻到对面**——上方放不下就翻到下方，右侧放不下就翻到左侧；上下方向如果左右越界，还会把对齐从居中改成左对齐或右对齐。

触发后先以 `opacity: 0` 渲染，量完位置再显示，所以翻转过程看不到跳动。`auto-flip: false` 可关掉这个逻辑（比如气泡内容会遮住重要信息，你希望它固定朝某个方向）。

## 主题与宽度

`theme="dark"`（默认）是深色底白字，适合浮在内容之上；`theme="light"` 白底描边，适合页面本身是浅色卡片、需要更弱的视觉重量。

`max-width` 默认 220px，超出自动换行。长文案不要靠 Tooltip 承载——超过两行就该写成页面里的说明文字。

## 组合用法

<DemoBlock src="/demos/tooltip/usage.vue" title="字段名旁的信息图标、禁用按钮的原因说明" desc="图标放在字段名后面，长按就能看到名词解释；禁用按钮外面包一层 flex 容器，否则部分浏览器不派发鼠标事件。" />

```vue
<jm-tooltip content="按实际调用次数计费，每小时结算一次" trigger="longpress" theme="light">
  <jm-icon name="info" class="hint" />
</jm-tooltip>
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| content | 提示文案 | `string` | - |
| placement | 展开方向 | `'top' \| 'bottom' \| 'left' \| 'right'` | `'top'` |
| align | 贴边对齐（左右方向忽略） | `'start' \| 'center' \| 'end'` | `'center'` |
| trigger | 触发方式 | `'hover' \| 'longpress' \| 'click' \| 'manual'` | `'hover'` |
| theme | 配色 | `'dark' \| 'light'` | `'dark'` |
| offset | 与触发元素的间距 | `number` | `8` |
| max-width | 面板最大宽度，数字按 px | `number \| string` | `220` |
| arrow | 显示小箭头 | `boolean` | `true` |
| disabled | 禁用 | `boolean` | `false` |
| show-delay | hover 出现延迟（ms） | `number` | `120` |
| hide-delay | 消失延迟（ms） | `number` | `60` |
| longpress-duration | 长按触发时长（ms） | `number` | `450` |
| auto-hide-delay | 长按抬手后多久收起（ms） | `number` | `1600` |
| auto-flip | 空间不足自动翻转 | `boolean` | `true` |
| z-index | 层级 | `number` | `1300` |
| show | 受控显示 | `boolean` | - |

### 事件

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:show | 显示状态变化 | `value: boolean` |
| show | 出现 | — |
| hide | 消失 | — |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| default | 触发元素 |
| content | 自定义气泡内容（富文本，但依然不可交互） |

### 方法

| 方法 | 说明 |
| --- | --- |
| show() | 强制显示 |
| hide() | 立即隐藏 |
| toggle() | 切换 |

## 无障碍

键盘用户 Tab 到触发元素时，`hover` 模式会立即显示气泡；气泡带 `role="tooltip"`，并通过 `aria-describedby` 关联到触发元素外层。

三个注意点：

1. **关键信息不要只放在 Tooltip 里**。读屏用户需要额外操作才能读到气泡，触屏用户也可能永远不会长按。必填规则、价格单位这类信息请直接写在页面上。
2. 触发元素本身要有可读名称（图标按钮加 `aria-label`），不要指望 Tooltip 的文案充当无障碍名称。
3. `trigger="hover"` 时移动端的行为取决于浏览器，正式项目里请显式改成 `longpress`。
