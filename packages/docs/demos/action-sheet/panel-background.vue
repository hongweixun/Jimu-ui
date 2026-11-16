<script setup lang="ts">
import { ref } from 'vue'

const showImage = ref(false)
const showGradient = ref(false)

const actions = [
  { name: 'course', label: '继续上次学习', subLabel: '第 3 章 · 函数与闭包' },
  { name: 'practice', label: '开始章节练习' },
  { name: 'note', label: '查看我的笔记' },
]

/** 深色面板：文字与分割线转白，否则深底上黑字读不出来 */
const darkVars: Record<string, string> = {
  '--jm-text-color': '#ffffff',
  '--jm-text-color-2': 'rgba(255, 255, 255, 0.78)',
  '--jm-text-color-3': 'rgba(255, 255, 255, 0.6)',
  '--jm-action-sheet-close-color': 'rgba(255, 255, 255, 0.7)',
  '--jm-action-sheet-header-border': 'rgba(255, 255, 255, 0.16)',
}
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="showImage = true">整张面板背景图</jm-button>
    <jm-button block @click="showGradient = true">整张面板渐变色</jm-button>

    <jm-action-sheet
      v-model:show="showImage"
      title="我的学习"
      description="今天还有 2 个任务待完成"
      :actions="actions"
      background-image="/img/as-panel.svg"
      background-mask="linear-gradient(180deg, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0) 42%)"
      :teleport="false"
    />

    <jm-action-sheet
      v-model:show="showGradient"
      title="我的学习"
      description="今天还有 2 个任务待完成"
      :actions="actions"
      background="linear-gradient(160deg, #111827 0%, #312e81 55%, #4c1d95 100%)"
      :style="darkVars"
      :teleport="false"
    />

    <p class="demo-note">
      background 收任意 CSS background（纯色 / 渐变），background-image
      铺图片并用 background-mask 压一层提亮或压暗，保证文字可读。
    </p>
  </div>
</template>

<style scoped>
.demo-page {
  display: flex;
  flex-direction: column;
  gap: var(--jm-space-3);
}
</style>
