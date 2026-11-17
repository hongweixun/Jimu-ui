---
title: Form 表单
description: 数据收集与校验，规则式校验、异步校验、提交与重置，和 Input / Switch / Rate 等控件自动联动。
---

# Form 表单

`Form` 负责「数据 + 规则 + 提交」，`FormItem` 负责「字段注册 + 校验状态」。内部控件（`Input`、`Switch`、`Rate`）会自动读取 FormItem 的校验状态：

- 校验失败时输入框自动转红、placeholder / label 变红，**报错文案由 Input 自己排**——`variant="plain"` 的行排版排进框内紧跟内容（Vant Field 习惯），其余外观排在框下
- 有规则带 `required` 时，Input 的红色星号自动出现，不用重复传 `required`
- 输入 / 失焦会自动按规则里声明的 `trigger` 触发校验；**已处于错误态时输入过程会用全量规则复检**，改对即恢复，不必等失焦
- 目前内置联动的控件：`Input`、`Switch`、`Rate`、`Stepper`、`Checkbox`、`Radio`、`Slider`、`Search`、`Uploader`；同时支持 `Form` 整表禁用与 `FormItem` 单字段禁用

## 基础用法

<DemoBlock src="/demos/form/basic.vue" title="行式表单、规则校验、异步校验与手动控制" desc="Form 传 model 与 rules；FormItem 的 name 关联字段。带 name 的 FormItem 只做校验容器，行视觉交给里面的 Input（自带 label），也可以给 FormItem 传 label 做「label + 任意控件」的行。" />

## 禁用

`Form` 的 `disabled` 会整表下发——`Input`、`Switch`、`Rate`、`Stepper`、`Checkbox`、`Radio`、`Slider`、`Search`、`Uploader` 都会跟着禁用；放在 `FormItem` 上则只禁该字段，两者叠加生效：

<DemoBlock src="/demos/form/disabled.vue" title="整表禁用与单字段禁用" desc="开关切到关，整表控件立即变灰不可交互；第二组的开关只影响「优惠码」一行。" />

## 两种 FormItem 用法

**① 纯校验容器**（推荐用于输入类）：FormItem 不产生任何视觉，行排版与 label 交给 Input：

```html
<jm-form :model="form" :rules="rules">
  <div class="form-card">
    <jm-form-item name="phone">
      <jm-input v-model="form.phone" label="手机号" label-placement="left" variant="plain" />
    </jm-form-item>
  </div>
</jm-form>
```

**② 整行模式**：FormItem 传 `label`，负责 label 列 + 值 + `#right`，值区自动右对齐，适合 Switch / Rate / Checkbox 这类小控件：

```html
<jm-form-item name="agree" label="用户协议">
  <jm-switch v-model="form.agree" />
</jm-form-item>
```

## 校验规则

`rules` 是 `{ [字段名]: Rule[] }`，字段名支持 `'user.name'` 路径。规则按数组顺序执行，**命中第一条失败的规则就停**，所以文案可控。

| 规则字段 | 说明 |
| --- | --- |
| `required` | 必填；纯空格默认也算空（`whitespace: true` 可放开） |
| `message` | 失败文案，不传用内置中文提示 |
| `trigger` | `'blur'` / `'change'` / 两者数组；不传则跟随表单级 `validate-trigger`（默认失焦与输入都校验） |
| `type` | `string` `number` `integer` `boolean` `array` `email` `tel` `url` `date` |
| `pattern` | 正则校验（`RegExp`） |
| `min` / `max` / `len` | 字符串与数组看长度，数字看大小 |
| `validator` | 自定义校验 `(value, rule, model) => boolean \| string \| Promise<...>`：返回 `true` 通过、`false` 用默认文案、字符串作为文案；支持 async |

非必填字段为空时会**跳过后续格式校验**，不会出现「没填却报格式错」。

```ts
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 10, message: '用户名需 2~10 个字符', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号' },
    { type: 'tel', message: '手机号格式不正确', trigger: 'change' },
  ],
  account: [
    { trigger: 'blur', validator: async (value) => {
      await checkRemote(String(value))       // 异步校验
      return taken.includes(String(value)) ? '该账号已被占用' : true
    } },
  ],
}
```

## 自定义校验进阶

`validator` 的三个参数是 `(value, rule, model)`——第三个参数给了整个表单数据，所以**跨字段校验**不用任何额外机制：确认密码直接和 `model.password` 比。

<DemoBlock src="/demos/form/validate.vue" title="异步查重、密码强度、跨字段校验与校验时机切换" desc="用户名 700ms 异步查重；密码强度同步 validator；确认密码跨字段比对；顶部按钮切「仅失焦」后输入过程不再实时报错。" />

四种典型写法：

```ts
// ① 同步自定义：返回 true 通过，字符串作为错误文案
{ validator: (v) => (/[a-zA-Z]/.test(v) && /\d/.test(v) ? true : '密码须同时包含字母和数字') }

// ② 异步：模拟查重，返回 Promise
{ validator: (v) => checkRemote(v).then(taken => taken.includes(v) ? '该用户名已被注册' : true) }

// ③ 跨字段：从 model 拿另一个字段
{ validator: (v, _rule, m) => (v === m.password ? true : '两次输入的密码不一致') }

// ④ 正则 + 自定义文案
{ pattern: /^1\d{10}$/, message: '手机号应为 1 开头的 11 位数字' }
```

**校验时机**由两层控制，规则自己声明 `trigger` 时以声明为准：

