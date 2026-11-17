---
title: Pagination 分页
description: 移动端分页器，悬浮卡片式页码条、页码折叠、简单模式、条数切换与快速跳转。
---

# Pagination 分页

移动端列表大多用「加载更多 / 下拉刷新」，但成绩单、题库、订单记录这类**需要跳转定位**的场景，分页器仍然是最直接的。

::: tip 先想清楚要不要分页
无限滚动适合「浏览」，分页适合「定位」——用户心里有个页码或要回到第几页时，分页器比无限滚动好用得多。一页 10~20 条、总共几十页以内，用分页；数据流式增长、用户只看最新的，用 List 加载更多。
:::

## 基础用法

普通模式是一条**悬浮卡片式页码条**：白色底 + 浅阴影，当前页为主色实底圆角块。配合 `show-size-changer` 可以切换每页条数：

<DemoBlock src="/demos/pagination/basic.vue" title="基础、总数、简单模式、快速跳转" desc="总页数由 total 与 pageSize 推导，也可直接传 pageCount；current 与 pageSize 双向绑定，change 事件返回 (page, size)。" />

```vue
<jm-pagination v-model="page" v-model:page-size="size" :total="96" show-size-changer />
```

## 页码折叠

页码多于 `pager-count`（默认 5）时自动折叠，规则是「首尾常驻 + 当前页居中」：

| 当前页 | 显示 |
| --- | --- |
| 第 1 页 | `1 2 3 4 … 10` |
| 第 5 页 | `1 … 4 5 6 … 10` |
| 第 10 页 | `1 … 7 8 9 10` |

省略号本身是**可点的按钮**：点前半段往前跳一屏，点后半段往后跳一屏——省掉「一格一格点」的麻烦。

## 总数与快速跳转

`total` 插槽显示数据总量和当前范围；`show-quick-jumper` 显示「跳至 N 页」输入框，输入越界页码会红字提示：

```vue
<jm-pagination v-model="page" :total="96" show-quick-jumper>
  <template #total="{ total, range }">
    共 {{ total }} 条，当前 {{ range[0] }}-{{ range[1] }} 条
  </template>
</jm-pagination>
```

## 简单模式

只保留「箭头 / 当前页 共 N 页 / 箭头」，适合空间紧张或页码意义不大的场景：

```vue
<jm-pagination v-model="page" simple :total="96" :page-size="10" />
```

## 窄容器自适应

组件自身是 CSS 容器，宽度不够时**分级压缩**：先收紧间距，再缩小页码，≤300px 才收起「上一页 / 下一页」文字只留箭头。宽度跟着组件自身走而不是视口——放进手机模拟框、侧栏、半屏弹层等窄容器里也会正确分级；不会出现文字与页码重叠。

## 参数怎么给

| 你的数据 | 传什么 |
| --- | --- |
| 有总条数 | `total` + `pageSize` |
| 只有总页数 | `pageCount` |
| 服务端已算好页数 | `pageCount`，`total` 不用传 |

`pageCount` 优先级高于 `total`；两者都不传时按 1 页处理。传了 `pageCount` 时每页条数切换器不显示（页数固定）。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前页（`v-model`） | `number` | `1` |
| total | 总条数 | `number` | `0` |
| pageSize | 每页条数（`v-model:page-size`） | `number` | `10` |
| pageCount | 总页数，优先于 total | `number` | - |
| simple | 简单模式 | `boolean` | `false` |
| pagerCount | 数字页码最多几个 | `number` | `5` |
| disabled | 禁用 | `boolean` | `false` |
| iconOnly | 上下页只显示箭头 | `boolean` | `false` |
| prevText | 上一页文字 | `string` | `'上一页'` |
| nextText | 下一页文字 | `string` | `'下一页'` |
| hideOnSinglePage | 只有一页时整体隐藏 | `boolean` | `false` |
| showSizeChanger | 显示每页条数切换器 | `boolean` | `false` |
| sizeOption | 每页条数可选项 | `number[]` | `[10, 20, 50, 100]` |
| showQuickJumper | 显示快速跳转输入框（普通模式） | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 页码变化 | `(page: number)` |
| update:pageSize | 每页条数变化 | `(size: number)` |
| change | 页码或条数变化 | `(page: number, size: number)` |

### 插槽

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| total | 总数与当前范围文案 | `{ total: number, range: [number, number] }` |
| 默认 | 追加在分页条尾部 | - |
