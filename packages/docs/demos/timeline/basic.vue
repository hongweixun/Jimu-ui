<script setup lang="ts">
const flow = [
  {
    time: '09:12',
    title: '提交作业',
    content: '第三章课后练习 · 共 12 题',
    type: 'success' as const,
    icon: 'check',
  },
  {
    time: '10:05',
    title: '系统批改完成',
    content: '客观题 10 题全对，主观题待老师批阅',
    type: 'success' as const,
    icon: 'check',
  },
  {
    time: '14:30',
    title: '老师批阅中',
    content: '王老师正在评阅第 11、12 题',
    type: 'primary' as const,
    active: true,
  },
  {
    time: '预计 18:00',
    title: '成绩公布',
    content: '成绩发布后会通过站内消息通知你',
  },
]

const dashed = [
  { time: '周一', title: '报名选课', content: '已完成' },
  { time: '周三', title: '资料审核', content: '已完成' },
  { time: '周五', title: '开课通知', content: '待发送' },
]
</script>

<template>
  <div class="demo-page">
    <jm-timeline>
      <jm-timeline-item
        v-for="item in flow"
        :key="item.title"
        :time="item.time"
        :title="item.title"
        :content="item.content"
        :type="item.type"
        :icon="item.icon"
        :active="item.active"
      />
    </jm-timeline>

    <p class="demo-label">虚线 + 空心点，适合「待办 / 未完成」</p>
    <jm-timeline line-style="dashed">
      <jm-timeline-item
        v-for="(item, i) in dashed"
        :key="item.time"
        :time="item.time"
        :title="item.title"
        :content="item.content"
        :type="i === dashed.length - 1 ? 'warning' : 'default'"
        :hollow="i === dashed.length - 1"
      />
    </jm-timeline>
  </div>
</template>
