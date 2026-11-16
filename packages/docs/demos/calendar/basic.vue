<script setup lang="ts">
import { ref } from 'vue'
import type { CalendarDay } from 'jimu-ui'

/* 1. 单选 + 逐日定制 */
const single = ref<Date>(new Date(2026, 10, 18))
const markDays = [3, 8, 15, 22, 26]
function formatter(day: CalendarDay) {
  if (day.type === 'current' && markDays.includes(day.day)) {
    return { bottomInfo: '可约' }
  }
  return undefined
}

/* 2. 区间 */
const range = ref<Date[]>([new Date(2026, 10, 10), new Date(2026, 10, 14)])

/* 3. 多选 */
const multi = ref<Date[]>([new Date(2026, 10, 5)])

const fmt = (d?: Date) => (d ? `${d.getMonth() + 1}/${d.getDate()}` : '—')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">单选（formatter 给指定日期加「可约」标记）</p>
    <jm-calendar v-model="single" title="预约日期" :formatter="formatter" :row-height="58" />
    <p class="demo-note">当前选中：{{ fmt(single) }}</p>

    <p class="demo-label">日期区间</p>
    <jm-calendar v-model="range" type="range" title="请假时间" :show-confirm="false" :row-height="54" />
    <p class="demo-note">区间：{{ fmt(range[0]) }} → {{ fmt(range[1]) }}</p>

    <p class="demo-label">多选 + 限制可选范围（10 号之后）</p>
    <jm-calendar
      v-model="multi"
      type="multiple"
      title="上课日"
      :min-date="new Date(2026, 10, 10)"
      :max-date="new Date(2026, 11, 31)"
      :show-confirm="false"
      :row-height="54"
      color="#FF6430"
    />
    <p class="demo-note">已选 {{ multi.length }} 天</p>
  </div>
</template>
