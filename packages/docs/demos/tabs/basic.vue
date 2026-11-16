<script setup lang="ts">
import { ref } from 'vue'

const active1 = ref('all')
const active2 = ref('live')
const active3 = ref('week')
const active4 = ref('all')
const activeScroll = ref('c1')
const activeScroll2 = ref('d1')
const activeAnim = ref('a1')
const activeSwipe = ref('b1')
const activeSticky = ref('hot')

function onTabClick(name: string | number) {
  console.log('[tabs click]', name)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">下划线 line（指示器默认跟文字等宽）</p>
    <jm-tabs v-model="active1">
      <jm-tab name="all" label="全部" badge="12">
        <div class="panel">全部课程内容</div>
      </jm-tab>
      <jm-tab name="live" label="直播">
        <div class="panel">直播中内容</div>
      </jm-tab>
      <jm-tab name="done" label="已结束">
        <div class="panel">已结束内容</div>
      </jm-tab>
      <jm-tab name="off" label="停用" disabled>
        <div class="panel">停用</div>
      </jm-tab>
    </jm-tabs>

    <p class="demo-label">固定线宽 line-width（居中于激活项）</p>
    <jm-tabs v-model="active4" :line-width="24">
      <jm-tab name="all" label="全部"><div class="panel">24px 定宽指示器</div></jm-tab>
      <jm-tab name="live" label="直播"><div class="panel">直播</div></jm-tab>
      <jm-tab name="done" label="已结束"><div class="panel">已结束</div></jm-tab>
    </jm-tabs>

    <p class="demo-label">标签栏滚动 scrollable（visible-count=4，一屏 4 个）</p>
    <jm-tabs v-model="activeScroll" scrollable :visible-count="4">
      <jm-tab v-for="i in 8" :key="i" :name="`c${i}`" :label="`分类 ${i}`">
        <div class="panel">分类 {{ i }} 的内容</div>
      </jm-tab>
    </jm-tabs>
    <jm-tabs v-model="activeScroll2" scrollable class="mt">
      <jm-tab v-for="i in 8" :key="i" :name="`d${i}`" :label="`频道 ${i}`">
        <div class="panel">频道 {{ i }} 的内容（默认一屏 3 个）</div>
      </jm-tab>
    </jm-tabs>

    <p class="demo-label">切换动效 animated（track 平移）</p>
    <jm-tabs v-model="activeAnim" animated>
      <jm-tab name="a1" label="推荐"><div class="panel">推荐内容（有平移动效）</div></jm-tab>
      <jm-tab name="a2" label="热榜"><div class="panel">热榜内容</div></jm-tab>
      <jm-tab name="a3" label="关注"><div class="panel">关注内容</div></jm-tab>
    </jm-tabs>

    <p class="demo-label">手势滑动切换 swipeable（触屏左右滑 / 鼠标拖拽都行）</p>
    <jm-tabs v-model="activeSwipe" animated swipeable>
      <jm-tab name="b1" label="第一页"><div class="panel">左右滑动切换，拖到一半松手会回弹</div></jm-tab>
      <jm-tab name="b2" label="第二页"><div class="panel">第二页</div></jm-tab>
      <jm-tab name="b3" label="第三页"><div class="panel">第三页</div></jm-tab>
      <jm-tab name="b4" label="第四页"><div class="panel">第四页</div></jm-tab>
    </jm-tabs>

    <p class="demo-label">分段 segment</p>
    <jm-tabs v-model="active3" type="segment" :radius="999">
      <jm-tab name="week" label="本周">
        <div class="panel">本周学习数据</div>
      </jm-tab>
      <jm-tab name="month" label="本月">
        <div class="panel">本月学习数据</div>
      </jm-tab>
    </jm-tabs>

    <p class="demo-label">卡片 card</p>
    <jm-tabs v-model="active2" type="card">
      <jm-tab name="live" label="直播">
        <div class="panel">卡片风格的标签页</div>
      </jm-tab>
      <jm-tab name="replay" label="回放">
        <div class="panel">回放列表</div>
      </jm-tab>
      <jm-tab name="note" label="讲义">
        <div class="panel">讲义文件</div>
      </jm-tab>
    </jm-tabs>

    <p class="demo-label">置顶吸顶 sticky + tabs（向上滚动看效果）</p>
    <jm-sticky :offset-top="0">
      <jm-tabs v-model="activeSticky" animated swipeable>
        <jm-tab name="hot" label="热门"><div class="panel">吸顶后滚动下方长内容，标签栏会钉在顶部</div></jm-tab>
        <jm-tab name="new" label="最新"><div class="panel">最新内容</div></jm-tab>
        <jm-tab name="follow" label="关注"><div class="panel">关注内容</div></jm-tab>
      </jm-tabs>
    </jm-sticky>
    <div v-for="i in 6" :key="i" class="filler">占位内容块 {{ i }}</div>

    <p class="demo-note">点击标签会触发 click 事件（disabled 也会触发，控制台可见）。</p>
  </div>
</template>

<style scoped>
.mt {
  margin-top: 12px;
}

.panel {
  padding: 14px;
  border-radius: 10px;
  background: var(--jm-bg-container);
  font-size: 13px;
  color: var(--jm-text-color-2);
}

.filler {
  margin-top: 10px;
  padding: 40px 14px;
  border-radius: 10px;
  background: var(--jm-bg-input);
  font-size: 13px;
  color: var(--jm-text-color-3);
  text-align: center;
}
</style>
