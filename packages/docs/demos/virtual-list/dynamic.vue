<script setup lang="ts">
import { onMounted, ref } from 'vue'

const TOTAL = 300

const texts = [
  '在的，你说。',
  '老师我把昨天那份实验报告的第三节重写了一遍，您看下这回的推导顺序对不对？之前那版把边界条件放在前面，读起来有点跳。',
  '收到，晚点看。',
  '好',
  '另外想问下，期末大作业允许两个人一组吗？我看通知里只写了「独立完成」，但去年好像是允许组队的。',
  '可以两人一组，提交时在封面写清分工就行。',
  '那太好了，谢谢老师！',
  '对了，第三节那个积分换元的写法我改成了先配方，看着清楚一些，但不确定符不符合课本的记号习惯。',
]

const messages = Array.from({ length: TOTAL }, (_, i) => {
  const mine = i % 3 !== 0
  const text = texts[i % texts.length]
  // 每 7 条塞一张「图片」，制造明显更高的行，检验动态测量
  const hasImage = i % 7 === 3
  return {
    id: i + 1,
    mine,
    text,
    time: `10:${String(i % 60).padStart(2, '0')}`,
    hasImage,
    name: mine ? '我' : '林老师',
  }
})

const listRef = ref<{
  scrollToIndex: (i: number, align?: 'start' | 'center' | 'end') => void
  scrollToBottom: () => void
} | null>(null)

const first = ref(1)
const height = ref(0)

function inspect() {
  const root = document.querySelector('.chat-stage__list')
  const content = root?.querySelector('.jm-virtual-list__content') as HTMLElement | null
  const head = root?.querySelector('.jm-virtual-list__item') as HTMLElement | null
  height.value = content ? Math.round(content.getBoundingClientRect().height) : 0
  first.value = Number(head?.dataset.index ?? 0) + 1
}

// 首屏测量是渲染后异步完成的，挂载后等两帧再读一次，避免 tip 一直显示「—」
onMounted(() => {
  requestAnimationFrame(() => requestAnimationFrame(inspect))
})
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">动态行高：300 条聊天气泡，行高由内容决定</p>
    <div class="chat-stage">
      <jm-virtual-list
        ref="listRef"
        class="chat-stage__list"
        :items="messages"
        dynamic
        :item-height="64"
        :estimated-item-height="64"
        :overscan="4"
        item-key="id"
        @scroll="inspect"
      >
        <template #item="{ item }">
          <div class="msg" :class="{ 'is-mine': item.mine }">
            <span class="msg__avatar">{{ item.mine ? '我' : '林' }}</span>
            <div class="msg__main">
              <p class="msg__meta">{{ item.name }} · {{ item.time }}</p>
              <div class="msg__bubble">
                <p class="msg__text">{{ item.text }}</p>
                <div v-if="item.hasImage" class="msg__image">
                  <span>图片 {{ item.id }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </jm-virtual-list>
    </div>
    <p class="demo-tip">已滚过约第 {{ first }} 条 · 内容总高 {{ height || '—' }} px</p>
    <div class="demo-actions">
      <jm-button size="small" @click="listRef?.scrollToBottom(); requestAnimationFrame(inspect)">跳到最新</jm-button>
      <jm-button size="small" @click="listRef?.scrollToIndex(150, 'center'); requestAnimationFrame(inspect)">
        第 151 条居中
      </jm-button>
    </div>
  </div>
</template>

<style scoped>
.chat-stage {
  height: 300px;
  border: 1px solid var(--jm-border-color-2);
  border-radius: var(--jm-radius-md);
  overflow: hidden;
  background: var(--jm-bg-container);
}

.chat-stage__list {
  height: 100%;
}

.msg {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  align-items: flex-start;
}

.msg.is-mine {
  flex-direction: row-reverse;
}

.msg__avatar {
  flex: 0 0 auto;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 12px;
}

.msg__main {
  min-width: 0;
  max-width: 76%;
}

.msg.is-mine .msg__main {
  text-align: right;
}

.msg__meta {
  margin: 0 0 3px;
  font-size: 11px;
  color: var(--jm-text-color-3);
}

.msg__bubble {
  display: inline-block;
  padding: 7px 10px;
  border-radius: 10px 10px 10px 2px;
  background: var(--jm-bg-page);
  text-align: left;
}

.msg.is-mine .msg__bubble {
  border-radius: 10px 10px 2px 10px;
  background: var(--jm-color-primary-light);
}

.msg__text {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  color: var(--jm-text-color);
  white-space: pre-wrap;
}

.msg__image {
  margin-top: 6px;
  height: 72px;
  border-radius: 6px;
  background: linear-gradient(135deg, #cfe9f7, #a9d8f0);
  color: #4a7f9c;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-tip {
  font-size: 12px;
  color: var(--jm-text-color-3);
  margin: 8px 0 0;
}

.demo-actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}
</style>
