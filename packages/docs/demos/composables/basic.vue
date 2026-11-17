<script setup lang="ts">
import { ref } from 'vue'
import {
  useClickOutsideWhen,
  useCountDown,
  useDebounceFn,
  useSwipe,
  useThrottleFn,
} from 'jimu-ui'

/* ---- useCountDown：验证码按钮 ---- */
const { remaining, running, start } = useCountDown(10, {
  onFinish: () => (codeTip.value = '倒计时结束，可以重发了'),
})
const codeTip = ref('点击获取验证码（10 秒演示）')
function sendCode() {
  if (running.value) return
  start(10)
  codeTip.value = '验证码已发送，10s 内不可重发'
}

/* ---- useClickOutsideWhen：点外部收起 ---- */
const panelOpen = ref(false)
const outsideTip = ref('点开面板，再点面板外任意位置收起')
const root = ref<HTMLElement | null>(null)
const trigger = ref<HTMLButtonElement | null>(null)
useClickOutsideWhen(panelOpen, [root, trigger], () => {
  panelOpen.value = false
  outsideTip.value = '已点外部收起'
})
function togglePanel() {
  panelOpen.value = !panelOpen.value
  if (panelOpen.value) outsideTip.value = '面板已打开'
}

/* ---- useSwipe：手势方向 ---- */
const swipeTip = ref('在这个方块上滑一下（超过 30px 才算）')
const dragging = ref(false)
const pad = ref<HTMLElement | null>(null)
const { offsetX, offsetY, direction } = useSwipe(pad, {
  onSwipeStart: () => (dragging.value = true),
  onSwipeEnd: (dir) => {
    dragging.value = false
    swipeTip.value = dir ? `滑动方向：${dir}` : '位移不够，不算滑动'
  },
})

/* ---- 防抖 / 节流 ---- */
const debounceCount = ref(0)
const throttleCount = ref(0)
const clickCount = ref(0)
const debounceLog = useDebounceFn(
  () => {
    debounceCount.value += 1
  },
  { delay: 400 },
)
const throttleLog = useThrottleFn(
  () => {
    throttleCount.value += 1
  },
  { interval: 500 },
)
function rapidClick() {
  clickCount.value += 1
  debounceLog()
  throttleLog()
}
</script>

<template>
  <div class="demo-page">
    <div class="row">
      <button class="btn" type="button" :disabled="running" @click="sendCode">
        {{ running ? `重发（${remaining}s）` : '获取验证码' }}
      </button>
      <p class="tip">{{ codeTip }}</p>
    </div>

    <div ref="root" class="row">
      <button ref="trigger" class="btn" type="button" @click="togglePanel">点外部收起</button>
      <div v-if="panelOpen" class="panel">这是一个面板</div>
      <p class="tip">{{ outsideTip }}</p>
    </div>

    <div
      ref="pad"
      class="pad"
      :class="{ 'is-dragging': dragging }"
      :style="{ transform: `translate(${offsetX}px, ${offsetY}px)` }"
    >
      滑我（{{ direction || '未判定' }}）
    </div>
    <p class="tip">{{ swipeTip }}</p>

    <button class="btn" type="button" @click="rapidClick">连点试试（防抖 vs 节流）</button>
    <p class="tip">
      原始点击 {{ clickCount }} 次 · 防抖只记 {{ debounceCount }} · 节流 {{ throttleCount }}
    </p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.btn {
  padding: 7px 14px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast, #fff);
  font-size: var(--jm-font-size-sm);
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.panel {
  padding: 8px 14px;
  border-radius: var(--jm-radius);
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color);
}

.pad {
  width: 100%;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--jm-radius-lg);
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color-2);
  touch-action: none;
  user-select: none;
  transition: transform 0.2s ease;
}

.pad.is-dragging {
  transition: none;
  box-shadow: inset 0 0 0 2px var(--jm-color-primary);
}

.tip {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-color-primary-text);
}
</style>
