<script setup lang="ts">
import { computed, ref } from 'vue'

const subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理']
const picked = ref<string[]>(['数学', '英语'])

const grades = ['一年级', '二年级', '三年级']
const grade = ref('二年级')

const tags = computed(() => subjects.map((s) => ({ label: s, checked: picked.value.includes(s) })))

function toggle(label: string, value: boolean) {
  picked.value = value
    ? [...picked.value, label]
    : picked.value.filter((item) => item !== label)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">多选：v-model 绑定每一项</p>
    <div class="tags">
      <jm-check-tag
        v-for="tag in tags"
        :key="tag.label"
        :model-value="tag.checked"
        @update:model-value="(v: boolean) => toggle(tag.label, v)"
        >{{ tag.label }}</jm-check-tag
      >
    </div>

    <p class="demo-label">单选（互斥）</p>
    <div class="tags">
      <jm-check-tag
        v-for="g in grades"
        :key="g"
        :model-value="grade === g"
        :checked-color="grade === g ? '#00A0E9' : undefined"
        @update:model-value="grade = g"
        >{{ g }}</jm-check-tag
      >
    </div>

    <p class="demo-label">尺寸与形状</p>
    <div class="tags">
      <jm-check-tag size="small" model-value>小号 24</jm-check-tag>
      <jm-check-tag model-value>默认 28</jm-check-tag>
      <jm-check-tag size="large" shape="square" model-value>大号方形</jm-check-tag>
      <jm-check-tag disabled>禁用</jm-check-tag>
      <jm-check-tag disabled model-value>禁用选中</jm-check-tag>
    </div>

    <p class="demo-note">
      传 checkedColor 会变成实底白字，不传则走主色浅底 + 主色文字，后者的信息密度更小、更适合一屏多个标签。
    </p>
  </div>
</template>

<style scoped>
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
