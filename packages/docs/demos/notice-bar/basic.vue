<script setup lang="ts">
import { ref } from 'vue'

const shows = ref(['notice1', 'notice2', 'notice3', 'notice4'])
const clickTip = ref('')

function close(name: string) {
  shows.value = shows.value.filter((n) => n !== name)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">跑马灯（超长文案自动滚动）</p>
    <jm-notice-bar
      v-if="shows.includes('notice1')"
      text="9 月新学期报名开始啦，早鸟价立减 300 元，名额有限先到先得，详情咨询班主任老师。"
      @close="close('notice1')"
    />

    <p class="demo-label">可关闭</p>
    <jm-notice-bar
      v-if="shows.includes('notice2')"
      text="本周六 20:00 直播课临时调整到周日同一时间，请留意通知。"
      mode="closeable"
      @close="close('notice2')"
    />

    <p class="demo-label">可点击（link）</p>
    <jm-notice-bar
      v-if="shows.includes('notice3')"
      text="您的试听课程已排好，点击查看详情"
      mode="link"
      @click="clickTip = '点了整条通知'"
    />

    <p class="demo-label">允许换行 + 自定义配色</p>
    <jm-notice-bar
      v-if="shows.includes('notice4')"
      text="因台风天气，9 月 16 日（周三）线下课程暂停一次，课时顺延，线上答疑照常进行。"
      wrapable
      color="#8A4B00"
      background="#FFF4E5"
    />

    <p v-if="shows.length === 0" class="demo-note">都关掉了，刷新页面可恢复</p>
    <p v-else-if="clickTip" class="demo-note">{{ clickTip }}</p>
  </div>
</template>
