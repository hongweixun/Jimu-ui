# Jimu UI（积木 UI）

金智安教育科技内部移动端 Vue 3 组件库。`Vue 3 + TypeScript + <script setup>`，轻量、可按需引入、支持日/夜皮肤与适老模式。

- 包名：`jimu-ui`
- 类名前缀：`jm-`
- CSS 变量前缀：`--jm-*`
- 主色：`#00A0E9`

## 目录结构

```
jimu-ui/
├─ packages/
│  ├─ tokens/        设计令牌（颜色 / 字号 / 圆角 / 动效 / 适老）
│  │  └─ src/
│  │     ├─ primitives.css   原始色板与尺寸刻度
│  │     ├─ tokens.css       语义层（组件只读这一层）
│  │     ├─ dark.css         夜间皮肤
│  │     ├─ elder.css        适老模式
│  │     └─ motion.css       动效开关与降级
│  ├─ core/          组件库本体
│  │  └─ src/
│  │     ├─ components/      91 个组件
│  │     ├─ composables/     useCountDown / useSwipe 等 8 个
│  │     ├─ directives/      v-longpress / v-copy / v-lazy
│  │     ├─ utils/
│  │     ├─ resolver.ts      unplugin-vue-components 解析器
│  │     └─ index.ts
│  └─ docs/          VitePress 文档站（PC 端，带手机模拟框）
│     ├─ components/         每个组件一页
│     ├─ demos/              示例源码（文档里的可运行 demo）
│     └─ guide/              快速上手 / 主题 / 动效与无障碍
└─ package.json      npm workspaces 根
```

## 常用命令

```bash
npm install          # 首次安装（根目录执行，workspaces 一并装好）

npm run docs:dev     # 文档站开发模式，http://localhost:5173（热更新，走源码）
npm run docs:build   # 构建文档站静态产物
npm run docs:preview # 预览构建产物，http://localhost:4173

npm run build:lib    # 构建组件库（ESM + d.ts + style.css）
npm run typecheck    # vue-tsc 类型检查
npm run build        # 库 + 文档全量构建
```

## 业务项目里怎么用

### 全量引入

```ts
import { createApp } from 'vue'
import JimuUI from 'jimu-ui'
import 'jimu-ui/style.css'
import App from './App.vue'

createApp(App).use(JimuUI).mount('#app')
```

### 按需引入（推荐）

```ts
// vite.config.ts
import Components from 'unplugin-vue-components/vite'
import { JimuResolver } from 'jimu-ui/resolver'

export default defineConfig({
  plugins: [
    Components({ resolvers: [JimuResolver()] }),
  ],
})
```

模板里直接写 `<jm-button />`，组件和对应样式自动引入，不需要手动 import。

## 组件清单（91 个）

| 分类 | 组件 |
| --- | --- |
| 基础 | Button、Cell / CellGroup、Tag、CheckTag、Badge、Divider、Icon、Space、Layout（Row / Col）、Grid / GridItem、Avatar / AvatarGroup、Fab、Image、PhotoWall、Card、Watermark、Progress、Circle、CountDown、Statistic、Descriptions、Tree、Table、Transfer |
| 导航 | NavBar、Tabbar / TabbarItem、Tabs / Tab、Segmented、Sticky、DropdownMenu / DropdownItem、Popover、Tooltip、Steps / Step、Timeline / TimelineItem、IndexBar / IndexAnchor、Pagination、BackTop、VirtualList |
| 表单 | Form / FormItem、Input、Search、Switch、Checkbox / CheckboxGroup、Radio / RadioGroup、Rate、Stepper、Slider、Picker、CascadePicker、DatePicker、Calendar、NumberKeyboard、PasswordInput、Uploader、Signature、TreeSelect |
| 反馈 | Popup、ActionSheet、Dialog、Toast（函数式 `showToast()`）、Notify（函数式 `showNotify()`）、Loading、Empty、Result、Skeleton、Swipe / SwipeItem、ImagePreview（函数式 `showImagePreview()`）、List、PullRefresh、Collapse / CollapseItem、SwipeCell、LoadingBar（函数式 `showLoadingBar()`）、Scanner 扫描动效、SafeBottom 安全区占位 |
| 指令 | v-ripple 水波纹（Button / Cell / ActionSheet / Dialog / Card 已内置）、v-longpress 长按、v-copy 复制、v-lazy 懒加载 |
| 工具类 | .jm-safe-pad-bottom 等安全区工具类（--jm-safe-* 变量内置 env(safe-area-inset-*)） |
| 工具类 | .jm-safe-pad-bottom 等安全区工具类（--jm-safe-* 变量内置 env(safe-area-inset-*)） |
| 组合式函数 | useCountDown、useClickOutside(When)、useLockScroll、useSwipe、useDebounceFn、useThrottleFn、useIntersection、useFocusTrap、useAppearance |

通用属性四件套：`type`（6 种语义色）× `variant`（solid / outline / ghost / text）× `size`（3 档）× `radius`（4 档，或任意数值），另有 `color` 可直接传色值并自动派生浅底与描边。

## 主题与外观

三档运行时开关，挂在 `<html>` 上即可全局生效：

```html
<html data-theme="dark">      <!-- 夜间皮肤；不写或 light 为日间 -->
<html data-elder="true">      <!-- 适老模式：字号 ×1.28、触控区 ≥48px、对比度提高、默认关动效 -->
<html data-motion="off">      <!-- 关闭全部动效 -->
```

也可以用 `useAppearance()` 在代码里切换，它会接管上述属性并持久化到 localStorage。

改品牌色只需覆盖语义层，不要动组件样式：

```css
:root {
  --jm-color-primary: #00a0e9;
  --jm-color-primary-hover: #0090d2;
  --jm-color-primary-active: #007fb9;
  --jm-color-primary-light: #e6f6fd;
  --jm-color-primary-border: #99dcf6;
}
```

## 开发约定

1. **组件内禁止写死颜色、字号、圆角、时长**，一律用 `var(--jm-*)` 令牌。三套皮肤和适老模式都靠令牌覆盖实现，写死就废了。
2. 动效统一用 `var(--jm-duration-*)` / `var(--jm-ease-*)`，不要写 `transition: .3s`。
3. 新增组件要同时补：`components/*.vue`、`demos/<组件>/*.vue`、`docs/components/<组件>.md`，并在 `src/index.ts` 与 `resolver.ts` 注册。
4. 文档示例即文档，禁止用静态截图替代可运行 demo。
5. 弹层类组件（Popup / Dialog / ActionSheet / Toast）在文档的手机框里必须传 `:teleport="false"`，否则 `position: fixed` 会脱离模拟框贴到整个视口。

## 移动端已知兼容处理

`100dvh` + `env(safe-area-inset-*)` 安全区、输入框字号锁 16px（避免 iOS 聚焦自动放大）、`-webkit-tap-highlight-color`、高 DPR 下的 1px 边框、弹层打开时的滚动穿透锁定。
