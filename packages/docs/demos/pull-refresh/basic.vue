<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const items = ref(['晨读打卡', '单词听写', '口算练习', '阅读记录'])

function onRefresh() {
  setTimeout(() => {
    items.value = [`刚刷新 · ${new Date().toLocaleTimeString('zh-CN', { hour12: false })}`, ...items.value.slice(0, 3)]
    loading.value = false
  }, 1200)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">在下方区域下拉（先滚到顶部）</p>
    <div class="scroller">
      <jm-pull-refresh v-model="loading" @refresh="onRefresh">
        <div class="body">
          <div v-for="(it, i) in items" :key="`${it}-${i}`" class="row">
            <span class="row__index">{{ i + 1 }}</span>
            <span>{{ it }}</span>
          </div>
          <div v-for="n in 8" :key="`fill-${n}`" class="row is-muted">占位内容 {{ n }}</div>
        </div>
      </jm-pull-refresh>
    </div>
    <p class="demo-note">加载状态由 <code>v-model</code> 控制：业务请求结束后置回 false，组件会先显示"刷新成功"再回弹。</p>

    <p class="demo-label">禁用下拉</p>
    <div class="scroller is-short">
      <jm-pull-refresh disabled>
        <div class="body">
          <div class="row is-muted">这一块禁用了下拉刷新</div>
        </div>
      </jm-pull-refresh>
    </div>
  </div>
</template>

<style scoped>
.scroller {
  height: 240px;
  overflow-y: auto;
  border-radius: 12px;
  background: var(--jm-bg-container);
  -webkit-overflow-scrolling: touch;
}

.scroller.is-short {
  height: 72px;
}

.body {
  padding: 10px 14px;
}

.row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid var(--jm-border-color);
  font-size: 13px;
  color: var(--jm-text-color-2);
}

.row:last-child {
  border-bottom: 0;
}

.row.is-muted {
  color: var(--jm-text-color-4);
}

.row__index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 6px;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 11px;
}
</style>
