<script setup lang="ts">
import { ref } from 'vue'

interface Row {
  id: number
  title: string
  desc: string
  locked?: boolean
}

const rows = ref<Row[]>([
  { id: 1, title: '三年级二班 作业合集', desc: '32 张图片 · 12.4MB' },
  { id: 2, title: '期末成绩单', desc: '锁定中，删除前需二次确认', locked: true },
  { id: 3, title: '活动照片', desc: '18 张图片 · 6.1MB' },
])

const asking = ref(false)
const target = ref<Row | null>(null)
let resolveAsk: ((ok: boolean) => void) | null = null

/** 点「删除」先问一句：resolve(true) 才收起并删除 */
function beforeClose({ action }: { action: HTMLElement }) {
  const id = Number(action.dataset.id)
  const row = rows.value.find((r) => r.id === id)
  if (!row) return true
  target.value = row
  asking.value = true
  return new Promise<boolean>((resolve) => {
    resolveAsk = resolve
  })
}

function answer(ok: boolean) {
  asking.value = false
  if (ok && target.value) {
    rows.value = rows.value.filter((r) => r.id !== target.value!.id)
  }
  resolveAsk?.(ok)
  resolveAsk = null
  target.value = null
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">左滑 → 点「删除」→ 二次确认，确认后才收起并删除</p>
    <div class="list">
      <jm-swipe-cell
        v-for="row in rows"
        :key="row.id"
        close-on-action
        :before-close="beforeClose"
      >
        <jm-cell :title="row.title" :label="row.desc" />
        <template #right>
          <button type="button" class="action" :data-id="row.id">删除</button>
        </template>
      </jm-swipe-cell>
    </div>

    <p v-if="!rows.length" class="empty">都删完了，刷新页面可以重来</p>

    <jm-dialog
      v-model:show="asking"
      title="确认删除？"
      :message="`「${target?.title ?? ''}」删除后无法恢复。`"
      confirm-text="删除"
      confirm-color="#FA5151"
      @confirm="answer(true)"
      @cancel="answer(false)"
    />
  </div>
</template>

<style scoped>
.list {
  border-radius: 10px;
  overflow: hidden;
  background: var(--jm-bg-container);
}

.action {
  width: 74px;
  border: 0;
  background: var(--jm-color-danger);
  color: #fff;
  font-family: inherit;
  font-size: 14px;
  cursor: pointer;
}

.empty {
  margin: 12px 0 0;
  color: var(--jm-text-color-3);
  font-size: 12px;
  text-align: center;
}
</style>
