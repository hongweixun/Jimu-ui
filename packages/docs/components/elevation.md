---
title: Elevation 海拔
description: Material 风格的海拔阴影体系，0-24 级变量与工具类，暗色主题自适应。
---

# Elevation 海拔

参照 Material Design 的海拔概念：元素离「纸面」越高，阴影越明显越扩散。我们提供 0/1/2/3/4/6/8/12/16/24 十个级别，每个级别是一个 CSS 变量 + 一个同名工具类，暗色主题下自动换为更重的纯黑阴影。

## 基本用法

<DemoBlock src="/demos/elevation/basic.vue" title="海拔一览" desc="十个级别从贴地到悬浮；hover 类交互元素推荐 1~4，弹层/浮出元素推荐 8~24。" />

```vue
<div class="jm-elevation-2">普通卡片</div>
<div class="jm-elevation-8">悬浮操作球</div>
<div class="jm-elevation-24">全屏弹层</div>
```

## 选级建议

| 场景 | 推荐级别 |
| --- | --- |
| 列表卡片、分页条 | 1 ~ 2 |
| 悬浮按钮、下拉菜单 | 4 ~ 6 |
| Dialog / ActionSheet | 8 ~ 12 |
| 全屏层、Snackbar | 16 ~ 24 |

## API

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-elevation-0` | 无阴影（贴地） |
| `--jm-elevation-1` ~ `--jm-elevation-24` | 由浅到深的双层阴影 |

### 工具类

| 类名 | 等价于 |
| --- | --- |
| `.jm-elevation-{0,1,2,3,4,6,8,12,16,24}` | `box-shadow: var(--jm-elevation-N)` |

::: tip 与 --jm-shadow-* 的关系
`--jm-shadow-1~4` 是早期语义化阴影（卡片/浮层/顶部投影），仍然可用；海拔体系是按数字分级的通用版本，新代码建议直接用 `--jm-elevation-*`。
:::
