---
title: 组合式函数
description: useCountDown / useClickOutside / useLockScroll / useSwipe / useDebounceFn / useThrottleFn / useIntersection——跨组件复用的横切能力。
---

# 组合式函数

组件解决"这一块长什么样"，组合式函数解决"这一类逻辑怎么不重复写"。倒计时、点外部收起、滚动锁定、手势、防抖节流——它们不属于任何单个组件，却在十几个地方反复出现，这就是横切能力：抽出来写一次，处处复用。

<DemoBlock src="/demos/composables/basic.vue" title="五个函数在一个 demo 里" desc="验证码倒计时、点外部收起、滑动手势、防抖 vs 节流的连点对比。" />

## useCountDown — 倒计时

验证码按钮（"60s 后重发"）、秒杀、考试计时。时间戳驱动：后台标签页被浏览器降频后回来，读的仍是真实剩余时间，不会越走越慢。

```ts
import { useCountDown } from 'jimu-ui'

const { remaining, running, start, pause, resume, stop, formatted } = useCountDown(60, {
  onFinish: () => console.log('倒计时结束'),
})

start(60) // 开始 / 重新开始，可传入新的总秒数
```

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| `remaining` | `Ref<number>` | 剩余秒数（向上取整，不会提前跳 0） |
| `remainingMs` | `Ref<number>` | 剩余毫秒 |
| `running` | `Ref<boolean>` | 是否在倒数 |
| `formatted` | `Ref<string>` | 格式化文案，默认 `mm:ss`；传 `format` 接管 |
| `start` | `(seconds?) => void` | 开始 / 重开 |
| `pause` / `resume` | `() => void` | 暂停 / 恢复（用真实剩余时间做锚点，暂停多久都不多扣） |
| `stop` | `() => void` | 归零并停止 |

选项：`onFinish`（归零回调）、`format`（自定义格式化）、`interval`（校准间隔，默认 250ms）。

## useClickOutside — 点击外部

弹层收起的另一半逻辑。两个手写容易踩的坑都在这里解决了：监听用 pointerdown（capture），打开面板的那次点击靠**双 rAF 武装延迟**自然豁免——用户打开后紧接着点外部，第一次就能正常收起，不需要"跳过下一条"的猜测。

```ts
import { useClickOutsideWhen } from 'jimu-ui'

const root = ref<HTMLElement | null>(null)       // 面板
const trigger = ref<HTMLElement | null>(null)    // 触发按钮（点它也不算外部）

useClickOutsideWhen(visible, [root, trigger], () => {
  visible.value = false
})
```

- `useClickOutside(target, handler)`：始终监听。
- `useClickOutsideWhen(active, target, handler)`：只在 `active` 为 true 时监听（推荐，面板关着不白跑事件）。
- `target` 支持单个 ref 或 ref 数组，命中任意一个都算"内部"。

## useLockScroll — 滚动锁定

弹层开着时页面不该跟着滚。真正的难点是多层弹层：Dialog 上再开 ActionSheet，底下关了不能把顶层的锁解掉——底层用与弹层组件同一套计数式锁（`lockScroll` / `unlockScroll`），嵌套安全；本函数把它接到响应式状态上，组件卸载自动解锁。

```ts
import { useLockScroll } from 'jimu-ui'

const visible = ref(false)
useLockScroll(visible) // visible 开关自动带锁
```

## useSwipe — 滑动手势

轮播、侧滑删除、抽屉拖拽的底层手势。统一 pointer 事件（触屏 / 鼠标一套代码），以主导轴判方向（|dx| 与 |dy| 谁大听谁的），位移不够或手势太长都不算滑动。

```ts
import { useSwipe } from 'jimu-ui'

const card = ref<HTMLElement | null>(null)
const { direction, offsetX, offsetY, isSwiping } = useSwipe(card, {
  threshold: 30, // 触发滑动的最小位移（px），默认 30
  onSwipeEnd: (dir, dx, dy) => {
    if (dir === 'left') showDelete()
  },
})
```

回调：`onSwipeStart`（按下即触发，做跟随反馈）、`onSwipe`（进行中）、`onSwipeEnd(dir, dx, dy)`；`dir` 为 `''` 表示未达到阈值。

## useDebounceFn — 防抖

连续触发只在停止后执行一次（搜索联想要的是"最终值"）。组件卸载自动取消 pending，不会在已销毁的回调里碰 DOM。

```ts
import { useDebounceFn } from 'jimu-ui'

const search = useDebounceFn((kw: string) => fetchSuggest(kw), { delay: 300 })

// search.cancel() 取消 pending；search.flush() 立刻把最后一次刷出去
```

选项：`delay`（默认 300ms）、`leading`（开始时是否立刻执行一次，默认 false）。

## useThrottleFn — 节流

固定频率放行（滚动加载要的是"过程中的采样"）。`leading` 默认开——用户滚动第一屏就该出结果，不用等第一个间隔；`trailing` 默认开——保证最后一拍不丢。

```ts
import { useThrottleFn } from 'jimu-ui'

const onScroll = useThrottleFn(() => checkLoadMore(), { interval: 200 })
```

::: tip 防抖还是节流？
要"最后的状态"用防抖（输入联想、resize 重排）；要"过程中的采样"用节流（滚动加载、拖动跟手）。拿不准就想想用户停手后还需要不需要一次执行——需要就防抖，不需要就节流。
:::

## useIntersection — 进入视口

IntersectionObserver 的薄封装，[`v-lazy`](/components/lazy) 的底层。默认 once（进入过就算，布局抖动不会反复触发）、提前 200px 预加载。滚动加载评论、曝光埋点、入场动画都靠它。

```ts
import { useIntersection } from 'jimu-ui'

const zone = ref<HTMLElement | null>(null)
const { visible, stop } = useIntersection(zone, {
  onEnter: () => loadComments(),
})
```

## useFocusTrap — 焦点陷阱

模态弹层打开后，Tab 不应该跑到背后的页面上。打开时记住触发元素 → 焦点移进面板 → Tab 在面板内首尾循环 → 关闭时焦点还给触发元素。Dialog / Popup 已内置；自制模态层时可用：

```ts
import { useFocusTrap } from 'jimu-ui'

const trap = useFocusTrap()
// 打开弹层：trap.activate(panelEl)；关闭：trap.deactivate()
```
