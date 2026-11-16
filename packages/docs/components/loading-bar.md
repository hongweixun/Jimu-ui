---
title: LoadingBar 顶部加载条
description: 页面顶部的一条细进度线，适合路由切换、全屏提交这类没有按钮承接的等待。
---

# LoadingBar 顶部加载条

按钮上的 loading 管的是「点下去的那个动作」，但有些等待没有按钮可挂：切路由、进页面拉数据、整页提交。这时顶部一条细细的进度线最合适——不打断内容，又能明确告诉用户「还在动」。

## 基础用法

函数式调用，拿到控制器后决定何时结束：

<DemoBlock src="/demos/loading-bar/basic.vue" title="三种收尾方式：成功、失败、手动推进" desc="不手动推进时进度会自动朝 94% 收敛，越接近越慢；结束时由 finish() 补满到 100% 再淡出，不会出现「停在 80% 突然消失」。" />

```ts
import { showLoadingBar } from 'jimu-ui'

const bar = showLoadingBar()

try {
  await saveForm()
  bar.finish()
} catch (e) {
  bar.error()
}
```

## 手动推进进度

有真实进度（上传分片、批量提交第 N/M 条）时自己 `update` 更准：

```ts
const bar = showLoadingBar({ progress: 0 })

for (let i = 0; i < files.length; i++) {
  await upload(files[i])
  bar.update(((i + 1) / files.length) * 100)
}
bar.finish()
```

## 并发请求

多次调用 `showLoadingBar()` 会累加计数，**最后一个 `finish()` 才真正收尾**。所以不用自己判断「是不是最后一个请求结束」，放心在每个请求里各开各的：

```ts
async function load(item: Item) {
  const bar = showLoadingBar()
  await fetchItem(item)
  bar.finish()
}

// 三个请求同时跑，全部结束才会隐藏
await Promise.all(list.map(load))
```

## 插入到容器内

默认贴在浏览器顶部（`position: fixed`）。在弹层、手机模拟框里演示时传 `target`，加载条会改成 `absolute` 定位并限制在该容器内：

```vue
<div ref="panel" class="my-panel">
  <jm-button @click="run">开始</jm-button>
</div>

<script setup lang="ts">
const panel = ref<HTMLElement>()
function run() {
  const bar = showLoadingBar({ target: panel.value })
  // ...
}
</script>
```

## 颜色与高度

```ts
showLoadingBar({ color: '#7C4DFF', height: 3 })
```

失败态用 `errorColor` 覆盖，默认取 `--jm-color-danger`。

## API

### showLoadingBar(options?)

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| color | 进度条颜色 | `string` | 主色 |
| errorColor | 失败态颜色 | `string` | 危险色 |
| height | 高度（px） | `number` | `2` |
| progress | 起始进度 0-100 | `number` | `0` |
| target | 挂载容器，传了则容器内绝对定位 | `HTMLElement \| null` | — |

### 控制器

| 方法 | 说明 |
| --- | --- |
| update(progress) | 推进到指定进度（0-100） |
| finish() | 补满到 100% 后淡出 |
| error() | 变红补满后淡出 |
| destroy() | 立刻收起，重置所有状态 |

### 其他导出

| 名称 | 说明 |
| --- | --- |
| hideLoadingBar() | 强制收起当前加载条（忽略并发计数） |
| loadingBarState | 内部状态（`visible` / `progress` / `failed` 等），只读查看用 |
| JmLoadingBar | 承载组件，一般不用自己挂 |

## 使用建议

- **别用它替代按钮 loading**。用户点了一个按钮，反馈必须落在那个按钮上；顶部进度条是给「没有具体触发点」的全局等待用的。
- **请求很快时不必显示**。加了 `showLoadingBar()` 却在 100ms 内 `finish()`，会闪一下反而显得卡。可以在 200ms 后才真正显示（现在没内置这个延迟，需要的话先自己 `setTimeout`）。
- **一个页面一条就够**。并发计数已经保证不会叠出好几条，不要自己再套一层。
