<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'

const loading = ref(true)
const animate = ref(true)
let timer: ReturnType<typeof setTimeout> | undefined

function reload() {
  loading.value = true
  clearTimeout(timer)
  timer = setTimeout(() => (loading.value = false), 1800)
}

onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">
      带内容切换（1.8s 后显示真实内容）
      <jm-switch v-model="animate" size="small" style="margin-left: 8px" />
    </p>

    <jm-skeleton :loading="loading" avatar :rows="3" :animate="animate">
      <div style="display: flex; gap: 12px">
        <div class="fake-avatar" />
        <div style="flex: 1">
          <div style="font-size: 15px; font-weight: 500; margin-bottom: 4px">王老师 · 数学</div>
          <div style="font-size: 13px; color: var(--jm-text-color-2); line-height: 1.6">
            教龄 8 年，擅长小学三四年级计算与应用题专项训练，累计带班 1200+。
          </div>
        </div>
      </div>
    </jm-skeleton>

    <jm-button size="small" style="margin-top: 12px" @click="reload">重新加载</jm-button>

    <p class="demo-label">标题 + 段落</p>
    <jm-skeleton :rows="2" />

    <p class="demo-label">圆角块（列表占位）</p>
    <jm-skeleton :title="false" :rows="3" round />
  </div>
</template>

<style scoped>
.fake-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--jm-color-primary-light);
  flex: 0 0 auto;
}
</style>
