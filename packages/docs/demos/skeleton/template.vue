<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'

const loading = ref(true)
let timer: ReturnType<typeof setTimeout> | undefined

function reload() {
  loading.value = true
  clearTimeout(timer)
  timer = setTimeout(() => (loading.value = false), 1800)
}
reload()
onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">自定义排版（#template + 骨架子组件）</p>
    <jm-skeleton :loading="loading">
      <template #template>
        <jm-skeleton-avatar size="56px" shape="square" />
        <div class="body">
          <jm-skeleton-title width="34%" />
          <jm-skeleton-paragraph :row="2" :row-width="['92%', '60%']" />
        </div>
      </template>
      <div class="real">
        <div class="real__avatar">J</div>
        <div class="body">
          <div class="real__name">Jimu UI</div>
          <div class="real__desc">轻量移动端组件库，Vue 3 + TypeScript，按需引入。</div>
        </div>
      </div>
    </jm-skeleton>
    <jm-button size="small" style="margin-top: 12px" @click="reload">重新加载</jm-button>

    <p class="demo-label">呼吸动效（animation="breath"）</p>
    <jm-skeleton animation="breath" :title="false" :rows="3" round />

    <p class="demo-label">指定标题宽度</p>
    <jm-skeleton :rows="2" title-width="70%" />
  </div>
</template>

<style scoped>
.body {
  flex: 1 1 auto;
  min-width: 0;
  padding-top: 4px;
}

.real {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.real__avatar {
  flex: 0 0 auto;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--jm-radius-md);
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 22px;
  font-weight: 600;
}

.real__name {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
}

.real__desc {
  font-size: 13px;
  color: var(--jm-text-color-2);
  line-height: 1.6;
}
</style>
