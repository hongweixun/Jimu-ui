<script setup lang="ts">
import { computed, ref } from 'vue'

const page = ref(1)
const many = ref(6)
const simple = ref(3)

const total = 96
const pageSize = 10
const pageCount = computed(() => Math.ceil(total / pageSize))
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：共 {{ total }} 条 / 每页 {{ pageSize }} 条</p>
    <jm-pagination v-model="page" :total="total" :page-size="pageSize" />

    <p class="demo-label">页码很多（10 页）</p>
    <jm-pagination v-model="many" :page-count="pageCount" />

    <p class="demo-label">只显示箭头</p>
    <jm-pagination v-model="many" :page-count="pageCount" icon-only />

    <p class="demo-label">简单模式</p>
    <jm-pagination v-model="simple" simple :total="total" :page-size="pageSize" />

    <p class="demo-label">禁用</p>
    <jm-pagination :model-value="2" :page-count="6" disabled />

    <p class="demo-note">
      当前第 {{ page }} 页，第 {{ many }} 页（多页码），简单模式第 {{ simple }} 页。
    </p>
  </div>
</template>
