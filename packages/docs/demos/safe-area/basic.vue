<template>
  <div class="demo-page">
    <p class="demo-tip">
      安全区占位：真机刘海屏下 env(safe-area-inset-bottom) &gt; 0，滚动内容末尾放
      SafeBottom 让最后一个元素不被 Home Indicator 遮住。桌面浏览器 env 为 0，
      demo 用 minHeight 兜底可视化。
    </p>

    <div class="mock-page">
      <div class="mock-scroll">
        <p v-for="i in 6" :key="i" class="mock-line">列表第 {{ i }} 行</p>
        <jm-safe-bottom :min-height="20" background="#f7f8fa" />
      </div>
      <div class="mock-tabbar">
        <span>首页</span><span>我的</span>
      </div>
      <!-- fixed 底栏上方让位：也可以用 .jm-safe-pad-bottom 工具类 -->
      <SafeBottom :min-height="14" background="#00a0e9" />
    </div>

    <p class="demo-tip">
      fixed 底栏内部让位：给底栏加 <code>.jm-safe-pad-bottom</code>，或直接
      <code>padding-bottom: var(--jm-safe-bottom)</code>；页面 meta 需
      <code>viewport-fit=cover</code>（文档站模板已内置）。
    </p>
  </div>
</template>

<script setup lang="ts">
import { SafeBottom } from 'jimu-ui'
</script>

<style scoped>
.mock-page {
  border: 1px solid #e5e6eb;
  border-radius: 12px;
  overflow: hidden;
  max-width: 320px;
}

.mock-scroll {
  height: 180px;
  overflow-y: auto;
  background: #fff;
}

.mock-line {
  margin: 0;
  padding: 12px 16px;
  border-bottom: 1px solid #f2f3f5;
  font-size: 14px;
  color: #323233;
}

.mock-tabbar {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  background: #00a0e9;
  color: #fff;
  font-size: 13px;
}
</style>
