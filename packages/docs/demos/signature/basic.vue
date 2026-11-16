<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const value = ref('')
const pad = ref<{ isEmpty: () => boolean } | null>(null)

function confirm() {
  if (!value.value || pad.value?.isEmpty()) {
    showToast('请先手写签名')
    return
  }
  showToast('签名已保存')
}
</script>

<template>
  <div class="demo-page">
    <jm-signature ref="pad" v-model="value" :height="180" show-toolbar />

    <jm-button type="primary" block @click="confirm">确认签名</jm-button>

    <template v-if="value">
      <p class="demo-label">导出的签名图（透明底已按笔迹裁剪）</p>
      <div class="preview">
        <img :src="value" alt="签名预览" />
      </div>

      <p class="demo-label">只读回显：把 value 传回 modelValue 即可</p>
      <jm-signature :model-value="value" :height="120" readonly :trim="false" />
    </template>
  </div>
</template>

<style scoped>
.preview {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 96px;
  padding: 8px;
  border: 1px dashed var(--jm-border-color);
  border-radius: 8px;
  background: repeating-conic-gradient(#f3f4f6 0% 25%, #fff 0% 50%) 50% / 12px 12px;
}

.preview img {
  max-width: 100%;
  max-height: 100%;
}
</style>
