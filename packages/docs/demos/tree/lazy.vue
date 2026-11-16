<script setup lang="ts">
import { ref } from 'vue'

const keyword = ref('')
const loadingTip = ref('点开任意章节，子节点会等 0.8 秒再出现')

/** 根节点不给 children：展开时才去「请求」 */
const tree = ref([
  { label: '第一章 走进 Vue 3', value: 'c1', extra: '待加载' },
  { label: '第二章 组件与状态', value: 'c2', extra: '待加载' },
  { label: '第三章 工程化实战', value: 'c3', extra: '待加载' },
])

const cache: Record<string, { label: string; value: string; extra: string }[]> = {
  c1: [
    { label: '1.1 环境搭建', value: 'c1-1', extra: '8 分钟' },
    { label: '1.2 模板语法', value: 'c1-2', extra: '12 分钟' },
    { label: '1.3 响应式原理', value: 'c1-3', extra: '15 分钟' },
  ],
  c2: [
    { label: '2.1 Props 与 Emit', value: 'c2-1', extra: '14 分钟' },
    { label: '2.2 插槽', value: 'c2-2', extra: '11 分钟' },
  ],
  c3: [
    { label: '3.1 打包策略', value: 'c3-1', extra: '18 分钟' },
    { label: '3.2 单元测试', value: 'c3-2', extra: '16 分钟' },
  ],
}

async function loadData(node: { value: string; label: string }) {
  loadingTip.value = `正在加载「${node.label}」…`
  await new Promise((resolve) => setTimeout(resolve, 800))
  const kids = cache[node.value] ?? []
  loadingTip.value = `「${node.label}」加载完成，共 ${kids.length} 节`
  return kids
}
</script>

<template>
  <div class="demo-page">
    <jm-search v-model="keyword" placeholder="搜索已加载的节点" />

    <jm-tree
      :data="tree"
      :load-data="loadData"
      :filter="keyword"
      show-line
      empty-text="没有匹配的节点"
    />

    <p class="demo-tip">{{ loadingTip }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}
</style>
