<template>
  <div class="demo-page">
    <p class="demo-label">包裹在其他元素上</p>
    <div class="demo-row">
      <jm-badge content="3">
        <span class="box">消息</span>
      </jm-badge>
      <jm-badge content="99" :max="9">
        <span class="box">通知</span>
      </jm-badge>
      <jm-badge dot>
        <span class="box">设置</span>
      </jm-badge>
      <jm-badge content="new" color="#00B98A">
        <span class="box">课程</span>
      </jm-badge>
    </div>

    <p class="demo-label">独立使用（无子元素）</p>
    <div class="demo-row">
      <jm-badge content="5" />
      <jm-badge dot />
      <jm-badge content="88" color="#7C4DFF" />
    </div>

    <p class="demo-label">常见场景</p>
    <div class="demo-row">
      <jm-badge content="2">
        <jm-button size="small" variant="outline" type="primary">我的课程</jm-button>
      </jm-badge>
    </div>
  </div>
</template>

<style scoped>
.box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
  font-size: 12px;
  color: var(--jm-text-color-2);
}
</style>
