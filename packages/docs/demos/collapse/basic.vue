<script setup lang="ts">
import { ref } from 'vue'

const active = ref<(string | number)[]>(['1'])
const accordion = ref(false)
const single = ref<string | number>('a')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（默认展开第一项）</p>
    <jm-collapse v-model="active">
      <jm-collapse-item name="1" title="怎么修改绑定的手机号？">
        进入「我的 - 账号安全 - 手机号」，通过原手机号验证后即可更换。
      </jm-collapse-item>
      <jm-collapse-item name="2" title="课程可以退费吗？">
        开课前 7 天内可全额退费，开课后按已上课时折算。
      </jm-collapse-item>
      <jm-collapse-item name="3" title="发票如何开具？" extra="必看">
        在订单详情页点击「申请发票」，电子发票 1 个工作日内开出。
      </jm-collapse-item>
    </jm-collapse>

    <p class="demo-label">手风琴模式（同时只展开一项）</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px">
      <jm-switch v-model="accordion" size="small" />
      <span style="font-size: 13px; color: var(--jm-text-color-2)">
        {{ accordion ? '已开启' : '已关闭' }}
      </span>
    </div>
    <jm-collapse v-model="single" :accordion="accordion">
      <jm-collapse-item name="a" title="账户与安全">
        手机号、密码、登录设备管理都在这里。
      </jm-collapse-item>
      <jm-collapse-item name="b" title="学习记录">
        包含课程进度、作业提交和错题本。
      </jm-collapse-item>
      <jm-collapse-item name="c" title="已停用项" disabled>
        这一项不可展开。
      </jm-collapse-item>
    </jm-collapse>
  </div>
</template>
