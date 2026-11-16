---
title: Pagination 分页
description: 移动端分页器，支持页码折叠、简单模式与禁用态。
---

# Pagination 分页

移动端列表大多用「加载更多 / 下拉刷新」，但成绩单、题库、订单记录这类**需要跳转定位**的场景，分页器仍然是最直接的。

::: tip 先想清楚要不要分页
无限滚动适合「浏览」，分页适合「定位」——用户心里有个页码或要回到第几页时，分页器比无限滚动好用得多。一页 10~20 条、总共几十页以内，用分页；数据流式增长、用户只看最新的，用 List 加载更多。
:::

## 基础用法

<DemoBlock src="/demos/pagination/basic.vue" title="基础、多页码、简单模式" desc="总页数由 total 与 pageSize 推导，也可直接传 pageCount。" />

```vue
<jm-pagination v-model="page" :total="96" :page-size="10" />
```

## 页码折叠

页码多于 `pager-count`（默认 5）时自动折叠，规则是「首尾常驻 + 当前页居中」：

| 当前页 | 显示 |
| --- | --- |
| 第 1 页 | `1 2 3 4 … 10` |
| 第 5 页 | `1 … 4 5 6 … 10` |
| 第 10 页 | `1 … 7 8 9 10` |

省略号本身是**可点的按钮**：点前半段往前跳一屏，点后半段往后跳一屏——省掉「一格一格点」的麻烦。

## 简单模式

只保留「上一页 / 当前页 共 N 页 / 下一页」，适合空间紧张或页码意义不大的场景：

```vue
<jm-pagination v-model="page" simple :total="96" :page-size="10" />
```

## 只显示箭头

`icon-only` 去掉「上一页 / 下一页」文字。窄屏（≤ 420px）下组件会自动隐藏这两个文字，避免挤掉页码——手机上通常不需要显式传。

## 参数怎么给

| 你的数据 | 传什么 |
| --- | --- |
| 有总条数 | `total` + `pageSize` |
| 只有总页数 | `pageCount` |
| 服务端已算好页数 | `pageCount`，`total` 不用传 |

`pageCount` 优先级高于 `total`；两者都不传时按 1 页处理。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前页（`v-model`） | `number` | `1` |
| total | 总条数 | `number` | `0` |
| pageSize | 每页条数 | `number` | `10` |
| pageCount | 总页数，优先于 total | `number` | - |
| simple | 简单模式 | `boolean` | `false` |
| pagerCount | 数字页码最多几个 | `number` | `5` |
| disabled | 禁用 | `boolean` | `false` |
| iconOnly | 上下页只显示箭头 | `boolean` | `false` |
| prevText | 上一页文字 | `string` | `'上一页'` |
| nextText | 下一页文字 | `string` | `'下一页'` |
| hideOnSinglePage | 只有一页时整体隐藏 | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 页码变化 | `number` |
| change | 同上 | `number` |

### 插槽

默认插槽放在最右侧，可加「共 96 条」这类统计文案：

```vue
<jm-pagination v-model="page" :total="96">
  <span class="total">共 96 条</span>
</jm-pagination>
```
