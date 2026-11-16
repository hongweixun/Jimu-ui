<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const pwd = ref('')
const plain = ref('')
const pwd2 = ref('')
const status = ref('')

function onComplete(value: string) {
  status.value = `已输入 ${value.length} 位，正在校验…`
  setTimeout(() => {
    showToast(value === '123456' ? '密码正确' : '密码错误，请重试')
    status.value = value === '123456' ? '校验通过' : '校验失败'
  }, 400)
}

function reset() {
  pwd.value = ''
  status.value = ''
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">密码输入（6 位，内置数字键盘）</p>
    <jm-password-input v-model="pwd" :length="6" keyboard-title="请输入支付密码" :teleport="false" @complete="onComplete" />
    <p class="demo-note">{{ status || '点击格子唤起键盘，输满 6 位触发 complete' }}</p>
    <div class="actions">
      <jm-button size="small" @click="reset">清空</jm-button>
    </div>

    <p class="demo-label">格子间距 + 明文</p>
    <jm-password-input v-model="plain" :length="4" :gutter="10" :mask="false" :show-keyboard="false" />
    <p class="demo-note">关掉内置键盘（show-keyboard=false）时，用键盘输入也能录入数字。</p>

    <p class="demo-label">连体样式（默认）</p>
    <jm-password-input v-model="pwd2" :length="6" :auto-close="true" :teleport="false" />
  </div>
</template>

<style scoped>
.actions {
  margin-top: 10px;
}
</style>
