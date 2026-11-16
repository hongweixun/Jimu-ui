<script setup lang="ts">
import { ref } from 'vue'

const tree = [
  {
    label: '第一章 走进 Vue 3',
    value: 'c1',
    extra: '4 节',
    children: [
      { label: '1.1 环境搭建与项目结构', value: 'c1-1', extra: '8 分钟' },
      { label: '1.2 模板语法与指令', value: 'c1-2', extra: '12 分钟' },
      { label: '1.3 响应式原理速览', value: 'c1-3', extra: '15 分钟' },
      { label: '1.4 章节测验', value: 'c1-4', extra: '10 题' },
    ],
  },
  {
    label: '第二章 组件与状态',
    value: 'c2',
    extra: '3 节',
    children: [
      { label: '2.1 Props 与 Emit', value: 'c2-1', extra: '14 分钟' },
      { label: '2.2 插槽与作用域插槽', value: 'c2-2', extra: '11 分钟' },
      { label: '2.3 生命周期与 ref', value: 'c2-3', extra: '9 分钟' },
    ],
  },
  {
    label: '第三章 工程化实战',
    value: 'c3',
    extra: '2 节',
    disabled: true,
    children: [
      { label: '3.1 打包与分包策略', value: 'c3-1', extra: '18 分钟' },
      { label: '3.2 单元测试入门', value: 'c3-2', extra: '16 分钟' },
    ],
  },
]

const selected = ref('c1-2')
const expanded = ref(['c1', 'c2'])
const last = ref('1.2 模板语法与指令')

function onNodeClick(node: { label: string }) {
  last.value = node.label
}
</script>

<template>
  <div class="demo-page">
    <jm-tree
      v-model="selected"
      v-model:expanded-values="expanded"
      :data="tree"
      show-line
      @node-click="onNodeClick"
    />
    <p class="demo-tip">
      当前选中：{{ last }}（值 {{ selected }}）。点整行选中并展开，点箭头只展开；「第三章」被禁用。
    </p>
  </div>
</template>
