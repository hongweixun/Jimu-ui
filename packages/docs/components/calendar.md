---
title: Calendar 日历
description: 单选、区间、多选三种模式，支持圆形/方形两种选中样式、月份面板切换、逐日定制与可选范围限制。
---

# Calendar 日历

预约、请假、打卡场景的日期选择。固定 6 行 × 7 列渲染，翻月时不会因为月份天数不同而跳高度。

## 基础用法

<DemoBlock src="/demos/calendar/basic.vue" title="单选定制、区间、多选限制" desc="formatter 可给单个日期加标记；type=range 点两次成区间；min-date / max-date 限制可选范围。" />

## 选中样式

`shape` 控制选中态：默认 `circle` 圆形；`square` 为整格色块（TDesign 风格），区间起止只圆外侧两个角，中间格用浅色带连成一条。

日期上下的描述（`topInfo` / `bottomInfo`）采用**绝对定位贴格子上下缘**，不参与布局：无论是否有备注、是否多选/区间，数字都保持同一基线，色带也始终与数字对齐，不会出现错位。

<DemoBlock src="/demos/calendar/shape.vue" title="方形选中 + 区间 + 备注" desc="shape=square 时为整格色块；有备注文字的日期，数字与区间色带依然对齐。" />

## 月份面板

`switch-mode` 让月份标题可点击，弹出滚轮面板快速跳转：

| 取值 | 行为 |
| --- | --- |
| `none` | 默认，只能用箭头 / 横滑翻月 |
| `month` | 点标题选月份（当年 1–12 月） |
| `year-month` | 点标题选年 + 月，年份范围跟随 `min-date` / `max-date`（未传则当前年 ±10 年） |

面板锚定在标题行下方展开（带淡入动画），点面板外区域关闭；年份范围跟随 `min-date` / `max-date`（未传则当前年 ±10 年）。切换后派发 `month-change`。

<DemoBlock src="/demos/calendar/switch-mode.vue" title="点标题选月份 / 选年月" desc="switch-mode=month 选月；switch-mode=year-month 选年月；month-change 会带上新的月份。" />

## 禁用与只读

`disable-date` 接收日期返回是否禁用，与 `min-date` / `max-date`、`formatter.disabled` 取并集；`readonly` 下只能翻月不能改选。

<DemoBlock src="/demos/calendar/disable.vue" title="自定义禁用规则与只读" desc="disable-date 可做「只能选周末」这类业务规则；readonly 保留翻月但禁用选择。" />

## 三种模式

| type | v-model | 交互 |
| --- | --- | --- |
| `single` | `Date` | 点选一天 |
| `range` | `Date[]` | 第一次点起点，第二次点终点；已有完整区间后再点则重新开始 |
| `multiple` | `Date[]` | 点一次加入，再点移除 |

`range` 在只选了起点时，`v-model` 里只有一个元素；补上终点后变成两个，且顺序总是**早 → 晚**（反着点会自动交换）。

## 逐日定制

`formatter` 接收当天的基础信息，返回对象会覆盖默认字段：

```ts
function formatter(day: CalendarDay) {
  if (day.type === 'current' && day.day % 7 === 0) return { bottomInfo: '名额紧张' }
}
```

可覆盖字段：`text`（显示文字）、`topInfo`（日期上方）、`bottomInfo`（日期下方）、`className`、`disabled`。
返回的 `disabled` 会与 `min-date` / `max-date` 的结果取并集，不能用来「解锁」超出范围的日期。

## 关于「今天」

今天的日期数字会以主色描边高亮（选中时被实底样式覆盖）。头部不再提供「今天」按钮——页面较长时直接点两次箭头，或调用实例方法 `goToday()` 带方向动画翻回今天所在月。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 选中值 | `Date \| Date[]` | — |
| type | 选择模式 | `'single' \| 'range' \| 'multiple'` | `'single'` |
| title | 标题 | `string` | `'选择日期'` |
| subtitle | 副标题（默认显示当前月份） | `string` | — |
| show-title | 显示标题 | `boolean` | `true` |
| show-subtitle | 显示月份切换栏 | `boolean` | `true` |
| show-confirm | 显示底部确认按钮 | `boolean` | `true` |
| confirm-text | 确认文案 | `string` | `'确定'` |
| confirm-disabled-text | 未选日期时的按钮文案 | `string` | — |
| min-date | 最小可选日期 | `Date \| string` | — |
| max-date | 最大可选日期 | `Date \| string` | — |
| first-day-of-week | 一周从周几开始（0=周日，1=周一） | `0 \| 1` | `0` |
| row-height | 每行高度 | `number \| string` | `64` |
| color | 选中色 | `string` | `var(--jm-color-primary)` |
| shape | 选中态形状 | `'circle' \| 'square'` | `'circle'` |
| readonly | 只读（可翻月不可改选） | `boolean` | `false` |
| allow-same-day | 区间允许起止同一天 | `boolean` | `true` |
| disable-date | 自定义禁用规则 | `(date: Date) => boolean` | — |
| switch-mode | 月份切换方式 | `'none' \| 'month' \| 'year-month'` | `'none'` |
| format | 自定义月份标题 | `(date: Date) => string` | — |
| formatter | 逐日定制 | `(day: CalendarDay) => Partial<CalendarDay> \| void` | — |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选中值变化 | `Date \| Date[]` |
| select | 点击某一天 | `date: Date` |
| confirm | 点击确认 | `Date \| Date[]` |
| month-change | 展示月份变化（箭头 / 横滑 / 月份面板） | `month: Date` |

### 实例方法

| 方法 | 说明 |
| --- | --- |
| prevMonth() / nextMonth() | 翻月（带方向滑动动画） |
| goToday() | 回到今天所在月（自动按跨的月数决定滑动方向） |
| openMonthPanel() | 打开月份 / 年月面板（`switch-mode` 不为 `none` 时有效） |

### 翻页交互

参照 TDesign 移动端日历：月份切换栏左右两个素色箭头；在日期网格上**横向滑动**（位移 > 48px 且大于纵向位移 1.5 倍）同样可以翻月，翻页时整页带方向滑动动画。

点击命中做了移动端加固：触摸/触控笔的轻点在 `pointerup` 里以**按下位置的那一天**为准（横向漂移 ≤ 48px、纵向 ≤ 10px 仍算轻点），不依赖浏览器派发的 click——部分内嵌 WebView 会因手指微抖吞掉 click 或把点击落到相邻格，表现为“点了几次才选中 / 选到隔壁一天”。鼠标与键盘仍走原生 click。按下时数字有轻微缩放反馈。
