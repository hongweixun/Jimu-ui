<script setup lang="ts">
import { ref } from 'vue'
import { showSnackbar, clearSnackbar } from 'jimu-ui'

let loadingBar: { clear: () => void } | null = null

function open(type: string) {
  const texts: Record<string, string> = {
    normal: '草稿已自动保存',
    success: '提交成功，审核将在 1 个工作日内完成',
    warning: '当前网络不稳定，操作可能延迟',
    info: '有 3 条新公告，点击查看',
    error: '保存失败，请检查网络后重试',
  }
  showSnackbar({ type: type as any, content: texts[type] ?? type, position: 'top' })
}

function openBottom() {
  showSnackbar({
    content: '已加入购物车',
    position: 'bottom',
    action: '去结算',
    onAction: () => showToastTip('跳转结算页'),
  })
}

function showToastTip(msg: string) {
  // Snackbar 的 action 里再弹一个提示
  import('jimu-ui').then(({ showToast }) => showToast({ message: msg, type: 'success' }))
}

function openVertical() {
  showSnackbar({
    content: '检测到新版本 v3.2.0，是否立即更新？',
    vertical: true,
    action: '立即更新',
    onAction: () => {},
  })
}

function openLoading() {
  loadingBar = showSnackbar.loading({ content: '正在同步数据…', position: 'top' })
  setTimeout(() => {
    loadingBar?.clear()
    showSnackbar.success('同步完成')
  }, 2000)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">类型（默认单例，新的顶掉旧的）</p>
    <div class="row">
      <button class="chip" @click="open('normal')">普通</button>
      <button class="chip chip--success" @click="open('success')">成功</button>
      <button class="chip chip--warning" @click="open('warning')">警告</button>
      <button class="chip chip--error" @click="open('error')">错误</button>
      <button class="chip chip--info" @click="open('info')">消息</button>
    </div>

    <p class="demo-label">底部显示 + 操作按钮</p>
    <button class="chip chip--primary" @click="openBottom">底部消息条</button>

    <p class="demo-label">竖排（内容 + 按钮上下两行）</p>
    <button class="chip" @click="openVertical">竖排消息条</button>

    <p class="demo-label">加载（常驻，需手动关闭）</p>
    <button class="chip" @click="openLoading">同步数据</button>

    <p class="demo-label">手动关闭全部</p>
    <button class="chip chip--ghost" @click="clearSnackbar">clearSnackbar()</button>

    <p class="demo-note">
      Snackbar 与 Toast 的区别：Snackbar 是带操作按钮的横条，适合「发生了什么 + 你可以怎么办」；Toast 是轻提示，只适合「告诉你一声」。
    </p>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 8px 14px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-sm);
  box-shadow: var(--jm-elevation-1);
  cursor: pointer;
}

.chip--primary { background: var(--jm-color-primary); color: var(--jm-color-primary-contrast); }
.chip--success { background: var(--jm-color-success); color: var(--jm-color-success-contrast); }
.chip--warning { background: var(--jm-color-warning); color: var(--jm-color-warning-contrast); }
.chip--error { background: var(--jm-color-danger); color: var(--jm-color-danger-contrast); }
.chip--info { background: var(--jm-color-info); color: var(--jm-color-info-contrast); }
.chip--ghost { background: transparent; border: var(--jm-border-width) solid var(--jm-border-color-2); }
</style>
