<script setup lang="ts">
import { ref } from 'vue'

const scroller = ref<HTMLElement | null>(null)
const scroller2 = ref<HTMLElement | null>(null)

const items = Array.from({ length: 30 }, (_, i) => ({
  id: i + 1,
  title: `第 ${i + 1} 条课程通知`,
  desc: `发布于 ${10 + (i % 12)}:${String((i * 7) % 60).padStart(2, '0')} · 教务中心`,
}))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">滚动超过 120px 后出现（容器内定位）</p>
    <div class="scroll-demo">
      <div ref="scroller" class="scroll-demo__body">
        <div v-for="item in items" :key="item.id" class="row">
          <p class="row__title">{{ item.title }}</p>
          <p class="row__desc">{{ item.desc }}</p>
        </div>
      </div>
      <jm-back-top inline :target="scroller" :visibility-height="120" :bottom="16" :offset="16" />
    </div>

    <p class="demo-label">带文字</p>
    <div class="scroll-demo">
      <div ref="scroller2" class="scroll-demo__body">
        <div v-for="item in items" :key="item.id" class="row">
          <p class="row__title">{{ item.title }}</p>
          <p class="row__desc">{{ item.desc }}</p>
        </div>
      </div>
      <jm-back-top
        inline
        :target="scroller2"
        :visibility-height="80"
        text="顶部"
        :bottom="16"
        :offset="16"
      />
    </div>

    <p class="demo-note">
      不传 target 时监听 window，配合页面级滚动使用；传元素则跟随该容器的 scrollTop 判断。
    </p>
  </div>
</template>

<style scoped>
.scroll-demo {
  position: relative;
  height: 200px;
  border-radius: 14px;
  background: var(--jm-bg-input);
  overflow: hidden;
}

.scroll-demo__body {
  height: 100%;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.row {
  padding: 12px 16px;
}

.row + .row {
  border-top: 1px solid var(--jm-border-color);
}

.row__title {
  margin: 0 0 4px;
  font-size: 13px;
  color: var(--jm-text-color);
}

.row__desc {
  margin: 0;
  font-size: 11px;
  color: var(--jm-text-color-3);
}
</style>
