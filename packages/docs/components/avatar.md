---
title: Avatar 头像
description: 图片、文字、图标三种头像形态，支持尺寸形状自定义与叠放头像组。
---

# Avatar 头像

用户、教师、班级都需要头像。`jm-avatar` 把三种形态（图片 / 文字 / 图标）收在一处，图片加载失败自动回退，业务不用自己判断。

## 基础用法

<DemoBlock src="/demos/avatar/basic.vue" title="尺寸形状、图片与兜底、头像组、列表中的用法" desc="有 src 用图；没有就依次回退到 text、icon，最后是默认人像图标。" />

## 三种形态

```vue
<!-- 图片：加载失败自动回退到 text，不会留一个破图 -->
<jm-avatar src="/u/1.png" text="张" alt="张老师" />

<!-- 文字：最多显示 2 个字，颜色/底色可调 -->
<jm-avatar text="三年级" background="#E6F1FB" color="#185FA5" shape="square" />

<!-- 图标 -->
<jm-avatar icon="graduation-cap" />
```

文字超过 2 个字会截断成前两个字（中文姓名两字、英文首字母都合适），完整名称用 `alt` 或外层文字说明。

## 尺寸

| size | 实际值 |
| --- | --- |
| `small` | 32px |
| `medium` | 40px |
| `large` | 56px |
| 数字 / 字符串 | 按 px / 原样使用 |

文字字号按尺寸的 36% 自动计算，所以自定义尺寸时文字不会失调。

## 头像组

`jm-avatar-group` 负责叠放，超过 `max` 折叠成 `+N`（`max` 包含 `+N` 本身）：

```vue
<jm-avatar-group :max="4" :total="12" :gap="26">
  <jm-avatar v-for="u in users" :key="u.id" :src="u.avatar" />
</jm-avatar-group>
```

`gap` 是每个头像露出的宽度，数字按 px；`total` 不传时按插槽数量算。子头像没写 `size`/`shape` 时，会继承头像组的设置。

## API

### Avatar Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| src | 图片地址 | `string` | — |
| alt | 图片替代文本 | `string` | — |
| text | 无图时显示的文字（最多 2 字） | `string` | — |
| icon | 无图时的图标名 | `string` | — |
| size | 尺寸 | `'small' \| 'medium' \| 'large' \| number \| string` | `medium` |
| shape | 形状 | `'circle' \| 'square'` | `circle` |
| radius | 圆角（square 时生效） | `number \| string` | — |
| fit | 图片裁切方式 | `'cover' \| 'contain' \| 'fill'` | `cover` |
| bordered | 白色描边（叠放时更清晰） | `boolean` | `false` |
| background | 文字头像底色 | `string` | — |
| color | 文字头像文字色 | `string` | — |

### Avatar Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| load | 图片加载成功 | `Event` |
| error | 图片加载失败（随后回退） | `Event` |

### AvatarGroup Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| max | 最多展示几个，超出折叠为 +N | `number` | `0`（全部） |
| total | 实际总数，用于折叠数字 | `number` | 插槽数量 |
| size | 统一尺寸，注入到未显式设置的子头像 | `同 Avatar` | — |
| shape | 统一形状 | `'circle' \| 'square'` | — |
| gap | 每个头像露出的宽度 | `number \| string` | `24` |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 无图时自定义内容（优先级高于 text/icon） |
