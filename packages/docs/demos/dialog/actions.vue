<script setup lang="ts">
import { ref } from 'vue'

const pill = ref(false)
const square = ref(false)
const single = ref(false)
const none = ref(false)

const last = ref('')

function close(msg: string) {
  last.value = msg
}

function onConfirmPill() {
  close('已退出登录')
  pill.value = false
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-row">
      <jm-button type="primary" @click="pill = true">胶囊按钮</jm-button>
      <jm-button type="primary" variant="outline" @click="square = true">方形按钮</jm-button>
    </div>
    <div class="demo-row">
      <jm-button variant="outline" @click="single = true">单个按钮</jm-button>
      <jm-button variant="outline" @click="none = true">隐藏按钮</jm-button>
    </div>

    <p class="demo-note">上一次操作：{{ last || '暂无' }}</p>

    <!-- 胶囊：取消描边 + 确认实心，颜色拉开层级 -->
    <jm-dialog
      v-model:show="pill"
      title="退出登录"
      message="退出后需要重新输入账号和密码才能继续学习，确定退出吗？"
      button-style="pill"
      confirm-text="退出"
      cancel-text="再想想"
      :teleport="false"
      @confirm="onConfirmPill"
      @cancel="close('再想想')"
    />

    <!-- 方形：confirm-color 可直接换实心底色 -->
    <jm-dialog
      v-model:show="square"
      title="提交订单"
      message="课程包共 12 节课，合计 ¥299，提交后将开始扣费。"
      button-style="square"
      confirm-color="#FF6430"
      confirm-text="提交订单"
      cancel-text="再逛逛"
      :teleport="false"
      @confirm="() => { close('已提交'); square = false }"
      @cancel="close('再逛逛')"
    />

    <!-- 只保留一个确认按钮 -->
    <jm-dialog
      v-model:show="single"
      title="恢复成功"
      message="学习记录已恢复到最近一次备份。"
      :show-cancel="false"
      confirm-text="我知道了"
      button-style="pill"
      :teleport="false"
      @confirm="() => { close('知道了'); single = false }"
    />

    <!-- 隐藏按钮：纯提示，点遮罩关闭 -->
    <jm-dialog
      v-model:show="none"
      title="新版本已发布"
      message="v2.4.0 修复了部分机型的播放卡顿问题。"
      :show-cancel="false"
      :show-confirm="false"
      close-on-click-mask
      :teleport="false"
      @update:show="(v: boolean) => { if (!v) close('已关闭提示') }"
    />
  </div>
</template>
