<script setup lang="ts">
const info = [
  { label: '合同编号', value: 'HT-2026-1116-07' },
  { label: '签署日期', value: '2026-11-16' },
  { label: '甲方', value: '杭州极目科技有限公司' },
  { label: '乙方', value: '杭州云栖设计工作室' },
  { label: '合同金额', value: '¥ 128,000.00' },
  { label: '付款方式', value: '分三期' },
]
</script>

<template>
  <div class="demo-page">
    <jm-descriptions :column="2" border label-width="72">
      <jm-descriptions-item
        v-for="i in info"
        :key="i.label"
        :label="i.label"
        :value="i.value"
      />
      <jm-descriptions-item
        label="备注"
        :span="2"
        value="首期款于合同签署后 5 个工作日内支付，尾款在验收通过后结清。"
      />
    </jm-descriptions>

    <p class="demo-label">vertical：标签在上，适合窄屏或字段名较长的场景</p>
    <jm-descriptions :column="2" direction="vertical">
      <jm-descriptions-item label="本月访问" value="12,486" />
      <jm-descriptions-item label="转化率" value="3.86%" />
      <jm-descriptions-item label="客单价" value="¥ 216.40" />
      <jm-descriptions-item label="复购率" value="41.2%" />
    </jm-descriptions>

    <p class="demo-label">自定义值（带状态点、按钮、链接）</p>
    <jm-descriptions border>
      <jm-descriptions-item label="服务状态">
        <span class="dot" />运行中
      </jm-descriptions-item>
      <jm-descriptions-item label="到期时间" value="2027-11-16" />
      <jm-descriptions-item label="操作">
        <jm-button size="small" variant="outline">续费</jm-button>
      </jm-descriptions-item>
    </jm-descriptions>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 20px;
}

.dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  margin-right: 5px;
  border-radius: 50%;
  background: var(--jm-color-success, #22c55e);
  vertical-align: middle;
}
</style>
