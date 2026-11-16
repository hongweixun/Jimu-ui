<script setup lang="ts">
import { computed, ref } from 'vue'
import type { UploaderFile } from 'jimu-ui'

const compress = ref(true)
const files = ref<(string | UploaderFile)[]>([])

const tips = computed(() =>
  compress.value
    ? '压缩开启：长边压到 1280px、质量 0.8，压缩后体积反而变大时回退原图。'
    : '压缩关闭：保留原始文件。',
)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">
      自动压缩
      <jm-switch v-model="compress" size="small" style="margin-left: 8px" />
    </p>
    <p class="demo-tip">{{ tips }}</p>

    <jm-uploader v-model="files" :compress="compress" :max-count="4" />
  </div>
</template>

<style scoped>
.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: -6px 0 10px;
  line-height: 1.6;
}
</style>
