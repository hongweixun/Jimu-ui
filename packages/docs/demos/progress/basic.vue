<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'

const percent = ref(40)
const auto = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

function play() {
  stop()
  auto.value = 0
  timer = setInterval(() => {
    auto.value += 10
    if (auto.value >= 100) stop()
  }, 400)
}
function stop() {
  if (timer) clearInterval(timer)
  timer = undefined
}
onBeforeUnmount(stop)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（右侧百分比文字）</p>
    <jm-progress :percentage="percent" />

    <p class="demo-label">自定义颜色与粗细</p>
    <jm-progress :percentage="70" color="#FF6430" :stroke-width="10" />
    <jm-progress :percentage="50" color="var(--jm-color-success)" :stroke-width="4" />

    <p class="demo-label">不显示文字 / 置灰</p>
    <jm-progress :percentage="60" :show-text="false" />
    <jm-progress :percentage="30" inactive />

    <p class="demo-label">动画（点击开始，每 400ms +10）</p>
    <jm-progress :percentage="auto" :stroke-width="8" color="var(--jm-color-warning)" />
    <div class="demo-actions">
      <jm-button size="small" @click="play">开始</jm-button>
      <jm-button size="small" @click="stop">暂停</jm-button>
      <jm-button size="small" @click="percent = (percent + 20) % 120">基础 +20</jm-button>
    </div>
  </div>
</template>

<style>
.demo-actions {
  display: flex;
  gap: var(--jm-space-2);
  margin-top: var(--jm-space-2);
}
</style>
