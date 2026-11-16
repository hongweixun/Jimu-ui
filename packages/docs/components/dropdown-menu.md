---
title: DropdownMenu 下拉菜单
description: 列表页顶部的筛选菜单，支持单选、多选与完全自定义面板。
---

# DropdownMenu 下拉菜单

课程列表、成绩单、通讯录这类页面顶部常见「年级 / 科目 / 排序」三个筛选入口。`jm-dropdown-menu` 负责栏位排布与遮罩，`jm-dropdown-item` 负责单个菜单的标题与面板。

## 基础用法

<DemoBlock src="/demos/dropdown-menu/basic.vue" title="单选、多选、自定义面板、禁用" desc="options 传 { text, value, icon?, disabled? }，选中项打勾并高亮；也可以整块面板自定义。" />

## 选项式

```vue
<jm-dropdown-menu active-color="#00A0E9">
  <jm-dropdown-item v-model="grade" :options="gradeOptions" placeholder="年级" />
  <jm-dropdown-item v-model="subject" :options="subjectOptions" placeholder="科目" />
</jm-dropdown-menu>
```

- 标题默认显示选中项文案，没有选中显示 `placeholder`；
- `multiple` 时 `modelValue` 用数组，选中后**不自动收起**，方便连续勾选；
- 选项带 `icon` 时在文字前渲染图标；
- `disabled` 的选项点击无响应，`disabled` 的整项无法展开。

## 自定义面板

需要「标签多选 + 确定按钮」这种形态时，把内容塞进默认插槽即可，选中逻辑自己管：

```vue
<jm-dropdown-item :model-value="tags" placeholder="兴趣标签">
  <div class="tags">
    <jm-tag v-for="t in all" :key="t" @click="toggle(t)">{{ t }}</jm-tag>
  </div>
</jm-dropdown-item>
```

`max-height` 控制面板最大高度，超出滚动。

## 与页面滚动

遮罩是**绝对定位在菜单下方**的，不是整屏 fixed——所以在手机模拟框、弹窗里的下拉菜单不会溢出容器。代价是菜单所在容器需要有明确宽度（一般是整行）。

## API

### DropdownMenu Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| activeColor | 展开标题与选中项的高亮色 | `string` | 主色 |
| overlay | 显示遮罩 | `boolean` | `true` |
| closeOnClickOption | 选项点击后收起（单选时） | `boolean` | `true` |
| zIndex | 基础层级 | `number` | `10` |

### DropdownMenu Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| open | 某项展开 | `index: number` |
| close | 全部收起 | — |

### DropdownItem Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 选中值，多选为数组 | `string \| number \| (string \| number)[]` | — |
| options | 选项列表 | `{ text, value, icon?, disabled? }[]` | `[]` |
| title | 固定标题（覆盖选中项文案） | `string` | — |
| placeholder | 未选中时的文案 | `string` | `请选择` |
| disabled | 禁用整项 | `boolean` | `false` |
| multiple | 多选 | `boolean` | `false` |
| maxHeight | 面板最大高度 | `number \| string` | — |

### DropdownItem Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 值变化 | `string \| number \| (string \| number)[]` |
| change | 选中某项 | `(value, option)` |
| open / close | 展开 / 收起 | — |

### Slots

| 组件 | 名称 | 说明 |
| --- | --- | --- |
| DropdownMenu | default | 若干 `jm-dropdown-item` |
| DropdownItem | default | 自定义面板内容（替代 options 渲染） |
