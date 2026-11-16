<script setup lang="ts">
import { ref } from 'vue'

const single = ref(36)
const range = ref<[number, number]>([24, 76])
const stepped = ref(40)
const disabled = ref(30)
const custom = ref(3)

const priceLabel = (v: number) => `${v}00 元`
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：{{ single }}</p>
    <jm-slider v-model="single" />

    <p class="demo-label">双滑块：{{ range[0] }} ~ {{ range[1] }}</p>
    <jm-slider v-model="range" show-tooltip />

    <p class="demo-label">步长 10（对齐刻度）</p>
    <jm-slider v-model="stepped" :step="10" />
    <div class="ticks">
      <span v-for="n in [0, 20, 40, 60, 80, 100]" :key="n">{{ n }}</span>
    </div>

    <p class="demo-label">禁用 / 自定义颜色</p>
    <jm-slider v-model="disabled" disabled />
    <jm-slider v-model="custom" :min="1" :max="5" :step="1" active-color="#1D9E75" :format="priceLabel" show-tooltip />
    <p class="demo-note">当前值：{{ custom }}（format 只影响气泡文案，不改值）</p>

    <p class="demo-label">小尺寸</p>
    <jm-slider v-model="single" :bar-height="2" :button-size="14" />
  </div>
</template>

<style scoped>
.ticks {
  display: flex;
  justify-content: space-between;
  padding: 4px 10px 0;
  font-size: 11px;
  color: var(--jm-text-tertiary);
}
</style>
