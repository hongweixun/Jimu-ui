<script setup lang="ts">
import { ref } from 'vue'

function svg(text: string, from: string, to: string, w = 500, h = 320) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="${w}" height="${h}" fill="url(#g)"/><text x="50%" y="50%" font-family="system-ui,-apple-system,sans-serif" font-size="26" fill="#fff" text-anchor="middle" dominant-baseline="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const scanning = ref(true)
const withGrid = ref(true)
const duration = ref(1800)
const img = svg('待识别的作业题', '#1F2A44', '#0B1220')

function toggle() {
  scanning.value = !scanning.value
}
</script>

<template>
  <div class="demo-page">
    <div class="ctl">
      <button class="btn" type="button" @click="toggle">
        {{ scanning ? '停止扫描' : '开始扫描' }}
      </button>
      <button class="btn" type="button" @click="withGrid = !withGrid">
        网格暗纹：{{ withGrid ? '开' : '关' }}
      </button>
      <label class="dur">
        时长
        <input v-model.number="duration" type="range" min="800" max="3600" step="200" />
        {{ duration }}ms
      </label>
    </div>

    <jm-scanner
      :active="scanning"
      :duration="duration"
      :show-grid="withGrid"
      :height="190"
    >
      <img :src="img" alt="待识别内容" />
    </jm-scanner>

    <jm-scanner
      :active="scanning"
      :duration="duration"
      line-color="#34D399"
      :height="120"
      corner-size="18"
    />

    <p class="demo-tip">
      上：slot 内容 + 默认主色扫描线；下：无 slot 占位、绿色扫描线、小角标。
      active=false 时线停住；系统「减少动效」时线停在中线。
    </p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.ctl {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.btn {
  padding: 6px 12px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-primary);
  /* 实心主色底上必须用对比色文字；--jm-color-primary-text 是浅底蓝字，会蓝底蓝字 */
  color: var(--jm-color-primary-contrast, #fff);
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  cursor: pointer;
}

.dur {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.demo-tip {
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}
</style>
