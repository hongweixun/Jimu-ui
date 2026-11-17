---
title: Snackbar 消息条
description: 带操作按钮的快速消息横条，支持类型染色、多位置、竖排、加载常驻，函数式调用。
---

# Snackbar 消息条

用于向用户显示**可以带操作**的快速消息——「已加入购物车 · 去结算」「有新版本 · 立即更新」这类「发生了什么 + 你可以怎么办」的场景。和 Toast 的分工：Toast 只负责「告诉你一声」，Snackbar 允许用户就地响应。

::: tip 与 Toast 的区别
Toast 打断感更弱、无操作；Snackbar 有操作按钮且默认禁止穿透点击（loading 时），更像一个轻量的「横幅确认框」。
:::

## 函数式调用

<DemoBlock src="/demos/snackbar/basic.vue" title="类型 / 底部 / 竖排 / 加载 / 清除" desc="默认单例模式，新消息顶掉旧消息；showSnackbar.allowMultiple(true) 开启多例堆叠。" />

```ts
import { showSnackbar, clearSnackbar } from 'jimu-ui'

// 快捷
showSnackbar('草稿已自动保存')
showSnackbar.success('提交成功')
showSnackbar.error('保存失败，请重试')

// 完整参数
const bar = showSnackbar({
  content: '已加入购物车',
  position: 'bottom',
  action: '去结算',
  onAction: () => goCheckout(),
})

// loading 常驻，处理完手动关
const loading = showSnackbar.loading('正在同步数据…')
await sync()
loading.clear()

clearSnackbar() // 关闭当前（单例）或全部（多例）
```

## 位置

`position` 支持 `top`（默认）、`center`、`bottom`。多条消息在同一位置纵向堆叠。

## 竖排

`vertical: true` 让内容与操作按钮上下两行，适合长文案 + 按钮的组合。

## 类型

| 类型 | 呈现 |
| --- | --- |
| `normal` | 深色横条（默认） |
| `success` / `warning` / `error` / `info` | 对应语义色横条，success/error 自带图标 |
| `loading` | 深色横条 + 旋转圈，默认常驻且禁止穿透点击，需手动 `clear` |

## API

### showSnackbar(options)

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| content | 消息内容 | `string` | - |
| type | 类型，见上表 | `SnackbarType` | `'normal'` |
| position | 位置 `top` `center` `bottom` | `string` | `'top'` |
| duration | 显示时长 ms，`0` 表示常驻 | `number` | `3000`（loading 为 `0`） |
| vertical | 内容与按钮竖排 | `boolean` | `false` |
| action | 操作按钮文字 | `string` | - |
| onAction | 点击操作按钮 | `() => void` | - |
| forbidClick | 禁止穿透点击 | `boolean` | `false`（loading 默认 `true`） |
| target | 挂载容器，消息条限制在容器内显示（嵌入弹窗、模拟框时用） | `HTMLElement` | -（挂 body 全屏） |
| onClose | 关闭回调 | `() => void` | - |

### 静态方法

| 方法 | 说明 |
| --- | --- |
| `showSnackbar.success/warning/info/error/loading(options \| string)` | 快捷类型方法 |
| `handle.clear()` | 关闭该实例 |
| `clearSnackbar()` | 关闭当前（单例）或全部（多例） |
| `showSnackbar.allowMultiple(boolean)` | 开启/关闭多例模式 |
| `showSnackbar.setDefaultOptions(options)` | 设置默认选项 |
| `showSnackbar.resetDefaultOptions()` | 重置默认选项 |

### 返回值

`SnackbarHandle`：`{ clear: () => void }`。
