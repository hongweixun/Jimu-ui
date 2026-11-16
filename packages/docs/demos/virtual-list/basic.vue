<script setup lang="ts">
import { ref } from 'vue'

const TOTAL = 2000
const HEIGHT = 56

const items = Array.from({ length: TOTAL }, (_, i) => ({
  id: i + 1,
  title: `联系人 #${i + 1}`,
  desc: ['北京 · 朝阳区', '上海 · 浦东新区', '深圳 · 南山区', '杭州 · 西湖区'][i % 4],
}))

const listRef = ref<{ scrollToIndex: (i: number) => void } | null>(null)
const current = ref(0)

function onScroll(offsetTop: number) {
  current.value = Math.floor(offsetTop / HEIGHT)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">2000 行固定行高虚拟滚动（只渲染可视区 + buffer）</p>
    <div class="scroll-stage">
      <jm-virtual-list
        ref="listRef"
        :items="items"
        :item-height="HEIGHT"
        class="scroll-stage__list"
        @scroll="onScroll"
      >
        <template #item="{ item }">
          <div class="row">
            <span class="row__avatar">{{ item.id }}</span>
            <div class="row__body">
              <p class="row__title">{{ item.title }}</p>
              <p class="row__desc">{{ item.desc }}</p>
            </div>
          </div>
        </template>
      </jm-virtual-list>
    </div>
    <p class="demo-tip">当前首行：{{ current + 1 }} / {{ TOTAL }}</p>
    <jm-button size="small" style="margin-top: 4px" @click="listRef?.scrollToIndex(1500)">
      跳到第 1501 行
    </jm-button>
  </div>
</template>

<style scoped>
.scroll-stage {
  height: 280px;
  border: 1px solid var(--jm-border-color-2);
  border-radius: var(--jm-radius-md);
  overflow: hidden;
  background: var(--jm-bg-container);
}

.scroll-stage__list {
  height: 100%;
}

.row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 12px;
  border-bottom: 1px solid var(--jm-border-color-1);
}

.row__avatar {
  flex: 0 0 auto;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 12px;
  font-weight: 600;
}

.row__body {
  min-width: 0;
}

.row__title {
  font-size: 14px;
  margin: 0;
}

.row__desc {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: 2px 0 0;
}

.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: 8px 0 0;
}
</style>
