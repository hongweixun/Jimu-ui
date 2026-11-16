---
title: Result 结果页
description: 提交成功、支付失败、审核中等操作结果页，支持状态配色与自定义图标。
---

# Result 结果页

表单提交、支付、审核结束后，用一整屏告诉用户「发生了什么、接下来做什么」。

## 基础用法

<DemoBlock src="/demos/result/basic.vue" title="五种状态与自定义图标" desc="status 决定图标与配色，底部按钮放在默认插槽里。" />

```vue
<jm-result
  status="success"
  title="作业提交成功"
  description="老师批改后会通知你，可在「我的作业」里查看记录。"
>
  <jm-button type="primary" block @click="goHome">回到首页</jm-button>
  <jm-button block @click="goDetail">查看详情</jm-button>
</jm-result>
```

## 状态

| status | 图标 | 配色 |
| --- | --- | --- |
| `success` | 对勾 | 成功绿 |
| `error` | 叉 | 危险红 |
| `warning` | 感叹号 | 警告黄 |
| `info`（默认） | i | 主色蓝 |
| `waiting` | 旋转的 loading | 中性灰 |

`icon` 可以覆盖图标（用图标名，见 `jm-icon`），配色仍跟随 `status`——比如「礼物 + 主色」这种营销场景。

## 插槽

| 插槽 | 说明 |
| --- | --- |
| icon | 换成自己的插画/图片 |
| title | 标题，可放富文本 |
| description | 描述，可放多行说明或列表 |
| default | 底部操作区（自动横向排列） |

插槽优先级高于同名 prop，传了插槽就不再看 `title` / `description`。

## 间距建议

结果页一般紧跟在页面顶部，垂直内边距用默认的 `--jm-space-8` 就够了；如果嵌在弹层里，外面再包一层 `padding` 会显得空，可以靠父容器控制。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| status | 状态 | `'success' \| 'error' \| 'warning' \| 'info' \| 'waiting'` | `'info'` |
| icon | 自定义图标名 | `string` | - |
| title | 标题 | `string` | - |
| description | 描述 | `string` | - |

### Slots

| 插槽 | 说明 |
| --- | --- |
| icon | 图标区 |
| title | 标题区 |
| description | 描述区 |
| default | 操作区 |
