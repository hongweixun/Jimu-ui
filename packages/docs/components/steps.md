---
title: Steps 步骤条
description: 横向/纵向步骤条，支持完成、进行中、错误状态与自定义图标。
---

# Steps 步骤条

订单进度、审批流、报名流程。状态由父级 `active` 推导：小于 `active` 为完成、等于为进行中、大于是未开始，某一项需要特殊状态（比如审核失败）时在 `jm-step` 上单独传 `status`。

## 基础用法

<DemoBlock src="/demos/steps/basic.vue" title="横向、错误态与纵向" desc="active 从 0 开始计数；纵向适合放时间、金额等多行说明。" />

## 用法

```vue
<jm-steps :active="2">
  <jm-step title="提交报名" description="09-01" />
  <jm-step title="资料审核" description="09-02" />
  <jm-step title="分配班级" description="09-05" />
  <jm-step title="开课" description="09-10" />
</jm-steps>
```

## API

### Steps Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| active | 当前步骤索引，从 0 开始 | `number` | `0` |
| direction | 方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| active-color | 进行中颜色 | `string` | `var(--jm-color-primary)` |
| done-color | 已完成颜色 | `string` | `var(--jm-color-primary)` |

### Step Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 标题 | `string` | — |
| description | 描述 | `string` | — |
| status | 强制状态 | `'wait' \| 'process' \| 'finish' \| 'error'` | 由 active 推导 |

### 插槽

| 名称（Step） | 说明 | 作用域 |
| --- | --- | --- |
| icon | 替换圆点内容（图标、头像） | `{ status, index }` |
| title | 自定义标题（可放标签） | — |
| description | 自定义描述（可放按钮） | — |

::: tip 连接线为什么不用伪元素
连接线是真实 DOM 元素，纵向时它会 flex-grow 撑满两步之间的高度。用 `::after` 画线在纵向布局里高度算不准，最后一项还得额外抹掉——现在靠 `.jm-step:last-child` 直接隐藏，SSR 也不会闪。
:::
