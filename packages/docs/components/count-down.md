---
title: CountDown 倒计时
description: 考试倒计时、验证码、限时活动，支持自定义格式、毫秒与手动控制。
---

# CountDown 倒计时

传入剩余毫秒数，组件自己跑秒并按 `format` 拆分渲染。到 0 触发 `finish`。

## 基础用法

<DemoBlock src="/demos/count-down/basic.vue" title="基础、插槽定制、毫秒、受控" desc="默认样式只有数字加粗，卡片式数字用插槽自己拼。" />

```vue
<jm-count-down :time="30 * 60 * 1000" format="HH:mm:ss" @finish="onFinish" />
```

## 格式令牌

| 令牌 | 含义 | 示例 |
| --- | --- | --- |
| `DD` | 天（两位） | `03` |
| `HH` | 时 | `08` |
| `mm` | 分 | `05` |
| `ss` | 秒 | `09` |
| `S` | 毫秒（三位） | `120` |

字面量（`:`、空格、中文）原样保留。天大于 0 时想让天消失，用插槽自己判断更灵活。

## 毫秒与精度

- 默认按 50ms 轮询检查：秒数变化才更新视图，不会因为定时器漂移而跑偏；
- 开 `millisecond` 后改用 `requestAnimationFrame`，按帧刷新；
- `change` 事件在秒级模式下每秒最多触发一次，避免外部频繁重渲染。

## 受控

```vue
<jm-count-down ref="cd" :time="10000" :auto-start="false" @finish="done = true" />

<jm-button @click="cd.start()">开始</jm-button>
<jm-button @click="cd.pause()">暂停</jm-button>
<jm-button @click="cd.reset()">重置</jm-button>
```

`reset(ms?)` 可以换一个新的时长：`cd.reset(60_000)`。

## 自定义外观

```vue
<jm-count-down :time="time" format="HH:mm:ss">
  <template #default="{ timeData }">
    <span class="chip">{{ timeData.hours }}</span>
    <span class="sep">:</span>
    <span class="chip">{{ timeData.minutes }}</span>
    <span class="sep">:</span>
    <span class="chip">{{ timeData.seconds }}</span>
  </template>
</jm-count-down>
```

`timeData` 含 `total / days / hours / minutes / seconds / milliseconds`。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| time | 剩余毫秒数 | `number` | `0` |
| format | 格式字符串 | `string` | `'HH:mm:ss'` |
| autoStart | 挂载后自动开始 | `boolean` | `true` |
| millisecond | 按帧显示毫秒 | `boolean` | `false` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| change | 时间变化 | `{ total, days, hours, minutes, seconds, milliseconds }` |
| finish | 归零 | - |

### Slots

| 插槽 | 说明 |
| --- | --- |
| default | 自定义渲染，作用域 `{ timeData }` |

### Exposes

| 方法 | 说明 |
| --- | --- |
| start() | 开始（归零后需要先 `reset`） |
| pause() | 暂停 |
| reset(ms?) | 重置时长并（`autoStart` 时）重新开始 |
| timeData | 当前拆分结果 |
