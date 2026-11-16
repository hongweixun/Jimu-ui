---
title: Dialog 对话框
description: 居中模态提示，用于二次确认与关键决策。
---

# Dialog 对话框

阻断式提示。只用于"必须让用户停下来做决定"的场景（删除、支付、权限申请），普通提示用 Toast。

## 基础用法

<DemoBlock src="/demos/dialog/basic.vue" title="确认与竖排按钮" desc="文案较长时用 vertical-actions，按钮竖排更好点；横排时左侧是取消，符合拇指热区。" />

## 异步提交与拦截

<DemoBlock src="/demos/dialog/before-close.vue" title="before-close：提交中不关、失败不关" desc="before-close 返回 Promise 时按钮自动转圈，返回 false 则这次点击完全无效。" />

```vue
<jm-dialog
  v-model:show="show"
  title="提交作业"
  :before-close="beforeClose"
  @confirm="show = false"
/>

<script setup>
// 接口成功才放行，失败时 return false
async function beforeClose(action) {
  if (action === 'cancel') return true
  return await submit()   // false 就不关
}
</script>
```

两个配套的 loading 属性给「业务自己管请求」的场景用：`confirm-button-loading` / `cancel-button-loading`。它们和 `before-close` 共用一套忙碌态——只要有任意一个在加载，另一个按钮也会被禁掉，避免重复提交。

## 按钮形态

<DemoBlock src="/demos/dialog/actions.vue" title="胶囊 / 方形 / 单按钮 / 无按钮" desc="button-style 切换按钮形态；填充形态下取消用描边、确认用实心主色，靠颜色区分层级；show-confirm=false 或 show-cancel=false 可隐藏任一按钮，全部隐藏即为纯提示框。" />

## 键盘与焦点

弹窗是模态的，键盘也必须"模态"：焦点不能跑到背后的页面上。

<DemoBlock src="/demos/dialog/keyboard.vue" title="Tab 只在弹窗内循环，Esc 关闭后焦点回到触发按钮" desc="用键盘打开弹窗后连续按 Tab，焦点在输入框与按钮之间循环；关闭后焦点归还给「打开表单弹窗」按钮。" />

实现细节（`useFocusTrap` composable）：

- 打开时记住当前焦点元素 → 把焦点移进面板 → 关闭时还回去；触发元素已被销毁（列表项被删）就跳过，不会把焦点丢到不存在的位置
- `Tab` / `Shift+Tab` 在面板内首尾循环；面板里一个可聚焦元素都没有时，焦点停在面板本身而不是跑出去
- 关闭动画期间焦点就已经归还，用户不会有一瞬间"焦点在虚空里"

如果需要自己控制焦点落点（比如聚焦某个关键输入框），在面板内给元素加 `autofocus` 或用业务自己的 `ref` 聚焦即可，陷阱只负责"圈住"不负责"指定"。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | `false` |
| title | 标题 | `string` | — |
| message | 内容 | `string` | — |
| show-cancel | 显示取消按钮 | `boolean` | `true` |
| show-confirm | 显示确认按钮 | `boolean` | `true` |
| button-style | 按钮形态：`text` 分隔线文字按钮 / `pill` 胶囊 / `square` 方形 | `'text' \| 'pill' \| 'square'` | `'text'` |
| confirm-text | 确认按钮文字 | `string` | `'确定'` |
| cancel-text | 取消按钮文字 | `string` | `'取消'` |
| round | 圆角 | `boolean` | `true` |
| radius | 圆角大小 | `number \| string` | `var(--jm-radius-lg)` |
| mask | 遮罩 | `boolean` | `true` |
| close-on-click-mask | 点遮罩关闭 | `boolean` | `false` |
| vertical-actions | 按钮竖排 | `boolean` | `false` |
| before-close | 关闭前钩子，返回 `false` 拦截；返回 Promise 时按钮自动 loading | `(action: 'confirm' \| 'cancel') => boolean \| void \| Promise<boolean \| void>` | — |
| confirm-button-loading | 确认按钮 loading | `boolean` | `false` |
| cancel-button-loading | 取消按钮 loading | `boolean` | `false` |
| confirm-color | 确认按钮颜色：`text` 形态是文字色，`pill`/`square` 形态是实心底色 | `string` | `var(--jm-color-primary)` |
| cancel-color | 取消按钮文字色 | `string` | `var(--jm-text-color-2)`（`pill`/`square` 形态为 `var(--jm-text-color)`） |
| lock | 锁定背景滚动 | `boolean` | `true` |
| close-on-esc | 按 `Esc` 关闭（走 `before-close` 与 `cancel`，等同点取消） | `boolean` | `true` |
| trap-focus | 焦点锁在弹窗内，关闭后归还给触发元素 | `boolean` | `true` |
| z-index | 层级 | `number` | `1100` |
| teleport | 挂载到 body | `boolean` | `true` |

### 键盘与焦点

| 按键 | 行为 |
| --- | --- |
| `Esc` | 关闭（等于点取消，同样受 `before-close` 拦截） |
| `Tab` / `Shift+Tab` | 在弹窗内按钮之间循环，不会跑到背后页面 |
| `Enter` / `Space` | 触发当前聚焦的按钮 |

打开后焦点落在第一个按钮（取消）上，关闭后回到打开它的元素。叠了多层弹窗时，`Esc` 只关最上面那层。

### 事件

| 事件名 | 说明 |
| --- | --- |
| update:show | 显示状态变化 |
| confirm | 点击确认（**不会自动关闭**，由你决定是否关） |
| cancel | 点击取消（会自动关闭） |
| closed | 关闭动画结束 |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 内容（覆盖 message） |
| title | 标题 |
| footer | 整个按钮区 |

::: warning confirm 不自动关闭
因为确认后往往要发请求，请求失败时对话框不应该消失。所以 `confirm` 只抛事件，关闭时机由业务控制：

```ts
async function onConfirm() {
  try {
    await submit()
    show.value = false
  } catch {
    /* 保持打开，让用户重试 */
  }
}
```
:::
