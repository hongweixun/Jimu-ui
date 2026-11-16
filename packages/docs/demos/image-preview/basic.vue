<script setup lang="ts">
import { ref } from 'vue'
import { showImagePreview } from 'jimu-ui'

const svg = (text: string, from: string, to: string) => {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="800"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="600" height="800" fill="url(#g)"/><text x="300" y="420" font-family="system-ui" font-size="46" fill="#fff" text-anchor="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const images = [
  svg('1', '#00A0E9', '#2B6BE4'),
  svg('2', '#FF8A3D', '#FF6430'),
  svg('3', '#22C55E', '#0E9F6E'),
  svg('4', '#7C4DFF', '#4A2ECC'),
]

const show = ref(false)
const start = ref(0)
const stage = ref<HTMLElement | null>(null)

function open(i: number) {
  start.value = i
  show.value = true
}

function openByFn(i: number) {
  showImagePreview({
    images,
    startPosition: i,
    target: stage.value,
    onChange: (idx) => (lastFnIndex.value = idx),
  })
}

const lastFnIndex = ref(0)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">点击缩略图打开预览（组件方式，限制在手机框内）</p>
    <div class="stage" ref="stage">
      <div class="thumbs">
        <jm-image
          v-for="(src, i) in images"
          :key="i"
          :src="src"
          :width="64"
          :height="64"
          :radius="8"
          clickable
          @click="open(i)"
        />
      </div>

      <jm-image-preview
        v-model:show="show"
        :images="images"
        :start-position="start"
        :teleport="false"
      />
    </div>

    <p class="demo-label">函数式调起（showImagePreview）</p>
    <div class="demo-row">
      <jm-button size="small" @click="openByFn(0)">第 1 张</jm-button>
      <jm-button size="small" @click="openByFn(2)">第 3 张</jm-button>
    </div>
    <p class="demo-note">函数式版本会用 onChange 回调同步当前页，最近一次：第 {{ lastFnIndex + 1 }} 张。左右滑动或点底部圆点切换。</p>
  </div>
</template>

<style scoped>
/* 注意：不要给 .stage 设 position:relative——
   teleprint=false 的预览与函数式的 target 宿主都是 absolute inset:0，
   需要锚到手机框（最近的定位祖先）才能铺满整个模拟器 */
.thumbs {
  display: flex;
  gap: 10px;
}
</style>
