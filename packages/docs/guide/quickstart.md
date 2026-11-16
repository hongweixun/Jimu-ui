# 快速开始

Jimu UI 是金智安教育科技内部使用的移动端 Vue 3 组件库，主色 `#00A0E9`，默认面向手机浏览器，同时兼顾平板与极窄屏。

## 安装

```bash
npm i jimu-ui
```

## 全量引入

适合项目初期、或想省事的场景：

```ts
// main.ts
import { createApp } from 'vue'
import JimuUI from 'jimu-ui'
import 'jimu-ui/style.css'
import App from './App.vue'

createApp(App).use(JimuUI).mount('#app')
```

`app.use(JimuUI)` 会顺带初始化一次外观设置（读 localStorage 里的主题 / 动效 / 适老偏好），所以不用再单独调 `setupAppearance()`。

## 按需引入

推荐生产项目使用，JS 体积只算用到的组件：

```bash
npm i -D unplugin-vue-components
```

```ts
// vite.config.ts
import Components from 'unplugin-vue-components/vite'
import { JimuResolver } from 'jimu-ui/resolver'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [JimuResolver()],
      dts: 'src/components.d.ts',
    }),
  ],
})
```

之后模板里直接写标签，不需要手写 import：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const checked = ref(false)
</script>

<template>
  <jm-button type="primary" block>开始学习</jm-button>
  <jm-switch v-model="checked" />
</template>
```

## 手动按需注册

不想装插件也可以，逐个注册：

```ts
import { Button, Cell, CellGroup } from 'jimu-ui'
import 'jimu-ui/style.css'

app.use(Button).use(Cell).use(CellGroup)
```

每个组件都带 `install`，`app.use(Button)` 等价于 `app.component('JmButton', Button)`。

## 页面基础设置

移动端必须带 `viewport-fit=cover`，否则安全区变量恒为 0：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
```

页面根节点建议用 `100dvh` 而不是 `100vh`，并把背景色设成 `--jm-bg-page`：

```css
html,
body,
#app {
  min-height: 100dvh;
  background: var(--jm-bg-page);
  color: var(--jm-text-color);
}
```

::: tip 为什么不写全局 reset
组件库只在自己的 `jm-` 前缀类上做 `box-sizing`，不重置 `body`、`h1`、`p` 等标签，接入到已有项目时不会打乱原有排版。
:::

## 兼容基线

| 平台 | 最低版本 | 说明 |
| --- | --- | --- |
| iOS Safari | 15 | 覆盖 iPhone 6s 及以上 |
| Android Chrome | 90 | 覆盖主流国产浏览器内核（QQ / UC / 微信 X5 近两年版本） |
| 桌面 | Chromium 90 / Safari 15 / Firefox 90 | 文档站与后台预览使用 |

::: warning 两个硬约束
1. **输入框字号不低于 16px**：低于 16px 时 iOS 聚焦输入框会自动放大整页，组件内部已经把 `font-size` 锁到 `max(16px, --jm-font-size-md)`。
2. **不使用 `color-mix()`**：Safari 16.2 以下不支持，浅色底一律走预生成的 `-light` 令牌。
:::
