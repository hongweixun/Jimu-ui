<script setup lang="ts">
import { ref } from 'vue'

const msg = ref('点一下左侧箭头试试')

function back() {
  msg.value = '触发了 click-left（业务里通常是 router.back()）'
}

function edit() {
  msg.value = '触发了 click-right'
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：返回 + 标题</p>
    <div class="demo-box">
      <jm-nav-bar title="课程详情" left-arrow left-text="返回" @click-left="back" />
    </div>

    <p class="demo-label">右侧操作</p>
    <div class="demo-box">
      <jm-nav-bar
        title="我的班级"
        left-arrow
        right-text="编辑"
        @click-left="back"
        @click-right="edit"
      />
    </div>

    <p class="demo-label">自定义品牌色（无描边）</p>
    <div class="demo-box">
      <jm-nav-bar background="#00A0E9" color="#ffffff" :border="false" left-arrow>
        <template #title>
          <span style="font-weight: 600">金智安教育</span>
        </template>
        <template #right>
          <span style="display: flex; width: 20px; height: 20px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="11" cy="11" r="6.5" />
              <path d="M16 16l4.5 4.5" stroke-linecap="round" />
            </svg>
          </span>
        </template>
      </jm-nav-bar>
    </div>

    <p class="demo-note">{{ msg }}</p>
  </div>
</template>

<style scoped>
.demo-box {
  overflow: hidden;
  border: 1px solid var(--jm-border-color);
  border-radius: 12px;
}
</style>
