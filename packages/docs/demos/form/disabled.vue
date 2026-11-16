<script setup lang="ts">
import { reactive, ref } from 'vue'

const form = reactive({
  name: '张小安',
  phone: '13800006688',
  notice: true,
  score: 4,
  step: 2,
  promo: '',
  memo: '',
})

const disabled = ref(true)
const single = ref(false)

const rules = {
  phone: [{ required: true, message: '请填写手机号' }],
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">
      整表禁用
      <jm-switch v-model="disabled" size="small" style="margin-left: 8px" />
    </p>
    <jm-form :model="form" :rules="rules" :disabled="disabled">
      <jm-input v-model="form.name" label="姓名" label-placement="left" variant="plain" />
      <jm-form-item name="phone">
        <jm-input v-model="form.phone" label="手机号" label-placement="left" variant="plain" />
      </jm-form-item>
      <jm-form-item label="上课提醒">
        <jm-switch v-model="form.notice" />
      </jm-form-item>
      <jm-form-item label="评分">
        <jm-rate v-model="form.score" size="16px" />
      </jm-form-item>
      <jm-form-item label="人数">
        <jm-stepper v-model="form.step" :min="1" :max="10" />
      </jm-form-item>
    </jm-form>

    <p class="demo-label">
      单字段禁用（disabled 放在 FormItem 上）
      <jm-switch v-model="single" size="small" style="margin-left: 8px" />
    </p>
    <jm-form :model="form">
      <jm-form-item label="优惠码" :disabled="single">
        <jm-input v-model="form.promo" placeholder="选填" variant="filled" />
      </jm-form-item>
      <jm-form-item label="备注">
        <jm-input v-model="form.memo" placeholder="选填" variant="filled" />
      </jm-form-item>
    </jm-form>
  </div>
</template>
