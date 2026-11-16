<script setup lang="ts">
const order = {
  no: 'JM20261116001',
  status: '待收货',
  amount: '¥39.90',
  payTime: '2026-11-16 14:02:31',
  address: '浙江省杭州市西湖区文一西路 1000 号 3 幢 1201',
  courier: '顺丰速运 SF1234567890',
}
</script>

<template>
  <div class="demo-page">
    <jm-descriptions title="订单信息" label-width="76">
      <jm-descriptions-item label="订单号" :value="order.no" />
      <jm-descriptions-item label="订单状态" :value="order.status" />
      <jm-descriptions-item label="实付金额" :value="order.amount" />
      <jm-descriptions-item label="支付时间" :value="order.payTime" />
      <jm-descriptions-item label="收货地址" :value="order.address" />
      <jm-descriptions-item label="物流单号" :value="order.courier" />
    </jm-descriptions>

    <p class="demo-label">两列 + 标签右对齐（关闭冒号）</p>
    <jm-descriptions :column="2" label-align="right" :colon="false" label-width="60">
      <jm-descriptions-item label="姓名" value="林小满" />
      <jm-descriptions-item label="年龄" value="28" />
      <jm-descriptions-item label="城市" value="杭州" />
      <jm-descriptions-item label="职业" value="产品经理" />
    </jm-descriptions>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 20px;
}
</style>
