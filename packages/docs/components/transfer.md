---
title: Transfer 穿梭框
description: 左右两块列表之间搬数据，适合「从一堆里挑几个」的场景。
---

# Transfer 穿梭框

勾选、搬过去、再勾选、搬回来——「从全集里挑一部分」这件事用穿梭框表达最直白。手机屏幕窄，两栏上下排，中间一行按钮承接移动。

## 基础用法

<DemoBlock src="/demos/transfer/basic.vue" title="章节可见性：把可选章节搬到已选" desc="上下两块面板分别是「还没选」和「已选」，中间按钮上的数字是当前勾选了几项；有搜索、有全选，禁用项不可勾选也不参与全选。" />

```vue
<jm-transfer
  v-model="selected"
  :data="data"
  :titles="['可选章节', '已选章节']"
  @change="(values, info) => console.log(info.direction, info.moved)"
/>
```

`model-value` 只存**已选的值**，顺序跟着 `data` 走，不会因为先后添加顺序不同而乱掉。

## 勾选与全选

每块面板右上角有全选。全选只作用于**当前搜索结果**：搜「1.」之后点全选，加进去的只有匹配的那几条，不会把整份数据都搬过去。

```vue
<jm-transfer v-model="selected" :data="data" searchable height="200px" />
```

面板中间的按钮是半选状态的说明——勾了一部分时，按钮上显示 `添加 2`，一处没勾时按钮禁用。

## 禁用项

```ts
const data = [
  { label: '3.1 打包与分包策略', value: 'l8', desc: '暂未开放', disabled: true },
]
```

禁用的项会置灰、点不动、不参与全选计算，也不会被移动。常用于「未解锁的章节」「已下架的商品」。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| data | 全部可选数据 | `TransferItem[]` | `[]` |
| model-value / v-model | 已选的值 | `(string \| number)[]` | — |
| titles | 左右（上下）两侧标题 | `[string, string]` | `['可选', '已选']` |
| searchable | 面板内搜索 | `boolean` | `true` |
| height | 每个列表的可视高度 | `string` | `220px` |
| empty-text | 可选列表为空时的文案 | `string` | `没有可选项` |
| disabled | 整体禁用 | `boolean` | `false` |

### TransferItem

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| label | 主文案 | `string` |
| value | 唯一值 | `string \| number` |
| desc | 次行说明 | `string` |
| disabled | 禁用 | `boolean` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:model-value | 已选值变化 | `values` |
| change | 发生移动 | `(values, info)`，`info.direction` 为 `to-right` / `to-left`，`info.moved` 是本次移动的值 |

## 和 CheckboxGroup 怎么选

| 场景 | 用哪个 |
| --- | --- |
| 选项少（一屏能看完）、不需要强调「已选」 | CheckboxGroup |
| 选项多、需要搜索、需要明确区分「已选 / 未选」 | Transfer |
| 层级数据里挑几个 | Tree（`checkable`） |
| 需要给已选项排序 | Transfer + 自己做一个拖拽排序列表 |

穿梭框的成本在于「两块列表占两次屏幕高度」。手机上如果只是勾三五个复选框，直接用 CheckboxGroup 更省地方。
