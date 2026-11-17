import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vitepress'

const resolve = (p: string) => fileURLToPath(new URL(p, import.meta.url))

/**
 * 部署子路径：GitHub Pages 项目站点形如 https://<user>.github.io/<repo>/
 * CI 里设 DOCS_BASE=/<repo>/；本地 dev 与根域名部署不设走默认 '/'
 */
const base = process.env.DOCS_BASE || '/'

const components = {
  base: [
    { text: 'Ripple 水波纹', link: '/components/ripple' },
    { text: 'Icon 图标', link: '/components/icon' },
    { text: 'Space 间距', link: '/components/space' },
    { text: 'Layout 布局', link: '/components/layout' },
    { text: 'Button 按钮', link: '/components/button' },
    { text: 'Cell 单元格', link: '/components/cell' },
    { text: 'Avatar 头像', link: '/components/avatar' },
    { text: 'Grid 宫格', link: '/components/grid' },
    { text: 'Fab 悬浮按钮', link: '/components/fab' },
    { text: 'Image 图片', link: '/components/image' },
    { text: 'PhotoWall 照片墙', link: '/components/photo-wall' },
    { text: 'Card 卡片', link: '/components/card' },
    { text: 'Tag 标签', link: '/components/tag' },
    { text: 'CheckTag 可选标签', link: '/components/check-tag' },
    { text: 'Badge 徽标', link: '/components/badge' },
    { text: 'Divider 分割线', link: '/components/divider' },
    { text: 'Watermark 水印', link: '/components/watermark' },
    { text: 'Progress 进度条', link: '/components/progress' },
    { text: 'Circle 环形进度', link: '/components/circle' },
    { text: 'CountDown 倒计时', link: '/components/count-down' },
    { text: 'Statistic 数值统计', link: '/components/statistic' },
    { text: 'Descriptions 描述列表', link: '/components/descriptions' },
    { text: 'Table 表格', link: '/components/table' },
    { text: 'Tree 树形控件', link: '/components/tree' },
    { text: 'Transfer 穿梭框', link: '/components/transfer' },
    { text: 'NavBar 导航栏', link: '/components/nav-bar' },
    { text: 'Tabbar 标签栏', link: '/components/tabbar' },
    { text: 'NoticeBar 通知栏', link: '/components/notice-bar' },
  ],
  form: [
    { text: 'Form 表单', link: '/components/form' },
    { text: 'Input 输入框', link: '/components/input' },
    { text: 'Search 搜索', link: '/components/search' },
    { text: 'Switch 开关', link: '/components/switch' },
    { text: 'Checkbox 复选框', link: '/components/checkbox' },
    { text: 'Radio 单选框', link: '/components/radio' },
    { text: 'Rate 评分', link: '/components/rate' },
    { text: 'Stepper 步进器', link: '/components/stepper' },
    { text: 'Slider 滑块', link: '/components/slider' },
    { text: 'Picker 选择器', link: '/components/picker' },
    { text: 'CascadePicker 级联选择', link: '/components/cascade-picker' },
    { text: 'TreeSelect 树选择', link: '/components/tree-select' },
    { text: 'DatePicker 日期选择', link: '/components/date-picker' },
    { text: 'Calendar 日历', link: '/components/calendar' },
    { text: 'NumberKeyboard 数字键盘', link: '/components/number-keyboard' },
    { text: 'PasswordInput 密码输入', link: '/components/password-input' },
    { text: 'Uploader 上传', link: '/components/uploader' },
    { text: 'Signature 手写签名', link: '/components/signature' },
  ],
  nav: [
    { text: 'Tabs 标签页', link: '/components/tabs' },
    { text: 'Segmented 分段控制器', link: '/components/segmented' },
    { text: 'Sticky 粘性布局', link: '/components/sticky' },
    { text: 'DropdownMenu 下拉菜单', link: '/components/dropdown-menu' },
    { text: 'Popover 气泡', link: '/components/popover' },
    { text: 'Tooltip 文字提示', link: '/components/tooltip' },
    { text: 'Steps 步骤条', link: '/components/steps' },
    { text: 'Timeline 时间轴', link: '/components/timeline' },
    { text: 'IndexBar 索引栏', link: '/components/index-bar' },
    { text: 'Pagination 分页', link: '/components/pagination' },
    { text: 'BackTop 回到顶部', link: '/components/back-top' },
    { text: 'VirtualList 虚拟列表', link: '/components/virtual-list' },
  ],
  feedback: [
    { text: 'Popup 弹出层', link: '/components/popup' },
    { text: 'ActionSheet 动作面板', link: '/components/action-sheet' },
    { text: 'Dialog 对话框', link: '/components/dialog' },
    { text: 'Toast 轻提示', link: '/components/toast' },
    { text: 'Notify 消息通知', link: '/components/notify' },
    { text: 'Loading 加载', link: '/components/loading' },
    { text: 'LoadingBar 顶部加载条', link: '/components/loading-bar' },
    { text: 'Scanner 扫描动效', link: '/components/scanner' },
    { text: 'Empty 空状态', link: '/components/empty' },
    { text: 'Result 结果页', link: '/components/result' },
    { text: 'Skeleton 骨架屏', link: '/components/skeleton' },
    { text: 'Swipe 轮播', link: '/components/swipe' },
    { text: 'ImagePreview 图片预览', link: '/components/image-preview' },
    { text: 'List 列表加载', link: '/components/list' },
    { text: 'PullRefresh 下拉刷新', link: '/components/pull-refresh' },
    { text: 'Collapse 折叠面板', link: '/components/collapse' },
    { text: 'SwipeCell 滑动单元格', link: '/components/swipe-cell' },
  ],
  cross: [
    { text: 'LongPress 长按指令', link: '/components/long-press' },
    { text: 'Copy 复制指令', link: '/components/copy' },
    { text: 'Lazy 懒加载指令', link: '/components/lazy' },
    { text: '组合式函数', link: '/components/composables' },
  ],
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'Jimu UI',
  description: '金智安教育科技 · 移动端 Vue 3 组件库',
  cleanUrls: true,
  base,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}logo.svg` }],
    ['meta', { name: 'theme-color', content: '#00A0E9' }],
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0, viewport-fit=cover' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Jimu UI',

    nav: [
      { text: '指南', link: '/guide/quickstart', activeMatch: '/guide/' },
      { text: '组件', link: '/components/button', activeMatch: '/components/' },
    ],

    sidebar: [
      {
        text: '指南',
        items: [
          { text: '快速开始', link: '/guide/quickstart' },
          { text: '主题与令牌', link: '/guide/theme' },
          { text: '动效系统', link: '/guide/motion' },
          { text: '适老与无障碍', link: '/guide/motion-a11y' },
        ],
      },
      {
        text: '基础组件',
        items: components.base,
      },
      {
        text: '表单组件',
        items: components.form,
      },
      {
        text: '导航组件',
        items: components.nav,
      },
      {
        text: '反馈与展示',
        items: components.feedback,
      },
      {
        text: '横切能力',
        items: components.cross,
      },
    ],

    outline: {
      level: [2, 3],
      label: '本页目录',
    },

    docFooter: {
      prev: '上一页',
      next: '下一页',
    },

    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到日间模式',
    darkModeSwitchTitle: '切换到夜间模式',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    langMenuLabel: '语言',

    footer: {
      message: '内部组件库 · 仅供金智安教育科技内部项目使用',
      copyright: 'Copyright © 2026 金智安教育科技',
    },

    search: {
      provider: 'local',
    },

    notFound: {
      title: '页面不存在',
      quote: '这个积木还没拼上，换个地方看看。',
      linkLabel: '回到首页',
      linkText: '返回首页',
    },
  },

  vite: {
    build: {
      /* CI 是全新 runner 无需清空；本地也避免每次构建前删目录 */
      emptyOutDir: false,
    },
    resolve: {
      alias: [
        { find: /^jimu-ui$/, replacement: resolve('../../core/src/index.ts') },
        { find: /^@jimu\/tokens/, replacement: resolve('../../tokens/src') },
      ],
    },
    server: {
      host: true,
    },
  },
})
