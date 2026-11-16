<script setup lang="ts">
import { ref } from 'vue'

const clicks = ref(0)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">指令可以直接用在任意元素上</p>
    <div class="demo-ripple-card" v-ripple @click="clicks++">
      <div class="demo-ripple-title">点我试试</div>
      <div class="demo-ripple-desc">水波从指尖扩散，铺满整个卡片</div>
    </div>

    <p class="demo-label">自定义颜色 / 从中心扩散</p>
    <div class="demo-row">
      <div class="demo-ripple-pill" v-ripple="{ color: '#00A0E9' }">主色波</div>
      <div class="demo-ripple-pill" v-ripple="{ color: '#E8344B', centered: true }">居中红波</div>
      <div class="demo-ripple-pill" v-ripple="{ disabled: true }">已禁用</div>
    </div>

    <p class="demo-note">
      指令只负责视觉反馈，点击事件照常自己绑：当前点击 {{ clicks }} 次
    </p>
  </div>
</template>

<style scoped>
.demo-ripple-card {
  position: relative;
  overflow: hidden;
  padding: 18px 16px;
  border-radius: 14px;
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  cursor: pointer;
  user-select: none;
}

.demo-ripple-card:active {
  border-color: var(--jm-color-primary-border);
}

.demo-ripple-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--jm-text-color);
}

.demo-ripple-desc {
  margin-top: 4px;
  font-size: 12px;
  color: var(--jm-text-color-3);
}

.demo-ripple-pill {
  position: relative;
  overflow: hidden;
  padding: 10px 18px;
  border-radius: 999px;
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: 13px;
  color: var(--jm-text-color-2);
  cursor: pointer;
  user-select: none;
}
</style>
