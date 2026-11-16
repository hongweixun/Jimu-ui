<template>
  <div class="demo-page">
    <p class="demo-label">四种类型</p>
    <div class="demo-row" style="gap: 22px">
      <jm-loading type="circular" />
      <jm-loading type="spinner" />
      <jm-loading type="dots" />
      <jm-loading type="pulse" />
    </div>

    <p class="demo-label">尺寸与颜色</p>
    <div class="demo-row" style="gap: 22px; align-items: flex-end">
      <jm-loading :size="16" />
      <jm-loading :size="24" />
      <jm-loading :size="36" color="#7C4DFF" />
    </div>

    <p class="demo-label">带文字</p>
    <jm-loading text="加载中..." />
    <jm-loading text="正在提交" vertical :size="30" />
    <jm-loading text="上传中" vertical :size="30" type="dots" color="#00B98A" />
  </div>
</template>
