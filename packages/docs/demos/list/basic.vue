<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'

const loading = ref(false)
const finished = ref(false)
const error = ref(false)
const list = ref<number[]>(Array.from({ length: 8 }, (_, i) => i + 1))

let timer: ReturnType<typeof setTimeout> | undefined

function onLoad() {
  if (loading.value || finished.value) return
  loading.value = true
  timer = setTimeout(() => {
    const start = list.value.length
    list.value.push(...Array.from({ length: 6 }, (_, i) => start + i + 1))
    loading.value = false
    if (list.value.length >= 26) finished.value = true
  }, 700)
}

function reset() {
  if (timer) clearTimeout(timer)
  list.value = Array.from({ length: 8 }, (_, i) => i + 1)
  loading.value = false
  finished.value = false
  error.value = false
}

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">滚动到底部自动加载</p>
    <div class="scroller">
      <jm-list v-model:loading="loading" v-model:error="error" :finished="finished" @load="onLoad">
        <div v-for="n in list" :key="n" class="row">列表项 {{ n }}</div>
      </jm-list>
    </div>
    <div class="demo-row">
      <jm-button size="small" @click="reset">重置列表</jm-button>
      <jm-button size="small" @click="finished = true">手动标记加载完</jm-button>
      <jm-button size="small" @click="error = true">模拟失败</jm-button>
    </div>
    <p class="demo-note">共 {{ list.length }} 条 · 加载中 {{ loading ? '是' : '否' }} · 已结束 {{ finished ? '是' : '否' }}</p>
    <p class="demo-note">失败态点击文案会清除 error 并自动重试（监听 <code>click-error</code> 可自行处理）。</p>
  </div>
</template>

<style scoped>
.scroller {
  height: 260px;
  overflow-y: auto;
  border-radius: 12px;
  background: var(--jm-bg-container);
  -webkit-overflow-scrolling: touch;
}

.row {
  padding: 12px 14px;
  border-bottom: 1px solid var(--jm-border-color);
  font-size: 13px;
  color: var(--jm-text-color-2);
}
</style>
