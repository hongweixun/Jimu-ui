<script setup lang="ts">
import { ref } from 'vue'
import type { GuideStep } from 'jimu-ui'

const current = ref(-1)
const currentDialog = ref(-1)

const steps: GuideStep[] = [
  {
    element: '#guide-step-1',
    title: '搜索课程',
    content: '在这里输入课程名、老师或关键词，快速找到想学的内容。',
    placement: 'bottom',
  },
  {
    element: '#guide-step-2',
    title: '学习进度',
    content: '完成今日任务后，这里的进度条会点亮一枚星星。',
    placement: 'right',
  },
  {
    element: '#guide-step-3',
    title: '我的课表',
    content: '点开可以查看本周排课和作业截止时间。',
    placement: 'top',
    highlightPadding: 6,
  },
]

const dialogSteps: GuideStep[] = [
  {
    element: '#guide-dialog-1',
    title: '欢迎来到 Jimu UI',
    content: '这是一条弹窗式引导，不指向具体元素，适合开场说明。',
    mode: 'dialog',
  },
  {
    element: '#guide-dialog-1',
    title: '快捷入口',
    content: '常见操作都收纳在右下角的悬浮球里，长按可拖动。',
    mode: 'dialog',
  },
]
</script>

<template>
  <div class="demo-page demo-guide">
    <p class="demo-label">气泡式引导（步骤气泡指向目标元素）</p>
    <div class="card">
      <div id="guide-step-1" class="row-item">🔍 搜索课程</div>
      <div id="guide-step-2" class="row-item">⭐ 学习进度 · 60%</div>
      <div id="guide-step-3" class="row-item">📅 我的课表</div>
    </div>
    <button class="chip chip--primary" @click="current = 0">开始引导</button>

    <p class="demo-label">弹窗式引导（不指向元素，居中弹窗）</p>
    <div class="card">
      <div id="guide-dialog-1" class="row-item">🏠 首页</div>
    </div>
    <button class="chip" @click="currentDialog = 0">弹窗引导</button>

    <p class="demo-note">
      v-model:current 控制步骤；目标元素会自动滚动到可视区并挖孔高亮；滚动/缩放时自动重算位置。
    </p>

    <jm-guide v-model:current="current" :steps="steps" />
    <jm-guide v-model:current="currentDialog" :steps="dialogSteps" />
  </div>
</template>

<style scoped>
.card {
  border: var(--jm-border-width) solid var(--jm-border-color);
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-elevated);
  margin-bottom: 12px;
}

.row-item {
  padding: 14px 16px;
  border-bottom: var(--jm-border-width) solid var(--jm-border-color);
  font-size: var(--jm-font-size-sm);
}

.row-item:last-child {
  border-bottom: 0;
}

.chip {
  padding: 8px 14px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-sm);
  box-shadow: var(--jm-elevation-1);
  cursor: pointer;
}

.chip--primary {
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
}
</style>
