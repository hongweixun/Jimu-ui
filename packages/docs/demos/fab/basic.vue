<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const open = ref(false)

const actions = [
  { icon: 'edit', label: '写作业' },
  { icon: 'camera', label: '拍照上传' },
  { icon: 'share', label: '分享' },
]

function onMain() {
  open.value = !open.value
}

function pick(label: string) {
  open.value = false
  showToast(`选择了「${label}」`)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：右下角主按钮</p>
    <div class="stage">
      <div class="stage__inner">
        <p class="stage__title">我的作业</p>
        <p class="stage__desc">这里模拟一个可滚动页面的右下角，悬浮按钮固定在这个区域内。</p>
      </div>
      <jm-fab inline icon="plus" :offset="16" :bottom="16" @click="showToast('新建')" />
    </div>

    <p class="demo-label">带文字 / 左侧</p>
    <div class="stage">
      <div class="stage__inner">
        <p class="stage__title">空状态引导</p>
        <p class="stage__desc">没有数据时用一个主行动按钮把用户带进流程。</p>
      </div>
      <jm-fab inline position="left" icon="edit" text="写作业" :offset="16" :bottom="16" />
    </div>

    <p class="demo-label">展开菜单</p>
    <div class="stage">
      <div class="stage__inner">
        <p class="stage__title">浮层菜单</p>
        <p class="stage__desc">active + active-icon 切成叉号，配合 popup 做展开。</p>
        <jm-popup v-model:show="open" position="bottom" :round="true" :z-index="950">
          <div class="sheet">
            <button
              v-for="a in actions"
              :key="a.label"
              type="button"
              class="sheet__item"
              @click="pick(a.label)"
            >
              <jm-icon :name="a.icon" size="18px" />
              {{ a.label }}
            </button>
          </div>
        </jm-popup>
      </div>
      <jm-fab
        inline
        :active="open"
        icon="plus"
        active-icon="close"
        :offset="16"
        :bottom="16"
        @click="onMain"
      />
    </div>
  </div>
</template>

<style scoped>
.stage {
  position: relative;
  height: 180px;
  border-radius: 14px;
  background: var(--jm-bg-input);
  overflow: hidden;
}

.stage__inner {
  padding: 16px 88px 16px 16px;
}

.stage__title {
  margin: 0 0 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--jm-text-color);
}

.stage__desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.7;
  color: var(--jm-text-color-3);
}

.sheet {
  display: flex;
  flex-direction: column;
  padding: 8px 0 4px;
  background: var(--jm-bg-elevated);
}

.sheet__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  border: 0;
  background: none;
  color: var(--jm-text-color);
  font-size: 14px;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}

.sheet__item:active {
  background: var(--jm-bg-hover);
}
</style>
