<script setup lang="ts">
import { ref } from 'vue'
import type { UploaderFile } from 'jimu-ui'

function svg(text: string, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="300" height="300" fill="url(#g)"/><text x="150" y="160" font-family="system-ui" font-size="30" fill="#fff" text-anchor="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const files = ref<(string | UploaderFile)[]>([
  { url: svg('已上传 1', '#00A0E9', '#2B6BE4'), name: '课程封面.png' },
  { url: svg('已上传 2', '#FF8A3D', '#FF6430'), name: '活动海报.png' },
])

const tip = ref('')
const readonlyFiles = ref<(string | UploaderFile)[]>([{ url: svg('只读', '#8E9AAF', '#5F6B7A'), name: '凭证.jpg' }])

function onOversize(list: File[]) {
  tip.value = `有 ${list.length} 个文件超过 2MB，已跳过`
}

function onExceed(list: File[]) {
  tip.value = `最多 4 张，多余的 ${list.length} 个已忽略`
}

function onDelete(_file: string | UploaderFile, index: number) {
  tip.value = `删除了第 ${index + 1} 张`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（最多 4 张，单张 ≤ 2MB，可多选）</p>
    <jm-uploader
      v-model="files"
      :max-count="4"
      multiple
      :max-size="2 * 1024 * 1024"
      :preview-teleport="false"
      @oversize="onOversize"
      @exceed="onExceed"
      @delete="onDelete"
    />
    <p class="demo-note">已选 {{ files.length }} / 4 张{{ tip ? ` · ${tip}` : '' }}</p>

    <p class="demo-label">只读（只展示，不可增删）</p>
    <jm-uploader v-model="readonlyFiles" readonly :columns="4" :preview-teleport="false" />

    <p class="demo-label">三列大图 · 关闭预览</p>
    <jm-uploader v-model="files" :columns="3" :preview-image="false" :preview-teleport="false" :upload-text="''" />
    <p class="demo-note">点击缩略图会派发 <code>click-preview</code>，可接自己的图片查看器；这里关闭了内置预览。</p>
  </div>
</template>
