<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const showGap = ref(false)

const actions = [
  { name: 'edit', label: '编辑课程信息' },
  { name: 'share', label: '分享给同事', subLabel: '生成海报或链接' },
  { name: 'delete', label: '删除课程', color: 'var(--jm-color-danger)' },
  { name: 'archive', label: '归档（暂不可用）', disabled: true },
]

function onSelect(action: { label: string }) {
  console.log('selected:', action.label)
}
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="show = true">打开动作面板</jm-button>
    <jm-button block @click="showGap = true">取消按钮带间隙</jm-button>

    <jm-action-sheet
      v-model:show="show"
      title="课程操作"
      description="选择后立即执行"
      :actions="actions"
      closeable
      :teleport="false"
      @select="onSelect"
    />

    <jm-action-sheet
      v-model:show="showGap"
      title="课程操作"
      :actions="actions"
      cancel-gap
      :teleport="false"
      @select="onSelect"
    />

    <p class="demo-note">
      第一个：取消紧贴列表（默认）；第二个：cancel-gap 开启后列表与取消之间有一条灰色间隙，视觉上分成两块。
    </p>
  </div>
</template>
