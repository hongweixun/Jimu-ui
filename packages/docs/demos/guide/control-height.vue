<template>
  <div class="demo-page">
    <p class="demo-label">默认中档 44px：Button / Input / Search 同屏混排，高度自动对齐</p>
    <div class="demo-row">
      <jm-input placeholder="输入课程名" class="demo-grow" />
      <jm-button type="primary" round>搜索</jm-button>
    </div>
    <jm-search placeholder="搜课程 / 搜老师" />
    <div class="demo-row">
      <jm-button type="primary" round block>整宽 CTA，同样是 44px</jm-button>
    </div>

    <p class="demo-label">大档 52px：首屏大按钮（登录、支付确认）</p>
    <div class="demo-row">
      <jm-button type="primary" size="large" round block>立即登录</jm-button>
    </div>
    <div class="demo-row">
      <jm-button variant="outline" size="large" round block>随便逛逛</jm-button>
    </div>
  </div>
</template>

<style scoped>
.demo-grow {
  flex: 1;
  min-width: 0;
}
</style>
