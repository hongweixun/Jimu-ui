<script setup lang="ts">
import { ref } from 'vue'

const sizes = ['small', 'medium', 'large'] as const
const wrap = ref(true)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">横向默认间距</p>
    <jm-space>
      <jm-button size="small">取消</jm-button>
      <jm-button size="small" type="primary">确定</jm-button>
      <jm-button size="small" plain>稍后</jm-button>
    </jm-space>

    <p class="demo-label">竖向排列</p>
    <jm-space direction="vertical" align="start" size="small">
      <jm-tag>一年级</jm-tag>
      <jm-tag type="success" plain>已完成</jm-tag>
      <jm-tag type="warning" plain>待审核</jm-tag>
    </jm-space>

    <p class="demo-label">预设间距 small / medium / large</p>
    <jm-space v-for="s in sizes" :key="s" :size="s" class="line">
      <span class="box">{{ s }}</span>
      <span class="box">间距 {{ s }}</span>
    </jm-space>

    <p class="demo-label">两端对齐 + 自定义 [横向, 纵向] 间距</p>
    <div class="card">
      <jm-space justify="between">
        <span class="label">本月课时</span>
        <span class="value">32 节</span>
      </jm-space>
      <jm-space justify="between">
        <span class="label">剩余课包</span>
        <span class="value">6 节</span>
      </jm-space>
    </div>

    <p class="demo-label">自动换行（标签流）</p>
    <jm-space :size="[8, 8]" :wrap="wrap">
      <jm-tag v-for="n in 10" :key="n" plain>科目 {{ n }}</jm-tag>
    </jm-space>
  </div>
</template>

<style scoped>
.line {
  margin-bottom: 8px;
}

.box {
  padding: 6px 10px;
  border-radius: 8px;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 12px;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--jm-bg-container);
}

.label {
  font-size: 14px;
  color: var(--jm-text-secondary);
}

.value {
  font-size: 14px;
  color: var(--jm-text-primary);
}
</style>
