---
title: Search 搜索
description: 搜索输入框，圆形/方形、取消按钮、清空、回车搜索。
---

# Search 搜索

移动端搜索框。输入框字号被强制锁在 16px 起（`max(16px, --jm-font-size-md)`），这是为了避免 iOS Safari 聚焦时自动放大整个页面——这个坑在移动端几乎必踩。

## 基础用法

<DemoBlock src="/demos/search/basic.vue" title="形状、尺寸、取消与状态" desc="回车的键盘文案是「搜索」，由 enterkeyhint 控制。" />

## 搜索即用

```vue
<script setup lang="ts">
const keyword = ref('')
const list = ref<Course[]>([])

async function onSearch(v: string) {
  if (!v.trim()) return
  list.value = await api.searchCourses(v)
}
</script>

<template>
  <jm-search v-model="keyword" placeholder="搜索课程" show-cancel @search="onSearch" />
</template>
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 输入值 | `string` | `''` |
| placeholder | 占位文案 | `string` | `'搜索'` |
| shape | 形状 | `'round' \| 'square'` | `'round'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| clearable | 显示清空按钮 | `boolean` | `true` |
| show-cancel | 显示右侧取消 | `boolean` | `false` |
| cancel-text | 取消文案 | `string` | `'取消'` |
| align | 文字对齐 | `'left' \| 'center'` | `'left'` |
| maxlength | 最大长度 | `number` | — |
| autofocus | 自动聚焦 | `boolean` | `false` |
| disabled / readonly | 禁用 / 只读 | `boolean` | `false` |
| background | 输入框底色 | `string` | `var(--jm-bg-input)` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 输入变化 | `string` |
| search | 回车或点搜索 | `string` |
| clear | 点击清空 | — |
| cancel | 点击取消（同时清空） | — |
| focus / blur | 聚焦 / 失焦 | `FocusEvent` |

### 插槽

| 名称 | 说明 |
| --- | --- |
| left-icon | 替换左侧放大镜 |
| right-icon | 右侧追加图标（如扫码） |

::: tip 焦点边框
聚焦时输入框底色会从灰变白、边框变主色，这是移动端唯一能在深色和浅色背景下都看得清的聚焦提示（不要只做底色变化，日光下几乎看不出）。
:::
