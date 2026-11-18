<script setup lang="ts">
import { ref } from 'vue'
import { registerIcon, vCopy } from 'jimu-ui'

const groups = [
  {
    title: '方向与操作',
    names: ['chevron-left', 'chevron-right', 'chevron-up', 'chevron-down', 'arrow-left', 'arrow-right', 'check', 'close', 'plus', 'minus', 'search', 'refresh'],
  },
  {
    title: '状态',
    names: ['check-circle', 'close-circle', 'warning', 'info', 'loading', 'star', 'star-fill', 'heart', 'heart-fill', 'eye', 'eye-close', 'lock'],
  },
  {
    title: '业务',
    names: ['user', 'users', 'phone', 'mail', 'location', 'calendar', 'clock', 'home', 'bell', 'camera', 'image', 'file'],
  },
  {
    title: '更多',
    names: ['download', 'upload', 'trash', 'edit', 'filter', 'sort', 'cart', 'gift', 'wallet', 'qr-code', 'share', 'link'],
  },
]

const copied = ref('')

/* 业务侧注册自己的图标，之后就能按名字用 */
registerIcon('school', {
  paths: ['M3 9.6L12 5l9 4.6-9 4.6z', 'M6.4 11.4V17c0 1.2 2.5 2.2 5.6 2.2s5.6-1 5.6-2.2v-5.6'],
})
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础用法：尺寸跟随字号</p>
    <div class="row">
      <jm-icon name="check-circle" />
      <span class="text">默认 1em，和文字基线对齐</span>
      <jm-icon name="chevron-right" />
    </div>

    <p class="demo-label">尺寸与颜色</p>
    <div class="row">
      <jm-icon name="star-fill" :size="14" color="#FFB300" />
      <jm-icon name="star-fill" :size="20" color="#FFB300" />
      <jm-icon name="star-fill" :size="28" color="#FFB300" />
      <jm-icon name="heart-fill" :size="24" color="#E24B4A" />
      <jm-icon name="graduation-cap" :size="24" color="var(--jm-color-primary)" />
    </div>

    <p class="demo-label">旋转：spin 用于 loading，rotate 固定角度</p>
    <div class="row">
      <jm-icon name="loading" :size="20" spin color="var(--jm-color-primary)" />
      <jm-icon name="refresh" :size="20" :rotate="90" />
      <jm-icon name="chevron-right" :size="20" :rotate="180" />
      <jm-icon name="school" :size="22" color="#1D9E75" />
      <span class="text">最后一个是 registerIcon 注册的</span>
    </div>

    <p class="demo-label">内置图标（点一下复制名字）</p>
    <div v-for="g in groups" :key="g.title" class="group">
      <p class="group-title">{{ g.title }}</p>
      <div class="icons">
        <button
          v-for="n in g.names"
          :key="n"
          v-copy="{ text: `<jm-icon name=&quot;${n}&quot; />`, feedback: `已复制 ${n}`, onSuccess: () => (copied = n) }"
          class="cell"
          type="button"
        >
          <jm-icon :name="n" :size="22" />
          <span class="cell-name">{{ n }}</span>
        </button>
      </div>
    </div>
    <p class="demo-note">点击图标格子复制用法代码，最近一次：{{ copied || '未选择' }}</p>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  color: var(--jm-text-primary);
}

.text {
  font-size: 13px;
  color: var(--jm-text-secondary);
}

.group {
  margin-bottom: 12px;
}

.group-title {
  margin: 0 0 6px;
  font-size: 12px;
  color: var(--jm-text-tertiary);
}

.icons {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 4px;
}

.cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 4px;
  border: 1px solid var(--jm-border-color);
  border-radius: 10px;
  background: var(--jm-bg-container);
  color: var(--jm-text-primary);
  cursor: pointer;
}

.cell:active {
  background: var(--jm-bg-input);
}

.cell-name {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 10px;
  color: var(--jm-text-tertiary);
}
</style>
