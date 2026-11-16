---
title: Checkbox 复选框
description: 多选，支持方形/圆形、半选状态与分组双向绑定。
---

# Checkbox 复选框

多选场景。勾选时白勾以 `stroke-dashoffset` 画出来，关掉动效则直接显示。

## 基础用法

<DemoBlock src="/demos/checkbox/basic.vue" title="单选、分组、半选" desc="放进 CheckboxGroup 时，勾选态由分组统一管理，只需要给每个 Checkbox 一个 value。" />

## API

### Checkbox Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 是否勾选（单独使用时） | `boolean` | `false` |
| value | 在分组中的取值 | `string \| number` | — |
| label | 文案 | `string` | — |
| disabled | 禁用 | `boolean` | `false` |
| shape | 形状 | `'square' \| 'circle'` | `'square'` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| color | 选中色 | `string` | 继承分组或主题主色 |
| indeterminate | 半选 | `boolean` | `false` |

## 选择数量限制

选课、投票、问卷多选常要「最多选 N 个」。传 `max` / `min`，越界的那一次点击会被直接拦下，`v-model` 数组不变：

<DemoBlock src="/demos/checkbox/limit.vue" title="最多选 3 门，最少留 1 门" desc="越界时触发 overLimit，配一个 Toast 提示体验最自然。" />

```vue
<jm-checkbox-group v-model="picked" :max="3" :min="1" @over-limit="onOverLimit">
  <jm-checkbox v-for="c in courses" :key="c.value" :value="c.value">{{ c.label }}</jm-checkbox>
</jm-checkbox-group>
```

```ts
function onOverLimit({ type }) {
  showToast({ message: type === 'max' ? '最多选 3 门' : '至少保留 1 门' })
}
```

组件本身不弹提示（免得和业务自己的 Toast / Dialog 打架），只把越界事件抛出来。`max` 从「已选数量」算，不关心具体选项；`min` 在取消勾选时生效。

### CheckboxGroup Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 选中值数组 | `(string \| number)[]` | `[]` |
| disabled | 整组禁用 | `boolean` | `false` |
| color | 整组选中色 | `string` | — |
| direction | 排列方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| gap | 间距 | `number \| string` | `16px` |
| max | 最多可选数量，超出拦截 | `number` | — |
| min | 最少保留数量，低于拦截 | `number` | — |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 勾选变化（Checkbox 为 boolean，Group 为数组） | — |
| overLimit | 超出 max / 低于 min，本次操作被拦截 | `{ value, type: 'max' \| 'min', selected }` |
| change | 同上 | — |

::: tip 原生 input 没被丢掉
勾选框视觉是自绘的，但底下是一个真实的 `<input type="checkbox">`（视觉隐藏、仍可聚焦），所以键盘 Space 能切换、屏幕阅读器能读出"复选框，已选中"。
:::
