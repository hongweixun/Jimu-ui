---
title: Ellipsis 文本省略
description: 单行/多行文本截断省略号，可展开收起，支持受控与自适应重测。
---

# Ellipsis 文本省略

长文本截断组件：单行或指定行数内截断显示省略号，可选「展开 / 收起」动作。容器尺寸变化时自动重测是否溢出，不会出现「明明放得下还显示展开」的误判。

## 基础用法

<DemoBlock src="/demos/ellipsis/basic.vue" title="单行截断、多行展开收起、受控模式" desc="rows 控制收起时保留几行；expandable 打开后，只有文本真的放不下才出现「展开」动作；expanded 走 v-model 受控。" />

## 用法

```html
<!-- 单行截断，纯展示 -->
<jm-ellipsis :content="text" />

<!-- 三行摘要 + 展开收起 -->
<jm-ellipsis :rows="3" expandable :content="text" />

<!-- 受控 + 动作独占一行靠右 -->
<jm-ellipsis :rows="3" expandable v-model:expanded="open" action-position="block" :content="text" />
```

展开态用真实内容高度判断，收起态用「临时解除截断量一次再恢复」的方式判断溢出，同步完成不会闪烁；宽度变化（旋转屏幕、面板开合）由 ResizeObserver 监听容器宽度触发重测。

## API

### Ellipsis Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| content | 文本内容，也可用默认插槽 | `string` | — |
| rows | 收起时保留的行数 | `number` | `1` |
| expandable | 是否可展开收起 | `boolean` | `false` |
| expanded | 展开态（`v-model:expanded`），不传内部维护 | `boolean` | — |
| expand-text | 展开动作文案 | `string` | `'展开'` |
| collapse-text | 收起动作文案 | `string` | `'收起'` |
| action-position | 动作位置：`text` 跟在文末，`block` 独占一行靠右 | `'text' \| 'block'` | `'text'` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:expanded | 展开态变化 | `boolean` |
| change | 展开态变化 | `boolean` |

### 方法

| 方法 | 说明 |
| --- | --- |
| `measure()` | 手动触发一次溢出重测（内容被外部改动后调用） |
