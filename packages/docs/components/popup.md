---
title: Popup 弹出层
description: 五个方向的弹层容器，圆角、遮罩、安全区、滚动锁都已内置。
---

# Popup 弹出层

所有弹层的底座。ActionSheet 就是基于它实现的。

## 基础用法

<DemoBlock src="/demos/popup/basic.vue" title="五个方向" desc="文档里传了 :teleport=&quot;false&quot; 让弹层留在手机框内，真实项目默认挂到 body。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | `false` |
| position | 出现位置 | `'bottom' \| 'top' \| 'left' \| 'right' \| 'center'` | `'bottom'` |
| round | 圆角 | `boolean` | `false` |
| radius | 圆角大小 | `number \| string` | `var(--jm-radius-lg)` |
| closeable | 右上角关闭按钮 | `boolean` | `false` |
| mask | 显示遮罩 | `boolean` | `true` |
| close-on-click-mask | 点遮罩关闭 | `boolean` | `true` |
| safe-area | 底部/顶部预留安全区 | `boolean` | `true` |
| lock | 锁定背景滚动 | `boolean` | `true` |
| eager | 内容常驻挂载（隐藏），打开时零 DOM 创建。重内容弹层（日历等几百节点）建议开，避免真机动画起步掉帧 | `boolean` | `false` |
| z-index | 层级 | `number` | `1000` |
| teleport | 挂载目标：`false` 就地渲染（嵌入手机模拟框/弹窗内），字符串按选择器、元素直接挂载（Vant 同款语义） | `boolean \| string \| Element` | `true` |
| beforeClose | 关闭前钩子，返回 false / reject 则不关闭 | `() => boolean \| Promise<boolean>` | — |
| closeOnEsc | 按 `Esc` 关闭（同样走 `beforeClose`） | `boolean` | `false` |
| trapFocus | 焦点锁在弹层内，关闭后归还触发元素 | `boolean` | `false` |
| ariaLabel | 无障碍名称，没有可见标题时给读屏软件用 | `string` | — |

`closeOnEsc` / `trapFocus` 默认关，是因为 Popup 也常被当成非模态容器（内嵌在页面里的筛选面板）。当抽屉、表单弹层用时建议都打开；`ActionSheet` 已经默认打开。

## 关闭前拦截

底部弹层里填了一半，用户点遮罩就走会丢内容。`beforeClose` 让遮罩点击、右上角关闭都先过一次校验：

<DemoBlock src="/demos/popup/before-close.vue" title="有未保存内容时先确认" desc="返回 Promise 时弹层保持打开，确认后才真正关闭。" />

```vue
<jm-popup v-model:show="show" position="bottom" round :before-close="beforeClose">
  …
</jm-popup>
```

```ts
function beforeClose() {
  if (!dirty.value) return true
  return new Promise<boolean>((resolve) => confirmLeave(resolve))
}
```

要点：

- 只拦「关闭」这一侧，打开不受影响；`v-model:show = false` 由父级直接赋值时也不会绕过（动画仍走 `close`）。
- 返回 `false` / reject → 保持打开；返回 `true` / 不返回 → 关闭。
- 异步期间重复点遮罩不会叠起第二个确认框。

### 事件

| 事件名 | 说明 |
| --- | --- |
| update:show | 显示状态变化 |
| open / opened | 开始打开 / 打开动画结束 |
| close / closed | 开始关闭 / 关闭动画结束 |
| click-mask | 点击遮罩 |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-popup-radius` | 圆角 |

::: warning 一定要用 teleport: false 的两个场景
1. **嵌在弹窗里**：遮罩层级会打架，弹层会被父级 `overflow: hidden` 裁掉
2. **手机模拟框 / iframe 预览**：`position: fixed` 会贴到整个视口，跑到框外面去

其他情况保持默认 `true`，避免被祖辈的 `transform` 或 `overflow` 影响。
:::

::: tip 后开的弹层永远在先开的之上
每个弹层打开时都会从全局计数器领取一个递增的 z-index（Vant 同款策略），不会再出现两张 1000 平级、层级看 DOM 顺序的随机局面。`zIndex` prop 只是"保底值"，通常不用管。
:::

::: tip 后开的弹层永远在先开的之上
每个弹层打开时都会从全局计数器领取一个递增的 z-index（Vant 同款策略），不会再出现两张 1000 平级、层级看 DOM 顺序的随机局面。`zIndex` prop 只是"保底值"，通常不用管。
:::

::: tip inline 模式不锁页面
`teleport="false"`（嵌入手机模拟框、页面内嵌抽屉等）时**不会锁 body 滚动**——弹层就在文档流里，锁 body 会把整个页面冻住。滚动锁只对挂 `body` 的弹层生效；想强制锁页面传 `:lock="false"` 之外的场景基本不存在，正常用就好。

::: tip inline 模式不锁页面
`teleport="false"`（嵌入手机模拟框、页面内嵌抽屉等）时**不会锁 body 滚动**——弹层就在文档流里，锁 body 会把整个页面冻住。滚动锁只对挂 `body` 的弹层生效；想强制锁页面传 `:lock="false"` 之外的场景基本不存在，正常用就好。

::: tip 滚动锁是计数式的
同时打开两个弹层不会互相解锁。关掉上层时背景仍然锁着，等最后一个关了才恢复。
:::
