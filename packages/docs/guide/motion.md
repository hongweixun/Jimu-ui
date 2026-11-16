# 动效系统

动效不是"给每个组件配个 0.3s"，而是**一套有语义的时间语言**：什么样的动作该多快、该用什么曲线、进场和退场要不要一样长。

Jimu UI 是移动端库，所以参考对象分两层：

- **时长阶梯与曲线**取 Arco Design 的标尺（100/200/300/400/500ms + 四条曲线）——这套数值经过大量桌面产品验证，作为基础语汇足够稳
- **触感与弹层节奏**取 [Varlet UI](https://www.varletjs.com/)——手机上的按压反馈、sheet 上滑，桌面端那套是为大屏长距离位移设计的，搬到 6 寸屏上会显得拖

组件里不允许出现写死的 `transition: .3s`，一律读语义令牌——这不只是规范洁癖，而是「一键关闭全部动效」「适老模式整体放慢」能够零改组件生效的前提。

## 四条曲线

同一段位移、同样 700ms，只换曲线，手感完全不同。点「重播」对比：

<DemoBlock src="/demos/motion/curves.vue" :phone="false" plain />

| 曲线 | 值 | 表达什么 | 用在哪 |
| --- | --- | --- | --- |
| `--jm-ease-standard` | `cubic-bezier(.34,.69,.1,1)` | 平稳移动，默认选它 | 状态切换、位移、变色 |
| `--jm-ease-decelerate` | `cubic-bezier(.4,.8,.74,1)` | 快起步、慢落位 | 进场（元素"停下来"） |
| `--jm-ease-accelerate` | `cubic-bezier(.26,0,.48,.9)` | 慢起步、快离开 | 退场 |
| `--jm-ease-overshoot` | `cubic-bezier(.3,1.3,.3,1)` | 有惯性、轻微过冲 | 开关滑块、勾选、点赞 |

## 时长阶梯

| 令牌 | 值 | 定位 |
| --- | --- | --- |
| `--jm-duration-1` | 100ms | 即时反馈的上限，再慢就有黏滞感 |
| `--jm-duration-2` | 200ms | 小元素进出、状态过渡 |
| `--jm-duration-3` | 300ms | 面板级进场、大范围位移 |
| `--jm-duration-4` | 400ms | 全屏级转场、适老模式 |
| `--jm-duration-5` | 500ms | 极限，超过就会觉得"卡" |

## 语义角色（组件只读这一层）

按时长选值是拍脑袋，按「这段动效在表达什么」选值才稳定。同一个 200ms 用在按下反馈上偏慢、用在弹层进场上偏快，所以时长必须带语义：

| 角色 | 时长 | 曲线 | 用在哪 |
| --- | --- | --- | --- |
| `feedback` | 100ms | standard | 按下、勾选、hover |
| `transition` | 200ms | standard | 同层状态变化：颜色、描边、透明度 |
| `enter` | 300ms | decelerate | 弹层、对话框、抽屉进场 |
| `exit` | 200ms | accelerate | 同上，退场 |
| `spring` | 300ms | overshoot | 开关滑块、单选圆点、图标抬起 |

**三条硬规则：**

1. **退场不长于进场**。桌面端进 300 出 200，关得快才不觉得"卡住了"；移动端 sheet 例外，进出都用 250ms（见下节），因为位移本来就只有半屏，对称反而更跟手。
2. **越小的元素动得越快**。提示条 200ms，全屏抽屉才用 300ms+。
3. **同一个交互里不要混用两套节奏**。比如弹层 300ms 进场，遮罩也跟着 300ms，不要遮罩 200、面板 400。

## 移动端触感：水波纹 + 250ms 弹层

桌面端靠 hover 和光标告诉你"这里能点"，手机没有光标，只能靠按下那一刻的视觉回应。所以移动端的按压反馈分两种，按元素面积选：

| 反馈 | 用在哪 | 参数 |
| --- | --- | --- |
| 水波纹 | Button、Cell、ActionSheet 项、Dialog 按钮 | 扩散 200ms + 淡出 140ms，详见 [Ripple 水波纹](/components/ripple) |
| 底色压暗 | 需要"瞬时"回应的元素（按钮保留 6%） | 100ms |

弹层单独一套节奏，与桌面端的 300/200 分离区分开：

| 令牌 | 值 | 说明 |
| --- | --- | --- |
| `--jm-motion-sheet-duration` | 250ms | sheet 上滑/下滑时长，取 Varlet 的实测值 |
| `--jm-motion-sheet-ease` | `cubic-bezier(.32,.72,0,1)` | iOS 抽屉曲线：起步快、尾巴长，落位不弹 |
| `--jm-motion-scrim-duration` | 250ms | 遮罩淡入淡出，必须与面板同时长 |
| `--jm-motion-scale-pop` | 0.85 | 居中弹层/对话框起始缩放 |

::: tip 为什么不用 Varlet 的 `ease`
Varlet 的 `transition: all .25s` 用的是默认 `ease`，起步偏肉。时长不动，只把曲线换成 iOS 抽屉曲线，滑到位的瞬间更利落——真机上对比一下就能感觉出来。
:::

## 组合预设

一长串 `transition: color ..., background-color ...` 容易写漏，用预设一次写完：

| 预设 | 展开为 | 场景 |
| --- | --- | --- |
| `--jm-motion-color` | color / background-color / border-color，200ms | Tag、Steps、Tabs 文字 |
| `--jm-motion-surface` | background-color / border-color / box-shadow，200ms | Input、Search 聚焦 |
| `--jm-motion-transform` | transform，200ms | 需要平滑位移的元素 |
| `--jm-motion-fade` | opacity，200ms | 淡入淡出 |
| `--jm-motion-press` | transform / background-color / opacity，100ms | 按钮、单元格按压 |

```css
.jm-my-card {
  transition: var(--jm-motion-surface);
}

.jm-my-card:active {
  transform: scale(var(--jm-motion-press-scale));
}
```

## 尺度也要统一

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--jm-motion-distance-xs` | 6px | 提示条上浮、图标抬起 |
| `--jm-motion-distance-sm` | 12px | 小面板位移 |
| `--jm-motion-distance-md` | 24px | 卡片入场 |
| `--jm-motion-scale-enter` | 0.92 | 小元素进场起始缩放（Toast 等） |
| `--jm-motion-scale-pop` | 0.85 | 居中弹层/对话框的起始缩放 |
| `--jm-motion-scale-exit` | 0.96 | 退场缩放（幅度小于进场，避免"弹回去"） |
| `--jm-motion-press-scale` | 0.96 | 按钮按压 |

## 组件里的实际选择

| 组件 | 动效 | 为什么 |
| --- | --- | --- |
| Button | 水波纹 + 底色压暗 6% | 水波铺满要 200ms，压暗负责那 200ms 的瞬时回应 |
| Cell / ActionSheet 项 | 水波纹（0.1~0.12） | 大面积元素上只留水波，去掉底色变化，避免叠两层显脏 |
| Popup | 进出对称 250ms，iOS 抽屉曲线 | 参照 Varlet；移动端 sheet 位移短，250ms 内结束最跟手 |
| Dialog | 缩放 0.85 → 1，250ms | Varlet 的 0.3 起点在手机上太夸张，0.85 更耐看 |
| Toast | 200ms 减速 + 6px 上浮 | 小元素用 300ms 会显得迟钝 |
| Switch | 滑块 `spring`，轨道 200ms 变色 | 滑块要有物理惯性，轨道不需要 |
| Checkbox | 勾选描线 200ms 减速 | 起笔快收笔稳，才看得清怎么勾上的 |
| Collapse | 高度 300ms standard | 200ms 在大面板上显急，400ms 又拖 |
| Tabs 下划线 | 300ms standard | 跨越整条导航，位移比变色长 |

## 性能：只动 transform 和 opacity

这两类属性由合成层处理，不触发布局。改 `width` / `height` / `left` / `top` 会让浏览器每帧重新排版，中低端安卓上必掉帧。

- 开关滑块的按压拉伸用 `transform: scaleX()`，不用 `width`
- Collapse 的高度动画是唯一例外（必须知道真实高度），已用 `will-change: height` 单独隔离
- `will-change` 只加在会持续动画的元素上（弹层面板、滑块），滥用会吃显存

## 关掉动效

```html
<!-- 全局：整站静止 -->
<html data-motion="off"></html>
```

```html
<!-- 局部：只停这一块 -->
<div data-motion="off">
  <jm-button>这块区域没有动效</jm-button>
</div>
```

```ts
// 代码控制，会写 localStorage
import { useAppearance } from 'jimu-ui'

const { setMotion } = useAppearance()
setMotion(false)
```

关闭时做了两件事：时长阶梯归零 + 全元素 `transition/animation` 压到 `0.01ms` 且只跑一次。用 `0.01ms` 而不是 `none`，是因为 Vue 的 `<Transition>` 依赖 `transitionend`，`none` 会让离场钩子挂起到超时。

::: tip 必要动效白名单
默认连加载转圈一起停（静态圆环仍然是可识别的加载指示）。如果业务认为"不转就看不出在加载"，给元素加 `jm-motion-essential` 即可保留：

```html
<span class="jm-loading__arc jm-motion-essential" />
```
:::

系统偏好也兜底：用户开了「减少动态效果」，效果等同 `data-motion="off"`。

## 适老模式

适老不是简单"放慢"，而是**降低眩晕风险**：时长整体下沉一档，位移距离砍三分之一。

| 角色 | 常规 | 适老 |
| --- | --- | --- |
| feedback | 100ms | 200ms |
| transition | 200ms | 300ms |
| enter | 300ms | 400ms |
| exit | 200ms | 300ms |
| 弹层 sheet | 250ms | 400ms |
| 水波纹 | 200ms / 0.25 | 300ms / 0.2 |
| `--jm-motion-distance-md` | 24px | 16px |

```html
<html data-elder="true"></html>
```
