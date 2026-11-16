<script setup lang="ts">
import { ref } from 'vue'

const active = ref(1)
const steps = ['提交报名', '资料审核', '分配班级', '开课']

function prev() {
  if (active.value > 0) active.value--
}

function next() {
  if (active.value < steps.length - 1) active.value++
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">横向（第 {{ active + 1 }} / 4 步）</p>
    <jm-steps :active="active">
      <jm-step
        v-for="(t, i) in steps"
        :key="t"
        :title="t"
        :description="i === 0 ? '9-01' : i === 1 ? '9-02' : i === 2 ? '9-05' : '9-10'"
      />
    </jm-steps>

    <div class="demo-row" style="margin-top: 20px">
      <jm-button size="small" :disabled="active === 0" @click="prev">上一步</jm-button>
      <jm-button size="small" type="primary" :disabled="active === 3" @click="next">
        下一步
      </jm-button>
    </div>

    <p class="demo-label">带错误状态</p>
    <jm-steps :active="2">
      <jm-step title="提交报名" description="已完成" />
      <jm-step title="资料审核" description="照片不清晰" status="error" />
      <jm-step title="分配班级" />
      <jm-step title="开课" />
    </jm-steps>

    <p class="demo-label">纵向</p>
    <jm-steps :active="1" direction="vertical">
      <jm-step title="下单" description="2026-09-01 10:24" />
      <jm-step title="支付成功" description="微信支付 ¥1,280.00" />
      <jm-step title="等待排课" description="预计 1 个工作日内完成" />
    </jm-steps>
  </div>
</template>
