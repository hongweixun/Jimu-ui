<script setup lang="ts">
import { ref } from 'vue'

const lastClick = ref('')

const entries = [
  { text: '首页', icon: 'M4 11l8-7 8 7v8a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z', badge: '' },
  { text: '课程', icon: 'M4 5h16v11H4zM8 20h8', badge: '12' },
  { text: '报表', icon: 'M5 19V9M12 19V5M19 19v-7', badge: '' },
  { text: '我的', icon: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM5 20c1.5-3.5 4-5 7-5s5.5 1.5 7 5', badge: '' },
]

const rows = [
  { text: '待办审批', icon: 'M5 5h14v14H5zM8 10h8M8 14h5' },
  { text: '数据看板', icon: 'M4 19h16M7 15V9M12 15V6M17 15v-4' },
  { text: '班级管理', icon: 'M12 12a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM4 20c1-4 4-6 8-6s7 2 8 6' },
  { text: '系统设置', icon: 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 3v3M12 18v3M4 12h3M17 12h3' },
]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">四列入口（可点击、带角标）</p>
    <jm-grid :columns="4" gutter="6" clickable @click="(i) => (lastClick = `第 ${i + 1} 个：${entries[i].text}`)">
      <jm-grid-item v-for="it in entries" :key="it.text" :text="it.text" :icon="it.icon" :badge="it.badge" />
    </jm-grid>
    <p class="demo-note">最近点击：{{ lastClick || '还没有点击' }}</p>

    <p class="demo-label">三列正方形 + 细线 + 卡片圆角</p>
    <jm-grid :columns="3" square border :gutter="1" :radius="12" background="var(--jm-bg-container)">
      <jm-grid-item v-for="n in 6" :key="n" :text="`格子 ${n}`" dot />
    </jm-grid>

    <p class="demo-label">图标在左（direction=column，列表式）</p>
    <jm-grid :columns="2" direction="column" gutter="8" clickable>
      <jm-grid-item v-for="it in rows" :key="it.text" :text="it.text" :icon="it.icon" :icon-size="22" />
    </jm-grid>
  </div>
</template>
