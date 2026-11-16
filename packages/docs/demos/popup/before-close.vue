<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const asking = ref(false)
const dirty = ref(true)
const result = ref('')
let resolveAsk: ((ok: boolean) => void) | null = null

/**
 * 返回 Promise 时 Popup 会等结论：确认前不关，遮罩和关闭按钮都走这里。
 */
function beforeClose() {
  if (!dirty.value) return true
  asking.value = true
  return new Promise<boolean>((resolve) => {
    resolveAsk = resolve
  })
}

function answer(ok: boolean) {
  asking.value = false
  if (!ok) result.value = '取消关闭，弹层还在'
  resolveAsk?.(ok)
  resolveAsk = null
}

function onClose() {
  result.value = '已关闭（beforeClose 放行）'
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">关闭前拦截：有未保存内容时先确认</p>
    <jm-button type="primary" block @click="show = true">打开弹层</jm-button>
    <p class="state">{{ result || '点遮罩或关闭按钮试试' }}</p>

    <jm-popup
      v-model:show="show"
      position="bottom"
      round
      closeable
      :teleport="false"
      :before-close="beforeClose"
      @close="onClose"
    >
      <div class="panel">
        <h4 class="panel__title">填写反馈</h4>
        <p class="panel__desc">这里有没保存的内容，直接关掉会丢。</p>
        <jm-button type="primary" block @click="show = false">保存并关闭</jm-button>
      </div>
    </jm-popup>

    <jm-dialog
      v-model:show="asking"
      title="放弃编辑？"
      message="内容还没保存，关闭后无法恢复。"
      confirm-text="放弃"
      cancel-text="继续编辑"
      @confirm="answer(true)"
      @cancel="answer(false)"
    />
  </div>
</template>

<style scoped>
.panel {
  padding: 20px 16px 24px;
}

.panel__title {
  margin: 0 0 6px;
  font-size: 16px;
}

.panel__desc {
  margin: 0 0 16px;
  color: var(--jm-text-color-2);
  font-size: 13px;
}

.state {
  margin: 12px 0 0;
  color: var(--jm-text-color-3);
  font-size: 12px;
}
</style>
