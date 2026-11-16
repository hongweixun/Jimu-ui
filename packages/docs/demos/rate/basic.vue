<script setup lang="ts">
import { ref } from 'vue'

const basic = ref(3)
const half = ref(3.5)
const readonly = ref(4)
const custom = ref(2)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（再点一次可清零）</p>
    <jm-rate v-model="basic" show-text />

    <p class="demo-label">允许半星</p>
    <jm-rate v-model="half" allow-half show-text />

    <p class="demo-label">只读</p>
    <jm-rate :model-value="readonly" readonly show-text />

    <p class="demo-label">自定义尺寸与颜色</p>
    <jm-rate v-model="custom" :size="30" active-color="#E8344B" />

    <p class="demo-label">10 星 + 大间距</p>
    <jm-rate v-model="basic" :count="10" :size="18" :gutter="6" />

    <p class="demo-note">当前评分：{{ basic }} / {{ half }} / {{ readonly }} / {{ custom }}</p>
  </div>
</template>
