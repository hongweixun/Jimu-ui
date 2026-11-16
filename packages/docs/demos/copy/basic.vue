<script setup lang="ts">
import { ref } from 'vue'
import { vCopy } from 'jimu-ui'

const orderNo = 'JM20261116002'
const status = ref('还没有复制记录')

function onCopy(text: string) {
  status.value = `已复制：${text}`
}
</script>

<template>
  <div class="demo-page">
    <div class="copy-row">
      <span class="copy-label">订单号</span>
      <span class="copy-value">{{ orderNo }}</span>
      <button v-copy="{ text: () => orderNo, onSuccess: onCopy }" class="copy-btn" type="button">
        复制
      </button>
    </div>

    <div class="copy-row">
      <span class="copy-label">邀请码</span>
      <span class="copy-value">EDU-8F3K-2026</span>
      <button v-copy="'EDU-8F3K-2026'" class="copy-btn" type="button">复制</button>
    </div>

    <div v-copy="{ text: '整块都能点：适合优惠券口令、网盘链接', onSuccess: onCopy }" class="copy-block">
      整块区域可复制
      <p class="copy-sub">v-copy 也可以直接挂在 div 上</p>
    </div>

    <p class="demo-tip">{{ status }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.copy-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: var(--jm-radius);
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
}

.copy-label {
  flex: 0 0 auto;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.copy-value {
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
  font-variant-numeric: tabular-nums;
}

.copy-btn {
  flex: 0 0 auto;
  padding: 5px 12px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-text);
  font-size: var(--jm-font-size-sm);
  cursor: pointer;
}

.copy-block {
  padding: 14px;
  border-radius: var(--jm-radius);
  background: var(--jm-bg-container);
  border: 1px dashed var(--jm-border-color);
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

.copy-sub {
  margin-top: 6px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.demo-tip {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-color-primary-text);
}
</style>
