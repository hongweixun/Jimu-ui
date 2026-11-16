<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const picked = ref('')

function pick(name: string) {
  picked.value = name
  showToast(`选择了「${name}」`)
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">点击触发器展开</p>
    <div class="demo-row">
      <jm-popover placement="top" content="默认深色气泡，向上弹出">
        <template #reference>
          <jm-button size="small" plain>上</jm-button>
        </template>
      </jm-popover>

      <jm-popover placement="bottom" theme="light" content="浅色带描边，适合放在白底卡片上">
        <template #reference>
          <jm-button size="small" plain>下</jm-button>
        </template>
      </jm-popover>

      <jm-popover placement="left" content="向左弹">
        <template #reference>
          <jm-button size="small" plain>左</jm-button>
        </template>
      </jm-popover>

      <jm-popover placement="right" content="向右弹">
        <template #reference>
          <jm-button size="small" plain>右</jm-button>
        </template>
      </jm-popover>
    </div>

    <p class="demo-label">气泡菜单</p>
    <jm-popover placement="bottom" align="start" close-on-click-content :offset="6">
      <template #reference>
        <jm-button size="small" type="primary">更多操作</jm-button>
      </template>
      <div class="menu">
        <button type="button" class="menu__item" @click="pick('编辑')">编辑</button>
        <button type="button" class="menu__item" @click="pick('复制链接')">复制链接</button>
        <button type="button" class="menu__item is-danger" @click="pick('删除')">删除</button>
      </div>
    </jm-popover>

    <p class="demo-note">
      当前选择：{{ picked || '暂无' }}。移动端没有 hover，气泡靠点击开合，点面板外部收起。
    </p>
  </div>
</template>

<style scoped>
.menu {
  display: flex;
  flex-direction: column;
  min-width: 116px;
  margin: -8px -12px;
}

.menu__item {
  padding: 10px 14px;
  border: 0;
  background: none;
  color: inherit;
  font-size: 13px;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
  white-space: nowrap;
}

.menu__item + .menu__item {
  border-top: 1px solid rgba(255, 255, 255, 0.12);
}

.menu__item:active {
  background: rgba(255, 255, 255, 0.08);
}

.menu__item.is-danger {
  color: #ff7a7a;
}
</style>
