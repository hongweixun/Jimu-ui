<script setup lang="ts">
import { ref } from 'vue'
import type { TabName } from 'jimu-ui'

const active = ref<TabName>('basic')
const asking = ref(false)
const blocked = ref(0)
let resolveAsk: ((ok: boolean) => void) | null = null

/**
 * 只有「离开已填写的表单」才拦一下。
 * 返回 Promise，Tabs 会等结论，期间连点不会叠起多次确认。
 */
function beforeChange(name: TabName) {
  if (name !== 'submit') return true
  asking.value = true
  return new Promise<boolean>((resolve) => {
    resolveAsk = resolve
  })
}

function answer(ok: boolean) {
  asking.value = false
  if (!ok) blocked.value += 1
  resolveAsk?.(ok)
  resolveAsk = null
}

const note = ref('')
</script>

<template>
  <div class="demo-page">
    <jm-tabs v-model="active" :before-change="beforeChange" swipeable>
      <jm-tab name="basic" label="基本信息">
        <p class="panel">第 1 步：填资料。点「提交结果」会被拦一次。</p>
      </jm-tab>
      <jm-tab name="extra" label="补充材料">
        <p class="panel">第 2 步：上传材料。</p>
      </jm-tab>
      <jm-tab name="submit" label="提交结果">
        <p class="panel">第 3 步：确认提交。</p>
      </jm-tab>
    </jm-tabs>

    <p class="state">已拦截 {{ blocked }} 次 · 当前页：{{ active }} {{ note }}</p>

    <p class="demo-note">
      <code>beforeChange</code> 返回 <code>false</code> 或 reject 就不切换；返回 Promise 时会等结论，异步期间重复点击会被忽略。
    </p>

    <jm-dialog
      v-model:show="asking"
      title="离开表单？"
      message="已填写的内容还没保存，离开后会丢失。"
      confirm-text="仍然离开"
      cancel-text="留在这里"
      @confirm="answer(true)"
      @cancel="answer(false)"
    />
  </div>
</template>

<style scoped>
.panel {
  margin: 0;
  padding: 20px 4px;
  color: var(--jm-text-color-2);
  font-size: 13px;
  line-height: 1.6;
}

.state {
  margin: 12px 0 0;
  color: var(--jm-text-color-3);
  font-size: 12px;
}
</style>
