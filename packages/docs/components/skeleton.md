---
title: Skeleton 骨架屏
description: 加载占位，带扫光动效，可整体关闭动效。
---

# Skeleton 骨架屏

首屏用骨架屏比转圈更能降低「等待感」——用户能预判内容结构。`loading` 为 false 时自动显示默认插槽，所以业务里只是把真实内容包一层，不用写两套结构。

## 基础用法

<DemoBlock src="/demos/skeleton/basic.vue" title="占位与内容切换" desc="1.8 秒后切到真实内容；扫光动效可单独关掉（也会跟随全局 data-motion）。" />

## 用法

```vue
<template>
  <jm-skeleton :loading="loading" avatar :rows="3">
    <UserCard :user="user" />
  </jm-skeleton>
</template>
```

## 自定义排版

内置排版不满足时，用 `#template` 插槽配合三个骨架子组件自由组合（`loading` 为 false 时仍渲染默认插槽）：

<DemoBlock src="/demos/skeleton/template.vue" title="自定义排版与呼吸动效" desc="#template 里用 SkeletonAvatar / SkeletonTitle / SkeletonParagraph 自由组合；animation 传 breath 用透明度呼吸代替扫光。" />

## API

### Skeleton Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| loading | 是否显示骨架 | `boolean` | `true` |
| avatar | 显示头像占位 | `boolean` | `false` |
| avatar-size | 头像尺寸 | `number \| string` | `48` |
| avatar-shape | 头像形状 | `'circle' \| 'square'` | `'circle'` |
| title | 显示标题行 | `boolean` | `true` |
| rows | 段落行数 | `number` | `3` |
| row-width | 行宽，可传数组逐行指定 | `number \| string \| array` | `'100%'` |
| last-row-width | 最后一行宽度 | `number \| string` | `'58%'` |
| title-width | 标题行宽度 | `number \| string` | `'40%'` |
| animation | 动效形态：`shine` 扫光 / `breath` 呼吸 | `'shine' \| 'breath'` | `'shine'` |
| animate | 动效开关 | `boolean` | `true` |
| round | 圆角块（列表占位风格） | `boolean` | `false` |

### Skeleton 插槽

| 名称 | 说明 |
| --- | --- |
| default | loading 为 false 时渲染的内容 |
| template | 自定义骨架排版，优先于内置 avatar/title/rows 结构 |

### SkeletonAvatar Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| size | 尺寸 | `number \| string` | `48` |
| shape | 形状 | `'circle' \| 'square'` | `'circle'` |

### SkeletonTitle Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| width | 标题宽度 | `number \| string` | `'40%'` |

### SkeletonParagraph Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| row | 段落行数 | `number` | `3` |
| row-width | 行宽，可传数组逐行指定（超出循环复用） | `number \| string \| array` | — |
| last-row-width | 最后一行宽度 | `number \| string` | `'58%'` |

::: tip 别把骨架屏做成「假内容」
占位块的高度要接近真实文本行高（这里用 `12px × font-scale`），差太多会在切换瞬间跳一下。行宽随机或递增也比全部 100% 更像文本。
:::
