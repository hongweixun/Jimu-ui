---
title: DatePicker 日期选择器
description: 基于 Picker 的日期/时间选择，支持日期、年月、时间与日期时间四种形态。
---

# DatePicker 日期选择器

`jm-date-picker` 把 `jm-picker` 的滚轮能力封装成日期语义：自动生成年、月、日、时、分各列，处理大小月与闰年，并把越界项置灰。

## 基础用法

<DemoBlock src="/demos/date-picker/basic.vue" title="日期、年月、日期时间、自定义文案" desc="弹层里用 Popup 包一层；内嵌时直接放在页面中即可。" />

## 常用形态

```vue
<jm-cell title="上课日期" :value="dateText" is-link clickable @click="show = true" />
<jm-popup v-model:show="show" position="bottom" round :safe-area="false">
  <jm-date-picker
    v-model="date"
    type="date"
    title="选择日期"
    :min-date="new Date(2026, 0, 1)"
    :max-date="new Date(2026, 11, 31)"
    @confirm="show = false"
    @cancel="show = false"
  />
</jm-popup>
```

- `modelValue` 是**字符串数组**（各列的值），不是 `Date`：`['2026', '11', '18']`。这样跨端传值不会踩时区坑；
- `confirm` 事件里额外给了拼好的 `selectedDate`，需要 `Date` 时直接用；
- 没选过值时默认落在今天，超出 `min-date` / `max-date` 会自动收敛到边界。

## 类型与列

| type | 列 | 值示例 |
| --- | --- | --- |
| `date`（默认） | 年 / 月 / 日 | `['2026','11','18']` |
| `year-month` | 年 / 月 | `['2026','11']` |
| `time` | 时 / 分 | `['09','30']` |
| `datetime` | 年 / 月 / 日 / 时 / 分 | `['2026','11','18','09','30']` |

`datetime` 是五列，360px 宽度下每列约 70px，足够点选；屏幕更窄时建议改用「日期 + 时间」两次选择。

## 越界处理

`min-date` 与 `max-date` 同时作用于三处：

1. **月份**：边界年份里超出范围的月份置灰；
2. **日期**：超出范围的日期置灰，`disabled` 项在拖动吸附时会被跳过；
3. **时分**：`datetime` 下若当天就是边界日，越界的时分置灰。

改年/月导致日期越界时（例如 1 月 31 日切到 2 月），组件会把日**收敛到当月最后一天**，而不是跳到 1 号。

## 自定义文案

```ts
const formatter = (type: 'year' | 'month' | 'day' | 'hour' | 'minute', value: string) => {
  if (type === 'hour') return `${value} 点`
  if (type === 'minute') return `${value} 分`
  return value
}
```

默认文案是「2026年 / 11月 / 18日 / 09时 / 30分」。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 各列选中的值 | `string[]` | `[]` |
| type | 选择器类型 | `'date' \| 'year-month' \| 'time' \| 'datetime'` | `'date'` |
| title | 顶部标题 | `string` | `选择日期` |
| minDate | 最小可选日期 | `Date` | `2000-01-01` |
| maxDate | 最大可选日期 | `Date` | `2030-12-31` |
| formatter | 自定义每列文案 | `(type, value) => string` | - |
| confirmButtonText | 确认按钮文案 | `string` | `确认` |
| cancelButtonText | 取消按钮文案 | `string` | `取消` |
| itemHeight | 每项高度（px） | `number` | `44` |
| visibleCount | 可见项数 | `number` | `5` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 选中值变化 | `string[]` |
| change | 拖动停下即触发 | `{ selectedValues, selectedDate }` |
| confirm | 点确认 | `{ selectedValues, selectedDate }` |
| cancel | 点取消 | - |

### Exposes

| 方法 | 说明 |
| --- | --- |
| confirm() | 以当前值触发一次确认 |
| cancel() | 触发取消 |
| values | 当前各列值 |
