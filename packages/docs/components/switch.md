---
title: Switch 开关
description: 开关选择器，带弹簧回弹的滑块动效，支持自定义颜色与内嵌文字。
---

# Switch 开关

用于即时生效的二元设置（消息推送、自动播放）。需要点确认才生效的，请用 Checkbox。

## 基础用法

<DemoBlock src="/demos/switch/basic.vue" title="尺寸、文字与颜色" desc="滑块位移走 --jm-motion-spring-ease 的轻微回弹，按下时朝切换方向拉伸；关掉动效后直接跳到终点。" />

## 切换前确认

<DemoBlock src="/demos/switch/before-change.vue" title="before-change：先调接口再放开" desc="返回 Promise 时开关自己转圈，pending 期间点击无效；返回 false 拦截切换。" />

```vue
<jm-switch v-model="on" :before-change="beforeChange" />

<script setup>
async function beforeChange(next) {
  // next 是「即将变成」的值
  if (!next) return true
  const ok = await subscribe()
  return ok            // false → 开关不动
}
</script>
```

适合「开通会员」「关闭重要提醒」这类**不能随手切**的开关：状态先不动，等接口回来再改，避免出现「界面已开、服务端没开」的不一致。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 是否打开 | `boolean` | `false` |
| disabled | 禁用 | `boolean` | `false` |
| loading | 加载中（不可切换） | `boolean` | `false` |
| size | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| active-color | 打开时的颜色 | `string` | `var(--jm-color-primary)` |
| inactive-color | 关闭时的颜色 | `string` | `var(--jm-gray-400)` |
| active-text | 打开时的说明文字 | `string` | — |
| inactive-text | 关闭时的说明文字 | `string` | — |
| before-change | 切换前钩子，返回 `false` 拦截；返回 Promise 时自动进入 loading | `(next: boolean) => boolean \| void \| Promise<boolean \| void>` | — |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 状态变化 | `boolean` |
| change | 状态变化（语义同 v-model） | `boolean` |
| click | 点击 | `MouseEvent` |

### CSS 变量

| 变量 | 说明 |
| --- | --- |
| `--jm-switch-active` | 打开态颜色 |
| `--jm-switch-inactive` | 关闭态颜色 |

::: tip 文字为什么放在轨道外面
放进轨道只有 26px 高，13px 的字会挤。放在轨道右侧做辅助说明，换行和放大（适老 1.28×）都不会挤爆，长文案也不会被裁掉。
:::
