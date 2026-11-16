<script setup lang="ts">
import { ref } from 'vue'

const online = ref(1286)
const score = ref(92.5)
const rate = ref(86.4)

function refresh() {
  online.value = 1000 + Math.floor(Math.random() * 1000)
  score.value = Number((70 + Math.random() * 30).toFixed(1))
  rate.value = Number((50 + Math.random() * 50).toFixed(1))
}
</script>

<template>
  <div class="demo-page">
    <div class="grid">
      <jm-statistic title="当前在线" :value="online" suffix="人" />
      <jm-statistic title="平均分" :value="score" :precision="1" size="lg" color="#00A0E9" />
      <jm-statistic title="完课率" :value="rate" :precision="1" suffix="%" size="sm">
        <template #prefix>≈</template>
      </jm-statistic>
    </div>

    <jm-button block @click="refresh">换一组数据（看滚动动画）</jm-button>

    <p class="demo-label">金额与千分位</p>
    <jm-statistic :value="1234567.891" :precision="2" prefix="¥" suffix="元" />

    <p class="demo-label">非数字内容原样展示</p>
    <jm-statistic title="本月奖励" value="—" />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.grid > :first-child {
  grid-column: span 2;
}
</style>
