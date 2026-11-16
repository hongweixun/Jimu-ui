---
title: NavBar 导航栏
description: 页面顶部导航，带安全区适配、返回箭头与左右插槽。
---

# NavBar 导航栏

移动端每个二级页面的顶部都需要它。默认已让出状态栏安全区（刘海屏、灵动岛），`fixed` 时会自动补等高占位块，不会盖住页面内容。

## 基础用法

<DemoBlock src="/demos/nav-bar/basic.vue" title="标题、返回与右侧操作" desc="左侧有箭头或文字时才可点，避免误触空白区域。" />

## 页面里怎么摆

```vue
<template>
  <jm-nav-bar title="课程详情" left-arrow left-text="返回" fixed placeholder @click-left="router.back()" />
  <div class="page-body">…</div>
</template>
```

`fixed` + `placeholder` 必须成对使用：前者让导航栏吸顶，后者补一块与之等高的占位，否则正文第一屏会被遮住。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 标题文字 | `string` | — |
| left-text | 左侧文字 | `string` | — |
| left-arrow | 显示返回箭头 | `boolean` | `false` |
| right-text | 右侧文字 | `string` | — |
| border | 底部 1px 描边（0.5px 视觉） | `boolean` | `true` |
| fixed | 吸顶固定 | `boolean` | `false` |
| placeholder | fixed 时生成等高占位 | `boolean` | `false` |
| safe-area-inset-top | 让出状态栏安全区 | `boolean` | `true` |
| z-index | 层级 | `number` | `100` |
| background | 背景色 | `string` | `var(--jm-bg-container)` |
| color | 文字色 | `string` | `var(--jm-text-color)` |

### 事件

| 事件名 | 说明 |
| --- | --- |
| click-left | 点击左侧（有箭头或文字时） |
| click-right | 点击右侧 |

### 插槽

| 名称 | 说明 |
| --- | --- |
| left | 自定义左侧，替代箭头 + 文字 |
| title | 自定义标题（可放头像、下拉等） |
| right | 自定义右侧（图标按钮组） |

::: tip 适老模式下导航栏不会被撑破
标题字号会随 `data-elder` 放大到 20px，但栏高是固定的 46px，内部用 `--jm-size-scale` 单独控制。业务页面正文的放大不影响这里。
:::
