<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'jimu-ui'

const dragRef = ref<any>(null)

function onTap() {
  showToast('只是点了一下，没有拖动')
}
</script>

<template>
  <div class="demo-page demo-drag">
    <p class="demo-label">基本使用（按住拖动，点一下不算拖拽）</p>
    <div id="stage1" class="stage">
      <jm-drag target="#stage1" style="left: 40px; top: 30px" @click="onTap">
        <button class="chip">拖我</button>
      </jm-drag>
    </div>

    <p class="demo-label">限制方向 + 吸附</p>
    <div id="stage2" class="stage">
      <jm-drag target="#stage2" direction="x" style="left: 30px; top: 20px">
        <button class="chip chip--primary">只能横着拖</button>
      </jm-drag>
      <jm-drag target="#stage2" attraction="x" style="left: 30px; top: 80px">
        <button class="chip">松手左右吸附</button>
      </jm-drag>
    </div>

    <p class="demo-label">重置位置（ref.reset）</p>
    <div id="stage3" class="stage">
      <jm-drag ref="dragRef" target="#stage3" style="left: 30px; top: 20px">
        <button class="chip chip--primary">任意拖</button>
      </jm-drag>
      <button class="chip chip--ghost reset" @click="dragRef?.reset?.()">重置</button>
    </div>

    <p class="demo-note">
      拖拽用的是 Pointer 事件，鼠标与触摸都支持；<code>target</code> 把拖拽约束在容器内，不传则相对视口拖动。
    </p>
  </div>
</template>

<style scoped>
.stage {
  position: relative;
  height: 130px;
  border: var(--jm-border-width) dashed var(--jm-border-color-2);
  border-radius: var(--jm-radius-md);
  margin-bottom: 4px;
  overflow: hidden;
}

.chip {
  padding: 8px 14px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-bg-elevated);
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-sm);
  box-shadow: var(--jm-elevation-2);
  cursor: grab;
}

.chip:active {
  cursor: grabbing;
}

.chip--primary {
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
}

.chip--ghost {
  background: transparent;
  border: var(--jm-border-width) solid var(--jm-border-color-2);
}

.reset {
  position: absolute;
  right: 12px;
  bottom: 12px;
}

.demo-note code {
  padding: 1px 4px;
  border-radius: 4px;
  background: var(--jm-bg-page);
  font-size: 12px;
}
</style>
