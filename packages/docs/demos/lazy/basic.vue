<script setup lang="ts">
import { ref } from 'vue'
import { vLazy } from 'jimu-ui'

function svg(text: string, from: string, to: string, w = 400, h = 200) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="${w}" height="${h}" fill="url(#g)"/><text x="50%" y="52%" font-family="system-ui,-apple-system,sans-serif" font-size="24" fill="#fff" text-anchor="middle" dominant-baseline="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const courses = [
  { id: 1, title: '第 1 讲 · 环境搭建', src: svg('第 1 讲', '#00A0E9', '#2B6BE4'), loaded: false },
  { id: 2, title: '第 2 讲 · 模板语法', src: svg('第 2 讲', '#7C5CFF', '#5C3BE4'), loaded: false },
  { id: 3, title: '第 3 讲 · 响应式原理', src: svg('第 3 讲', '#22C55E', '#0E9F6E'), loaded: false },
  { id: 4, title: '第 4 讲 · 组件通信', src: svg('第 4 讲', '#FF8A3D', '#FF6430'), loaded: false },
  { id: 5, title: '第 5 讲 · 插槽体系', src: svg('第 5 讲', '#F43F5E', '#D9264D'), loaded: false },
  { id: 6, title: '第 6 讲 · 组合式函数', src: svg('第 6 讲', '#14B8A6', '#0E8F85'), loaded: false },
]

const commentsVisible = ref(false)
const commentCount = ref(0)

function loadComments() {
  commentsVisible.value = true
  commentCount.value = 42
}
</script>

<template>
  <div class="demo-page">
    <p class="lazy-intro">图片滚进视口（提前 200px）才真正加载，加载完成淡入。</p>

    <div v-for="c in courses" :key="c.id" class="course-card">
      <img v-lazy="{ src: c.src, onLoad: () => (c.loaded = true) }" class="course-img" alt="" />
      <div class="course-info">
        <p class="course-title">{{ c.title }}</p>
        <p class="course-state">{{ c.loaded ? '已加载' : '未加载' }}</p>
      </div>
    </div>

    <div v-lazy="{ onVisible: loadComments }" class="comment-zone">
      <template v-if="commentsVisible">
        <p class="comment-title">课堂讨论（{{ commentCount }} 条）</p>
        <p class="comment-item">王同学：老师，第 3 讲的响应式可以再讲一遍吗？</p>
        <p class="comment-item">李同学：笔记已下载，讲得很细。</p>
      </template>
      <p v-else class="comment-pending">继续往下滚，评论区才加载…</p>
    </div>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.lazy-intro {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.course-card {
  display: flex;
  gap: 12px;
  padding: 10px;
  border-radius: var(--jm-radius);
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
}

.course-img {
  flex: 0 0 auto;
  width: 108px;
  height: 64px;
  border-radius: 6px;
  object-fit: cover;
  background: var(--jm-bg-secondary, #eee);
}

.course-info {
  flex: 1 1 auto;
  min-width: 0;
}

.course-title {
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

.course-state {
  margin-top: 4px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-4);
}

.comment-zone {
  padding: 14px;
  border-radius: var(--jm-radius);
  background: var(--jm-bg-container);
  border: 1px dashed var(--jm-border-color);
}

.comment-title {
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color);
}

.comment-item {
  margin-top: 8px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
}

.comment-pending {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-4);
}
</style>
