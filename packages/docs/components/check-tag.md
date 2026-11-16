---
title: CheckTag 可选标签
description: 可以点选、取消的标签，用于标签筛选与多选场景。
---

# CheckTag 可选标签

标签本身不表达「选中」这个状态，CheckTag 补上：点一下选中、再点取消，选中态用主色浅底 + 对勾表达。适合科目筛选、兴趣选择、订单状态过滤。

和 [Tag](/components/tag) 的分工：Tag 只展示、可带关闭；CheckTag 是**可切换的选项**，天然带 `checked` 语义。

## 基础用法

<DemoBlock src="/demos/check-tag/basic.vue" title="多选、单选与尺寸" desc="多选用数组维护，单选用一个值维护。" />

```vue
<jm-check-tag v-model="checked">数学</jm-check-tag>
```

多选时用一个数组维护即可：

```vue
<jm-check-tag
  v-for="tag in tags"
  :key="tag.label"
  :model-value="picked.includes(tag.label)"
  @update:model-value="(v) => toggle(tag.label, v)"
>
  {{ tag.label }}
</jm-check-tag>
```

单选（互斥）把 `model-value` 绑成 `grade === g` 就行——选中一个新的，旧的自动变成未选中。

## 选中样式

默认选中态是「主色浅底 + 主色文字 + 对勾」，信息密度小，一屏放七八个也不吵。

需要更强强调时传 `checkedColor`，会变成实底白字：

```vue
<jm-check-tag v-model="on" checked-color="#00A0E9">已选</jm-check-tag>
```

## 尺寸与形状

| size | 高度 |
| --- | --- |
| `small` | 24px |
| `medium`（默认） | 28px |
| `large` | 34px |

`shape="square"` 换成小圆角，配 `large` 更像筛选按钮；默认 `round` 是胶囊。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 是否选中（`v-model`） | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| shape | 形状 | `'round' \| 'square'` | `'round'` |
| checkedColor | 选中实底色（白字） | `string` | - |
| color | 未选中文字色 | `string` | 次要文字色 |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 选中态变化 | `boolean` |
| change | 同上 | `boolean` |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| default | 标签文字 |

## 无障碍

渲染成 `<button role="checkbox" aria-checked>`，屏幕阅读器会读成「复选框，已选中/未选中」，而不是一个普通按钮。禁用时用原生 `disabled`，不会被 Tab 聚焦。
