<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)

const actions = [
  { name: 'year', label: '按年订阅', subLabel: '¥198 / 年，省 40%' },
  { name: 'month', label: '按月订阅', subLabel: '¥26 / 月' },
  { name: 'trial', label: '先试用 7 天' },
]

/** 标题区文字全给白色：说明文字用变量覆盖，避免在渐变上灰扑扑 */
const headerText: Record<string, string> = {
  '--jm-action-sheet-subtitle-color': 'rgba(255, 255, 255, 0.82)',
  '--jm-action-sheet-close-color': 'rgba(255, 255, 255, 0.75)',
  '--jm-action-sheet-header-border': 'transparent',
}
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="show = true">渐变标题区</jm-button>

    <jm-action-sheet
      v-model:show="show"
      title="升级到专业版"
      description="解锁全部课程、离线缓存与导出"
      :actions="actions"
      title-background="linear-gradient(120deg, #4f7cff 0%, #8b5cf6 55%, #c15cff 100%)"
      title-color="#ffffff"
      :title-size="18"
      :style="headerText"
      closeable
      :teleport="false"
    />

    <p class="demo-note">
      title-background 收任意 CSS background：纯色、渐变都行；title-color / title-size
      控制文字，其它颜色走 CSS 变量。
    </p>
  </div>
</template>
