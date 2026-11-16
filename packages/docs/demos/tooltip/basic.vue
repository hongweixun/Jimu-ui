<script setup lang="ts">
import { ref } from 'vue'

const clickCount = ref(0)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">纯图标按钮最需要提示：鼠标移上去、键盘 Tab 到都会出现</p>
    <div class="row">
      <jm-tooltip content="刷新数据">
        <jm-button size="small" variant="outline"><jm-icon name="refresh" /></jm-button>
      </jm-tooltip>
      <jm-tooltip content="收藏">
        <jm-button size="small" variant="outline"><jm-icon name="star" /></jm-button>
      </jm-tooltip>
      <jm-tooltip content="分享给同事">
        <jm-button size="small" variant="outline"><jm-icon name="share" /></jm-button>
      </jm-tooltip>
      <jm-tooltip content="删除后不可恢复" theme="light">
        <jm-button size="small" variant="outline" type="danger"><jm-icon name="trash" /></jm-button>
      </jm-tooltip>
    </div>

    <p class="demo-label">四个方向（空间不够会自动翻到对面）</p>
    <div class="row">
      <jm-tooltip content="在上方" placement="top"><jm-button size="small">top</jm-button></jm-tooltip>
      <jm-tooltip content="在下方" placement="bottom"><jm-button size="small">bottom</jm-button></jm-tooltip>
      <jm-tooltip content="在左侧" placement="left"><jm-button size="small">left</jm-button></jm-tooltip>
      <jm-tooltip content="在右侧" placement="right"><jm-button size="small">right</jm-button></jm-tooltip>
    </div>

    <p class="demo-label">移动端：长按 0.45 秒显示，抬手 1.6 秒后自动消失</p>
    <div class="row">
      <jm-tooltip content="设备编号 JM-A12-0031" trigger="longpress">
        <jm-tag>长按这行字</jm-tag>
      </jm-tooltip>
      <jm-tooltip content="长按我也行" trigger="longpress" placement="bottom" theme="light">
        <jm-tag type="primary">再试一个</jm-tag>
      </jm-tooltip>
    </div>

    <p class="demo-label">点击触发 + 多行文案（max-width 控制换行）</p>
    <jm-tooltip
      trigger="click"
      :max-width="200"
      content="这里放稍长一点的说明：气泡会在 200px 处换行，不会被撑成一条长条。"
      placement="bottom"
    >
      <jm-button size="small" block @click="clickCount++">点我查看说明（已点 {{ clickCount }} 次）</jm-button>
    </jm-tooltip>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}
</style>
