<script setup lang="ts">
import { ref } from 'vue'

const longText =
  'iPhone 17 Pro Max 256GB 沙漠色钛金属 全网通 5G 手机 国行原封全新正品 现货秒发'
const shortText = '库存充足'

const speed = ref(40)
</script>

<template>
  <div class="demo-page ts-demo">
    <p class="demo-label">超长文本自动滚动（不超出则静止）</p>
    <div class="ts-card">
      <jm-text-scroll :text="longText" />
      <jm-text-scroll :text="shortText" class="ts-gap-top" />
    </div>

    <p class="demo-label">放在任意布局里：卡片标题 / Cell 标题</p>
    <div class="ts-card">
      <div class="ts-title-row">
        <strong>商品名：</strong>
        <jm-text-scroll class="ts-title" :text="longText" :speed="60" />
      </div>
    </div>

    <p class="demo-label">速度可调（当前 {{ speed }}px/s）</p>
    <div class="ts-card">
      <jm-text-scroll :text="longText" :speed="speed" />
      <input v-model.number="speed" class="ts-range" type="range" min="20" max="120" step="10" />
    </div>

    <p class="demo-note">
      内容宽度超过容器才开始滚动，刚好放得下就静止显示；悬停/按住会暂停滚动。
      公告栏场景（带喇叭图标和背景色）请用 NoticeBar。
    </p>
  </div>
</template>

<style scoped>
.ts-card {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color);
}

.ts-gap-top {
  margin-top: 10px;
}

.ts-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ts-title {
  flex: 1 1 auto;
  min-width: 0;
}

.ts-range {
  width: 100%;
  margin-top: 12px;
}
</style>
