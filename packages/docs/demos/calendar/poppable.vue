<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const showRange = ref(false)

const single = ref<Date>(new Date())
const range = ref<Date[]>([])

const fmt = (d?: Date) =>
  d ? `${d.getMonth() + 1}月${d.getDate()}日` : '未选择'
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="show = true">选择日期（底部弹出）</jm-button>
    <jm-button block @click="showRange = true">选择请假区间</jm-button>

    <jm-calendar
      v-model:show="show"
      v-model="single"
      poppable
      title="请选择日期"
      :teleport="false"
      confirm-text="确认"
    />

    <jm-calendar
      v-model:show="showRange"
      v-model="range"
      poppable
      type="range"
      title="请假时间"
      :teleport="false"
      confirm-text="确认"
      :min-date="new Date(2026, 10, 1)"
      :max-date="new Date(2027, 11, 31)"
    />

    <p class="demo-note">
      弹出模式（poppable）：从底部滑出、遮罩可关、确认后自动收起。
      日期区上下滑动即可连续翻月——本例区间日历限定了 2026-11 ~ 2027-12，可以一路滚到明年。
    </p>
    <p class="demo-note">当前选择：{{ fmt(single) }}；区间：{{ range.length === 2 ? `${fmt(range[0])} → ${fmt(range[1])}` : '未选择' }}</p>
  </div>
</template>
