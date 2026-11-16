---
title: Space 间距
description: 一行/一列元素之间的统一间距，省掉到处写 margin 的麻烦。
---

# Space 间距

组合排版时最烦的是「最后一个元素不要 margin」。`jm-space` 用 flex `gap` 统一处理，子元素有多少个都不用特判。

## 基础用法

<DemoBlock src="/demos/space/basic.vue" title="横向、纵向、预设间距、两端对齐与换行" desc="size 支持 small/medium/large 预设、数字(px)、[横向, 纵向] 数组三种写法。" />

## 预设与自定义

| size | 实际值 |
| --- | --- |
| `small` | `var(--jm-space-2)`（8px） |
| `medium` | `var(--jm-space-4)`（16px） |
| `large` | `var(--jm-space-6)`（24px） |
| 数字 / 字符串 | 按 px / 原样使用 |

需要横向纵向不同间距时传数组：

```vue
<jm-space :size="[8, 12]" wrap>
  <jm-tag v-for="t in tags" :key="t">{{ t }}</jm-tag>
</jm-space>
```

## 行内场景

默认 `display: flex` 占满整行；放在文字流里时加 `inline` 变成 `inline-flex`：

```vue
<span>共 <jm-space inline :size="4"><b>12</b><span>条</span></jm-space> 记录</span>
```

## API

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| direction | 排列方向 | `'horizontal' \| 'vertical'` | `horizontal` |
| size | 间距 | `'small' \| 'medium' \| 'large' \| number \| string \| [横, 纵]` | `small` |
| align | 交叉轴对齐（映射到 flex 的 align-items） | `'start' \| 'center' \| 'end' \| 'baseline' \| 'stretch'` | `center` |
| justify | 主轴分布 | `'start' \| 'center' \| 'end' \| 'between' \| 'around' \| 'evenly'` | `start` |
| wrap | 自动换行 | `boolean` | `false` |
| inline | 行内元素（inline-flex） | `boolean` | `false` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 需要排列的内容 |
