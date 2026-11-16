<script setup lang="ts">
import { ref } from 'vue'

const dense = ref(false)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">文字水印（插槽包裹内容）</p>
    <jm-watermark text="金智安 · 内部资料" :opacity="0.12" :gap="[90, 66]" :rotate="-20">
      <div class="card">
        <h4 class="card__title">第 3 讲 · 二次函数图像</h4>
        <p class="card__text">
          水印层铺在内容之上、不接收指针事件，所以不影响选择、点击与滚动。
        </p>
        <p class="card__text">讲义编号：JZA-MATH-0307</p>
      </div>
    </jm-watermark>

    <p class="demo-label">多行 + 密度</p>
    <jm-watermark
      :text="['仅限本人使用', '请勿外传']"
      :opacity="0.16"
      :gap="dense ? [72, 56] : [120, 96]"
      :font-size="12"
      :rotate="dense ? -30 : -18"
    >
      <div class="card card--tall">
        <p class="card__text">试读章节 · 面积法求阴影部分</p>
        <p class="card__text">这段内容常被截图转发，加上水印便于追溯来源。</p>
      </div>
    </jm-watermark>
    <div class="actions">
      <jm-button size="small" plain type="primary" @click="dense = !dense">
        {{ dense ? '稀疏' : '密集' }}
      </jm-button>
    </div>

    <p class="demo-label">纯覆盖层（不给插槽，铺满父容器）</p>
    <div class="stage">
      <jm-watermark text="草稿" :opacity="0.2" :font-size="16" :gap="[110, 80]" />
      <span class="stage__text">父容器需要 relative 定位</span>
    </div>
  </div>
</template>

<style scoped>
.card {
  padding: 14px;
  border-radius: 12px;
  background: var(--jm-bg-container);
}

.card--tall {
  min-height: 110px;
}

.card__title {
  margin: 0 0 6px;
  font-size: 15px;
}

.card__text {
  margin: 0 0 4px;
  color: var(--jm-text-color-2);
  font-size: 13px;
  line-height: 1.7;
}

.actions {
  margin-top: 10px;
}

.stage {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 96px;
  border-radius: 12px;
  background: var(--jm-bg-input);
}

.stage__text {
  color: var(--jm-text-color-3);
  font-size: 13px;
}
</style>
