<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

/** 复用一小批渐变图：1200 张图不重复造 data URI，省内存 */
function photo(label: string, w: number, h: number, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/>
    </linearGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#g)"/>
    <text x="${w / 2}" y="${h / 2}" font-family="system-ui" font-size="${Math.min(w, h) * 0.16}"
      fill="#ffffff" text-anchor="middle" dominant-baseline="middle" opacity="0.9">${label}</text>
  </svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const colors: Array<[string, string]> = [
  ['#00A0E9', '#2B6BE4'],
  ['#FF8A3D', '#FF5B30'],
  ['#22C55E', '#0E9F6E'],
  ['#7C4DFF', '#4A2ECC'],
  ['#F43F5E', '#BE123C'],
  ['#F59E0B', '#B45309'],
]

const heights = [420, 560, 320, 640, 480, 360, 520, 400, 600, 340, 460, 540]
const seeds = heights.map((h, i) => {
  const [from, to] = colors[i % colors.length]
  return { src: photo(String(i + 1), 360, h, from, to), ratio: h / 360 }
})

const TOTAL = 1200
const photos = Array.from({ length: TOTAL }, (_, i) => {
  const seed = seeds[i % seeds.length]
  return { ...seed, alt: `相册照片 ${i + 1}` }
})

const virtualOn = ref(true)
const mounted = ref(0)
const stage = ref<HTMLElement | null>(null)

let timer = 0
onMounted(() => {
  timer = window.setInterval(() => {
    mounted.value = stage.value?.querySelectorAll('.jm-photo-wall__item').length ?? 0
  }, 250)
})
onBeforeUnmount(() => clearInterval(timer))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">1200 张：虚拟渲染只挂载可视区附近的格子</p>
    <div class="virtual-bar">
      <span>虚拟渲染</span>
      <jm-switch v-model="virtualOn" size="small" />
      <span class="virtual-count">DOM {{ mounted }} / {{ TOTAL }}</span>
    </div>
    <div ref="stage">
      <jm-photo-wall :items="photos" :virtual="virtualOn" :gap="6" :radius="6" />
    </div>
    <p class="demo-tip">
      关掉虚拟渲染后可以对比滚动流畅度：1200 个节点全挂上，滚动明显变沉。
    </p>
  </div>
</template>

<style scoped>
.virtual-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--jm-text-color-2);
  margin-bottom: 8px;
}

.virtual-count {
  margin-left: auto;
  font-variant-numeric: tabular-nums;
  color: var(--jm-text-color-3);
}

.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: 10px 0 0;
}
</style>
