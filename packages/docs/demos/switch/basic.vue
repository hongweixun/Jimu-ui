<script setup lang="ts">
import { ref } from 'vue'

const a = ref(true)
const b = ref(false)
const c = ref(true)
const d = ref(false)
const e = ref(true)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础</p>
    <div class="demo-row">
      <jm-switch v-model="a" />
      <jm-switch v-model="b" />
    </div>

    <p class="demo-label">尺寸</p>
    <div class="demo-row">
      <jm-switch v-model="a" size="small" />
      <jm-switch v-model="a" />
      <jm-switch v-model="a" size="large" />
    </div>

    <p class="demo-label">带文字说明</p>
    <div class="demo-col">
      <jm-switch v-model="c" active-text="已开启" inactive-text="已关闭" />
      <jm-switch v-model="d" active-text="允许推送" inactive-text="不接受推送" size="small" />
    </div>

    <p class="demo-label">自定义颜色</p>
    <div class="demo-row">
      <jm-switch v-model="c" active-color="#00B98A" />
      <jm-switch v-model="c" active-color="#7C4DFF" />
    </div>

    <p class="demo-label">禁用 / 加载</p>
    <div class="demo-row">
      <jm-switch v-model="e" disabled />
      <jm-switch :model-value="false" disabled />
      <jm-switch v-model="c" loading />
    </div>
  </div>
</template>
