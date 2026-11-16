<script setup lang="ts">
import { ref } from 'vue'

const plan = ref('month')
const grade = ref('g1')
const style = ref('solid')
const theme = ref('light')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：图标变色，文字保持常规色</p>
    <jm-radio-group v-model="plan">
      <jm-radio value="month" label="月付" />
      <jm-radio value="season" label="季付" />
      <jm-radio value="year" label="年付" />
    </jm-radio-group>

    <p class="demo-label">竖排</p>
    <jm-radio-group v-model="grade" direction="vertical">
      <jm-radio value="g1" label="高一" />
      <jm-radio value="g2" label="高二" />
      <jm-radio value="g3" label="高三" />
    </jm-radio-group>

    <p class="demo-label">圆点样式：实心 / 空心环</p>
    <jm-radio-group v-model="style">
      <jm-radio value="solid" label="实心" dot="solid" />
      <jm-radio value="ring" label="空心环" dot="ring" />
    </jm-radio-group>

    <p class="demo-label">文字跟随主色（label-color="active"）</p>
    <jm-radio-group v-model="theme">
      <jm-radio value="light" label="浅色" label-color="active" />
      <jm-radio value="dark" label="深色" label-color="active" />
    </jm-radio-group>

    <p class="demo-label">自定义颜色 / 尺寸 / 禁用</p>
    <jm-radio-group v-model="plan" color="#7C4DFF">
      <jm-radio value="month" label="紫色小号" size="small" />
      <jm-radio value="season" label="紫色大号" size="large" />
    </jm-radio-group>
    <div class="demo-row">
      <jm-radio :model-value="'x'" value="x" disabled label="禁用选中" />
      <jm-radio :model-value="'y'" value="x" disabled label="禁用" />
    </div>

    <p class="demo-note">当前选中：{{ plan }} / {{ grade }} · 点击选中项可以看到从图标散开的水波纹</p>
  </div>
</template>
