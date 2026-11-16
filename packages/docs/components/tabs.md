---
title: Tabs 标签页
description: 内容切换，支持下划线、卡片、分段三种形态；标签栏滚动、切换动效、手势滑动、置顶吸顶。
---

# Tabs 标签页

切换同层级的内容。指示器默认**跟激活项文字等宽**（可配 `line-width` 定宽），用 `transform` 移动不触发重排；配合 `Sticky` 组件可实现滚动置顶。

## 基础用法

<DemoBlock src="/demos/tabs/basic.vue" title="滚动 / 动效 / 手势 / 吸顶" desc="line 指示器默认跟文字等宽；scrollable 标签栏滚动；animated 平移动效；swipeable 手势切换；Sticky 包住 Tabs 即可吸顶。" />

## 标签栏滚动

标签较多时传 `scrollable`，标签栏可横向滚动（隐藏滚动条），激活项自动滚动到中间。`visible-count` 控制一屏可见的标签数量（默认 3）：

```html
<jm-tabs v-model="active" scrollable :visible-count="4">
  <jm-tab v-for="i in 8" :key="i" :name="`c${i}`" :label="`分类 ${i}`">…</jm-tab>
</jm-tabs>
```

## 切换动效与手势

`animated` 开启内容区 track 平移动效；`swipeable` 开启手势滑动切换——基于 **Pointer Events**，触屏左右滑和桌面鼠标拖拽都能触发（自带方向锁，`touch-action: pan-y` 不干扰页面纵向滚动；两端有阻尼回弹；拖过 25% 宽度即翻页）。`duration` 控制动效时长（默认 300ms）。`swipeable` 会自动启用 track 布局，无需再传 `animated`。

```html
<jm-tabs v-model="active" animated swipeable :duration="300">
  <jm-tab name="a" label="第一页">…</jm-tab>
  <jm-tab name="b" label="第二页">…</jm-tab>
</jm-tabs>
```

## 置顶吸顶（Sticky）

`Sticky` 是独立的粘性布局组件（详见 [Sticky 粘性布局](/components/sticky)），用原生 `position: sticky` 实现：由最近的滚动容器驱动，不监听 scroll、不打破文档流。包住 Tabs 即可在内容滚过时把标签栏钉在顶部：

```html
<jm-sticky :offset-top="0">
  <jm-tabs v-model="active" animated swipeable>…</jm-tabs>
</jm-sticky>
```

也可以单独包 NavBar、索引栏等任意需要吸顶的内容。

## 指示器宽度

line 形态的指示器默认**跟激活项文字等宽**并跟随切换平滑移动；需要固定宽度时传 `line-width`（数字按 px），会居中在激活项下方：

```html
<jm-tabs v-model="active" :line-width="24">…</jm-tabs>
```

## API

### Tabs Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 当前激活的 name | `string \| number` | 第一个 tab |
| type | 形态 | `'line' \| 'card' \| 'segment'` | `'line'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| color | 激活色 | `string` | `var(--jm-color-primary)` |
| radius | 圆角（card / segment 生效） | `number \| string` | `var(--jm-radius)` |
| padded | 内容区是否加内边距 | `boolean` | `true` |
| animated | 内容切换动效（track 平移） | `boolean` | `false` |
| swipeable | 手势滑动切换（自动启用 track 布局） | `boolean` | `false` |
| duration | 动效时长，数字按 ms | `number \| string` | `300` |
| scrollable | 标签栏横向滚动，激活项自动滚到中间 | `boolean` | `false` |
| visibleCount | scrollable 时一屏可见的标签数量 | `number` | `3` |
| lineWidth | line 指示器宽度，默认跟文字等宽；数字按 px，定宽居中 | `number \| string` | 跟随文字 |
| beforeChange | 切换前钩子，返回 false / reject 则不切换 | `(name) => boolean \| Promise<boolean>` | — |

### Tab Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 唯一标识 | `string \| number` | — (必填) |
| label | 标签文字 | `string` | — (必填) |
| disabled | 禁用 | `boolean` | `false` |
| badge | 角标内容 | `string \| number` | — |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 切换 | `string \| number` |
| change | 切换 | `string \| number` |
| click | 点击标签（disabled 也会触发） | `string \| number` |

### Tabs 方法（defineExpose）

| 方法 | 说明 |
| --- | --- |
| resize | 重新测量指示器（容器尺寸变化后可手动触发） |
| scrollToActive | 把激活项滚动到标签栏中间 |

### 键盘操作

| 按键 | 行为 |
| --- | --- |
| `Tab` | 整组标签只占一个停靠点，落在当前激活项上 |
| `←` / `→`（`↑` / `↓`） | 切到相邻标签，自动跳过 `disabled`，到头环绕 |
| `Home` / `End` | 第一个 / 最后一个标签 |
| `Enter` / `Space` | 同点击 |

这是 WAI-ARIA tabs 的 roving tabindex 模式：标签多的时候，键盘用户不必按十几次 Tab 穿过标签栏。

## 切换拦截
表单页切走前要问一句「内容没保存，确定离开？」——把判断放进 `beforeChange` 就行：

<DemoBlock src="/demos/tabs/before-change.vue" title="离开前二次确认" desc="返回 Promise 时 Tabs 会等结论，异步期间连点不会叠起多次确认。" />

```vue
<jm-tabs v-model="active" :before-change="beforeChange">
  <jm-tab name="basic" title="基本信息" />
  <jm-tab name="submit" title="提交结果" />
</jm-tabs>
```

```ts
function beforeChange(name) {
  if (name !== 'submit') return true          // 同步放行
  return new Promise<boolean>((resolve) => {  // 异步等用户点确认
    ask(resolve)
  })
}
```

规则很直白：

- 返回 `true` / 不返回 → 放行；返回 `false` 或 `reject` → 拦下，标签保持原样。
- 异步期间再点别的标签会被忽略，不会排队弹出第二个确认框（避免叠对话框）。
- 点当前已激活的标签不触发 `beforeChange`（没有切换动作）。
- 手势 `swipeable` 也走同一套校验：拦下时轨道自动弹回原位。

## Sticky Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| offset-top | 吸顶后距滚动容器顶部的偏移，数字按 px | `number \| string` | `0` |
| z-index | 吸顶层 z-index | `number \| string` | `99` |

::: tip sticky 生效条件
`position: sticky` 需要**滚动容器内**有足够的内容高度；组件本身不监听滚动，嵌套滚动容器（如弹窗内）同样直接生效。
:::

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-tabs-color` | 激活色 |
| `--jm-tabs-radius` | 圆角 |

::: tip 标签很多时
开启 `scrollable`，激活项会自动滚到中间；不开启时标签均分宽度、超长省略。
:::
