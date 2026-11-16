<script setup lang="ts">
import { ref } from 'vue'

const weekend = ref<Date>(new Date(2026, 10, 21))
const readonly = ref<Date>(new Date(2026, 10, 16))

/* 只能选周末：与 min-date / max-date 取并集 */
function disableDate(d: Date) {
  return d.getDay() !== 0 && d.getDay() !== 6
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">自定义禁用（只能选周末）</p>
    <jm-calendar
      v-model="weekend"
      :disable-date="disableDate"
      :show-confirm="false"
      :row-height="54"
    />

    <p class="demo-label">只读（可翻月，不能改选）</p>
    <jm-calendar v-model="readonly" readonly :show-confirm="false" :row-height="54" />
  </div>
</template>
