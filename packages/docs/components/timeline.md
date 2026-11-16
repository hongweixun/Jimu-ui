---
title: Timeline 时间轴
description: 纵向时间轴，用于展示审批流、订单进度、操作记录等按时间排列的信息。
---

# Timeline 时间轴

一列竖着的「什么时候发生了什么」。审批流、物流轨迹、作业批改记录，都可以用它串起来。

`jm-timeline` 只负责轴线样式，内容由子节点 `jm-timeline-item` 承载——时间在左、圆点在轴、内容在右，三列对齐是这套组件的核心。

## 基础用法

<DemoBlock src="/demos/timeline/basic.vue" title="进度节点与虚线待办" desc="type 决定圆点颜色，icon 让圆点变成带图标的实心点。" />

```vue
<jm-timeline>
  <jm-timeline-item time="09:12" title="提交作业" content="第三章课后练习 · 共 12 题" type="success" icon="check" />
  <jm-timeline-item time="14:30" title="老师批阅中" content="正在评阅第 11、12 题" type="primary" active />
  <jm-timeline-item time="预计 18:00" title="成绩公布" content="发布后会通知你" />
</jm-timeline>
```

## 时间列

`time` 支持任意短文本（`09:12`、`周一`、`3 天前`），也可以完全不给——不给时左侧时间列自动收起，轴线左移到最外侧，不会留出空白。

需要多行或带图标的时间，用 `time` 插槽代替：

```vue
<jm-timeline time-width="72px">
  <jm-timeline-item title="开课">
    <template #time>
      <div>09-01<br />08:00</div>
    </template>
  </jm-timeline-item>
</jm-timeline>
```

## 节点状态

| type | 圆点颜色 | 典型场景 |
| --- | --- | --- |
| `default` | 四级文字灰 | 普通记录、历史节点 |
| `primary` | 主色 `#00A0E9` | 当前进行中 |
| `success` | 成功绿 | 已完成 |
| `warning` | 警示橙 | 待确认、有风险 |
| `danger` | 危险红 | 失败、驳回 |
| `info` | 信息蓝 | 系统通知 |

`active` 会在圆点外再加一圈主色光环，并把标题染成主色——同一屏里只标一个，多了就失去重点。`color` 可以直接覆盖圆点颜色，用于业务自定义色（如按学科配色）。

## 空心点与虚线

`hollow` 把圆点变成空心描边，`line-style="dashed"` 把轴线改成虚线。两者叠起来就是「还没发生的事」：已完成用实心实线，待办用空心虚线。

```vue
<jm-timeline line-style="dashed">
  <jm-timeline-item time="周一" title="报名选课" type="success" />
  <jm-timeline-item time="周五" title="开课通知" type="warning" hollow />
</jm-timeline>
```

`hide-line` 可以单独掐掉某个节点向下的连线；最后一个节点本身就不画线，不需要手动处理。

## 自定义圆点

`icon` 传入内置图标名后，圆点会放大到 20px 并把图标放进去。需要更自由的内容（头像、数字、图片）用 `dot` 插槽：

```vue
<jm-timeline-item title="李老师 批阅">
  <template #dot>
    <jm-avatar size="24" text="李" />
  </template>
</jm-timeline-item>
```

## API

### Timeline Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| lineStyle | 轴线样式 | `'solid' \| 'dashed'` | `'solid'` |
| lineColor | 轴线颜色 | `string` | 边框色 |
| dotSize | 默认圆点直径（px） | `number` | `10` |
| timeWidth | 左侧时间列宽度 | `string` | `'60px'` |

### TimelineItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| time | 左侧时间文字 | `string` | - |
| title | 标题 | `string` | - |
| content | 正文 | `string` | - |
| type | 语义色 | `'default' \| 'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'` | `'default'` |
| color | 圆点自定义颜色（优先于 type） | `string` | - |
| hollow | 空心圆点 | `boolean` | `false` |
| icon | 圆点内图标名 | `string` | - |
| active | 高亮当前节点 | `boolean` | `false` |
| hideLine | 不画该节点向下的连线 | `boolean` | `false` |
| dotSize | 该节点圆点直径（px） | `number` | - |

### 插槽

| 组件 | 插槽 | 说明 |
| --- | --- | --- |
| TimelineItem | default | 正文内容（替代 `content`） |
| TimelineItem | time | 自定义时间列 |
| TimelineItem | title | 自定义标题 |
| TimelineItem | dot | 完全自定义圆点 |

## 无障碍

圆点与连线是纯装饰，标了 `aria-hidden`，屏幕阅读器只读标题与正文；时间列是普通文本，会按「时间 + 标题 + 内容」的顺序朗读，语义顺序与视觉顺序一致。
