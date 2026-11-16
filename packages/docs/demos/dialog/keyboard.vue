<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)
const name = ref('')
const note = ref('')
const log = ref('')

function onConfirm() {
  log.value = `已保存：${name.value || '（未填姓名）'}`
  show.value = false
}

function onCancel() {
  log.value = '已取消'
}
</script>

<template>
  <div class="demo-page">
    <jm-button type="primary" block @click="show = true">打开表单弹窗</jm-button>
    <p class="demo-note">
      在电脑上按 <kbd>Tab</kbd> 试试：焦点只在弹窗内的输入框和按钮之间循环，不会跑到背后的页面；按
      <kbd>Esc</kbd> 关闭后，焦点回到下面这个按钮上。{{ log }}
    </p>

    <jm-dialog
      v-model:show="show"
      title="填写收件人"
      confirm-text="保存"
      :teleport="false"
      @confirm="onConfirm"
      @cancel="onCancel"
    >
      <div class="kb-form">
        <jm-input v-model="name" label="姓名" placeholder="请输入姓名" clearable />
        <jm-input v-model="note" label="备注" placeholder="选填" />
      </div>
    </jm-dialog>
  </div>
</template>

<style scoped>
.kb-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px 0 2px;
}

kbd {
  padding: 1px 5px;
  border: 1px solid var(--jm-border-color-2);
  border-bottom-width: 2px;
  border-radius: 4px;
  background: var(--jm-bg-input);
  font-family: inherit;
  font-size: 11px;
}
</style>
