---
layout: home

hero:
  name: Jimu UI
  text: 像搭积木一样写页面
  tagline: 金智安教育科技移动端组件库 · Vue 3 + TypeScript · 移动优先 · 支持日夜双肤与适老模式
  image:
    src: ./logo.svg
    alt: Jimu UI 标识——三块积木拼成的 J
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/quickstart
    - theme: alt
      text: 组件总览
      link: /components/button

features:
  - title: 令牌驱动，一套代码多套皮肤
    details: 颜色、字号、间距、圆角、动效全部走 CSS 变量。改三五个变量就能换成公司品牌色，日夜与适老只是换一组映射。
  - title: 每个组件都能调形状与大小
    details: 统一的 type / variant / size / radius 四件套，按钮、标签、输入框、开关都能自由切换形态，还能直接传自定义颜色。
  - title: 动效一次开关全库生效
    details: 四条缓动曲线 + 五档时长组成语义化动效层，进场减速、退场加速；一个 data-motion="off" 就能让全站动效静止，同时尊重系统的减少动态偏好。
  - title: 适老模式不是第二套组件
    details: data-elder="true" 自动放大字号基准 1.28 倍、加厚对比、放宽行高、抬高触控区，代码零改动。
  - title: 按需加载，体积可控
    details: ESM 产物配合 tree-shaking，只打包用到的组件；同时提供 unplugin-vue-components 解析器，模板里直接写标签。
  - title: 移动端踩过的坑都填了
    details: 100dvh、安全区、iOS 输入框缩放、拍点高亮、滚动锁、高 DPR 细线、单行省略，全在基础层统一处理。
---

<div class="feature-grid">
  <a class="feature-card" href="/components/button">
    <span class="feature-card__name">Button 按钮</span>
    <span class="feature-card__desc">6 种语义色 × 4 种样式 × 3 种尺寸</span>
  </a>
  <a class="feature-card" href="/components/cell">
    <span class="feature-card__name">Cell 单元格</span>
    <span class="feature-card__desc">列表骨架，卡片式分组</span>
  </a>
  <a class="feature-card" href="/components/input">
    <span class="feature-card__name">Input 输入框</span>
    <span class="feature-card__desc">描边 / 灰底 / 下划线三种外观</span>
  </a>
  <a class="feature-card" href="/components/popup">
    <span class="feature-card__name">Popup 弹出层</span>
    <span class="feature-card__desc">五个方向，支持内嵌不 Teleport</span>
  </a>
  <a class="feature-card" href="/components/tabs">
    <span class="feature-card__name">Tabs 标签页</span>
    <span class="feature-card__desc">下划线 / 卡片 / 分段</span>
  </a>
  <a class="feature-card" href="/guide/theme">
    <span class="feature-card__name">主题定制</span>
    <span class="feature-card__desc">令牌清单与覆盖姿势</span>
  </a>
</div>
