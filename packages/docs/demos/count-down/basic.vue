<script setup lang="ts">
import { ref } from 'vue'

const basic = ref(30 * 60 * 1000)
const card = ref(2 * 3600 * 1000 + 45 * 60 * 1000)
const ms = ref(12 * 1000)

const controlled = ref()
const finished = ref(false)
const cdTime = ref(10 * 1000)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（HH:mm:ss）</p>
    <jm-count-down :time="basic" class="big" />
    <p class="demo-note">传入剩余毫秒数，组件按 format 拆分渲染。</p>

    <p class="demo-label">自定义外观（插槽）</p>
    <jm-count-down :time="card" format="HH:mm:ss">
      <template #default="{ timeData }">
        <span v-if="timeData.days > 0" class="chip">{{ timeData.days }} 天</span>
        <span class="chip">{{ String(timeData.hours).padStart(2, '0') }}</span>
        <span class="sep">:</span>
        <span class="chip">{{ String(timeData.minutes).padStart(2, '0') }}</span>
        <span class="sep">:</span>
        <span class="chip">{{ String(timeData.seconds).padStart(2, '0') }}</span>
      </template>
    </jm-count-down>

    <p class="demo-label">毫秒级</p>
    <jm-count-down :time="ms" format="ss.S" millisecond class="mono" />

    <p class="demo-label">受控：开始 / 暂停 / 重置</p>
    <jm-count-down
      ref="controlled"
      :time="cdTime"
      format="mm:ss"
      :auto-start="false"
      class="big"
      @finish="finished = true"
    />
    <div class="actions">
      <jm-button size="small" type="primary" @click="controlled?.start()">开始</jm-button>
      <jm-button size="small" @click="controlled?.pause()">暂停</jm-button>
      <jm-button size="small" @click="controlled?.reset(); finished = false">重置</jm-button>
    </div>
    <p class="demo-note">{{ finished ? '倒计时已结束（finish 事件）' : '还剩 10 秒，点「开始」试试' }}</p>
  </div>
</template>

<style scoped>
.big {
  font-size: 26px;
  font-weight: 600;
}

.mono {
  font-size: 20px;
}

.chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 26px;
  height: 26px;
  padding: 0 4px;
  border-radius: 6px;
  background: #1f2329;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.sep {
  margin: 0 3px;
  color: var(--jm-text-color-3);
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
</style>
