<script setup lang="ts">
import { ref } from 'vue'

const showSlot = ref(false)
const showPath = ref(false)

const actions = [
  { name: 'edit', label: '编辑课程信息', icon: 'M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16v4Z' },
  { name: 'share', label: '分享给同事', icon: 'M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2' },
  { name: 'delete', label: '删除课程', color: 'var(--jm-color-danger)' },
]
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="showSlot = true">插槽自定义关闭图标</jm-button>
    <jm-button block @click="showPath = true">path 传入「收起」箭头</jm-button>

    <jm-action-sheet
      v-model:show="showSlot"
      title="选择操作"
      :actions="actions"
      closeable
      :teleport="false"
    >
      <template #close-icon>
        <span class="as-close">
          <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
          </svg>
        </span>
      </template>
    </jm-action-sheet>

    <jm-action-sheet
      v-model:show="showPath"
      title="选择操作"
      :actions="actions"
      closeable
      close-icon="M6 9l6 6 6-6"
      :teleport="false"
    />

    <p class="demo-note">
      关闭图标两种给法：close-icon 传 SVG 的 path d 值（右图是「收起」箭头），或者 #close-icon 插槽整块替换，想放 img
      也行。
    </p>
  </div>
</template>

<style scoped>
.as-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--jm-bg-input);
  color: var(--jm-text-color-2);
}

.demo-page {
  display: flex;
  flex-direction: column;
  gap: var(--jm-space-3);
}
</style>
