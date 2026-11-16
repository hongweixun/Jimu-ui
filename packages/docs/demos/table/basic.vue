<script setup lang="ts">
import { ref } from 'vue'

function money(value: unknown) {
  return `¥${Number(value).toFixed(2)}`
}

const columns = [
  { key: 'id', title: '订单号', width: 128, fixed: 'left' as const },
  { key: 'title', title: '商品', minWidth: 130, ellipsis: true },
  { key: 'amount', title: '金额', width: 88, align: 'right' as const, formatter: money },
  { key: 'status', title: '状态', width: 76, align: 'center' as const },
]

const rows = ref([
  { id: 'JM20261116001', title: '青柠气泡水 × 6 瓶', amount: 39.9, status: '待收货' },
  { id: 'JM20261116002', title: '硅胶折叠水杯 500ml', amount: 68, status: '已发货' },
  { id: 'JM20261116003', title: '手冲咖啡挂耳包礼盒（12 片装）', amount: 128, status: '已完成' },
  { id: 'JM20261116004', title: '冷萃咖啡液', amount: 59, status: '已完成' },
])

const last = ref('点任意一行试试')
</script>

<template>
  <div class="demo-page">
    <jm-table
      :columns="columns"
      :data="rows"
      row-key="id"
      stripe
      clickable
      max-height="260"
      @row-click="(row) => (last = `打开订单 ${row.id}`)"
    >
      <template #cell-status="{ value }">
        <jm-tag :type="value === '已完成' ? 'success' : value === '待收货' ? 'warning' : 'primary'" size="small">
          {{ value }}
        </jm-tag>
      </template>
    </jm-table>

    <p class="demo-tip">{{ last }}。首列 fixed="left" 固定在左侧，横向滚动时不动。</p>
  </div>
</template>
