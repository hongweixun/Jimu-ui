<script setup lang="ts">
import { ref } from 'vue'

const basic = ref(false)
const vertical = ref(false)
const last = ref('')

function onConfirmBasic() {
  last.value = '确认'
  basic.value = false
}

function onCancelBasic() {
  last.value = '取消'
}

function onConfirmVertical() {
  last.value = '已开启提醒'
  vertical.value = false
}

function onCancelVertical() {
  last.value = '暂不开启'
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-row">
      <jm-button type="primary" @click="basic = true">基础对话框</jm-button>
      <jm-button variant="outline" @click="vertical = true">竖排按钮</jm-button>
    </div>

    <p class="demo-note">上一次操作：{{ last || '暂无' }}</p>

    <jm-dialog
      v-model:show="basic"
      title="确认删除"
      message="删除后该课程的所有学习记录将无法恢复，确定继续吗？"
      :teleport="false"
      @confirm="onConfirmBasic"
      @cancel="onCancelBasic"
    />

    <jm-dialog
      v-model:show="vertical"
      title="订阅提醒"
      message="开启后，课程开始前 15 分钟会通过公众号提醒你。"
      confirm-text="立即开启"
      cancel-text="以后再说"
      vertical-actions
      :teleport="false"
      @confirm="onConfirmVertical"
      @cancel="onCancelVertical"
    />
  </div>
</template>