| 层级 | 配置 | 说明 |
| --- | --- | --- |
| 表单级 | `<jm-form :validate-trigger="['blur']">` | 只约束「未声明 trigger 的规则」；传 `['blur']` 即关闭输入过程实时校验 |
| 规则级 | `{ trigger: 'blur' }` | 优先级高于表单级 |

处于错误态的字段在输入过程中仍会**全量复检**——改对了立即恢复，不用等失焦。

## 常用控件整合

整行模式的 FormItem 能装下任何控件——单选、多选、下拉（Cell + Popup + Picker）、半星评分、步进器、开关、图片上传、多行备注，全部纳入同一套校验与提交流程：

<DemoBlock src="/demos/form/controls.vue" title="Radio / Checkbox / Picker / Rate / Stepper / Switch / Uploader 整合演示" desc="性别单选、服务标签多选、城市下拉选择（底部弹层 Picker）、半星评分、限购步进器、物流通知开关、凭证照片上传与备注，点提交统一校验。" />

## 提交与重置

`<form>` 原生提交被接管：校验通过才触发 `submit`，否则触发 `failed`（带上每条错误）：

```html
<jm-form ref="formRef" :model="form" :rules="rules" scroll-to-error
  @submit="onSubmit" @failed="onFailed">
  …
  <jm-button type="primary" native-type="submit" block>提交</jm-button>
</jm-form>
```

`scroll-to-error` 会在校验失败时把第一个出错的字段滚到视野中间。

## 手动控制

通过 ref 拿到实例方法：

| 方法 | 说明 |
| --- | --- |
| `validate()` | 校验全部字段，返回 `Promise<boolean>`（不 reject，直接 `if` 判断即可） |
| `validateField(name)` | 校验指定字段，支持数组 |
| `clearValidate(name?)` | 只清校验状态与文案，数据不动 |
| `resetFields(name?)` | 数据恢复为首次挂载时的值，同时清校验状态 |
| `scrollToField(name)` | 滚动到指定字段 |

```ts
const formRef = ref()
const ok = await formRef.value.validate()
if (ok) submit(form)

formRef.value.clearValidate('phone')
formRef.value.resetFields()
```

## 报错呈现

| 属性（FormItem） | 说明 | 默认 |
| --- | --- | --- |
| `show-error` | 是否展示文案；关掉后仍保留红框状态（Form 上的 `show-error` 可全局关） | 继承 Form |
| `error-message` | 外部直接指定文案，优先级最高 | — |
| `error-align` | 文案对齐 `'left' \| 'center' \| 'right'` | `'left'`（有 label 时与值列对齐） |
| `error-color` | 文案颜色 | `var(--jm-color-danger)` |
| `validate-status` | 外部接管状态 `'' \| 'error' \| 'success'` | — |

::: tip 和 Input 的 `error` / `error-message` 什么关系？
两个层次的同一件事：FormItem 里的校验结果会自动喂给 Input（等价于给它传 `error` 和 `error-message`），Input 单独使用时仍然可以用这两个 props 自己控制。**两者可以混用**——外部校验（如接口返回的字段错误）直接给 Input 传 `error-message` 即可，Form 的校验不会覆盖它。
:::

## API

### Form Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model | 表单数据对象 | `Record<string, any>` | — |
| rules | 全局校验规则，键为字段名 | `Record<string, FormRule[]>` | — |
| label-width | 字段标签列宽（FormItem 共用，数字按 px） | `number \| string` | `96px` |
| show-error | 是否展示报错文案 | `boolean` | `true` |
| scroll-to-error | 校验失败时滚动到第一个出错字段 | `boolean` | `false` |
| disabled | 整表禁用，内部所有表单控件继承 | `boolean` | `false` |
| validate-trigger | 表单级校验时机，只约束未声明 trigger 的规则 | `('blur' \| 'change')[]` | `['blur','change']` |

### Form Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| submit | 校验通过后提交 | `model` |
| failed | 校验失败 | `{ errors: Array<{ name, message }> }` |
| validate | 每次校验结束（通过与否都触发） | `passed: boolean` |

### FormItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 关联字段名，支持 `'a.b'`；不传则不参与校验 | `string` | — |
| label | 行标签；不传则 FormItem 只做纯校验容器 | `string` | — |
| rules | 该字段规则，与 Form 同名规则叠加（item 在前） | `FormRule[]` | — |
| required | 必填红星；不传自动从规则推导 | `boolean` | — |
| colon | 标签后追加冒号 | `boolean` | `false` |
| label-width | 标签列宽（数字按 px） | `number \| string` | `96px` |
| label-align | 标签位置 `'left' \| 'right' \| 'top'` | `string` | `'left'` |
| show-error | 是否展示该字段文案 | `boolean` | 继承 Form |
| disabled | 单字段禁用，与 Form 的整表禁用叠加 | `boolean` | `false` |
| error-message | 外部指定文案 | `string` | — |
| error-align | 文案对齐 | `'left' \| 'center' \| 'right'` | `'left'` |
| error-color | 文案颜色 | `string` | danger |
| validate-status | 外部接管校验状态 | `'' \| 'error' \| 'success'` | — |

### FormItem Slots

| 插槽 | 说明 |
| --- | --- |
| default | 字段控件 |
| label | 自定义标签内容 |
| right | 行尾附加内容（单位、说明、跳转等） |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-form-label-width` | 标签列宽 | `96px` |
| `--jm-form-item-height` | 整行模式的最小行高 | `48px` |
| `--jm-form-pad-x` | 整行模式的左右内边距 | `12px` |
| `--jm-form-error-align` | 文案对齐（由 `error-align` 写入） | `left` |
| `--jm-form-error-color` | 文案颜色 | `var(--jm-color-danger)` |
