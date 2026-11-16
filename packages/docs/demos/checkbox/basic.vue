<script setup lang="ts">
import { ref } from 'vue'

const checked = ref(false)
const alone = ref(true)
const hobbies = ref<(string | number)[]>(['math'])
const terms = ref(false)
const subjects = ref<(string | number)[]>(['chinese', 'english'])
const half = ref(false)
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础</p>
    <div class="demo-row">
      <jm-checkbox v-model="checked" label="同意《用户协议》" />
      <jm-checkbox v-model="alone" label="默认选中" />
    </div>

    <p class="demo-label">形状：方形 / 圆形</p>
    <div class="demo-row">
      <jm-checkbox v-model="alone" label="方形" shape="square" />
      <jm-checkbox v-model="alone" label="圆形" shape="circle" />
    </div>

    <p class="demo-label">复选框组</p>
    <jm-checkbox-group v-model="hobbies">
      <jm-checkbox value="math" label="数学" />
      <jm-checkbox value="physics" label="物理" />
      <jm-checkbox value="code" label="编程" />
    </jm-checkbox-group>

    <p class="demo-label">竖排 + 自定义颜色</p>
    <jm-checkbox-group v-model="subjects" direction="vertical" color="#00B98A">
      <jm-checkbox value="chinese" label="语文" />
      <jm-checkbox value="english" label="英语" />
      <jm-checkbox value="history" label="历史" />
    </jm-checkbox-group>

    <p class="demo-label">半选 / 禁用</p>
    <div class="demo-row">
      <jm-checkbox :model-value="false" indeterminate label="全选（半选）" />
      <jm-checkbox :model-value="true" disabled label="禁用选中" />
      <jm-checkbox :model-value="false" disabled label="禁用" />
    </div>

    <p class="demo-note">已选：{{ hobbies.join('、') || '无' }}</p>
  </div>
</template>
