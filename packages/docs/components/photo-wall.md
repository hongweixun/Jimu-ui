---
title: PhotoWall 照片墙
description: 瀑布流照片墙，列数随容器宽度自动响应，图片懒加载，点击大图预览，长按可拖拽换位。
---

# PhotoWall 照片墙

相册、活动照片、作业图片、商品橱窗——一堆尺寸不一的图片，用等宽网格排会切掉内容，用瀑布流排才能保住每张图的比例。

`jm-photo-wall` 一次解决四件事：

1. **响应式列数**：按容器宽度和 `column-width` 自动算列数，手机 2 列、平板 4 列，不用写断点。
2. **瀑布流**：每张图塞进当前最矮的一列，高度按真实比例算，不留空隙、不裁切。
3. **懒加载**：图片进入视口附近才真正加载，首屏只下前几张。
4. **预览与排序**：点击开大图（复用 [ImagePreview](/components/image-preview)），`sortable` 打开后长按即可拖动换位。
5. **上千张不卡**：超过 200 张自动启用虚拟渲染，只挂载可视区附近的格子。

## 基础用法

<DemoBlock src="/demos/photo-wall/basic.vue" title="瀑布流、响应式列数与点击预览" desc="同一个组件，列宽从 150px 改成 100px 就自动从 2 列变 3 列。" />

```vue
<jm-photo-wall :items="photos" :gap="8" :radius="10" />
```

数据结构很薄，`src` 必需，其余都可省：

```ts
interface PhotoWallItem {
  src: string       // 列表里显示的图
  full?: string     // 预览用大图，不传用 src
  thumb?: string    // 低清占位图，加载完成前先显示
  ratio?: number    // 高 / 宽；不传则图片加载后自动测量
  alt?: string
}
```

## 响应式列数

不传 `columns` 时列数由容器宽度决定：

```
列数 = max(1, floor((容器宽 + gap) / (columnWidth + gap)))
```

`columnWidth` 是**单列的基准宽度**而不是固定宽度——列数定了之后，列宽会把剩余空间均分掉，所以 360px 的屏幕用 150px 基准得到 2 列（每列 176px），400px 屏幕依旧是 2 列（每列 196px），到 620px 才变成 3 列。

需要「就只要 4 列，不管多宽」时传 `columns="4"`，此时 `columnWidth` 失效。

容器尺寸变化（横竖屏切换、侧边栏展开、弹窗拉伸）由 `ResizeObserver` 接管，列数或列宽变了会重新排版，已有图片滑到新位置而不是闪一下重排。

## 瀑布流与图片比例

每张图的占位高度 = 列宽 × `ratio`。`ratio` 有三种来源，优先级从高到低：

1. 数据里显式给的 `ratio`（推荐：列表接口一般能带回来，能避免加载前后的跳动）
2. 图片 `load` 后测量的 `naturalHeight / naturalWidth`
3. `fallbackRatio`（默认 1，即正方形占位）

没给 `ratio` 时首屏会先按正方形排列，图片加载完再「长高」到真实比例——所以在意布局稳定性的场景，建议后端把宽高一起返回。

## 懒加载

`lazy` 默认开启：先用 `IntersectionObserver` 观察每个格子，进入视口前 `lazyOffset`（默认 200px）就开始加载。未加载的格子显示骨架色块；如果数据里给了 `thumb`，会先铺一张模糊小图，加载完再淡入清晰图。

```vue
<jm-photo-wall :items="photos" lazy lazy-offset="300px" />
```

嵌套在可滚动容器（弹窗、手机模拟框）里也能正确工作——IntersectionObserver 会按最近的裁剪祖先计算可见性。

## 点击预览

`preview` 默认开启，点击任意图片打开大图，预览顺序跟随当前排序，支持左右滑动。`full` 有值时预览用大图、列表用小图：

```vue
<jm-photo-wall :items="photos" @click="(item, i) => track(i)" />
```

只想自己处理点击、不开预览，传 `:preview="false"`，然后监听 `click`。

内嵌在手机模拟框或弹窗里演示时，预览默认会挂到最近的 `data-jm-preview-scope` 容器，也可以显式指定：

```vue
<jm-photo-wall :items="photos" :preview-target="stageEl" />
```

## 拖拽排序

`sortable` 打开后，**长按 0.3 秒**拿起图片（`sort-delay` 可调，设 0 则按下即拖），拖动时目标位置的其他图片会自动让位，松手落位并触发排序事件。

<DemoBlock src="/demos/photo-wall/sortable.vue" title="长按拖拽换位" desc="拖动过程中其他图片实时让位，松手后顺序写回 items。" />

```vue
<jm-photo-wall v-model:items="photos" sortable @sort="(e) => console.log(e.from, e.to)" />
```

