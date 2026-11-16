---
title: PasswordInput 密码输入框
description: 支付密码、验证码的点阵输入框，内置数字键盘，输满自动派发 complete。
---

# PasswordInput 密码输入框

一排格子 + 圆点占据位，点一下唤起数字键盘。适合支付密码、短信验证码这类「固定位数、纯数字」的输入。

## 基础用法

<DemoBlock src="/demos/password-input/basic.vue" title="6 位密码、间距与明文、自动收起" desc="输满触发 complete，业务拿到完整密码再做校验。" />

```vue
<jm-password-input
  v-model="pwd"
  :length="6"
  keyboard-title="请输入支付密码"
  @complete="onComplete"
/>
```

## 焦点与键盘

`focused` 支持 `v-model:focused` 受控；不传时组件自己管：

- 点格子 → 聚焦 + 唤起键盘；
- 点键盘右上角关闭 → 失焦 + 收起键盘；
- `auto-close` 输满后自动收起键盘。

不想要内置键盘（例如接了别处的安全键盘、或在桌面端想用物理键盘）时传 `:show-keyboard="false"`，组件仍然支持直接用键盘敲数字与退格。

## 外观

| 写法 | 效果 |
| --- | --- |
| 默认 `gutter=0` | 格子连体，相邻边框重叠成单线，外侧圆角 |
| `:gutter="10"` | 独立小方块，间距 10px |
| `:mask="false"` | 显示真实数字而不是圆点 |

焦点所在的那一格会有主色描边，一眼看出还要输几位。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 已输入内容 | `string` | `''` |
| length | 位数 | `number` | `6` |
| gutter | 格子间距，数字按 px | `number \| string` | `0` |
| mask | 用圆点遮挡 | `boolean` | `true` |
| focused | 受控聚焦（`v-model:focused`） | `boolean` | - |
| showKeyboard | 使用内置数字键盘 | `boolean` | `true` |
| autoClose | 输满后自动收起键盘 | `boolean` | `false` |
| keyboardTitle | 键盘标题 | `string` | - |
| zIndex | 键盘层级 | `number` | `1100` |
| safeArea | 键盘安全区适配 | `boolean` | `true` |
| teleport | 键盘挂载目标，`false` 就地渲染 | `boolean \| string \| Element` | `true` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 内容变化 | `value: string` |
| update:focused | 聚焦状态变化 | `boolean` |
| input | 每次输入 | `value: string` |
| complete | 输满 `length` 位 | `value: string` |
| focus / blur | 聚焦 / 失焦 | - |

### Exposes

| 方法 | 说明 |
| --- | --- |
| focus() / blur() | 手动控制焦点与键盘 |
| clear() | 清空 |

::: warning 安全提示
`complete` 拿到的是明文密码。真实项目里应在校验后立刻清空、只把必要的凭证发给后端，不要把它写进日志或本地存储。
:::
