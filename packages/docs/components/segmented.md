---
title: Segmented 分段控制器
description: 在少量互斥选项之间切换，滑块跟随选中项平移。
---

# Segmented 分段控制器

2~5 个互斥选项的切换器。相比 Tabs，它更紧凑、更像「开关」；相比 Radio，它的选中态更醒目，适合放在列表顶部做视图切换（全部 / 进行中 / 已结束）。

选项多于 5 个或文案较长时，用 [Tabs](/components/tabs)，分段控制器挤不下会截断。

## 基础用法

<DemoBlock src="/demos/segmented/basic.vue" title="尺寸、图标与禁用" desc="options 支持纯文字、带图标、单段禁用。" />

```vue
<jm-segmented v-model="tab" :options="tabs" @change="onChange" />
```

```ts
const tabs = [
  { label: '全部', value: 'all' },
  { label: '进行中', value: 'doing' },
  { label: '已结束', value: 'done', disabled: true },
]
```

## 滑块怎么动

滑块宽度 = 内容区宽度 ÷ 段数，位移用 `translateX(段号 × 100%)`，所以：

- 段数变化（动态增删选项）不需要额外测量，重算 `--jm-segmented-count` 即可；
- 位移只走 transform，不触发布局，滑动过程不掉帧；
- 选中项切换时走弹性曲线，停下来的瞬间有一点点回弹，和 Switch 的手感一致。

## 尺寸

| size | 高度 | 场景 |
| --- | --- | --- |
| `small` | 28px | 卡片内的次级切换 |
| `medium`（默认） | 34px | 页面主切换 |
| `large` | 40px | 顶部主导航式切换 |

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前值（`v-model`） | `string \| number` | - |
| options | 选项列表 | `SegmentedOption[]` | `[]` |
| disabled | 禁用整组 | `boolean` | `false` |
| block | 撑满父容器（否则 inline） | `boolean` | `true` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| activeColor | 选中项文字色 | `string` | 主色 |
| indicatorColor | 滑块底色 | `string` | 卡片色 |

`SegmentedOption`：`{ label?: string; value: string | number; icon?: string; disabled?: boolean }`。

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 选中项变化 | `string \| number` |
| change | 同上，便于只监听变化 | `(value, index)` |

## 和无障碍

容器是 `role="tablist"`，每段是 `role="tab"` + `aria-selected`，禁用段带原生 `disabled`。

键盘走 roving tabindex：整组只占一个 Tab 停靠点（停在选中段上），进去后用 `←` `→`（`↑` `↓`）切换，`Home` / `End` 跳首尾，禁用段自动跳过、到头环绕。鼠标与手指的点击行为完全不变。
