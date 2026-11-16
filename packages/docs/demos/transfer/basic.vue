<script setup lang="ts">
import { ref } from 'vue'

const data = [
  { label: '1.1 环境搭建与项目结构', value: 'l1', desc: '8 分钟 · 视频' },
  { label: '1.2 模板语法与指令', value: 'l2', desc: '12 分钟 · 视频' },
  { label: '1.3 响应式原理速览', value: 'l3', desc: '15 分钟 · 文档' },
  { label: '1.4 章节测验', value: 'l4', desc: '10 题 · 测验' },
  { label: '2.1 Props 与 Emit', value: 'l5', desc: '14 分钟 · 视频' },
  { label: '2.2 插槽与作用域插槽', value: 'l6', desc: '11 分钟 · 视频' },
  { label: '2.3 生命周期与 ref', value: 'l7', desc: '9 分钟 · 文档' },
  { label: '3.1 打包与分包策略', value: 'l8', desc: '暂未开放', disabled: true },
]

const selected = ref<string[]>(['l2', 'l3'])
const last = ref('勾选章节后点「添加」，或勾选已选章节点「移除」')
</script>

<template>
  <div class="demo-page">
    <jm-transfer
      v-model="selected"
      :data="data"
      :titles="['可选章节', '已选章节']"
      height="180px"
      @change="(_v, info) => (last = `${info.direction === 'to-right' ? '移入' : '移出'} ${info.moved.length} 项`)"
    />
    <p class="demo-tip">{{ last }}；禁用的「3.1」不可勾选。</p>
  </div>
</template>
