<script setup lang="ts">
import { ref } from 'vue'

const bottom = ref(false)
const center = ref(false)
const left = ref(false)
const top = ref(false)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">四个方向 + 居中</p>
    <div class="demo-row">
      <jm-button type="primary" size="small" @click="bottom = true">底部</jm-button>
      <jm-button type="primary" size="small" @click="center = true">居中</jm-button>
      <jm-button type="primary" size="small" @click="left = true">左侧</jm-button>
      <jm-button type="primary" size="small" @click="top = true">顶部</jm-button>
    </div>

    <p class="demo-note">
      文档里的示例加了 <code>:teleport="false"</code>，弹层会限制在手机框内；真实项目默认挂到 body。
    </p>

    <jm-popup v-model:show="bottom" position="bottom" round closeable :teleport="false">
      <div class="sheet">
        <h4>底部弹出</h4>
        <p>带圆角、可点关闭按钮、点遮罩关闭。</p>
        <jm-button type="primary" block @click="bottom = false">知道了</jm-button>
      </div>
    </jm-popup>

    <jm-popup v-model:show="center" position="center" round :teleport="false">
      <div class="center-box">
        <h4>居中提示</h4>
        <p>适合二次确认、版本更新说明。</p>
      </div>
    </jm-popup>

    <jm-popup v-model:show="left" position="left" :teleport="false">
      <div class="side">
        <h4>侧边抽屉</h4>
        <p>宽度 76%，最大 320px。</p>
      </div>
    </jm-popup>

    <jm-popup v-model:show="top" position="top" round :teleport="false">
      <div class="sheet">
        <h4>顶部弹出</h4>
        <p>适合筛选条、通知条。</p>
      </div>
    </jm-popup>
  </div>
</template>

<style scoped>
.sheet {
  padding: 20px 18px 24px;
}

.center-box {
  width: 240px;
  padding: 20px 18px;
  text-align: center;
}

.side {
  padding: 60px 18px 20px;
}

h4 {
  margin: 0 0 6px;
  font-size: 15px;
  font-weight: 500;
  color: var(--jm-text-color);
}

p {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--jm-text-color-2);
}
</style>
