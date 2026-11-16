---
title: Input 输入框
description: 单行文本输入，三种外观、三种尺寸，浮动标签、下划线展开动效、清空与字数统计。
---

# Input 输入框

移动端表单的基础。**字号被强制锁在 `max(16px, --jm-font-size-md)`**——低于 16px 时 iOS Safari 聚焦会自动放大整页，这个坑在组件里就堵掉了。

聚焦动效参照 Varlet 的 FieldDecorator（已按本项目令牌体系收敛）：

- **标签上浮**：传入 `label` 后，空值未聚焦时它就是占位文案；聚焦或有值后以 280ms 上浮并缩到 0.75——`outline` 落在边框上、`filled` 落在框内顶部、`underlined` 浮到框外上方
- **下划线展开**：`underlined` 外观聚焦时，一条 2px 主色高亮线从中心 `scaleX(0) → scaleX(1)`（300ms），只动 transform 不引起重排
- **颜色过渡**：标签、光标、前后缀图标统一跟随主色（200ms）；清空按钮出现时带 160ms 的缩放弹入

全部走动效令牌，`data-motion="off"` 或系统「减弱动态效果」开启时瞬时到位。

## 基础用法

<DemoBlock src="/demos/input/basic.vue" title="浮动标签、外观、尺寸与附加内容" desc="传 label 即进入浮动标签模式；variant 三种外观对表单密度不同的场景都能覆盖；前缀插槽适合放搜索图标、+86 区号。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 输入值 | `string \| number` | — |
| type | 原生 type，`textarea` 时渲染多行文本域 | `string` | `'text'` |
| placeholder | 占位文案 | `string` | — |
| label | 标签；配合 label-placement 决定浮动还是固定在上 | `string` | — |
| label-placement | 标签位置：`float` 浮动上浮 / `top` 固定在输入框上方（配合 `variant="plain"` 即 Vant 的 `label-align="top"` 顶部对齐）/ `left` 固定在左侧（Vant Field 行式排版，配合 `variant="plain"` + 外部卡片） | `'float' \| 'top' \| 'left'` | `'float'` |
| label-width | `left` 模式下标签列宽 | `number \| string` | `'96px'` |
| colon | `left` 模式下 label 后追加冒号 | `boolean` | `false` |
| required | 必填：label 前显示红色星号 | `boolean` | `false` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| variant | 外观 | `'outline' \| 'filled' \| 'underlined' \| 'plain'` | `'outline'` |
| radius | 圆角（推荐小圆角如 `'10px'`，数字按 px） | `number \| string` | `var(--jm-radius)` |
| clearable | 可清空 | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| readonly | 只读 | `boolean` | `false` |
| error | 校验失败态：描边、标签与光标转红 | `boolean` | `false` |
| error-message | 错误提示文案（为 Form 校验预留）；plain 外观时渲染在输入行内、紧贴输入内容，其余外观显示在输入框下方 | `string` | — |
| error-align | 错误提示文案对齐，不传时默认跟随 `align` | `'left' \| 'center' \| 'right'` | 跟随 `align` |
| error-color | 错误提示文案颜色 | `string` | `var(--jm-color-danger)` |
| autocomplete | 原生 autocomplete | `string` | — |
| maxlength | 最大长度 | `number` | — |
| show-word-limit | 显示字数统计 | `boolean` | `false` |
| align | 文字对齐 | `'left' \| 'center' \| 'right'` | `'left'` |
| inputmode | 移动端键盘类型 | `'text' \| 'numeric' \| 'decimal' \| 'tel' \| 'email' \| 'search' \| 'url'` | — |
| autosize | textarea 内容撑开高度 | `boolean` | `false` |
| rows | textarea 行数（非 autosize 时按此定高） | `number` | `3` |
| max-height | textarea autosize 时的最大高度 | `number \| string` | — |
| prefix-text | 固定前缀文案，带分隔竖线（如 `+86`）；放图标用 `#prefix` 插槽 | `string` | — |
| code | 内嵌「获取验证码」按钮 | `boolean` | `false` |
| code-text | 验证码按钮文案 | `string` | `'获取验证码'` |
| code-shape | 验证码按钮形状：`auto` 跟随输入框自身圆角（输入框是胶囊按钮才是胶囊）/ `pill` 强制胶囊 / `square` 方形 | `'auto' \| 'pill' \| 'square'` | `'auto'` |
| code-type | 验证码样式：`button` 实心按钮 / `text` 纯文字链接（主色文字、无底色） | `'button' \| 'text'` | `'button'` |
| code-duration | 验证码倒计时秒数（点击后自动倒计时并禁用，倒计时固定两位数 `08s`，按钮宽度不跳动） | `number` | `60` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 值变化 | `string` |
| focus / blur | 聚焦 / 失焦 | `FocusEvent` |
| clear | 点击清空 | — |
| enter | 按下回车（textarea 不触发） | `string` |
| send | 点击验证码按钮（点击后组件内部自动开始倒计时并禁用按钮） | — |

