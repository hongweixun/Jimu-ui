---
title: Guide 引导
description: 分步引导遮罩，自动挖孔高亮目标元素，气泡 / 弹窗两种模式，参照 TDesign Guide。
---

# Guide 引导

新手引导：按步骤依次高亮页面元素（遮罩挖孔），配气泡或弹窗说明。参照 TDesign Guide 的交互——目标元素自动滚动到可视区、高亮区跟随滚动/缩放实时重算、`v-model:current` 受控步进。

## 基础用法

<DemoBlock src="/demos/guide/basic.vue" title="气泡式与弹窗式引导" desc="气泡式指向目标元素并支持四方向；弹窗式不指向元素、居中展示，适合开场说明；底部自带 跳过 / 上一步 / 下一步。" />

```vue
<jm-guide v-model:current="current" :steps="steps" />
```

```ts
const steps: GuideStep[] = [
  {
    element: '#search',
    title: '搜索课程',
    content: '在这里输入关键词找课。',
    placement: 'bottom',
    highlightPadding: 6,
  },
]
const current = ref(-1) // -1 表示关闭；引导开始时置 0
```

## 气泡与弹窗混用

每个步骤可独立设置 `mode`：`popover`（默认，指向目标）/ `dialog`（居中弹窗）。同一轮引导里可以混着来——开场用 dialog，逐功能讲解用 popover。

## 行为细节

| 行为 | 说明 |
| --- | --- |
| 自动滚动 | 每步开始时把目标元素 `scrollIntoView` 到屏幕中部再测量 |
| 实时跟随 | 页面滚动、窗口缩放都会重新挖孔定位（滚动用捕获监听，容器内滚动也生效） |
| 步进控制 | `v-model:current` 受控：置 `-1` 关闭；点「完成」或「跳过」会回到 `-1` |
| 高亮外扩 | `highlightPadding` 让挖孔比元素大一圈（默认 0） |

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| steps | 引导步骤 | `GuideStep[]` | - |
| current | 当前步骤（`v-model:current`），`-1` 关闭 | `number` | - |
| zIndex | 遮罩层级 | `number` | `2100` |
| mask | 是否挖孔遮罩（`false` 只盖全屏黑片） | `boolean` | `true` |
| teleport | 挂载容器（选择器或元素）：传后遮罩与气泡限制在容器内，默认挂 body 全屏 | `string \| HTMLElement` | `body` |

### GuideStep

| 字段 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| element | 目标元素（选择器 / 元素 / 函数） | `string \| HTMLElement \| (() => HTMLElement \| null)` | - |
| title | 步骤标题 | `string` | - |
| content | 步骤说明 | `string` | - |
| placement | 气泡方位 `top` `bottom` `left` `right` `center` | `string` | `'bottom'` |
| mode | `popover` / `dialog` | `string` | `'popover'` |
| highlightPadding | 挖孔外扩像素 | `number` | `0` |
| skipText / prevText / nextText | 按钮文案 | `string` | `'跳过' / '上一步' / '下一步'`（最后一步 `'完成'`） |

### Events

| 事件 | 说明 |
| --- | --- |
| update:current | 步骤变化 |
| change | 同上 |
| skip | 点击「跳过」 |
| finish | 走完最后一步或跳过 |
