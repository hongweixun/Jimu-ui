<template>
  <div class="demo-page">
    <p class="demo-label">实心 solid</p>
    <div class="demo-row">
      <jm-button type="primary">主要</jm-button>
      <jm-button type="danger">危险</jm-button>
      <jm-button>默认</jm-button>
    </div>

    <p class="demo-label">描边 outline</p>
    <div class="demo-row">
      <jm-button type="primary" variant="outline">主要</jm-button>
      <jm-button type="danger" variant="outline">危险</jm-button>
      <jm-button variant="outline">默认</jm-button>
    </div>

    <p class="demo-label">浅底 ghost</p>
    <div class="demo-row">
      <jm-button type="primary" variant="ghost">主要</jm-button>
      <jm-button type="success" variant="ghost">成功</jm-button>
      <jm-button type="warning" variant="ghost">警告</jm-button>
    </div>

    <p class="demo-label">纯文字 text</p>
    <div class="demo-row">
      <jm-button type="primary" variant="text">查看详情</jm-button>
      <jm-button type="danger" variant="text">删除</jm-button>
      <jm-button variant="text">更多</jm-button>
    </div>
  </div>
</template>
