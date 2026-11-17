<script setup lang="ts">
const levels = [0, 1, 2, 3, 4, 6, 8, 12, 16, 24]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">点击卡片切换海拔</p>
    <div class="grid">
      <div
        v-for="lv in levels"
        :key="lv"
        class="card"
        :class="`jm-elevation-${lv}`"
        :style="{ background: 'var(--jm-bg-elevated)' }"
      >
        <b>elevation-{{ lv }}</b>
        <span>海拔 {{ lv }}</span>
      </div>
    </div>
    <p class="demo-note">
      数字越大离纸面越高。工具类 <code>.jm-elevation-N</code> 可叠加在任何元素上，暗色主题自动换为更重的阴影。
    </p>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 4px 0 8px;
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 16px 8px;
  border-radius: var(--jm-radius-md);
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-2);
  transition: box-shadow 0.3s var(--jm-motion-feedback-ease);
}

.card b {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color);
}

.demo-note code {
  padding: 1px 4px;
  border-radius: 4px;
  background: var(--jm-bg-page);
  font-size: 12px;
}
</style>
