<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import { hideLoadingBar, showLoadingBar } from 'jimu-ui'

const root = ref<HTMLElement | null>(null)
const status = ref('空闲')

/** 演示用：把加载条限制在手机模拟框内，真实项目不传 target 就贴在浏览器顶部 */
function scope() {
  return (root.value?.closest('.phone__screen') as HTMLElement | null) ?? null
}

function mockRequest(ok: boolean) {
  status.value = '请求中…'
  const bar = showLoadingBar({ target: scope() })
  window.setTimeout(() => {
    if (ok) {
      bar.finish()
      status.value = '请求完成'
    } else {
      bar.error()
      status.value = '请求失败'
    }
  }, 1500)
}

function parallel() {
  status.value = '两个并发任务'
  const first = showLoadingBar({ target: scope() })
  const second = showLoadingBar({ target: scope() })
  window.setTimeout(() => first.finish(), 900)
  window.setTimeout(() => second.finish(), 2000)
}

function manual() {
  status.value = '手动推进'
  const bar = showLoadingBar({ target: scope(), progress: 8 })
  let progress = 8
  const timer = window.setInterval(() => {
    progress += 14
    bar.update(progress)
    if (progress >= 100) {
      window.clearInterval(timer)
      bar.finish()
      status.value = '手动推进完成'
    }
  }, 200)
}

onBeforeUnmount(hideLoadingBar)
</script>

<template>
  <div ref="root" class="demo-page">
    <jm-button block @click="mockRequest(true)">模拟请求（成功）</jm-button>
    <jm-button block variant="outline" @click="mockRequest(false)">模拟请求（失败）</jm-button>
    <jm-button block variant="ghost" @click="parallel">两个并发任务</jm-button>
    <jm-button block variant="ghost" @click="manual">手动推进进度</jm-button>
    <p class="demo-tip">
      状态：{{ status }}。调用 showLoadingBar() 拿到的控制器可以 update / finish / error，
      不手动推进时会自动朝 94% 收敛，结束时才补满。
    </p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}
</style>
