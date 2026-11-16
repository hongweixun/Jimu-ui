<template>
  <div class="demo-page">
    <p class="demo-label">基础分割线</p>
    <jm-divider />

    <p class="demo-label">带文案</p>
    <jm-divider>本周学习计划</jm-divider>
    <jm-divider position="left">左对齐</jm-divider>
    <jm-divider position="right">右对齐</jm-divider>

    <p class="demo-label">虚线 / 细线</p>
    <jm-divider dashed />
    <jm-divider hairline />

    <p class="demo-label">行内竖线</p>
    <div class="demo-row" style="font-size: 13px; color: var(--jm-text-color-2)">
      <span>课程</span>
      <jm-divider vertical />
      <span>讲义</span>
      <jm-divider vertical />
      <span>作业</span>
    </div>
  </div>
</template>
