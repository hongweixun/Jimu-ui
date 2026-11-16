<script setup lang="ts">
import { ref } from 'vue'
import type { CalendarDay } from 'jimu-ui'

const single = ref<Date>(new Date(2026, 10, 20))
const range = ref<Date[]>([new Date(2026, 10, 14), new Date(2026, 10, 18)])

/* 给部分日期加下方备注：数字与区间带必须保持对齐 */
function formatter(day: CalendarDay) {
  if (day.type !== 'current') return undefined
  if (day.day === 18) return { bottomInfo: '已满' }
  if (day.day % 7 === 0) return { bottomInfo: '名额紧张' }
  return undefined
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">方形选中（整格色块，TDesign 风格）</p>
    <jm-calendar
      v-model="single"
      shape="square"
      title="预约日期"
      :row-height="62"
      :formatter="formatter"
      :show-confirm="false"
    />

    <p class="demo-label">方形 + 区间 + 备注（数字与色带始终对齐）</p>
    <jm-calendar
      v-model="range"
      type="range"
      shape="square"
      title="请假时间"
      :row-height="62"
      :formatter="formatter"
      :show-confirm="false"
    />
    <p class="demo-note">备注文字绝对定位在格子上下缘，不会把数字挤偏</p>
  </div>
</template>
