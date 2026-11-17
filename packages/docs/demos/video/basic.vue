<script setup lang="ts">
import { ref } from 'vue'

/* CC0 测试视频，实际项目替换成自己的资源 */
const src = 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4'

function svg(text: string, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="640" height="360" fill="url(#g)"/><text x="50%" y="50%" font-family="system-ui,-apple-system,sans-serif" font-size="30" fill="#fff" text-anchor="middle" dominant-baseline="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const poster = svg('视频封面 · 16:9', '#1F2A44', '#0B1220')
const poster2 = svg('进视口自动播放', '#134E4A', '#0B1220')

const progress = ref(0)
const duration = ref(0)

function onTimeUpdate(t: number, d: number) {
  progress.value = d ? Math.round((t / d) * 100) : 0
  duration.value = Math.round(d)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：封面 + 原生控制条（preload=none，滚动到才拉数据）</p>
    <jm-video :src="src" :poster="poster" :radius="12" />

    <p class="demo-label">进视口自动播放（静音）· 离开视口自动暂停</p>
    <jm-video
      :src="src"
      :poster="poster2"
      play-in-view
      :controls="false"
      loop
      :radius="12"
      @timeupdate="onTimeUpdate"
    />
    <p class="demo-note">
      muted 静音轮播：滚出屏幕立即暂停、切后台也会暂停，不会出现「划走了还在播」；
      进度 {{ progress }}% / 总长约 {{ duration }}s（500ms 节流回调）。
    </p>

    <div class="spacer"></div>

    <p class="demo-tip">
      性能要点：默认 preload=none 懒加载；playInView 走 IntersectionObserver，一屏内多个视频只有可见的在播；
      自动播放强制 muted（浏览器策略），页面隐藏时统一暂停。
    </p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 12px;
}

.spacer {
  height: 420px;
}

.demo-note,
.demo-tip {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
  line-height: 1.6;
}
</style>
