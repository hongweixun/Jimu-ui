<script setup lang="ts">
import { ref } from 'vue'

const pushOn = ref(true)
const autoPlay = ref(false)
</script>

<template>
  <div class="demo-page">
    <jm-cell-group title="账号设置">
      <jm-cell title="头像" is-link>
        <template #right>
          <span class="avatar">Z</span>
        </template>
      </jm-cell>
      <jm-cell title="昵称" value="张小安" is-link />
      <jm-cell title="手机号" value="138****6688" is-link />
      <jm-cell title="消息推送" label="关闭后将不再收到课程提醒">
        <jm-switch v-model="pushOn" />
      </jm-cell>
    </jm-cell-group>

    <jm-cell-group title="播放设置">
      <jm-cell title="自动播放下一节">
        <jm-switch v-model="autoPlay" size="small" />
      </jm-cell>
      <jm-cell title="缓存空间" value="128 MB" is-link clickable />
      <jm-cell title="版本" value="1.4.2" />
    </jm-cell-group>

    <p class="demo-note">Cell 只负责布局与点击反馈，右侧内容完全由插槽决定。</p>
  </div>
</template>

<style scoped>
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary-text);
  font-size: 13px;
  font-weight: 500;
}
</style>
