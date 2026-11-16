<script setup lang="ts">
import { ref } from 'vue'

const count = ref(1)
const countLog = ref('')
const big = ref(30)
const decimal = ref(1.5)
const inForm = ref(2)
const formLog = ref('')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础：min 1 / max Infinity / step 1</p>
    <div class="demo-row">
      <jm-stepper v-model="count" @change="(v) => (countLog = `change: ${v}`)" @over-limit="(a) => (countLog = `over-limit: ${a}`)" />
      <span class="demo-note">{{ countLog || '试试点到边界再加减' }}</span>
    </div>

    <p class="demo-label">范围与步长：min 0 / max 50 / step 5</p>
    <jm-stepper v-model="big" :min="0" :max="50" :step="5" />

    <p class="demo-label">小数步长：step 0.5（integer 关闭）</p>
    <jm-stepper v-model="decimal" :min="0" :max="3" :step="0.5" :integer="false" />

    <p class="demo-label">禁用与禁输入</p>
    <div class="demo-row">
      <jm-stepper :model-value="3" disabled />
      <jm-stepper :model-value="3" disable-input />
    </div>

    <p class="demo-label">自定义尺寸</p>
    <jm-stepper :model-value="6" :input-width="48" :button-size="36" />

    <p class="demo-label">放进 FormItem 行（配合 Form 校验 min 1）</p>
    <jm-form :model="{ num: inForm }" :rules="{ num: [{ min: 1, message: '至少选 1 份', trigger: 'change' }] }">
      <div class="form-card">
        <jm-form-item name="num" label="购买数量">
          <jm-stepper v-model="inForm" :min="0" :max="99" @change="formLog = `change: ${inForm}`" />
        </jm-form-item>
      </div>
      <p v-if="formLog" class="demo-note">{{ formLog }}{{ inForm < 1 ? '（已触发行内校验）' : '' }}</p>
    </jm-form>
  </div>
</template>

<style>
.demo-row {
  display: flex;
  align-items: center;
  gap: var(--jm-space-3);
}

.form-card {
  overflow: hidden;
  background: var(--jm-bg-container);
  border-radius: var(--jm-radius);
}

.form-card .jm-form-item + .jm-form-item {
  border-top: 1px solid var(--jm-border-color);
}
</style>
