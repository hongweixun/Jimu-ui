<script setup lang="ts">
import { ref } from 'vue'

const longText =
  '移动端卡片摘要是最常见的截断场景：一段一百多字的介绍文案，收起时只保留三行，超出部分交给省略号，用户感兴趣再点「展开」看全文，看完了随手「收起」回到摘要态，阅读节奏不会被打断。'

const expanded = ref(false)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">单行截断（不可展开）</p>
    <jm-ellipsis
      class="card"
      content="订单编号 JM20261116001，收货地址：浙江省杭州市西湖区文一西路 1000 号 3 幢 1201 室，联系电话 138****0000，预计 11 月 20 日前送达。"
    />

    <p class="demo-label">三行截断 + 展开 / 收起（动作跟在文末）</p>
    <jm-ellipsis class="card" :rows="3" expandable :content="longText" />

    <p class="demo-label">受控展开（v-model:expanded）+ 动作独占一行</p>
    <jm-ellipsis
      class="card"
      :rows="3"
      expandable
      v-model:expanded="expanded"
      action-position="block"
      :content="longText"
    />
    <p class="demo-note">当前状态：{{ expanded ? '已展开' : '已收起' }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 12px;
}

.card {
  padding: 12px;
  border-radius: var(--jm-radius-lg);
  background: var(--jm-bg-container);
}
</style>
