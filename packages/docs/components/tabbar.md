---
title: Tabbar 标签栏
description: 底部导航，支持徽标、小红点、自定义颜色与安全区适配。
---

# Tabbar 标签栏

App 的主框架。默认固定底部并让出 Home Indicator 安全区，`placeholder` 会自动补一块等高占位，页面内容不会被压住。

## 基础用法

<DemoBlock src="/demos/tabbar/basic.vue" title="气泡凸起与中间悬浮" desc="给 item 加 bubble，选中时图标落入渐变圆盘并向上凸起；Tabbar 加 float-center，5 个 tab 时中间项自动悬浮成 FAB（文字隐藏、点击后不自动关闭）。" />

## 完整页面骨架

```vue
<template>
  <div class="app">
    <main class="app__body">
      <router-view />
    </main>
    <jm-tabbar v-model="active" fixed placeholder>
      <jm-tabbar-item name="home" text="首页">
        <template #icon><IconHome /></template>
      </jm-tabbar-item>
      <jm-tabbar-item name="course" text="课程" badge="2">
        <template #icon><IconBook /></template>
      </jm-tabbar-item>
      <jm-tabbar-item name="mine" text="我的">
        <template #icon><IconUser /></template>
      </jm-tabbar-item>
    </jm-tabbar>
  </div>
</template>
```

## API

### Tabbar Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中项的 name | `string \| number` | — |
| fixed | 固定底部 | `boolean` | `true` |
| placeholder | fixed 时生成等高占位 | `boolean` | `true` |
| safe-area-inset-bottom | 让出底部安全区 | `boolean` | `true` |
| border | 顶部描边 | `boolean` | `true` |
| active-color | 选中色 | `string` | `var(--jm-color-primary)` |
| inactive-color | 未选中色 | `string` | `var(--jm-text-color-3)` |
| z-index | 层级 | `number` | `100` |
| background | 背景色 | `string` | `var(--jm-bg-container)` |
| float-center | 中间项自动悬浮成 FAB（奇数个 tab 时取正中间） | `boolean` | `false` |

### TabbarItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 唯一标识，必填 | `string \| number` | — |
| text | 文字 | `string` | — |
| icon | 图标类名（也可用 #icon 插槽） | `string` | — |
| badge | 徽标内容 | `string \| number` | — |
| dot | 只显示小红点 | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| bubble | 选中时图标落入渐变圆盘并向上凸起 | `boolean` | `false` |
| ring | 圆盘外加一圈描边环（bubble / float 通用；未选中的气泡不显示环） | `boolean` | `false` |
| shadow | 圆盘投影，`false` 关掉 | `boolean` | `true` |
| float | 该项悬浮成圆形 FAB（也可由 Tabbar 的 float-center 自动指定） | `boolean` | `false` |

### CSS 变量

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `--jm-tabbar-bubble-size` | 气泡圆盘直径 | `36px` |
| `--jm-tabbar-bubble-lift` | 选中时凸起高度 | `6px` |
| `--jm-tabbar-bubble-bg-from` / `-to` | 圆盘渐变起止色 | `#4cc3f5` / `var(--jm-color-primary)` |
| `--jm-tabbar-bubble-bg` | 整个圆盘背景（覆盖渐变拆分色） | 渐变 |
| `--jm-tabbar-bubble-icon` | 圆盘内图标色 | `#fff` |
| `--jm-tabbar-ring-width` | `ring` 描边环粗细 | `3px` |
| `--jm-tabbar-ring-color` | `ring` 描边环颜色，**默认跟随标签栏底色**（`--jm-tabbar-bg` → `--jm-bg-container`），看起来像被栏面包裹；换深色栏时环自动变深 | `var(--jm-tabbar-bg)` |
| `--jm-tabbar-disc-shadow` | 气泡圆盘阴影（`shadow` 开启时生效） | `0 6px 14px rgba(0,0,0,.16)` |
| `--jm-tabbar-float-shadow` | 悬浮圆盘阴影（`shadow` 开启时生效） | `0 8px 18px rgba(0,0,0,.22)` |

::: tip 关于"整个 Tabbar 的边框"
标签栏顶部那条 1px 细线由 Tabbar 的 `border` 属性控制（默认 `true`），`:border="false"` 即去掉；细线颜色全局走 `--jm-border-color`。demo 演示容器外围的圆角框是文档示例的展示容器，不是组件的边框。
:::
| `--jm-tabbar-float-size` | 悬浮圆盘直径 | `50px` |
| `--jm-tabbar-float-lift` | 悬浮高度 | `16px` |
| `--jm-tabbar-float-bg` / `--jm-tabbar-float-icon` | 悬浮盘背景 / 图标色 | 同气泡 |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 切换选中项 | `string \| number` |
| change | 同 update:modelValue | `string \| number` |

::: warning 文档 demo 里为什么要写 :fixed="false"
演示是在手机模拟框里跑的，`position: fixed` 会相对整个浏览器视口定位，标签栏会跑出手机框底部。真实项目里保持默认 `fixed` 即可。
:::
