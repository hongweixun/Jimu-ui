---
title: NumberKeyboard 数字键盘
description: 金额、验证码、支付密码的纯数字键盘，支持自定义按键与长按连删。
---

# NumberKeyboard 数字键盘

移动端输入金额、验证码时，系统键盘常常挡住页面、还带一堆用不上的符号。`jm-number-keyboard` 是一个贴底的纯数字键盘，按键事件交给业务处理。

## 基础用法

<DemoBlock src="/demos/number-keyboard/basic.vue" title="基础、辅助键、随机排列、自定义按键" desc="键盘本身不存值，只通过 input/delete 事件告诉你按了什么。" />

```vue
<jm-number-keyboard
  v-model:show="show"
  title="输入金额"
  extra-key="00"
  close-button-text="完成"
  :value="value"
  :maxlength="6"
  @input="value += $event"
  @delete="value = value.slice(0, -1)"
/>
```

## 关于 teleport

键盘默认挂到 `body`、`position: fixed` 贴底——真实手机上这是对的。

在手机模拟框、弹窗、或需要「键盘只盖住某个容器」的演示场景里，传 `:teleport="false"`，键盘会改成就地渲染 + `position: absolute`，贴住最近的定位祖先。

## 自定义按键

`theme="custom"` 时九宫格整体交给插槽，插槽作用域给了三个方法：

```vue
<jm-number-keyboard v-model:show="show" theme="custom" title="快捷金额">
  <template #default="{ input, delete: del }">
    <button class="jm-number-keyboard__key" @click="input('100')">¥100</button>
    <button class="jm-number-keyboard__key" @click="del">删除</button>
  </template>
</jm-number-keyboard>
```

按键外观直接复用 `.jm-number-keyboard__key` 这个全局类即可，不需要额外写样式。

## 交互细节

- **长按退格**：按下先删一个，460ms 后以 90ms 间隔连删，松手/移出立即停；
- **maxlength**：传 `value` 后，长度到达上限时数字键置灰且不派发事件；
- **随机排列**：`random-key-order` 每次打开重新打乱，用于防偷窥；
- 键盘不锁背景滚动（`lock=false`），避免和页面里已有的滚动容器打架。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | `false` |
| theme | 布局 | `'default' \| 'custom'` | `'default'` |
| title | 标题 | `string` | - |
| extraKey | 左下角辅助键，字符串为键值 | `boolean \| string` | `false` |
| closeButtonText | 关闭按钮文案，传了才显示 | `string` | - |
| randomKeyOrder | 数字键随机排列 | `boolean` | `false` |
| value | 已输入内容，用于 maxlength 判断 | `string` | `''` |
| maxlength | 最大长度 | `number` | 不限 |
| deleteRepeat | 长按退格连删 | `boolean` | `true` |
| zIndex | 层级 | `number` | `1100` |
| safeArea | 底部安全区适配 | `boolean` | `true` |
| teleport | 挂载目标，`false` 就地渲染 | `boolean \| string \| Element` | `true` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:show | 显隐变化 | `boolean` |
| input | 按下数字键 | `key: string` |
| delete | 按下退格 | - |
| close | 点关闭按钮 | - |

### Slots

| 插槽 | 说明 |
| --- | --- |
| default | `theme="custom"` 时的按键区，作用域 `{ input, delete, close }` |

::: tip 和 PasswordInput 的关系
`jm-password-input` 内置了这个键盘。需要「点阵密码框 + 数字键盘」这套组合时直接用 `jm-password-input`，只有纯键盘场景才单独引这个组件。
:::
