---
title: Toast 轻提示
description: 函数式调用的轻量反馈，支持文字、成功、失败、加载四种类型。
---

# Toast 轻提示

不需要在模板里放组件，直接调用函数。同一时刻只显示一条，后一条会顶掉前一条。

动效是「由小变大弹入、由大变小弹出」：进场 200ms 从 0.6 放大到 1 并淡入，退场 150ms 缩回 0.6 同步淡出，四个位置统一只做缩放。

动效是「由小变大弹入、由大变小弹出」：进场 200ms 从 0.6 放大到 1 并淡入，退场 150ms 缩回 0.6 同步淡出，四个位置统一只做缩放。

## 基础用法

<DemoBlock src="/demos/toast/basic.vue" title="四种类型" desc="示例传了 target，把提示限制在手机框内；不传则挂到 body 居中显示。" />

```ts
import { showToast, closeToast } from 'jimu-ui'

showToast('已保存')
showToast({ message: '提交成功', type: 'success' })
showToast({ message: '网络异常', type: 'fail', position: 'top' })

showToast({ message: '正在上传…', type: 'loading' })
closeToast() // loading 类型不会自动关闭，需要手动关
```

## API

### 参数

| 字段 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| message | 提示内容 | `string` | — (必填) |
| type | 类型 | `'text' \| 'success' \| 'fail' \| 'loading'` | `'text'` |
| duration | 显示时长（ms），`0` 表示不自动关 | `number` | 2000（loading 为 0） |
| position | 位置 | `'top' \| 'middle' \| 'bottom'` | `'middle'` |
| mask | 显示透明遮罩（阻止点击穿透） | `boolean` | `false` |
| icon | 自定义图标名（内置图标），替代 type 的默认图标 | `string` | — |
| closeOnClick | 点击提示本身即关闭 | `boolean` | `false` |
| onClose | 关闭回调（自动消失 / 手动关闭 / 被新提示顶掉） | `() => void` | — |
| target | 挂载容器 | `HTMLElement` | `document.body` |

### 图标、点击关闭与关闭回调

<DemoBlock src="/demos/toast/custom.vue" title="自定义图标 / 点击关闭 / onClose" desc="onClose 适合做「提示结束后再跳转」这类串联动作。" />

```ts
showToast({
  message: '已加入学习计划',
  icon: 'star',                      // 内置图标名，替代默认对勾
  closeOnClick: true,                // 点提示即关
  duration: 0,                       // 不自动消失
  onClose: () => router.push('/plan'),
})
```

`type: 'loading'` 默认 `duration` 为 0（常驻），处理完记得 `closeToast()`；它同样支持 `mask` 挡住背后的点击。`onClose` 在自动消失、点击关闭、`closeToast()`、被新提示顶掉这四种情况下都会触发，且只触发一次。

### 方法

| 方法 | 说明 |
| --- | --- |
| `showToast(options \| string)` | 显示提示 |
| `closeToast()` | 立即关闭 |

::: tip 为什么用深色底而不是白底
Toast 会出现在任意页面背景上，白底在浅色页面上和内容糊在一起。深色半透明 + `backdrop-filter` 在两种主题下都能拉开层次，这也是 iOS 系统提示的做法。
:::

::: warning 不要用它做"确认"
Toast 无按钮、会自动消失，用户来不及看清就没了。要用户做决定请用 Dialog。
:::
