<script setup lang="ts">
import { ref } from 'vue'
import { showToast, closeToast } from 'jimu-ui'

const host = ref<HTMLElement | null>(null)

function text() {
  showToast({ message: '已保存', target: host.value })
}

function success() {
  showToast({ message: '提交成功', type: 'success', target: host.value })
}

function fail() {
  showToast({ message: '网络异常，请稍后重试', type: 'fail', target: host.value })
}

function loading() {
  showToast({ message: '正在上传…', type: 'loading', target: host.value })
  setTimeout(() => closeToast(), 1500)
}

function top() {
  showToast({ message: '顶部提示', position: 'top', target: host.value })
}
</script>

<template>
  <div ref="host" class="demo-relative demo-page">
    <div class="demo-row">
      <jm-button size="small" @click="text">文字</jm-button>
      <jm-button size="small" type="success" @click="success">成功</jm-button>
      <jm-button size="small" type="danger" @click="fail">失败</jm-button>
      <jm-button size="small" type="primary" @click="loading">加载</jm-button>
      <jm-button size="small" variant="outline" @click="top">顶部</jm-button>
    </div>

    <p class="demo-note">
      <code>showToast()</code> 是函数式调用，不需要在模板里放组件。传 <code>target</code> 可以把提示限制在指定容器内。
    </p>
  </div>
</template>
