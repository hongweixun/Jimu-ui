<template>
  <div class="demo-page">
    <p class="demo-label">默认</p>
    <jm-empty />

    <p class="demo-label">带操作按钮</p>
    <jm-empty description="还没有报名任何课程">
      <jm-button type="primary" size="small">去选课</jm-button>
    </jm-empty>

    <p class="demo-label">尺寸</p>
    <jm-empty size="small" description="小号空状态，适合卡片内" />
  </div>
</template>
