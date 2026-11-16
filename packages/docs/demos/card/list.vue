<script setup lang="ts">
import { ref } from 'vue'

function cover(label: string, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/>
    </linearGradient></defs>
    <rect width="200" height="200" fill="url(#g)"/>
    <text x="100" y="104" font-family="system-ui" font-size="26" fill="#ffffff"
      text-anchor="middle" dominant-baseline="middle" opacity="0.92">${label}</text>
  </svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const orders = ref([
  {
    id: 'JM20261116001',
    title: '青柠气泡水 × 6 瓶',
    desc: '下单时间 11-16 14:02 · 顺丰配送',
    thumb: cover('饮品', '#22C55E', '#0E9F6E'),
    price: 39.9,
    status: '待收货',
  },
  {
    id: 'JM20261112037',
    title: '硅胶折叠水杯 500ml',
    desc: '下单时间 11-12 09:31 · 已完成',
    thumb: cover('水杯', '#7C4DFF', '#4A2ECC'),
    price: 68,
    status: '已完成',
  },
])

const clicked = ref('')

function confirmReceived(title: string) {
  clicked.value = `确认收货：${title}`
}
</script>

<template>
  <div class="demo-page">
    <jm-card
      v-for="o in orders"
      :key="o.id"
      :title="o.title"
      :desc="o.desc"
      :thumb="o.thumb"
      :price="o.price"
      :extra="o.status"
      thumb-position="left"
      clickable
      @click="clicked = `打开订单 ${o.id}`"
    >
      <template #footer>
        <jm-button size="small" variant="outline" @click.stop>查看物流</jm-button>
        <jm-button
          v-if="o.status === '待收货'"
          size="small"
          @click.stop="confirmReceived(o.title)"
        >
          确认收货
        </jm-button>
      </template>
    </jm-card>

    <jm-card title="无封面也能用" desc="纯文字卡片：公告、设置分组、富文本内容" :bordered="true">
      卡片本身只是个容器，正文放列表、表单、图表都行；页脚区域自带一条分割线，正好放操作按钮。
    </jm-card>

    <p class="demo-tip">{{ clicked || '点卡片空白处试试点击态；footer 按钮用 .stop 阻止冒泡，不会连带打开订单' }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 12px;
}
</style>
