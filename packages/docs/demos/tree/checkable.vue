<script setup lang="ts">
import { computed, ref } from 'vue'

const tree = [
  {
    label: '前端基础',
    value: 'fe',
    children: [
      { label: 'HTML 语义化', value: 'fe-1' },
      { label: 'CSS 布局', value: 'fe-2' },
      { label: 'JavaScript 异步', value: 'fe-3' },
    ],
  },
  {
    label: '框架与工程',
    value: 'fw',
    children: [
      { label: 'Vue 3 组合式 API', value: 'fw-1' },
      { label: 'Vite 构建', value: 'fw-2' },
      { label: 'TypeScript', value: 'fw-3', disabled: true },
    ],
  },
  { label: '计算机基础', value: 'cs' },
]

const checked = ref<string[]>(['fe-2'])
const half = ref<string[]>([])
const treeRef = ref<{ expandAll: () => void; collapseAll: () => void; setCheckedValues: (v: string[]) => void } | null>(null)

const names: Record<string, string> = {
  fe: '前端基础',
  'fe-1': 'HTML 语义化',
  'fe-2': 'CSS 布局',
  'fe-3': 'JavaScript 异步',
  fw: '框架与工程',
  'fw-1': 'Vue 3 组合式 API',
  'fw-2': 'Vite 构建',
  cs: '计算机基础',
}

const chosen = computed(() => checked.value.map((v) => names[v] ?? v))

function onCheck(values: string[], info: { halfCheckedValues: string[] }) {
  checked.value = values
  half.value = info.halfCheckedValues
}

function pickAll() {
  treeRef.value?.expandAll()
  treeRef.value?.setCheckedValues(['fe-1', 'fe-2', 'fe-3', 'fw-1', 'fw-2'])
}

function reset() {
  treeRef.value?.setCheckedValues([])
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-actions">
      <jm-button size="small" variant="outline" @click="pickAll">推荐全选</jm-button>
      <jm-button size="small" variant="outline" @click="reset">清空</jm-button>
    </div>

    <jm-tree
      ref="treeRef"
      :data="tree"
      checkable
      :default-expanded-values="['fe', 'fw']"
      v-model:checked-values="checked"
      @check="onCheck"
    />

    <p class="demo-tip">
      已选 {{ checked.length }} 项：{{ chosen.join('、') || '无' }}
      <template v-if="half.length">；{{ half.length }} 个父节点处于半选</template>
    </p>
  </div>
</template>

<style scoped>
.demo-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
</style>
