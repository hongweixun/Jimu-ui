<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const tab = ref<string | number>('all')
const week = ref<string | number>('mon')
const withIcon = ref<string | number>('list')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '进行中', value: 'doing' },
  { label: '已结束', value: 'done' },
]

const weeks = [
  { label: '一', value: 'mon' },
  { label: '二', value: 'tue' },
  { label: '三', value: 'wed' },
  { label: '四', value: 'thu' },
  { label: '五', value: 'fri' },
  { label: '六', value: 'sat', disabled: true },
  { label: '日', value: 'sun', disabled: true },
]

const views = [
  { label: '列表', value: 'list', icon: 'sort' },
  { label: '课表', value: 'calendar', icon: 'calendar' },
  { label: '附件', value: 'file', icon: 'file' },
]

function onChange(value: string | number) {
  showToast(`切换到 ${value}`)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础</p>
    <jm-segmented v-model="tab" :options="tabs" @change="onChange" />

    <p class="demo-label">小号 / 等宽七段</p>
    <jm-segmented v-model="week" :options="weeks" size="small" />

    <p class="demo-label">带图标</p>
    <jm-segmented v-model="withIcon" :options="views" size="large" @change="onChange" />

    <p class="demo-label">禁用整组</p>
    <jm-segmented v-model="tab" :options="tabs" disabled />

    <p class="demo-note">
      滑块宽度按段数均分，段数变化会自动重算；禁用的单段不响应点击，但滑块仍会停在它的位置。
    </p>
  </div>
</template>
