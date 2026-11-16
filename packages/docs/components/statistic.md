---
title: Statistic 数值统计
description: 展示关键指标，数字变化时带滚动动画，支持千分位、小数位与前缀后缀。
---

# Statistic 数值统计

「本月在线 1,286 人」比「在线人数：1286」更像一个仪表盘。Statistic 把标题、数值、单位三段排好，数值变化时做一次缓出滚动，数字自己走进新值，比直接跳变更容易被注意到。

## 基础用法

<DemoBlock src="/demos/statistic/basic.vue" title="三种字号、动画与前后缀" desc="点按钮换数据，可以看到数字从旧值滚到新值。" />

```vue
<jm-statistic title="当前在线" :value="online" suffix="人" />
<jm-statistic title="平均分" :value="92.5" :precision="1" size="lg" color="#00A0E9" />
<jm-statistic :value="1234567.891" :precision="2" prefix="¥" suffix="元" />
```

数值变化时从**当前显示值**滚到新值，不是每次都从 0 重来；首次渲染才从 0 起步。`duration` 控制时长（默认 900ms），传 `0` 直接落位——列表里成片出现时建议关掉动画。

## 小数位与分隔符

`precision` 不传时按 `value` 自带的小数位推断：`92` 显示两位小数点后的 0 是不必要的，`92.50` 则会保留两位。

| 属性 | 作用 | 示例 |
| --- | --- | --- |
| `precision` | 固定小数位，最多 6 位 | `:precision="2"` → `1,234.50` |
| `separator` | 是否千分位分隔（默认开） | `false` → `1234.5` |
| `groupSeparator` | 千分位符号 | 欧洲习惯传 `'.'` |
| `decimalSeparator` | 小数点符号 | 欧洲习惯传 `','` |

## 前缀与后缀

`prefix` 和 `suffix` 会跟着数值基线对齐，字号自动缩到 0.62em / 0.55em——这样 `¥1,286` 里的币种符号不会和数字抢视线。需要图标或更复杂的排版，用同名插槽：

```vue
<jm-statistic title="完课率" :value="0.864" :precision="1" suffix="%">
  <template #prefix>≈</template>
</jm-statistic>
```

## 非数字内容

`value` 传 `'—'`、`'待统计'` 这类非数字文本时，不做动画、不补小数位，原样展示。加载失败或数据未出时不必再写一个空状态组件。

## 字号

| size | 数值字号 |
| --- | --- |
| `sm` | 18px |
| `md`（默认） | 26px |
| `lg` | 34px |

数值用等宽数字（`tabular-nums`）渲染，滚动过程中宽度不抖；标题 14px 次要色，副说明走默认插槽 12px 三级色。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 标题 | `string` | - |
| value | 数值，非数字原样展示 | `number \| string` | - |
| precision | 小数位，默认按 value 推断 | `number` | - |
| separator | 千分位分隔 | `boolean` | `true` |
| groupSeparator | 千分位符号 | `string` | `','` |
| decimalSeparator | 小数点符号 | `string` | `'.'` |
| prefix | 前缀文字 | `string` | - |
| suffix | 后缀文字 | `string` | - |
| duration | 滚动时长（ms），0 关闭 | `number` | `900` |
| size | 字号 | `'sm' \| 'md' \| 'lg'` | `'md'` |
| color | 数值颜色 | `string` | 一级文字色 |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| title | 自定义标题 |
| prefix | 自定义前缀（图标、符号） |
| suffix | 自定义后缀 |
| default | 数值下方的补充说明 |

### 方法

| 方法 | 说明 |
| --- | --- |
| finish() | 跳过动画，直接落到目标值（适合在截图、打印前调用） |

## 无障碍

滚动期间数字文本每帧都在变，容器显式标了 `aria-live="off"`，避免读屏把中间值一帧一帧念出来。数值本身是普通文本，聚焦或浏览到时仍能正常读到最终值；需要「数值更新时播报」的场景，在外层包一个 `aria-live="polite"` 的区域即可。
