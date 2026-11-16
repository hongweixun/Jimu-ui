<script setup lang="ts">
import { ref } from 'vue'

const month = ref<Date>(new Date(2026, 10, 16))
const ym = ref<Date>(new Date(2026, 5, 12))
const shown = ref('')

function onMonthChange(d: Date) {
  shown.value = `${d.getFullYear()}年${d.getMonth() + 1}月`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">点标题选月份（switch-mode="month"）</p>
    <jm-calendar
      v-model="month"
      switch-mode="month"
      title="选择月份"
      :show-confirm="false"
      :row-height="54"
      @month-change="onMonthChange"
    />
    <p class="demo-note">当前展示：{{ shown || '—' }}</p>

    <p class="demo-label">点标题选年月（switch-mode="year-month"）</p>
    <jm-calendar
      v-model="ym"
      switch-mode="year-month"
      title="选择年月"
      :show-confirm="false"
      :row-height="54"
    />
    <p class="demo-note">面板年份范围跟随 min-date / max-date，未传则当前年 ±10 年</p>
  </div>
</template>
