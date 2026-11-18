---
title: Copy 复制指令
description: 点一下就把文本复制进剪贴板：订单号、邀请码、口令链接的标配交互。
---

# Copy 复制指令

用户通常不知道系统输入框可以长按全选。要复制一个订单号，最省事的交互不是教用户长按，而是**点一下就复制**——复制这件事在移动端应该是零成本的。

`v-copy` 优先走 `navigator.clipboard`（现代浏览器、安全上下文），自动降级到隐藏 `textarea` + `execCommand`（老设备 / 非安全上下文兜底），两层策略都失败才走 `onError`。

## 基础用法

<DemoBlock src="/demos/copy/basic.vue" title="复制订单号与邀请码" desc="字符串直接传值；动态内容用函数取值，复制到的永远是点击那一刻的最新值。" />

```vue
<template>
  <!-- 静态文本：直接传字符串 -->
  <button v-copy="'EDU-8F3K-2026'">复制邀请码</button>

  <!-- 动态内容：传函数，点击时求值 -->
  <button v-copy="{ text: () => orderNo, onSuccess: tip }">复制订单号</button>

  <!-- 整块区域可复制 -->
  <div v-copy="'优惠券口令 XJ2026'">口令：XJ2026</div>
</template>

<script setup>
import { vCopy } from 'jimu-ui'
const orderNo = ref('JM20261116002')
function tip(text) {
  showToast(`已复制 ${text}`)
}
</script>
```

## 选项

| 选项 | 类型 | 说明 |
| --- | --- | --- |
| `text` | `string \| (() => string)` | 要复制的文本；函数在**点击时**求值 |
| `feedback` | `boolean \| string` | 成功提示：默认弹「复制成功」消息条；传字符串自定义文案；`false` 关闭 |
| `onSuccess` | `(text) => void` | 复制成功，参数是实际复制的内容 |
| `onError` | `(reason) => void` | 两层策略都失败（极少出现）；未传时自动弹「复制失败」提示 |

值的三种形态：

| 写法 | 含义 |
| --- | --- |
| `v-copy="'文本'"` | 等价于 `{ text: '文本' }` |
| `v-copy="{ text, onSuccess }"` | 带回调的完整配置 |
| `v-copy="() => dynamic"` | 等价于 `{ text: () => dynamic }` |

::: tip 复制成功一定有反馈
剪贴板是用户看不见的地方，没有反馈用户根本不知道复制成没成功。`v-copy` **默认自带**「复制成功」消息条，不需要自己写 `onSuccess` 弹 toast；想要不同文案传 `feedback: '口令已复制'`，想完全自己接管传 `feedback: false`。
:::

## 实现细节

| 策略 | 条件 | 说明 |
| --- | --- | --- |
| `navigator.clipboard.writeText` | 首选 | 需要 HTTPS（或 localhost）；异步 API |
| 隐藏 `textarea` + `execCommand('copy')` | 自动降级 | textarea 挪到视口外、复制完立刻移除，不闪屏、不抢焦点滚动 |

## 可访问性

指令挂在非交互元素（`div` / `span`）上时，会自动补 `tabindex="0"` 与 `role="button"`，键盘用户可以 Tab 到它并用 Enter 触发；挂在 `button` / `a` 上则保持原语义不动。
