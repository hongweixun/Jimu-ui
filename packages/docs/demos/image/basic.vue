<script setup lang="ts">
import { ref } from 'vue'

function svg(text: string, from: string, to: string, w = 400, h = 240) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="${w}" height="${h}" fill="url(#g)"/><text x="50%" y="52%" font-family="system-ui,-apple-system,sans-serif" font-size="26" fill="#fff" text-anchor="middle" dominant-baseline="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const wide = svg('宽图 400×240', '#00A0E9', '#2B6BE4')
const square = svg('方图 300×300', '#FF8A3D', '#FF6430', 300, 300)
const vlong = svg('长图 200×420', '#22C55E', '#0E9F6E', 200, 420)
const broken = 'https://example.invalid/not-found.png'

const clicked = ref('')
const visible = ref(0)

const lazyImgs = Array.from({ length: 6 }, (_, i) =>
  svg(`懒加载 ${i + 1}`, ['#7C4DFF', '#00A0E9', '#FF6430', '#22C55E', '#F5A623', '#8E9AAF'][i], ['#4A2ECC', '#0072A8', '#C93F13', '#0E9F6E', '#C97F00', '#5F6B7A'][i], 360, 120),
)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（宽度铺满 + 固定高度）</p>
    <jm-image :src="wide" block height="120" fit="cover" :radius="10" />

    <p class="demo-label">圆形头像 / 圆角卡片</p>
    <div class="demo-row">
      <jm-image :src="square" :width="64" :height="64" round />
      <jm-image :src="square" :width="64" :height="64" :radius="14" />
      <jm-image :src="vlong" :width="64" :height="64" :radius="10" fit="cover" />
    </div>

    <p class="demo-label">三种 fit 对比（100×100 容器内放长图）</p>
    <div class="demo-row">
      <div class="fit-cell">
        <jm-image :src="vlong" :width="100" :height="100" fit="cover" :radius="8" />
        <span>cover</span>
      </div>
      <div class="fit-cell">
        <jm-image :src="vlong" :width="100" :height="100" fit="contain" :radius="8" />
        <span>contain</span>
      </div>
      <div class="fit-cell">
        <jm-image :src="vlong" :width="100" :height="100" fit="fill" :radius="8" />
        <span>fill</span>
      </div>
    </div>

    <p class="demo-label">加载失败占位（可自定义 error 插槽）</p>
    <jm-image :src="broken" :width="120" :height="90" :radius="8" error-text="图片挂了" />

    <p class="demo-label">懒加载（滚动到这里才会真正请求）</p>
    <div class="stack">
      <jm-image v-for="(src, i) in lazyImgs" :key="i" :src="src" lazy block height="64" :radius="8" @load="visible += 1" />
    </div>
    <p class="demo-note">已加载 {{ visible }} / {{ lazyImgs.length }} 张 · 点击图片事件：{{ clicked || '—' }}</p>
    <jm-image :src="wide" :width="140" :height="80" :radius="8" clickable block @click="clicked = '被点击了'" />
  </div>
</template>

<style scoped>
.fit-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--jm-text-color-3);
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
