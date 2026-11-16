---
title: Rate 评分
description: 星级评分，支持半星、清零、只读与键盘操作。
---

# Rate 评分

课程评价、商品打分。半星不是靠鼠标坐标算的，而是把每颗星切成左右两个热区，触屏上点左半格就是半星——避免了 `getBoundingClientRect` 在滚动、缩放场景下算偏的问题。

## 基础用法

<DemoBlock src="/demos/rate/basic.vue" title="基础、半星、只读与自定义" desc="键盘左右方向键可加减分，无障碍下以 slider 角色暴露给读屏。" />

## 用法

```vue
<script setup lang="ts">
const score = ref(4.5)
</script>

<template>
  <jm-rate v-model="score" allow-half show-text />
</template>
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前分值 | `number` | `0` |
| count | 星星总数 | `number` | `5` |
| size | 星星尺寸 | `number \| string` | `24` |
| gutter | 间距 | `number` | `4` |
| active-color | 选中颜色 | `string` | `var(--jm-color-warning)` |
| void-color | 未选中颜色 | `string` | `var(--jm-gray-300)` |
| allow-half | 允许半星 | `boolean` | `false` |
| allow-clear | 再次点击当前分值清零 | `boolean` | `true` |
| readonly | 只读（仍可聚焦） | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| show-text | 右侧显示分值 | `boolean` | `false` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 分值变化 | `number` |
| change | 分值变化 | `number` |

::: tip 评分一定要给文字
只靠星星颜色，色觉障碍用户分不出 3 星和 5 星。放一个 `show-text`，或者在旁边写死「4.8 分 · 128 人评价」，比纯图形可靠。
:::
