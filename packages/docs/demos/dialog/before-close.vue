<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const mode = ref<'async' | 'reject'>('async')
const last = ref('')

/** 返回 Promise 期间按钮自己转圈，返回 false 则这次点击不生效 */
function beforeClose() {
  if (mode.value === 'reject') return false
  return new Promise<boolean>((resolve) => {
    setTimeout(() => resolve(true), 900)
  })
}

function onConfirm() {
  last.value = '已提交'
  show.value = false
}

function onCancel() {
  last.value = '已取消'
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-row">
      <jm-tag
        :type="mode === 'async' ? 'primary' : 'default'"
        :plain="mode !== 'async'"
        @click="mode = 'async'"
        >异步提交</jm-tag
      >
      <jm-tag
        :type="mode === 'reject' ? 'primary' : 'default'"
        :plain="mode !== 'reject'"
        @click="mode = 'reject'"
        >拦截关闭</jm-tag
      >
    </div>

    <jm-button type="primary" block @click="show = true">提交作业</jm-button>
    <p class="demo-note">
      当前模式：{{ mode === 'async' ? 'beforeClose 900ms 后放行，按钮转圈' : 'beforeClose 返回 false，弹窗不关' }}；上一次结果：{{ last || '暂无' }}
    </p>

    <jm-dialog
      v-model:show="show"
      title="提交作业"
      message="提交后不能修改，确认现在提交吗？"
      confirm-text="提交"
      :before-close="beforeClose"
      :teleport="false"
      @confirm="onConfirm"
      @cancel="onCancel"
    />
  </div>
</template>
