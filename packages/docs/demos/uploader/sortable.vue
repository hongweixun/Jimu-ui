<script setup lang="ts">
import { ref } from 'vue'
import type { UploaderFile } from 'jimu-ui'

/* 用色块 URL 当文件：真实场景是选完图或已上传的图片地址 */
const files = ref<(string | UploaderFile)[]>([
  'https://picsum.photos/seed/jm-a/200/200',
  'https://picsum.photos/seed/jm-b/200/200',
  'https://picsum.photos/seed/jm-c/200/200',
  'https://picsum.photos/seed/jm-d/200/200',
  'https://picsum.photos/seed/jm-e/200/200',
])

function onChange(next: (string | UploaderFile)[]) {
  files.value = next
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">长按缩略图抬起，拖到目标位置松手（实时让位）</p>
    <jm-uploader
      v-model="files"
      sortable
      :columns="3"
      :deletable="false"
      :preview-image="false"
      @change="onChange"
    />
    <p class="demo-tip">顺序：{{ files.map((f) => (typeof f === 'string' ? f.slice(-5, -4) : '?')).join(' → ') }}</p>
  </div>
</template>

<style scoped>
.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: 10px 0 0;
}
</style>
