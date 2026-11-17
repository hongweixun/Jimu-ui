---
title: Descriptions 描述列表
description: 键值对详情展示，支持多列、跨列、表格线与标签在上两种方向。
---

# Descriptions 描述列表

「订单号：JM2026…」这类详情页，手写十几行 `label + value` 最容易出问题是**对不齐**：字段名两个字和六个字混在一起，值列怎么摆都是锯齿。Descriptions 用 grid 固定标签列宽，多列时每列宽度一致，扫读时视线能顺着一条竖线往下走。

底层是 `<dl>` / `<dt>` / `<dd>`，语义上就是「名称—描述」成对出现的关系，读屏会念成「订单号，JM2026…」。

## 基础用法

<DemoBlock src="/demos/descriptions/basic.vue" title="单列订单详情与两列字段" desc="label-width 决定标签列宽，不传时取 72px；两列时每列的标签宽度都一致，右对齐更整齐。" />

```vue
<jm-descriptions title="订单信息" label-width="76">
  <jm-descriptions-item label="订单号" value="JM20261116001" />
  <jm-descriptions-item label="订单状态" value="待收货" />
  <jm-descriptions-item label="收货地址" value="浙江省杭州市…" />
</jm-descriptions>
```

`title` 会横跨整行显示在顶部，也可以换成 `#title` 插槽放标题加操作按钮。

## 表格线

`border` 打开后每个字段变成带线单元格，标签列铺浅底色——字段多、需要一眼扫完时比纯文字更清楚。

<DemoBlock src="/demos/descriptions/border.vue" title="表格线、跨列、栅栏方向与自定义值" desc="span=2 让「备注」横跨整行；direction=“vertical” 把标签换到值上方，适合窄屏和长字段名。" />

```vue
<jm-descriptions :column="2" border label-width="72">
  <jm-descriptions-item label="合同编号" value="HT-2026-1116-07" />
  <jm-descriptions-item label="签署日期" value="2026-11-16" />
  <jm-descriptions-item label="备注" :span="2" value="首期款于签署后 5 个工作日内支付。" />
</jm-descriptions>
```

表格线只画上、左两条外框，右、下由每个单元格自己补齐：这样最后一行、最后一列的外框自然收口，不需要再写 `:last-child` 去线，也不会因为 `span` 变化出现断线。

## 两种方向

| `direction` | 排布 | 适合 |
| --- | --- | --- |
| `horizontal`（默认） | 标签在左、值在右 | 字段名短（2–4 字），一屏放得多 |
| `vertical` | 标签在上、值在下 | 字段名长、值很长，或手机窄屏 |

`vertical` 下标签会自动降一号字并变次要色，值单独占一行，长地址换行不会把标签挤成两行。

## 列数与跨列

`column` 是**一行放几项**，不是 grid 的列数——`horizontal` 下每项内部还分「标签 / 值」两格，所以实际网格列数是 `column × 2`。

`span` 是跨几项：`horizontal` 下 `span=2` 会占「标签 + 值 + 标签 + 值」共 4 格。跨列项放不下时会自动换到下一行，不会溢出容器。

## 冒号与对齐

| 属性 | 说明 |
| --- | --- |
| `colon` | 标签后加「：」（默认开，仅 `horizontal` 生效） |
| `label-align` | `left`（默认）/ `right`，表格线模式下 `right` 更常见 |

`vertical` 方向不会加冒号——标签已经独占一行，冒号没有意义。

## API

### Descriptions Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| column | 一行放几项 | `number` | `1` |
| border | 显示表格线 | `boolean` | `false` |
| label-width | 标签列宽，数字按 px | `number \| string` | `72px` |
| label-align | 标签对齐 | `'left' \| 'right'` | `'left'` |
| direction | 排列方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| colon | 标签后加冒号 | `boolean` | `true` |
| size | 单元格内边距 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| title | 顶部标题 | `string` | - |

### DescriptionsItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| label | 字段名 | `string` | - |
| value | 字段值 | `string \| number` | - |
| span | 跨几项 | `number` | `1` |

### 插槽

| 组件 | 插槽 | 说明 |
| --- | --- | --- |
| Descriptions | title | 自定义顶部标题 |
| DescriptionsItem | label | 自定义字段名（带图标、必填星号） |
| DescriptionsItem | default | 自定义值（状态点、按钮、链接） |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-desc-label-w` | 标签列宽兜底值 | `72px` |
| `--jm-desc-border-color` | 表格线颜色 | `--jm-border-color` |
| `--jm-desc-label-bg` | 标签列底色（表格线模式） | `--jm-bg-page` |
| `--jm-desc-pad-inline` | 内容与白色背景之间的左右间距（无边框模式） | `16px`（small `12px` / large `20px`） |

## 无障碍

用 `<dl>` 承载，标签是 `<dt>`、值是 `<dd>`，读屏会把「订单号」和它的值作为一个整体念出来，不需要额外 `aria-label`。值为空时仍会保留 `<dd>`，避免读屏把两项错误的配成一对。需要强调的字段（如金额）在值插槽里用 `<strong>` 包一层即可，不要只靠颜色区分。
