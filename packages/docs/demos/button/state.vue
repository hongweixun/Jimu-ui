<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)

function submit() {
  loading.value = true
  setTimeout(() => (loading.value = false), 1800)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">加载与禁用</p>
    <div class="demo-row">
      <jm-button type="primary" :loading="loading" @click="submit">
        {{ loading ? '提交中' : '点击提交' }}
      </jm-button>
      <jm-button type="primary" disabled>禁用</jm-button>
      <jm-button variant="outline" disabled>禁用</jm-button>
    </div>

    <p class="demo-label">带图标</p>
    <div class="demo-row">
      <jm-button type="primary">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path
              d="M12 5v14M5 12h14"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </template>
        新建课程
      </jm-button>
      <jm-button variant="outline" type="primary">下一步</jm-button>
    </div>

    <p class="demo-label">自定义颜色（浅底与描边自动派生）</p>
    <div class="demo-row">
      <jm-button color="#7C4DFF">紫色实心</jm-button>
      <jm-button color="#7C4DFF" variant="ghost">紫色浅底</jm-button>
      <jm-button color="#7C4DFF" variant="outline">紫色描边</jm-button>
    </div>
  </div>
</template>
