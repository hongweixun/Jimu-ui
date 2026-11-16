<script setup lang="ts">
import { ref } from 'vue'
import { vLongpress } from 'jimu-ui'

const tip = ref('长按下面的卡片试试')
const pressing = ref(false)

/* 注意：长按回调在计时器里触发，事件早已结束——不要读 e.currentTarget，
   从宿主拿信息要么闭包要么在这里只做动作本身 */
function onLongPress() {
  tip.value = `已长按「书架卡片」— ${new Date().toLocaleTimeString()}`
}
function onLongPressSlow() {
  tip.value = `已长按「慢速卡片」— ${new Date().toLocaleTimeString()}`
}
</script>

<template>
  <div class="demo-page">
    <div
      v-longpress="{ onLongPress, onStart: () => (pressing = true), onEnd: () => (pressing = false), duration: 500 }"
      data-name="书架卡片"
      class="lp-card"
      :class="{ 'is-pressing': pressing }"
    >
      长按我（500ms）
      <p class="lp-sub">移动手指或提前松手都会取消</p>
    </div>

    <div
      v-longpress="{ onLongPress: onLongPressSlow, duration: 1200 }"
      class="lp-card lp-card--alt"
    >
      长按我（1200ms）
      <p class="lp-sub">duration 可调，慢一点的适合"危险操作确认"</p>
    </div>

    <p class="demo-tip">{{ tip }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 12px;
}

.lp-card {
  padding: 16px;
  border-radius: var(--jm-radius-lg);
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  user-select: none;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.lp-card.is-pressing {
  transform: scale(0.97);
  box-shadow: inset 0 0 0 2px var(--jm-color-primary);
}

.lp-card--alt {
  background: var(--jm-color-warning-bg, #fff7e6);
}

.lp-sub {
  margin-top: 6px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.demo-tip {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-color-primary-text);
}
</style>
