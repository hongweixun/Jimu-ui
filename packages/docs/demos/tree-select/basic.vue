<script setup lang="ts">
import { ref } from 'vue'

const data = [
  {
    label: '语文',
    value: 'chinese',
    children: [
      { label: '现代文阅读', value: 'chinese-1', extra: '8 个知识点' },
      { label: '古诗文默写', value: 'chinese-2', extra: '12 个知识点' },
      { label: '作文素材', value: 'chinese-3', extra: '20 个知识点' },
    ],
  },
  {
    label: '数学',
    value: 'math',
    children: [
      {
        label: '函数',
        value: 'math-1',
        children: [
          { label: '一次函数', value: 'math-1-1' },
          { label: '二次函数', value: 'math-1-2' },
        ],
      },
      { label: '立体几何', value: 'math-2' },
    ],
  },
  {
    label: '英语',
    value: 'english',
    children: [
      { label: '完形填空', value: 'english-1' },
      { label: '语法填空', value: 'english-2' },
    ],
  },
]

const value = ref('math-1-2')
const plain = ref('')
</script>

<template>
  <div class="demo-page">
    <jm-tree-select
      v-model="value"
      :data="data"
      label="知识点"
      title="选择知识点"
      :teleport="false"
    />
    <jm-tree-select
      v-model="plain"
      :data="data"
      placeholder="未选择时显示占位文案"
      title="选择知识点"
      :teleport="false"
    />
    <jm-tree-select
      :data="data"
      model-value="english-1"
      label="已锁定"
      disabled
      :teleport="false"
    />

    <p class="demo-tip">
      当前值：{{ value || '空' }}。触发器显示从根到选中项的完整路径，弹层打开时自动展开到已选项，可搜索。
    </p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}
</style>
