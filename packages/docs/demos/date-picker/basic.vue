<script setup lang="ts">
import { computed, ref } from 'vue'

/* 1. 日期：常用形态，弹层里打开 */
const dateShow = ref(false)
const dateValue = ref<string[]>(['2026', '11', '18'])
const dateText = computed(() => dateValue.value.join('-'))

/* 2. 年月：只有两列 */
const monthShow = ref(false)
const monthValue = ref<string[]>(['2026', '11'])

/* 3. 日期时间：五列，直接内嵌展示 */
const datetime = ref<string[]>(['2026', '11', '20', '09', '30'])
const datetimeText = computed(() => {
  const [y, m, d, h, mi] = datetime.value
  return `${y}-${m}-${d} ${h}:${mi}`
})

/* 4. 时间 + 自定义文案 */
const time = ref<string[]>(['14', '00'])
const timeText = computed(() => time.value.join(':'))

const pad = (n: number) => String(n).padStart(2, '0')
function customFormatter(type: 'year' | 'month' | 'day' | 'hour' | 'minute', value: string) {
  if (type === 'hour') return `${pad(Number(value))} 点`
  if (type === 'minute') return `${pad(Number(value))} 分`
  return value
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">日期（弹层）</p>
    <jm-cell title="上课日期" :value="dateText" is-link clickable @click="dateShow = true" />
    <jm-popup v-model:show="dateShow" position="bottom" round :safe-area="false" :teleport="false">
      <jm-date-picker
        v-model="dateValue"
        type="date"
        title="选择日期"
        :min-date="new Date(2026, 0, 1)"
        :max-date="new Date(2026, 11, 31)"
        @confirm="dateShow = false"
        @cancel="dateShow = false"
      />
    </jm-popup>
    <p class="demo-note">限制在 2026 年内：范围外的月份、日期会置灰并自动跳过。</p>

    <p class="demo-label">年月</p>
    <jm-cell title="账单月份" :value="monthValue.join('-')" is-link clickable @click="monthShow = true" />
    <jm-popup v-model:show="monthShow" position="bottom" round :safe-area="false" :teleport="false">
      <jm-date-picker
        v-model="monthValue"
        type="year-month"
        title="选择月份"
        @confirm="monthShow = false"
        @cancel="monthShow = false"
      />
    </jm-popup>

    <p class="demo-label">日期时间（内嵌，五列）</p>
    <div class="card">
      <jm-date-picker v-model="datetime" type="datetime" title="到校时间" />
    </div>
    <p class="demo-note">当前：{{ datetimeText }}</p>

    <p class="demo-label">时间 + formatter</p>
    <div class="card">
      <jm-date-picker
        v-model="time"
        type="time"
        title="上课时间"
        :formatter="customFormatter"
        :visible-count="3"
      />
    </div>
    <p class="demo-note">当前：{{ timeText }}</p>
  </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
  overflow: hidden;
}
</style>