- 顺序直接写回 `items`（`update:items`），`sort` 事件额外给出 `from` / `to` 下标，便于埋点或调接口。
- 长按前的轻微滑动会让位给页面滚动：手指在 8px 内没动才算长按，超过就当作滚动，不会误触发拖拽。
- 拖动期间纵向滑动被接管，页面不会跟着滚；松手后的那次 `click` 会被吞掉，不会顺手打开预览。
- 排序只改顺序，不改 DOM 顺序语义——无障碍读屏仍按视觉顺序朗读，但键盘用户无法排序，需要提供「上移 / 下移」按钮作为替代。

## 自定义格子

需要角标、选中态、删除按钮，用 `item` 插槽拿到当前数据和下标：

```vue
<jm-photo-wall :items="photos">
  <template #item="{ item, index }">
    <span class="badge">{{ index + 1 }}</span>
  </template>
</jm-photo-wall>
```

列表为空时渲染 `empty` 插槽。

## 虚拟渲染

超过 `virtualThreshold`（默认 200 张）自动开启虚拟渲染：只把可视带上下 `virtualBuffer`（默认 400px）范围内的格子挂到 DOM 上，其余只保留布局坐标，滚动时按需增删。相册、图库这种几千张的列表不用分页也能直接滚。

<DemoBlock src="/demos/photo-wall/virtual.vue" title="1200 张，只挂载十几张" desc="右上角实时显示当前挂载的节点数；关掉虚拟渲染再滚一遍可以对比手感。" />

```vue
<jm-photo-wall :items="photos.slice(0, 12)" />   <!-- 12 张：不虚拟 -->
<jm-photo-wall :items="photos" />                <!-- 1200 张：自动虚拟 -->
<jm-photo-wall :items="photos" :virtual="false" />  <!-- 强制全量挂载 -->
```

实现上不猜视口：向上遍历所有 `overflow: auto/scroll` 的祖先，取它们与浏览器视口的交集，再换算成相册内坐标。所以它既能跟着整个页面滚，也能嵌在弹层、手机模拟框这类自己的滚动容器里工作。

两点要知道：

- 关掉 `lazy` 但没有虚拟渲染时，所有图片会同时请求；两者搭配才是「既省 DOM 又省流量」。
- 正在拖拽的那一格永远参与渲染（哪怕被拖出可视带），否则拖到边缘会突然消失。

## 性能提示

- 每张图都在自己的绝对定位格子里，重排只改 `transform` / 宽高，不触发整墙 reflow 级别的重绘。
- 几百张以内全量挂载也没问题；上千张交给虚拟渲染，DOM 节点数会稳定在可视区那十几个。
- `will-change: transform` 已加在格子上，几百张以内开销可接受；如果只做展示不做排序，可关掉 `sortable`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| items | 图片列表 | `PhotoWallItem[]` | `[]` |
| columns | 固定列数，不传则自动 | `number` | - |
| columnWidth | 单列基准宽度（px） | `number` | `150` |
| gap | 间距（px） | `number` | `8` |
| radius | 圆角 | `number \| string` | `8` |
| lazy | 懒加载 | `boolean` | `true` |
| lazyOffset | 懒加载提前量 | `string` | `'200px'` |
| preview | 点击打开预览 | `boolean` | `true` |
| previewTarget | 预览挂载容器 | `HTMLElement \| null` | 最近的 `data-jm-preview-scope` |
| sortable | 长按拖拽排序 | `boolean` | `false` |
| sortDelay | 长按激活时长（ms），0 为立即 | `number` | `300` |
| fallbackRatio | 比例未知时的占位比例 | `number` | `1` |
| virtual | 虚拟渲染；不传则按 `virtualThreshold` 自动判断 | `boolean` | 自动 |
| virtualThreshold | 超过多少张自动开启虚拟渲染 | `number` | `200` |
| virtualBuffer | 虚拟渲染视口上下额外保留的像素 | `number` | `400` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:items | 拖拽排序后的新数组 | `PhotoWallItem[]` |
| click | 点击某张图 | `(item, index)` |
| sort | 排序完成 | `{ from, to, items }` |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| item | 自定义格子内容，参数 `{ item, index }` |
| empty | 列表为空时显示 |

### 方法

| 方法 | 说明 |
| --- | --- |
| relayout() | 手动重排（容器尺寸被外部手段改变、且 ResizeObserver 没捕捉到时调用） |
| renderedCount() | 当前实际挂载的格子数，虚拟渲染时用来观察节点量 |

## 无障碍

每个格子是 `role="button"` 且可聚焦，`aria-label` 取 `alt`，没有 `alt` 时读作「第 N 张图片」；回车 / 空格打开预览。骨架色块与装饰图标标了 `aria-hidden`，不会被读屏重复朗读。
