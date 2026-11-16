<template>
  <div class="demo-page">
    <p class="demo-label">实心</p>
    <div class="demo-row">
      <jm-tag>默认</jm-tag>
      <jm-tag type="default">信息</jm-tag>
      <jm-tag type="success">已完成</jm-tag>
      <jm-tag type="warning">待确认</jm-tag>
      <jm-tag type="danger">已过期</jm-tag>
    </div>

    <p class="demo-label">浅底 plain</p>
    <div class="demo-row">
      <jm-tag plain>默认</jm-tag>
      <jm-tag type="primary" plain>直播中</jm-tag>
      <jm-tag type="success" plain>已批改</jm-tag>
      <jm-tag type="warning" plain>待支付</jm-tag>
      <jm-tag type="danger" plain>缺勤</jm-tag>
    </div>

    <p class="demo-label">尺寸与圆角</p>
    <div class="demo-row">
      <jm-tag size="small" plain>小号</jm-tag>
      <jm-tag plain>中号</jm-tag>
      <jm-tag size="large" plain>大号</jm-tag>
      <jm-tag round>胶囊</jm-tag>
    </div>

    <p class="demo-label">可关闭 · 自定义颜色</p>
    <div class="demo-row">
      <jm-tag closable @close="() => {}">可关闭</jm-tag>
      <jm-tag color="#7C4DFF" round>紫色</jm-tag>
      <jm-tag color="#7C4DFF" plain>紫色浅底</jm-tag>
    </div>
  </div>
</template>
