<script setup lang="ts">
import { ref } from 'vue'
import { closeToast, showToast } from 'jimu-ui'

const host = ref<HTMLElement | null>(null)
const log = ref('还没有关闭过提示')

const closedTimes = ref(0)

function customIcon() {
  showToast({
    message: '已加入学习计划',
    icon: 'star',
    target: host.value,
    onClose: () => {
      closedTimes.value += 1
      log.value = `第 ${closedTimes.value} 次提示关闭（自动消失）`
    },
  })
}

function clickToClose() {
  showToast({
    message: '点我立刻关闭',
    icon: 'bell',
    closeOnClick: true,
    duration: 0,
    target: host.value,
    onClose: () => {
      log.value = '手动点击关闭，回调已触发'
    },
  })
}

function withMask() {
  showToast({
    message: '处理中，请稍候…',
    type: 'loading',
    mask: true,
    target: host.value,
    onClose: () => (log.value = 'loading 关闭时也会回调'),
  })
  setTimeout(() => closeToast(), 1600)
}
</script>

<template>
  <div ref="host" class="demo-relative demo-page">
    <div class="demo-row">
      <jm-button size="small" type="primary" @click="customIcon">自定义图标</jm-button>
      <jm-button size="small" @click="clickToClose">点击关闭</jm-button>
      <jm-button size="small" variant="outline" @click="withMask">带遮罩</jm-button>
    </div>

    <p class="state">{{ log }}</p>
    <p class="demo-note">
      <code>onClose</code> 在自动消失、点击关闭、被新提示顶掉时都会触发，适合做「提示结束后再跳转」。
    </p>
  </div>
</template>

<style scoped>
.state {
  margin: 12px 0 0;
  color: var(--jm-text-color-3);
  font-size: 12px;
}

.demo-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
