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
  <div class="demo-page cal-demo">
    <section class="cal-card">
      <header class="cal-head">
        <span class="cal-tag">单选</span>
        <div class="cal-head-text">
          <h4 class="cal-title">预约日期</h4>
          <p class="cal-desc">formatter 给指定日期加「可约」标记，备注占数字下方的独立小字行</p>
        </div>
      </header>
      <jm-calendar
        v-model="single"
        :formatter="formatter"
        :row-height="56"
        :show-title="false"
        :show-confirm="false"
      />
      <footer class="cal-result">
        <span>当前选中</span>
        <b>{{ fmt(single) }}</b>
      </footer>
    </section>

    <section class="cal-card">
      <header class="cal-head">
        <span class="cal-tag">区间</span>
        <div class="cal-head-text">
          <h4 class="cal-title">请假时间</h4>
          <p class="cal-desc">type=range：先点起点再点终点，反着点会自动交换</p>
        </div>
      </header>
      <jm-calendar
        v-model="range"
        type="range"
        :row-height="56"
        :show-title="false"
        :show-confirm="false"
      />
      <footer class="cal-result">
        <span>区间</span>
        <b>{{ fmt(range[0]) }} → {{ fmt(range[1]) }}</b>
      </footer>
    </section>

    <section class="cal-card">
      <header class="cal-head">
        <span class="cal-tag is-orange">多选</span>
        <div class="cal-head-text">
          <h4 class="cal-title">上课日</h4>
          <p class="cal-desc">min-date / max-date 限制 11/10 之后可选，再点一次取消选中</p>
        </div>
      </header>
      <jm-calendar
        v-model="multi"
        type="multiple"
        :min-date="new Date(2026, 10, 10)"
        :max-date="new Date(2026, 11, 31)"
        :row-height="56"
        :show-title="false"
        :show-confirm="false"
        color="#FF6430"
      />
      <footer class="cal-result">
        <span>已选</span>
        <b>{{ multi.length }} 天</b>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.cal-demo {
  gap: 14px;
  padding: 14px;
  background: var(--jm-bg-page, #f4f6f9);
}

.cal-card {
  border-radius: 14px;
  background: var(--jm-bg-elevated, #fff);
  box-shadow: var(--jm-shadow-sm, 0 1px 4px rgba(16, 35, 47, 0.06));
  overflow: hidden;
}

.cal-head {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px 8px;
}

.cal-tag {
  flex: 0 0 auto;
  margin-top: 1px;
  padding: 2px 9px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--jm-color-primary) 12%, transparent);
  color: var(--jm-color-primary);
  font-size: 11px;
  line-height: 18px;
  font-weight: var(--jm-font-weight-medium);
}

.cal-tag.is-orange {
  background: rgba(255, 100, 48, 0.12);
  color: #ff6430;
}

.cal-head-text {
  min-width: 0;
}

.cal-title {
  margin: 0;
  color: var(--jm-text-color);
  font-size: 14px;
  font-weight: var(--jm-font-weight-medium);
  line-height: 20px;
}

.cal-desc {
  margin: 2px 0 0;
  color: var(--jm-text-color-3);
  font-size: 11px;
  line-height: 1.5;
}

.cal-result {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 14px;
  border-top: 1px solid var(--jm-border-color, #ebeef0);
  color: var(--jm-text-color-3);
  font-size: 12px;
}

.cal-result b {
  color: var(--jm-text-color);
  font-weight: var(--jm-font-weight-medium);
  font-variant-numeric: tabular-nums;
}
</style>
