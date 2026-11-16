<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const courses = [
  { value: 'math', label: '数学思维' },
  { value: 'art', label: '创意美术' },
  { value: 'coding', label: '少儿编程' },
  { value: 'music', label: '声乐启蒙' },
  { value: 'science', label: '科学实验' },
]

const picked = ref<string[]>(['math'])

function onOverLimit(payload: { type: 'max' | 'min' }) {
  showToast({
    message: payload.type === 'max' ? '最多选 3 门，先取消一门再选' : '至少保留 1 门',
  })
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">最多选 3 门，最少保留 1 门</p>
    <jm-checkbox-group
      v-model="picked"
      direction="vertical"
      :max="3"
      :min="1"
      @over-limit="onOverLimit"
    >
      <jm-checkbox v-for="c in courses" :key="c.value" :value="c.value">{{ c.label }}</jm-checkbox>
    </jm-checkbox-group>

    <p class="state">已选 {{ picked.length }} 门：{{ picked.join('、') || '无' }}</p>
    <p class="demo-note">
      超出上限时勾选会被拦下，并触发 <code>overLimit</code>；用 Toast 提示一下是最轻的做法。
    </p>
  </div>
</template>

<style scoped>
.state {
  margin: 12px 0 0;
  color: var(--jm-text-color-3);
  font-size: 12px;
}
</style>
