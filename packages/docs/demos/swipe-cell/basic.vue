<script setup lang="ts">
import { ref } from 'vue'

const messages = ref([
  { id: 1, title: '作业批改提醒', desc: '三年级二班 32 份作业待批改', time: '10:24' },
  { id: 2, title: '调课申请', desc: '王老师申请把周四第 3 节调到周五', time: '09:12' },
  { id: 3, title: '家长留言', desc: '李明的家长：孩子今天请假', time: '昨天' },
])

const snapshot = ref('')

function remove(id: number) {
  messages.value = messages.value.filter((m) => m.id !== id)
  snapshot.value = `已删除第 ${id} 条`
}

function mark(id: number) {
  snapshot.value = `已标记第 ${id} 条`
}

const first = ref<{ open: (s: 'left' | 'right') => void; close: () => void }>()
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">左滑露出删除按钮（点内容区之外可收起）</p>
    <div class="list">
      <jm-swipe-cell v-for="m in messages" :key="m.id">
        <jm-cell :title="m.title" :label="`${m.desc} · ${m.time}`" />
        <template #right>
          <button class="btn btn--danger" type="button" @click="remove(m.id)">删除</button>
        </template>
      </jm-swipe-cell>
    </div>
    <p class="demo-note">{{ snapshot || '试着向左滑动某一条' }}</p>

    <p class="demo-label">两侧按钮 + 编程控制</p>
    <jm-swipe-cell ref="first">
      <jm-cell title="点击右侧按钮查看效果" label="左侧「标记」，右侧「删除」「归档」" />
      <template #left>
        <button class="btn" type="button" @click="mark(1)">标记</button>
      </template>
      <template #right>
        <button class="btn btn--warning" type="button" @click="snapshot = '已归档'">归档</button>
        <button class="btn btn--danger" type="button" @click="snapshot = '已删除'">删除</button>
      </template>
    </jm-swipe-cell>
    <jm-space class="ops" :size="8">
      <jm-button size="small" plain @click="first?.open('right')">打开右侧</jm-button>
      <jm-button size="small" plain @click="first?.open('left')">打开左侧</jm-button>
      <jm-button size="small" plain @click="first?.close()">收起</jm-button>
    </jm-space>

    <p class="demo-label">禁用滑动</p>
    <jm-swipe-cell disabled>
      <jm-cell title="不可滑动" label="disabled 时手势完全交给页面滚动" is-link />
      <template #right>
        <button class="btn btn--danger" type="button">删除</button>
      </template>
    </jm-swipe-cell>
  </div>
</template>

<style scoped>
.list {
  overflow: hidden;
  border-radius: 12px;
  background: var(--jm-bg-container);
}

.list .jm-swipe-cell + .jm-swipe-cell {
  border-top: 1px solid var(--jm-border-color);
}

.btn {
  padding: 0 18px;
  border: none;
  background: var(--jm-color-primary);
  color: #fff;
  font-size: 13px;
}

.btn--danger {
  background: var(--jm-color-danger);
}

.btn--warning {
  background: var(--jm-color-warning, #EF9F27);
}

.ops {
  margin-top: 8px;
}
</style>
