<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)

const actions = [
  { name: 'point', label: '积分兑换课程券', subLabel: '1200 积分' },
  { name: 'goods', label: '兑换周边礼品' },
  { name: 'rule', label: '查看积分规则' },
]

/** 标题区加高，背景图才有发挥空间；说明文字转白 */
const headerStyle: Record<string, string> = {
  '--jm-action-sheet-header-min-height': '96px',
  '--jm-action-sheet-subtitle-color': 'rgba(255, 255, 255, 0.85)',
  '--jm-action-sheet-close-color': 'rgba(255, 255, 255, 0.8)',
  '--jm-action-sheet-header-border': 'transparent',
}
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="show = true">标题区背景图</jm-button>

    <jm-action-sheet
      v-model:show="show"
      title="积分商城"
      description="用学习积分兑换课程与周边"
      :actions="actions"
      title-image="/img/as-header.svg"
      title-color="#ffffff"
      :style="headerStyle"
      closeable
      :teleport="false"
    />

    <p class="demo-note">
      title-image 直接传图片地址（自动补 url()），标题区高度用 --jm-action-sheet-header-min-height 加高。
    </p>
  </div>
</template>
