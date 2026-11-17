<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const value = ref('https://cli.im/')
const level = ref<'L' | 'M' | 'Q' | 'H'>('M')
const dotStyle = ref<'square' | 'rounded' | 'dots'>('square')
const useGradient = ref(false)
const useLogo = ref(false)
const qrRef = ref<any>(null)

const levels = ['L', 'M', 'Q', 'H'] as const
const styles = ['square', 'rounded', 'dots'] as const

function download() {
  const url = qrRef.value?.toDataURL?.(2)
  if (!url) return
  const a = document.createElement('a')
  a.href = url
  a.download = 'qrcode.png'
  a.click()
  showToast({ message: '已导出 2x PNG', type: 'success' })
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（跟随内容实时生成）</p>
    <div class="center">
      <jm-qrcode :value="value || ' ' " :size="180" />
    </div>
    <jm-input v-model="value" placeholder="修改内容，二维码实时刷新" clearable />

    <p class="demo-label">纠错级别（放 Logo 建议 H）</p>
    <div class="row">
      <button
        v-for="lv in levels"
        :key="lv"
        class="chip"
        :class="{ 'is-on': level === lv }"
        @click="level = lv"
      >
        {{ lv }}
      </button>
      <span class="note">{{ { L: '7%', M: '15%', Q: '25%', H: '30%' }[level] }} 可纠正</span>
    </div>

    <p class="demo-label">码点样式 + 渐变 + Logo</p>
    <div class="row">
      <button
        v-for="st in styles"
        :key="st"
        class="chip"
        :class="{ 'is-on': dotStyle === st }"
        @click="dotStyle = st"
      >
        {{ st }}
      </button>
      <button class="chip" :class="{ 'is-on': useGradient }" @click="useGradient = !useGradient">渐变</button>
      <button class="chip" :class="{ 'is-on': useLogo }" @click="useLogo = !useLogo">Logo</button>
    </div>
    <div class="center">
      <jm-qrcode
        ref="qrRef"
        :value="value || ' '"
        :size="180"
        :level="level"
        :dot-style="dotStyle"
        :fg-color="useGradient ? '#00A0E9' : '#000000'"
        :fg-color2="useGradient ? '#6A5AE0' : undefined"
        :bg-color="'#ffffff'"
        :logo="useLogo ? 'https://hongweixun.github.io/Jimu-ui/logo.svg' : undefined"
        :logo-radius="10"
      />
    </div>

    <p class="demo-label">导出 PNG（ref.toDataURL）</p>
    <button class="chip chip--primary" @click="download">下载 2x PNG</button>

    <p class="demo-note">
      纯 TS 实现的编码器（版本 1~40、字节模式、掩码自动择优），已通过 jsQR 解码回环与 Nayuki 参考实现的逐模块矩阵比对。
    </p>
  </div>
</template>

<style scoped>
.center {
  display: flex;
  justify-content: center;
  padding: 8px 0 12px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.chip {
  padding: 6px 12px;
  border: var(--jm-border-width) solid var(--jm-border-color-2);
  border-radius: var(--jm-radius-round);
  background: transparent;
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-sm);
  cursor: pointer;
}

.chip.is-on {
  background: var(--jm-color-primary);
  border-color: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
}

.chip--primary {
  background: var(--jm-color-primary);
  border-color: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
}

.note {
  font-size: var(--jm-font-size-xs);
  color: var(--jm-text-color-3);
}
</style>
