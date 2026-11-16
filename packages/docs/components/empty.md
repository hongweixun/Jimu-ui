---
title: Empty 空状态
description: 无数据时的占位，可自定义插画与操作按钮。
---

# Empty 空状态

列表为空、搜索无结果、网络异常时用它。内置一张两色几何插画，跟随主色变化。

## 基础用法

<DemoBlock src="/demos/empty/basic.vue" title="默认与自定义" desc="插画默认读 --jm-color-primary 与 -light，换主色时会自动跟着变。" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| description | 说明文字 | `string` | `'暂无数据'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| image-size | 插画宽度 | `number \| string` | 110 / 76 / 150 |

### Slots

| 名称 | 说明 |
| --- | --- |
| image | 自定义插画（替换内置 SVG） |
| description | 自定义说明 |
| default | 操作区，一般放一个按钮 |

::: tip 空状态要给出路
只写"暂无数据"等于把用户堵在死路上。带上一个明确的下一步（"去选课""重新加载""清空筛选条件"），转化率差别很大。
:::
