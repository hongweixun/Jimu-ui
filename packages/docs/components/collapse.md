---
title: Collapse 折叠面板
description: 可折叠的内容区块，支持手风琴模式与高度动画。
---

# Collapse 折叠面板

常见于 FAQ、筛选条件、分组详情。高度动画是真实测量内容高度后过渡的，不写死 `max-height`，所以内容长短都能正确展开，也不会出现「展开一半被裁」的残影。

## 基础用法

<DemoBlock src="/demos/collapse/basic.vue" title="普通模式与手风琴" desc="手风琴模式（accordion）下同时只展开一项，v-model 传单个 name 而不是数组。" />

## 用法

```vue
<script setup lang="ts">
const active = ref<(string | number)[]>(['faq1'])
</script>

<template>
  <jm-collapse v-model="active">
    <jm-collapse-item name="faq1" title="怎么修改手机号？">…</jm-collapse-item>
    <jm-collapse-item name="faq2" title="课程可以退费吗？">…</jm-collapse-item>
  </jm-collapse>
</template>
```

## API

### Collapse Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 展开项的 name；手风琴模式传单个值 | `(string \| number)[]` | `[]` |
| accordion | 手风琴模式 | `boolean` | `false` |
| border | 上下外边框 | `boolean` | `true` |

### CollapseItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 唯一标识，必填 | `string \| number` | — |
| title | 标题 | `string` | — |
| disabled | 禁用展开 | `boolean` | `false` |
| show-arrow | 显示右侧箭头 | `boolean` | `true` |
| content-padding | 内容区内边距 | `string` | `'0 16px 14px'` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 展开项变化 | 同 v-model |
| change | 展开项变化 | 同 v-model |
| click（Item） | 点击标题 | `name` |

### 插槽

| 名称（Item） | 说明 |
| --- | --- |
| title | 自定义标题 |
| extra | 标题右侧附加内容（如「必看」标签） |
| default | 面板内容 |

::: warning 关闭动效时高度会瞬变
`data-motion="off"` 下高度不过渡，直接跳变。这是预期行为——关闭动效的用户通常是前庭功能敏感人群，突然的高度动画反而是负担。
:::
