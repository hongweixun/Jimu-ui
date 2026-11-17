<template>
  <div class="demo-page">
    <p class="demo-tip">banner 通栏上传：整宽触发卡 + 文件行，适合"一次传一张证书/证件"的场景。</p>

    <div class="mock-card">
      <Uploader
        v-model="certFiles"
        layout="banner"
        banner-title="上传证书图片"
        banner-desc="支持 JPG / PNG / PDF，可拍照上传"
        accept="image/*,.pdf"
        :max-count="3"
        :preview-teleport="false"
      />

      <p class="demo-tip">不带副标题、已传文件时的计数角标：</p>

      <Uploader
        v-model="photoFiles"
        layout="banner"
        banner-title="上传现场照片"
        :max-count="5"
        :preview-teleport="false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Uploader } from 'jimu-ui'

const certFiles = ref<string[]>([])
const photoFiles = ref<string[]>([
  'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg',
])
</script>

<style scoped>
.mock-card {
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
