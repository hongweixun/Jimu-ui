<script setup lang="ts">
import { computed, ref } from 'vue'

function photo(label: string, w: number, h: number, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/>
    </linearGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#g)"/>
    <text x="${w / 2}" y="${h / 2}" font-family="system-ui" font-size="${Math.min(w, h) * 0.2}"
      fill="#ffffff" text-anchor="middle" dominant-baseline="middle" opacity="0.92">${label}</text>
  </svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const palette: Array<[string, string, number]> = [
  ['#00A0E9', '#2B6BE4', 420],
  ['#FF8A3D', '#FF5B30', 300],
  ['#22C55E', '#0E9F6E', 520],
  ['#7C4DFF', '#4A2ECC', 360],
  ['#F43F5E', '#BE123C', 480],
  ['#F59E0B', '#B45309', 340],
]

const items = ref(
  palette.map(([from, to, h], i) => ({
    src: photo(String(i + 1), 360, h, from, to),
    ratio: h / 360,
    alt: String(i + 1),
  })),
)

const lastSort = ref('')
const orderText = computed(() => items.value.map((i) => i.alt).join(' · '))

function onSort(payload: { from: number; to: number }) {
  lastSort.value = `第 ${payload.from + 1} 张 → 第 ${payload.to + 1} 位`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">长按 0.3 秒拿起，拖动换位，松手落位</p>
    <jm-photo-wall v-model:items="items" sortable :gap="8" @sort="onSort" />

    <div class="state">
      <p>当前顺序：{{ orderText }}</p>
      <p class="state__last">{{ lastSort || '还没有拖动过' }}</p>
    </div>
  </div>
</template>

<style scoped>
.state {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--jm-bg-container);
  color: var(--jm-text-color-2);
  font-size: 12px;
  line-height: 1.6;
}

.state p {
  margin: 0;
}

.state__last {
  color: var(--jm-text-color-3);
}
</style>
