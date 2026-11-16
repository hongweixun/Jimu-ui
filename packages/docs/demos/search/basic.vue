<script setup lang="ts">
import { ref } from 'vue'

const keyword = ref('')
const submitted = ref('')
const keyword2 = ref('三年级数学')

function onSearch(v: string) {
  submitted.value = v || '（空）'
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（回车或点放大镜触发 search）</p>
    <jm-search v-model="keyword" placeholder="搜索课程、老师" @search="onSearch" />

    <p class="demo-label">方形 + 取消按钮</p>
    <jm-search
      v-model="keyword2"
      shape="square"
      show-cancel
      cancel-text="取消"
      @search="onSearch"
      @cancel="submitted = '点了取消'"
    />

    <p class="demo-label">尺寸</p>
    <jm-search v-model="keyword" size="small" placeholder="小号" />
    <jm-search v-model="keyword" size="large" placeholder="大号" />

    <p class="demo-label">禁用 / 只读</p>
    <jm-search model-value="禁用状态不可输入" disabled />
    <jm-search model-value="只读，仅展示" readonly />

    <p class="demo-note">已提交：{{ submitted || '还没搜过' }}</p>
  </div>
</template>
