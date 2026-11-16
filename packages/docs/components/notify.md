---
title: Notify 消息通知
description: 顶部滑入的消息条，支持四种状态色、自动关闭、堆叠与函数式调用。
---

# Notify 消息通知

比 Toast 更「有分量」的反馈：从顶部滑下来，带标题和一行说明，适合系统公告、接口报错、审核结果这类需要用户读到具体文案的场景。

和 NoticeBar 的区别：NoticeBar 常驻在页面内容里，Notify 是浮在页面之上、会自动消失的提示。

## 基础用法

<DemoBlock src="/demos/notify/basic.vue" title="组件式与函数式" desc="组件式用 v-model:show 控制；函数式直接 showNotify()，可堆叠。" />

```vue
<jm-notify
  v-model:show="show"
  type="primary"
  title="课程即将开始"
  message="《高等数学》直播课 5 分钟后开始。"
  :duration="4000"
/>
```

## 函数式

```ts
import { showNotify, closeNotify } from 'jimu-ui'

// 返回 id，可提前关闭
const id = showNotify({
  type: 'success',
  title: '提交成功',
  message: '老师批改后会通知你。',
  duration: 2600,
  onClick: () => goDetail(),
})

closeNotify(id) // 关单条
closeNotify() // 关全部
```

函数式调用会自动挂一个宿主到 `body`，多条同时存在时按「最新在最上」纵向堆叠，默认最多 3 条（`max` 可调），超出时顶掉最早的一条。**同一条 message 重复触发只会刷新原来那条**，不会变成三条重复提示——轮询接口报错时很常见。

嵌入弹窗或手机模拟框时，用 `target` 把宿主挂进容器：

```ts
showNotify({ message: '已保存', target: containerEl })
```

## 状态色

| type | 底色 | 图标 |
| --- | --- | --- |
| `primary` | 主色 | i |
| `success` | 成功绿 | 对勾 |
| `warning` | 警告黄（深色文字） | 感叹号 |
| `danger`（默认） | 危险红 | 叉 |

`icon` 可覆盖图标，`background` / `color` 可直接改配色（会同时改掉图标与文字的继承色）。

## 自动关闭

`duration` 单位毫秒，默认 3000；传 `0` 表示不自动关，适合「必须让用户看到」的提示，配 `closeable` 让用户自己关。

## 安全区

全面屏设备上打开 `safe-area-inset-top`，通知会额外让出状态栏高度，不会撞到刘海。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | `false` |
| type | 状态色 | `'primary' \| 'success' \| 'warning' \| 'danger'` | `'danger'` |
| title | 标题 | `string` | - |
| message | 正文 | `string` | - |
| duration | 自动关闭毫秒数，0 为不关 | `number` | `3000` |
| closeable | 显示右上角关闭按钮 | `boolean` | `true` |
| icon | 自定义图标名 | `string` | - |
| color | 文字/图标颜色 | `string` | - |
| background | 背景色 | `string` | - |
| safeAreaInsetTop | 让出顶部安全区 | `boolean` | `false` |
| zIndex | 层级 | `number` | `2100` |
| teleport | 挂载位置 | `boolean \| string \| Element` | `true` |
| inline | 绝对定位在父容器内 | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:show | 显隐变化 | `boolean` |
| click | 点击通知主体 | `MouseEvent` |
| close | 点了关闭按钮或自动关闭 | - |
| closed | 退场动画结束 | - |

### 函数

| 方法 | 说明 | 参数 |
| --- | --- | --- |
| showNotify | 弹出一条通知，返回 id | `NotifyOptions \| string` |
| closeNotify | 关闭指定 id；不传则关闭全部 | `id?: number` |

`NotifyOptions` 在组件 props 之外多了 `max`、`target`、`onClick`、`onClose`。

### 插槽

| 插槽 | 说明 |
| --- | --- |
| default | 正文 |
| title | 标题 |
