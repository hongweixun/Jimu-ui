<script setup lang="ts">
import { computed, ref } from 'vue'
import type { UploaderFile, UploaderHelpers } from 'jimu-ui'

const auto = ref<(string | UploaderFile)[]>([])
const manual = ref<(string | UploaderFile)[]>([])
const manualRef = ref<{ submit: () => void; retry: (i: number) => void } | null>(null)
const log = ref('还没有文件')

/** 记录每个文件的尝试次数：带 fail 的文件第一次必失败，重试才成功 */
const attempts = new Map<string, number>()

/** 假装上传：每 60ms 涨 8%，带 fail 的第一次失败 */
function fakeUpload(file: File, helpers: UploaderHelpers): Promise<string | void> {
  const tries = (attempts.get(file.name) ?? 0) + 1
  attempts.set(file.name, tries)

  return new Promise((resolve, reject) => {
    let percent = 0
    const timer = setInterval(() => {
      percent = Math.min(100, percent + 8)
      helpers.onProgress(percent)
      if (percent < 100) return
      clearInterval(timer)
      if (file.name.includes('fail') && tries === 1) reject(new Error('网络异常，上传失败'))
      else resolve()
    }, 60)
  })
}

const pendingCount = computed(
  () =>
    manual.value.filter((f) => typeof f === 'object' && (f.status === 'pending' || f.status === 'error'))
      .length,
)

function onSuccess(file: UploaderFile) {
  log.value = `${file.name} 上传成功`
}

function onError(file: UploaderFile, _index: number, reason: unknown) {
  log.value = `${file.name} 失败：${reason instanceof Error ? reason.message : '未知错误'}，点「重试」再试一次`
}

function onManualSuccess(file: UploaderFile) {
  log.value = `${file.name} 手动上传成功`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">自动上传：选完立刻传，进度环走完变完成</p>
    <jm-uploader
      v-model="auto"
      :upload="fakeUpload"
      :max-count="6"
      :preview-teleport="false"
      @success="onSuccess"
      @error="onError"
    />

    <p class="demo-label">手动上传：先攒着，点按钮再提交</p>
    <jm-uploader
      ref="manualRef"
      v-model="manual"
      :upload="fakeUpload"
      :auto-upload="false"
      :max-count="6"
      :preview-teleport="false"
      @success="onManualSuccess"
    />
    <jm-button size="small" type="primary" :disabled="!pendingCount" @click="manualRef?.submit()">
      开始上传（{{ pendingCount }} 个待上传）
    </jm-button>

    <p class="state">{{ log }}</p>
    <p class="demo-note">文件名里带 <code>fail</code> 的文件会被模拟成上传失败，点红色「重试」可以重传。</p>
  </div>
</template>

<style scoped>
.state {
  margin: 10px 0 0;
  padding: 8px 10px;
  border-radius: 8px;
  background: var(--jm-bg-container);
  color: var(--jm-text-color-2);
  font-size: 12px;
  line-height: 1.5;
}
</style>
