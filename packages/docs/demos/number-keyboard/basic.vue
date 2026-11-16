<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const value = ref('')
const randomOrder = ref(false)

const customShow = ref(false)
const amount = ref('')

function onInput(key: string) {
  if (value.value.length < 6) value.value += key
}

function onDelete() {
  value.value = value.value.slice(0, -1)
}

const quick = ['100', '200', '500', '1000']
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础用法</p>
    <jm-cell title="输入金额" :value="value || '点击输入'" is-link clickable @click="show = true" />
    <jm-cell title="随机排列" :value="randomOrder ? '开' : '关'">
      <jm-switch v-model="randomOrder" size="small" />
    </jm-cell>

    <p class="demo-label">带辅助键与关闭按钮</p>
    <jm-button type="primary" block @click="show = true">打开键盘</jm-button>

    <p class="demo-label">自定义按键（theme="custom"）</p>
    <jm-cell title="快捷金额" :value="amount ? `¥ ${amount}` : '未选择'" is-link clickable @click="customShow = true" />

    <jm-number-keyboard
      v-model:show="show"
      title="输入金额"
      extra-key="00"
      close-button-text="完成"
      :value="value"
      :maxlength="6"
      :random-key-order="randomOrder"
      :teleport="false"
      @input="onInput"
      @delete="onDelete"
    />

    <jm-number-keyboard
      v-model:show="customShow"
      theme="custom"
      title="选择快捷金额"
      close-button-text="取消"
      :teleport="false"
      @input="(k: string) => (amount = k)"
    >
      <template #default="{ input, delete: del }">
        <button
          v-for="q in quick"
          :key="q"
          type="button"
          class="jm-number-keyboard__key custom-key"
          @click="input(q); customShow = false"
        >
          ¥{{ q }}
        </button>
        <button type="button" class="jm-number-keyboard__key custom-key is-ghost" @click="del">
          删除
        </button>
      </template>
    </jm-number-keyboard>

    <p class="demo-note">键盘默认挂到 body；在手机模拟框/弹窗里演示时传 :teleport="false" 就地渲染。</p>
  </div>
</template>

<style scoped>
.custom-key {
  font-size: 17px;
}

.custom-key.is-ghost {
  color: var(--jm-text-color-2);
  background: var(--jm-bg-input);
}
</style>
