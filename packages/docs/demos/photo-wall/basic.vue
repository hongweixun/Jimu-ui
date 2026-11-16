<script setup lang="ts">
import { ref } from 'vue'

/** 造一张带尺寸的渐变图，方便演示瀑布流的不同高度 */
function photo(label: string, w: number, h: number, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/>
    </linearGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#g)"/>
    <circle cx="${w * 0.78}" cy="${h * 0.22}" r="${Math.min(w, h) * 0.14}" fill="#ffffff" opacity="0.22"/>
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
  ['#06B6D4', '#0E7490'],
  ['#8B5CF6', '#6D28D9'],
]

// 高度各不相同，瀑布流才有错落感
const heights = [420, 560, 320, 640, 480, 360, 520, 400, 600, 340, 460, 540]

const photos = heights.map((h, i) => {
  const [from, to] = colors[i % colors.length]
  return {
    src: photo(String(i + 1), 360, h, from, to),
    // 第 5 张故意不给 ratio，演示「图片加载后自动测量」的兜底
    ...(i === 4 ? {} : { ratio: h / 360 }),
    alt: `示例照片 ${i + 1}`,
  }
})

const wide = ref(photos.slice(0, 6))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">瀑布流 + 响应式（默认按 150px 列宽推算，手机框内是 2 列）</p>
    <jm-photo-wall :items="photos" :gap="8" :radius="10" />

    <p class="demo-label">列宽基准改成 96px，同一个组件自动变 3 列</p>
    <jm-photo-wall :items="wide" :column-width="96" :gap="6" :radius="6" />
  </div>
</template>
