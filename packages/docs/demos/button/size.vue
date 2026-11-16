<template>
  <div class="demo-page">
    <p class="demo-label">尺寸</p>
    <div class="demo-row">
      <jm-button type="primary" size="small">小号</jm-button>
      <jm-button type="primary">中号</jm-button>
      <jm-button type="primary" size="large">大号</jm-button>
    </div>
    <div class="demo-row">
      <jm-button size="small">小号</jm-button>
      <jm-button>中号</jm-button>
      <jm-button size="large">大号</jm-button>
    </div>

    <p class="demo-label">圆角：数字按 px，字符串原样透传</p>
    <div class="demo-row">
      <jm-button type="primary" :radius="0">方角</jm-button>
      <jm-button type="primary" :radius="4">4px</jm-button>
      <jm-button type="primary" :radius="12">12px</jm-button>
      <jm-button type="primary" radius="50%">胶囊</jm-button>
    </div>

    <p class="demo-label">胶囊形态：round 一键开，移动端最常用</p>
    <div class="demo-row">
      <jm-button type="primary" round>立即报名</jm-button>
      <jm-button variant="outline" round>收藏</jm-button>
      <jm-button variant="ghost" size="small" round>关注</jm-button>
    </div>
    <div class="demo-row">
      <jm-button type="primary" round block>提交订单</jm-button>
    </div>

    <p class="demo-label">小尺寸 + 胶囊，适合卡片内的次要操作</p>
    <div class="demo-row">
      <jm-button type="primary" variant="ghost" size="small" radius="50%">关注</jm-button>
      <jm-button size="small" radius="50%">分享</jm-button>
    </div>
  </div>
</template>
