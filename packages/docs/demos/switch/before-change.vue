<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const on = ref(false)
const pending = ref(false)

/** 模拟「开通前先调接口」：900ms 后放行，期间开关自己转圈 */
function beforeChange(next: boolean) {
  if (!next) return true
  pending.value = true
  return new Promise<boolean>((resolve) => {
    setTimeout(() => {
      pending.value = false
      showToast('已开通，扣费 9.9 元')
      resolve(true)
    }, 900)
  })
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">开通前先调接口</p>
    <div class="demo-row">
      <jm-switch v-model="on" :before-change="beforeChange" />
      <span class="demo-note">会员免广告：{{ on ? '已开通' : '未开通' }}</span>
    </div>

    <p class="demo-label">拦截：余额不足时不允许关闭</p>
    <div class="demo-row">
      <jm-switch :model-value="true" :before-change="(next: boolean) => next || showToast('还有 3 节课未上完，暂不能关闭')" />
      <span class="demo-note">课程提醒</span>
    </div>

    <p class="demo-note">
      接口失败时抛错或返回 false 即可，开关状态不会变；pending 期间点击无效，避免重复提交。
    </p>
  </div>
</template>
