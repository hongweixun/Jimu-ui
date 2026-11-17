<script setup lang="ts">
import { computed, ref } from 'vue'
import { showToast } from 'jimu-ui'

const page = ref(1)
const many = ref(6)
const simple = ref(3)
const size = ref(10)

const total = 96
const pageSize = 10
const pageCount = computed(() => Math.ceil(total / pageSize))

function onChange(p: number, s: number) {
  showToast(`第 ${p} 页 · 每页 ${s} 条`)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：共 {{ total }} 条 / 每页 {{ size }} 条</p>
    <jm-pagination
      v-model="page"
      v-model:page-size="size"
      :total="total"
      show-size-changer
      @change="onChange"
    />

    <p class="demo-label">页码很多（10 页）</p>
    <jm-pagination v-model="many" :page-count="pageCount" />

    <p class="demo-label">总数 + 快速跳转</p>
    <jm-pagination v-model="many" :page-count="pageCount" :total="total" show-quick-jumper>
      <template #total="{ total: t, range }">
        共 {{ t }} 条，当前 {{ range[0] }}-{{ range[1] }} 条
      </template>
    </jm-pagination>

    <p class="demo-label">简单模式</p>
    <jm-pagination v-model="simple" simple :total="total" :page-size="pageSize" />

    <p class="demo-label">禁用</p>
    <jm-pagination :model-value="2" :page-count="6" disabled />

    <p class="demo-note">
      当前第 {{ page }} 页、每页 {{ size }} 条；第 {{ many }} 页（多页码）；简单模式第 {{ simple }} 页。
    </p>
  </div>
</template>
