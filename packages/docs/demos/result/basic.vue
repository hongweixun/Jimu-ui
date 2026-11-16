<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const status = ref<'success' | 'error' | 'warning' | 'info' | 'waiting'>('success')

const items = [
  { key: 'success', label: '提交成功' },
  { key: 'error', label: '支付失败' },
  { key: 'warning', label: '信息待完善' },
  { key: 'info', label: '已提交审核' },
  { key: 'waiting', label: '排队处理中' },
] as const

const copy: Record<string, { title: string; desc: string }> = {
  success: { title: '作业提交成功', desc: '老师批改后会通知你，可在「我的作业」里查看记录。' },
  error: { title: '支付失败', desc: '银行卡余额不足，请更换支付方式后重试。' },
  warning: { title: '信息待完善', desc: '还差 2 项资料未填写，完成后才能开始上课。' },
  info: { title: '已提交审核', desc: '预计 1 个工作日内完成审核，请留意站内消息。' },
  waiting: { title: '排队处理中', desc: '前面还有 12 人，请不要关闭页面。' },
}

function act(msg: string) {
  showToast(msg)
}
</script>

<template>
  <div class="demo-page">
    <div class="tabs">
      <jm-tag
        v-for="i in items"
        :key="i.key"
        :type="status === i.key ? 'primary' : 'default'"
        :plain="status !== i.key"
        size="medium"
        @click="status = i.key"
        >{{ i.label }}</jm-tag
      >
    </div>

    <jm-result :status="status" :title="copy[status].title" :description="copy[status].desc">
      <jm-button type="primary" block @click="act('回到首页')">回到首页</jm-button>
      <jm-button block @click="act('查看详情')">查看详情</jm-button>
    </jm-result>

    <p class="demo-label">自定义图标</p>
    <jm-result icon="gift" status="info" title="恭喜获得 3 天会员" description="奖励已发放到账户，可在「我的」中查看。">
      <jm-button type="primary" plain size="small" @click="act('去查看')">去看看</jm-button>
    </jm-result>
  </div>
</template>

<style scoped>
.tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 4px;
}
</style>
