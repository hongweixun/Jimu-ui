---
title: IndexBar 索引栏
description: 通讯录、城市列表的右侧字母索引，支持点击、拖动定位与吸顶分组标题。
---

# IndexBar 索引栏

长列表按首字母分组后，右侧给一条索引条，点一下或按住拖动就能跳到对应分组。`jm-index-bar` 负责索引条与滚动监听，`jm-index-anchor` 声明一个分组。

## 基础用法

<DemoBlock src="/demos/index-bar/basic.vue" title="通讯录" desc="分组标题吸顶，索引条高亮跟随滚动；按住索引条上下拖动可连续定位。" />

```vue
<div id="contact" class="contact">
  <jm-index-bar scroll-container="#contact">
    <jm-index-anchor v-for="g in groups" :key="g.letter" :index="g.letter">
      <jm-cell v-for="p in g.people" :key="p" :title="p" clickable />
    </jm-index-anchor>
  </jm-index-bar>
</div>
```

```css
.contact {
  height: 340px;
  overflow-y: auto;
}
```

## 滚动容器

`scroll-container` 不传时监听整页滚动（`window`）。放在手机模拟框、弹窗、或任何 `overflow: auto` 的容器里时，必须告诉组件监听谁：

- 传 CSS 选择器字符串（推荐，写起来最省事）；
- 或传元素本身。

组件在挂载时解析一次容器，所以选择器指向的元素必须在挂载前就存在。

## 吸顶

`sticky`（默认 `true`）给分组标题加 `position: sticky; top: 0`。是否真能吸顶取决于滚动容器——这是原生行为，不需要 JS 介入，也不会破坏文档流。

不想吸顶的场景（例如标题本身有背景图）把它关掉即可：

```vue
<jm-index-bar :sticky="false">…</jm-index-bar>
```

## 高亮与定位

- 滚动时按「最后一个到达容器顶部的分组」决定当前索引；
- 点索引条直接 `scrollTo`，`smooth` 走平滑滚动；
- 按住索引条拖动时会出现大号提示气泡，并实时定位（此时用 `auto`，避免平滑滚动追不上手指）。

## API

### IndexBar Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| indexList | 索引列表；不传则按锚点顺序生成 | `string[]` | - |
| sticky | 分组标题吸顶 | `boolean` | `true` |
| highlightColor | 当前索引的高亮色 | `string` | 主色 |
| scrollContainer | 滚动容器 | `string \| HTMLElement` | `window` |

### IndexBar Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| change | 当前索引变化（滚动或点选） | `index: string` |

### IndexBar Exposes

| 方法 | 说明 |
| --- | --- |
| scrollToIndex(index, smooth?) | 滚到指定索引 |
| active | 当前高亮索引 |

### IndexAnchor Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| index | 分组索引，与索引条一一对应 | `string` | - |
| title | 标题文案，默认显示 index | `string` | - |

### IndexAnchor Slots

| 插槽 | 说明 |
| --- | --- |
| default | 分组内容 |
| title | 自定义标题（可放图标、计数） |

::: tip 与 Sticky 的关系
`IndexAnchor` 的吸顶用的是原生 `sticky`，没有复用 `jm-sticky`：分组标题需要在**自己的分组范围内**停住，`jm-sticky` 是相对滚动容器全局停住，语义不同。
:::
