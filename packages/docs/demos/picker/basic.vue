<script setup lang="ts">
import { computed, ref } from 'vue'

/* ---- 日期（三列联动取值） ---- */
const dateVisible = ref(false)
const date = ref<(string | number)[]>(['2026', '11', '15'])

const years = Array.from({ length: 8 }, (_, i) => String(2023 + i))
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const days = computed(() => {
  const y = Number(date.value[0])
  const m = Number(date.value[1])
  const total = new Date(y, m, 0).getDate()
  return Array.from({ length: total }, (_, i) => String(i + 1).padStart(2, '0'))
})

/* ---- 单选（对象选项 + 字段映射） ---- */
const cityVisible = ref(false)
const city = ref<(string | number)[]>(['hz'])
const cities = [
  { code: 'bj', label: '北京' },
  { code: 'sh', label: '上海' },
  { code: 'hz', label: '杭州' },
  { code: 'sz', label: '深圳', disabled: true },
  { code: 'cd', label: '成都' },
]

/* ---- 两列（年级 + 班级） ---- */
const classVisible = ref(false)
const klass = ref<(string | number)[]>(['二年级', '1 班'])
const grades = ['一年级', '二年级', '三年级']
const classes = ['1 班', '2 班', '3 班', '4 班']
</script>

<template>
  <div class="demo-page">
    <jm-cell title="选择日期" :value="date.join('-')" is-link clickable @click="dateVisible = true" />
    <jm-popup v-model:show="dateVisible" position="bottom" round :safe-area="false" :teleport="false">
      <jm-picker
        v-model="date"
        title="选择日期"
        :columns="[years, months, days]"
        @confirm="dateVisible = false"
        @cancel="dateVisible = false"
      />
    </jm-popup>

    <jm-cell title="所在城市" :value="cities.find((c) => c.code === city[0])?.label" is-link clickable @click="cityVisible = true" />
    <jm-popup v-model:show="cityVisible" position="bottom" round :safe-area="false" :teleport="false">
      <jm-picker
        v-model="city"
        title="所在城市"
        :columns="[cities]"
        :columns-field-names="{ text: 'label', value: 'code' }"
        @confirm="cityVisible = false"
        @cancel="cityVisible = false"
      />
    </jm-popup>
    <p class="demo-note">「深圳」被标记为 disabled：拖到它会被吸附到相邻可用项。</p>

    <jm-cell title="年级 / 班级" :value="klass.join(' · ')" is-link clickable @click="classVisible = true" />
    <jm-popup v-model:show="classVisible" position="bottom" round :safe-area="false" :teleport="false">
      <jm-picker
        v-model="klass"
        :columns="[grades, classes]"
        title="班级信息"
        :visible-count="5"
        @confirm="classVisible = false"
        @cancel="classVisible = false"
      />
    </jm-popup>

    <p class="demo-label">直接内嵌使用（不加弹层）</p>
    <div class="inline-picker">
      <jm-picker v-model="klass" :columns="[grades, classes]" :show-toolbar="false" :visible-count="3" :item-height="40" />
    </div>
  </div>
</template>

<style scoped>
.inline-picker {
  border-radius: 12px;
  background: var(--jm-bg-container);
  overflow: hidden;
}
</style>
