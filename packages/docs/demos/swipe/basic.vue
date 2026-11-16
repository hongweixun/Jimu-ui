<script setup lang="ts">
import { ref } from 'vue'

const slides = [
  { id: 1, title: '秋季课程上新', desc: '小学语文 · 阅读理解专项', bg: 'linear-gradient(135deg, #00A0E9, #2B6BE4)' },
  { id: 2, title: '限时优惠', desc: '两科联报立减 200 元', bg: 'linear-gradient(135deg, #FF8A3D, #FF6430)' },
  { id: 3, title: '名师直播', desc: '今晚 19:30 准时开讲', bg: 'linear-gradient(135deg, #22C55E, #0E9F6E)' },
]

const notices = [
  '系统将于今晚 23:00 维护升级',
  '新版作业批改已上线，支持语音点评',
  '本月新增 12 门精品课程',
]

const current = ref(0)
const verticalIndex = ref(0)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">循环 + 自动播放（当前第 {{ current + 1 }} 张）</p>
    <jm-swipe :autoplay="3000" loop height="150" :radius="12" @change="(i) => (current = i)">
      <div v-for="s in slides" :key="s.id" class="slide" :style="{ background: s.bg }">
        <strong class="slide__title">{{ s.title }}</strong>
        <span class="slide__desc">{{ s.desc }}</span>
      </div>
    </jm-swipe>
    <p class="demo-note">自动播放会在手指按下时暂停、抬起后恢复；循环靠首尾克隆页实现无缝。</p>

    <p class="demo-label">非循环（拖到两端有阻尼回弹）</p>
    <jm-swipe height="120" :autoplay="false" indicator-active-color="#00A0E9" indicator-color="rgba(0,0,0,0.15)">
      <div v-for="s in slides.slice(0, 2)" :key="s.id" class="slide" :style="{ background: s.bg }">
        <strong class="slide__title">{{ s.title }}</strong>
      </div>
    </jm-swipe>

    <p class="demo-label">纵向轮播（当前第 {{ verticalIndex + 1 }} 条通知）</p>
    <jm-swipe
      vertical
      loop
      :autoplay="2500"
      height="44"
      indicator-position="top"
      :show-indicators="false"
      class="notice-swipe"
      @change="(i) => (verticalIndex = i)"
    >
      <div v-for="n in notices" :key="n" class="notice">
        <span class="notice__dot" />
        {{ n }}
      </div>
    </jm-swipe>
  </div>
</template>

<style scoped>
.slide {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 6px;
  height: 100%;
  padding: 0 20px;
  color: #fff;
}

.slide__title {
  font-size: 18px;
  font-weight: 600;
}

.slide__desc {
  font-size: 13px;
  opacity: 0.85;
}

.notice-swipe {
  border-radius: 10px;
  background: var(--jm-bg-container);
}

.notice {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 100%;
  padding: 0 14px;
  font-size: 13px;
  color: var(--jm-text-color-2);
}

.notice__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--jm-color-warning);
  flex: 0 0 auto;
}
</style>
