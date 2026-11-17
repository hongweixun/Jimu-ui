---
title: Popover 气泡
description: 点击触发器展开的轻量浮层，支持上下左右四个方向与深浅两种主题。
---

# Popover 气泡

移动端没有 hover，所以这里是**点击开合**：点触发器展开，点面板外部收起。适合放一小段说明、一个两三项的操作菜单，或者筛选条件的快捷切换。

需要全屏遮罩、多级联动、带动画的下拉筛选时，用 [DropdownMenu](/components/dropdown-menu)；需要从底部整块弹出的用 [ActionSheet](/components/action-sheet)。

## 基础用法

<DemoBlock src="/demos/popover/basic.vue" title="四个方向与气泡菜单" desc="placement 控制方向，theme 控制深浅。" />

```vue
<jm-popover placement="top" content="默认深色气泡">
  <template #reference>
    <jm-button size="small">上</jm-button>
  </template>
</jm-popover>
```

## 方向与对齐

`placement` 决定面板贴在触发器的哪一侧，`align` 决定贴着的那条边怎么对齐：

| align | 效果 |
| --- | --- |
| `start` | 面板左边缘与触发器左边缘对齐 |
| `center`（默认） | 居中对齐 |
| `end` | 右边缘对齐 |

`placement="left" / "right"` 时面板垂直居中，`align` 不生效。靠近屏幕边时建议用 `start` / `end` 把面板往里推，避免被裁掉。

## 主题

| theme | 外观 | 场景 |
| --- | --- | --- |
| `dark`（默认） | 半透明深底 + 白字 | 说明性文字、暗色卡片 |
| `light` | 白底 + 细描边 | 白色背景页面上的菜单 |

箭头由 `arrow` 控制，默认显示；面板与触发器之间的距离由 `offset` 调节（默认 8px）。

## 受控与关闭时机

- `v-model:show` 受控，`trigger="manual"` 时点击触发器不会自己开合，完全由业务控制（比如「长按」或「滚动到某处」才展开）。
- `close-on-click-outside` 默认开启，监听的是 `pointerdown`，所以按下就收起，不用等 click，手感更利落。
- `close-on-click-content` 打开后，点面板内任意位置都会关闭，做菜单时通常打开；面板里放的是表单或需要连续操作的按钮时保持关闭。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| show | 是否显示（`v-model:show`） | `boolean` | - |
| content | 气泡内容 | `string` | - |
| trigger | 触发方式 | `'click' \| 'manual'` | `'click'` |
| placement | 方向 | `'top' \| 'bottom' \| 'left' \| 'right'` | `'top'` |
| align | 对齐 | `'start' \| 'center' \| 'end'` | `'center'` |
| theme | 主题 | `'dark' \| 'light'` | `'dark'` |
| offset | 与触发器的距离 | `number` | `8` |
| arrow | 显示箭头 | `boolean` | `true` |
| disabled | 禁用 | `boolean` | `false` |
| closeOnClickOutside | 点外部关闭 | `boolean` | `true` |
| closeOnClickContent | 点内容关闭 | `boolean` | `false` |
| maxWidth | 面板最大宽度 | `number \| string` | `min(86vw, 320px)` |
| zIndex | 层级 | `number` | `1200` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:show | 显隐变化 | `boolean` |
| open | 展开 | - |
| close | 收起 | - |

### 插槽

| 插槽 | 说明 |
| --- | --- |
| reference | 触发器 |
| default | 面板内容，优先于 `content` |

## 注意

气泡**不 teleport**，DOM 上就在触发器旁边——这样它天然跟随父容器的滚动与定位，不需要在滚动时重算坐标。代价是父级如果设了 `overflow: hidden`，面板可能被裁掉，这时请把气泡放到裁剪层之外，或改用 DropdownMenu。
