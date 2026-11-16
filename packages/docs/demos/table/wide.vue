<script setup lang="ts">
import { ref } from 'vue'

const columns = [
  { key: 'name', title: '学生', width: 92, fixed: 'left' as const },
  { key: 'className', title: '班级', width: 110 },
  { key: 'chinese', title: '语文', width: 72, align: 'right' as const },
  { key: 'math', title: '数学', width: 72, align: 'right' as const },
  { key: 'english', title: '英语', width: 72, align: 'right' as const },
  { key: 'total', title: '总分', width: 86, align: 'right' as const },
  { key: 'rank', title: '年级排名', width: 92, align: 'center' as const },
]

const rows = ref([
  { id: 1, name: '林一', className: '高二（3）班', chinese: 118, math: 142, english: 126, total: 386, rank: 12 },
  { id: 2, name: '周舟', className: '高二（3）班', chinese: 126, math: 138, english: 131, total: 395, rank: 6 },
  { id: 3, name: '陈默', className: '高二（1）班', chinese: 109, math: 150, english: 118, total: 377, rank: 23 },
  { id: 4, name: '苏晚', className: '高二（1）班', chinese: 133, math: 129, english: 140, total: 402, rank: 3 },
])

const empty = ref(false)

function toggle() {
  empty.value = !empty.value
  rows.value = empty.value
    ? []
    : [
        { id: 1, name: '林一', className: '高二（3）班', chinese: 118, math: 142, english: 126, total: 386, rank: 12 },
        { id: 2, name: '周舟', className: '高二（3）班', chinese: 126, math: 138, english: 131, total: 395, rank: 6 },
        { id: 3, name: '陈默', className: '高二（1）班', chinese: 109, math: 150, english: 118, total: 377, rank: 23 },
        { id: 4, name: '苏晚', className: '高二（1）班', chinese: 133, math: 129, english: 140, total: 402, rank: 3 },
      ]
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-actions">
      <jm-button size="small" variant="outline" @click="toggle">
        {{ empty ? '填回数据' : '清空数据看空态' }}
      </jm-button>
      <span class="demo-hint">左右滑动表格</span>
    </div>

    <jm-table
      :columns="columns"
      :data="rows"
      row-key="id"
      bordered
      sticky-header
      max-height="240"
      empty-text="本学期还没有成绩记录"
    />

    <p class="demo-tip">列宽合计超过屏幕宽度时整表横向滚动，「学生」列固定在左侧不跟着动。</p>
  </div>
</template>

<style scoped>
.demo-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.demo-hint {
  font-size: 12px;
  color: var(--jm-text-color-3);
}
</style>