### 暴露方法

| 方法 | 说明 |
| --- | --- |
| focus() / blur() | 聚焦 / 失焦 |
| startCountdown(seconds?) | 手动开始验证码倒计时（如请求成功后再开始） |
| stopCountdown() | 停止倒计时并恢复按钮 |

### Slots

| 名称 | 说明 |
| --- | --- |
| prefix | 输入框左侧内容（聚焦时跟随主色） |
| suffix | 输入框右侧内容 |
| left-icon | 左侧图标（位于 label 之前，Vant Field 的 left-icon） |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-input-radius` | 圆角 |
| `--jm-input-label-bg` | 浮起标签的遮挡底色（仅 `outline` 需要，默认跟随页面底色） |
| `--jm-input-placeholder-color` | placeholder 文字色 |
| `--jm-input-placeholder-font-size` | placeholder 字号 |
| `--jm-input-placeholder-font-family` | placeholder 字体 |
| `--jm-input-placeholder-font-weight` | placeholder 字重 |
| `--jm-input-textarea-max-height` | textarea autosize 最大高度（也可用 `max-height` 属性） |
| `--jm-input-code-height` | 验证码按钮高度（默认 32px） |
| `--jm-input-code-radius` | 验证码按钮圆角（默认由 code-shape 决定） |

::: tip 浮动标签放在彩色卡片上
`outline` 外观的标签浮起时要「切断」边框，实现方式是给标签补一块和页面同色的底。若输入框放在非页面底色的容器里（彩色卡片、图片上），给该输入框设 `--jm-input-label-bg: <卡片色>` 即可；`filled` / `underlined` 不需要。
:::

::: warning textarea 的字数统计在框内右下角
`type="textarea"` 的字数统计覆盖在**文本域内右下角**（Vant 同款），单行输入框的字数统计在框内右侧。`type="textarea"` 时浮动标签不生效；需要标签请用 `label-placement="top"`（固定在文本域上方）。`autosize` 与 `rows` 二选一：传 `autosize` 高度跟随内容，传 `rows` 定高。
:::

::: tip 为 Form 校验预留的错误呈现
`error` 置真后描边、label、placeholder 与光标整体转红；`error-message` 显示报错文案，`error-align` 控制左/中/右对齐（**不传时默认跟随 `align`**，与输入文字同排）、`error-color` 覆盖颜色。`label-placement="left"` 的行排版里，报错文案会自动缩进到值列（与输入内容对齐）。**plain 外观时文案渲染在输入行内、紧贴输入内容正下方**（Vant Field 习惯），行底自动留 10px 间距不贴分割线；其余外观文案显示在输入框下方。

`error` / `error-message` 是**受控 props**：组件只负责呈现，不内置校验规则，输入合法后把状态置回，报错即消失。

```html
<jm-input
  v-model="phone"
  :error="phoneError"
  :error-message="phoneMsg"
  label="手机号"
  label-placement="left"
  variant="plain"
/>
```

```ts
watch(phone, (v) => {
  const ok = /^1[3-9]\d{9}$/.test(v)
  phoneError.value = !ok
  phoneMsg.value = ok ? '' : '手机号格式错误'
})
```

放进 `Form` + `FormItem` 时这些状态自动由校验结果驱动（红框、文案、必填星号全联动），无需手动传。
:::

::: tip Vant Field 式行排版
`label-placement="left"` + `variant="plain"` 即可得到 Vant 的行式布局：label 固定在左（`label-width` 控列宽，默认 96px）、输入区在右、无边框透明。把若干输入框放进一个白卡容器、行间加细分割线（demo 里两行 CSS），就是完整的 Field 列表；`required` 显示红色必填星号，`colon` 追加冒号，`#left-icon` / `#suffix` 插槽放图标。**plain 聚焦时也没有任何描边和底线**，保持干净的行式外观。

`label-placement="top"` + `variant="plain"` 则是 Vant 的**顶部对齐**（`label-align="top"`）：label 在上一行、输入内容在下一行，同样无边框透明，适合 label 文字较长或多行输入的行卡片；`required` / `colon` / 错误文案在顶部对齐模式下同样生效。
:::

::: warning 不要用 type="number" 收数字
`type="number"` 在 iOS 上会出现上下箭头、能输入 `e`，而且 `maxlength` 失效。收纯数字请用 `type="text"` + `inputmode="numeric"`。
:::
