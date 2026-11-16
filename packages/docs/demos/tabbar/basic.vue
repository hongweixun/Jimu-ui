<script setup lang="ts">
import { ref } from 'vue'

const active = ref<string | number>('home')
const active2 = ref<string | number>('course')
const active3 = ref<string | number>('campus')
const active4 = ref<string | number>('home')
const active5 = ref<string | number>('campus')
const active6 = ref<string | number>('home')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础（{{ active }}）</p>
    <div class="demo-box">
      <jm-tabbar v-model="active" :fixed="false">
        <jm-tabbar-item name="home" text="首页">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="course" text="课程">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="4" y="4" width="16" height="16" rx="2.5" />
              <path d="M8 9h8M8 13h5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="mine" text="我的">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8.5" r="3.5" />
              <path d="M5 20c0-3.6 3.1-5.5 7-5.5s7 1.9 7 5.5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
      </jm-tabbar>
    </div>

    <p class="demo-label">带徽标 / 小红点 / 禁用</p>
    <div class="demo-box">
      <jm-tabbar v-model="active2" :fixed="false" active-color="#00A0E9">
        <jm-tabbar-item name="home" text="首页" badge="2">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="course" text="课程" dot>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="4" y="4" width="16" height="16" rx="2.5" />
              <path d="M8 9h8M8 13h5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="vip" text="会员" disabled>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 3l2.6 5.6 6.1.8-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 9.4l6.1-.8L12 3z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
      </jm-tabbar>
    </div>

    <p class="demo-label">选中气泡凸起（bubble + ring 白边，参照数字校园样式）</p>
    <div class="demo-box">
      <jm-tabbar v-model="active3" :fixed="false">
        <jm-tabbar-item name="home" text="首页" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="campus" text="数字校园" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 4L2 9l10 5 10-5-10-5z" stroke-linejoin="round" />
              <path d="M6.5 11.5V15c0 1.5 2.5 2.8 5.5 2.8s5.5-1.3 5.5-2.8v-3.5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="agent" text="智能体" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="5" y="8" width="14" height="10" rx="3" />
              <path d="M12 8V5.2" stroke-linecap="round" />
              <circle cx="9.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
              <circle cx="14.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
              <path d="M9.5 15.3h5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="mine" text="个人中心" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8.8" r="3.4" />
              <path d="M5.5 19.5c0-3.4 3-5.2 6.5-5.2s6.5 1.8 6.5 5.2" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
      </jm-tabbar>
    </div>

    <p class="demo-label">5 个 tab，中间悬浮（float-center）</p>
    <div class="demo-box">
      <jm-tabbar v-model="active4" :fixed="false" float-center>
        <jm-tabbar-item name="home" text="首页">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="course" text="课程">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="4" y="4" width="16" height="16" rx="2.5" />
              <path d="M8 9h8M8 13h5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="publish" ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5.5v13M5.5 12h13" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="message" text="消息" badge="6">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 6.5A2.5 2.5 0 016.5 4h11A2.5 2.5 0 0120 6.5v8a2.5 2.5 0 01-2.5 2.5H9l-4.2 3.4A.8.8 0 013.5 20v-3.6A2.5 2.5 0 014 15z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="mine" text="我的">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8.5" r="3.5" />
              <path d="M5 20c0-3.6 3.1-5.5 7-5.5s7 1.9 7 5.5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
      </jm-tabbar>
    </div>

    <p class="demo-label">环色跟随栏底色：深色栏时环自动变深</p>
    <div class="demo-box">
      <jm-tabbar v-model="active5" :fixed="false" background="#1f2430">
        <jm-tabbar-item name="home" text="首页" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="campus" text="数字校园" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 4L2 9l10 5 10-5-10-5z" stroke-linejoin="round" />
              <path d="M6.5 11.5V15c0 1.5 2.5 2.8 5.5 2.8s5.5-1.3 5.5-2.8v-3.5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="agent" text="智能体" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="5" y="8" width="14" height="10" rx="3" />
              <path d="M12 8V5.2" stroke-linecap="round" />
              <circle cx="9.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
              <circle cx="14.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
              <path d="M9.5 15.3h5" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
        <jm-tabbar-item name="mine" text="个人中心" bubble ring>
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8.8" r="3.4" />
              <path d="M5.5 19.5c0-3.4 3-5.2 6.5-5.2s6.5 1.8 6.5 5.2" stroke-linecap="round" />
            </svg>
          </template>
        </jm-tabbar-item>
      </jm-tabbar>
    </div>

    <p class="demo-label">无阴影 + 无边框（shadow / border 配置项）</p>
    <jm-tabbar v-model="active6" :fixed="false" :border="false" background="transparent">
      <jm-tabbar-item name="home" text="首页" bubble ring :shadow="false">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1v-9.5z" stroke-linejoin="round" />
          </svg>
        </template>
      </jm-tabbar-item>
      <jm-tabbar-item name="campus" text="数字校园" bubble ring :shadow="false">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M12 4L2 9l10 5 10-5-10-5z" stroke-linejoin="round" />
            <path d="M6.5 11.5V15c0 1.5 2.5 2.8 5.5 2.8s5.5-1.3 5.5-2.8v-3.5" stroke-linecap="round" />
          </svg>
        </template>
      </jm-tabbar-item>
      <jm-tabbar-item name="agent" text="智能体" bubble ring :shadow="false">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="5" y="8" width="14" height="10" rx="3" />
            <path d="M12 8V5.2" stroke-linecap="round" />
            <circle cx="9.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
            <circle cx="14.5" cy="12.5" r="1" fill="currentColor" stroke="none" />
            <path d="M9.5 15.3h5" stroke-linecap="round" />
          </svg>
        </template>
      </jm-tabbar-item>
      <jm-tabbar-item name="mine" text="个人中心" bubble ring :shadow="false">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="8.8" r="3.4" />
            <path d="M5.5 19.5c0-3.4 3-5.2 6.5-5.2s6.5 1.8 6.5 5.2" stroke-linecap="round" />
          </svg>
        </template>
      </jm-tabbar-item>
    </jm-tabbar>

    <p class="demo-note">当前选中：{{ active }} / {{ active2 }} / {{ active3 }} / {{ active4 }}</p>
  </div>
</template>

<style scoped>
/* 悬浮 FAB 会浮出栏顶，不能裁剪 */
.demo-box {
  border: 1px solid var(--jm-border-color);
  border-radius: 12px;
}
</style>
