<script setup lang="ts">
/** 造一张渐变封面图，避免 demo 依赖外部图片 */
function cover(label: string, w: number, h: number, from: string, to: string) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/>
    </linearGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#g)"/>
    <text x="${w / 2}" y="${h / 2}" font-family="system-ui" font-size="${Math.min(w, h) * 0.14}"
      fill="#ffffff" text-anchor="middle" dominant-baseline="middle" opacity="0.92">${label}</text>
  </svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

const courses = [
  {
    id: 1,
    title: '零基础学 Vue 3 组合式 API',
    desc: '从 setup 到 composable，用 12 个小项目把响应式吃透',
    thumb: cover('Vue 3', 640, 360, '#00A0E9', '#2B6BE4'),
    price: 199,
    originPrice: 399,
    tags: ['共 24 讲', '可回放'],
    extra: '1.2 万人学过',
  },
  {
    id: 2,
    title: '移动端动效设计实战：从手势到物理',
    desc: '60fps 的手势跟手、回弹与打断，全部用原生 Pointer 事件实现',
    thumb: cover('Motion', 640, 360, '#FF8A3D', '#FF5B30'),
    price: 128,
    originPrice: 268,
    tags: ['新课', '含源码'],
    extra: '昨天上新',
  },
]

function onBuy(id: number) {
  alert(`加入购物车：课程 ${id}`)
}
</script>

<template>
  <div class="demo-page">
    <jm-card
      v-for="c in courses"
      :key="c.id"
      :title="c.title"
      :desc="c.desc"
      :thumb="c.thumb"
      :price="c.price"
      :origin-price="c.originPrice"
      :tags="c.tags"
      :extra="c.extra"
      clickable
      shadow="always"
    >
      <template #footer>
        <jm-button size="small" variant="text">查看详情</jm-button>
        <jm-button size="small" @click="onBuy(c.id)">立即报名</jm-button>
      </template>
    </jm-card>

    <p class="demo-tip">封面在上方时按 16:9 撑开，价格数字自动格式化成千分位两位小数。</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 12px;
}
</style>
