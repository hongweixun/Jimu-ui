<script setup lang="ts">
import { ref } from 'vue'
import { showNotify, closeNotify } from 'jimu-ui'

const host = ref<HTMLElement | null>(null)
const show = ref(false)
const lastId = ref(0)

const types = [
  { type: 'primary', label: '普通通知' },
  { type: 'success', label: '成功' },
  { type: 'warning', label: '警告' },
  { type: 'danger', label: '错误' },
] as const

function fire(type: 'primary' | 'success' | 'warning' | 'danger', index: number) {
  lastId.value = showNotify({
    type,
    title: ['提示', '提交成功', '注意', '操作失败'][index],
    message: [
      '您有一条新的课程提醒，点击查看详情。',
      '作业已提交，老师批改后会通知你。',
      '还有 2 项资料未完善，可能影响开课。',
      '网络异常，请稍后重试。',
    ][index],
    target: host.value,
    duration: 2600,
  })
}

function stack() {
  showNotify({ type: 'primary', message: '正在同步通讯录…', target: host.value, duration: 0 })
  showNotify({ type: 'success', message: '同步完成，共 128 位联系人', target: host.value, duration: 3000 })
}

function closeAll() {
  closeNotify()
  show.value = false
}
</script>

<template>
  <div class="demo-page">
    <!-- 函数式通知的挂载点：绝对定位在演示区顶部 -->
    <div ref="host" class="notify-stage" />

    <p class="demo-label">函数式：showNotify()</p>
    <div class="demo-row">
      <jm-button
        v-for="(item, i) in types"
        :key="item.type"
        size="small"
        :type="item.type === 'danger' ? 'danger' : item.type === 'success' ? 'success' : 'default'"
        @click="fire(item.type, i)"
        >{{ item.label }}</jm-button
      >
    </div>

    <div class="demo-row">
      <jm-button size="small" plain @click="stack">连续两条堆叠</jm-button>
      <jm-button size="small" plain @click="closeAll">全部关闭</jm-button>
    </div>

    <p class="demo-label">组件式：v-model:show</p>
    <div class="notify-stage">
      <jm-notify
        v-model:show="show"
        inline
        type="primary"
        title="课程即将开始"
        message="《高等数学》直播课 5 分钟后开始，做好准备。"
        :duration="4000"
      />
    </div>
    <jm-button size="small" block @click="show = true">显示顶部通知</jm-button>

    <p class="demo-note">
      组件式适合「常驻一条横幅」；函数式适合接口回来时就地弹一条，同一个 message 重复触发只会更新，不会叠成三条。
    </p>
  </div>
</template>

<style scoped>
.notify-stage {
  position: relative;
  height: 0;
}
</style>
