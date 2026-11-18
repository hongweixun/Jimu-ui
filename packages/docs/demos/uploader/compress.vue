<script setup lang="ts">
import { computed, ref } from 'vue'
import type { UploaderFile } from 'jimu-ui'

const compress = ref(true)
/* 目标体积：200KB 以内 */
const target = ref(true)
const TARGET_BYTES = 200 * 1024

const basic = ref<(string | UploaderFile)[]>([])
const targeted = ref<(string | UploaderFile)[]>([])

const tips = computed(() =>
  compress.value
    ? '压缩开启：长边压到 1280px、质量 0.8，压缩后体积反而变大时回退原图。'
    : '压缩关闭：保留原始文件。',
)

const targetTips = computed(() =>
  target.value
    ? `目标体积开启：压到 ${fmt(TARGET_BYTES)} 以内（先降质量最低 0.3，再缩长边最低 480px）。`
    : `目标体积关闭：只做常规压缩（1280px / 质量 0.8）。`,
)

const sizes = (list: (string | UploaderFile)[]) =>
  list.map((it) => (typeof it === 'object' && it?.size ? fmt(it.size) : '—')).join(' / ') || '未选择'

function fmt(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">
      常规压缩（1280px / 质量 0.8）
      <jm-switch v-model="compress" size="small" style="margin-left: 8px" />
    </p>
    <p class="demo-tip">{{ tips }}</p>
    <jm-uploader v-model="basic" :compress="compress" :max-count="2" />
    <p class="demo-tip">压缩后大小：{{ sizes(basic) }}</p>

    <p class="demo-label">
      压到 200KB 以内（compress-target）
      <jm-switch v-model="target" size="small" style="margin-left: 8px" />
    </p>
    <p class="demo-tip">{{ targetTips }}</p>
    <jm-uploader
      v-model="targeted"
      :compress="true"
      :compress-target="target ? TARGET_BYTES : 0"
      :compress-min="30 * 1024"
      :max-count="2"
    />
    <p class="demo-tip">压缩后大小：{{ sizes(targeted) }}（低于 30KB 的原图不压缩）</p>
  </div>
</template>

<style scoped>
.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: -6px 0 10px;
  line-height: 1.6;
}

.demo-label {
  display: flex;
  align-items: center;
  margin-top: 16px;
}
</style>
