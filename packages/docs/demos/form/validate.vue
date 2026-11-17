<script setup lang="ts">
import { ref } from 'vue'
import { Button, Form, FormItem, Input } from 'jimu-ui'
import type { FormRule } from 'jimu-ui'

const formRef = ref<InstanceType<typeof Form>>()
const result = ref('填写后点「提交」看校验结果')
const submitted = ref('')

const model = ref({
  username: '',
  password: '',
  confirm: '',
  phone: '',
})

/** 表单级校验时机：默认失焦+输入都校验，切到「仅失焦」后输入过程不再实时报错 */
const validateTrigger = ref<('blur' | 'change')[]>(['blur', 'change'])

/* 自定义异步校验：模拟向服务端查重 */
const checking = ref(false)
const takenNames = ['admin', 'zhangsan']
function checkName(value: string): Promise<boolean | string> {
  checking.value = true
  return new Promise((resolve) => {
    setTimeout(() => {
      checking.value = false
      resolve(takenNames.includes(value) ? '该用户名已被注册' : true)
    }, 700)
  })
}

const usernameRules: FormRule[] = [
  { required: true, message: '请输入用户名' },
  { min: 3, max: 16, message: '用户名 3~16 个字符' },
  { validator: checkName },
]

/* 自定义同步校验：返回 true 通过，返回字符串作为错误文案 */
const passwordRules: FormRule[] = [
  { required: true, message: '请输入密码' },
  {
    validator: (v: string) => {
      if (v.length < 6) return '密码至少 6 位'
      if (!/[a-zA-Z]/.test(v) || !/\d/.test(v)) return '密码须同时包含字母和数字'
      return true
    },
  },
]

/* 跨字段校验：validator 第三个参数是整个 model */
const confirmRules: FormRule[] = [
  { required: true, message: '请再次输入密码' },
  {
    validator: (v: string, _rule, m: Record<string, unknown>) => (v === m.password ? true : '两次输入的密码不一致'),
  },
]

const phoneRules: FormRule[] = [
  { required: true, message: '请输入手机号' },
  { pattern: /^1\d{10}$/, message: '手机号应为 1 开头的 11 位数字' },
]

async function onSubmit() {
  const passed = await formRef.value?.validate()
  result.value = passed
    ? `✅ 校验全部通过：${JSON.stringify(model.value)}`
    : '❌ 校验未通过，已滚动到第一个错误字段'
}

function onFailed() {
  /* form 的 failed 事件里也拿得到错误清单 */
}

function onFailedTip(e: { errors: Array<{ name?: string; message: string }> }) {
  submitted.value = `failed 事件：${e.errors.map((x) => `${x.name}: ${x.message}`).join('；')}`
}
</script>

<template>
  <div class="demo-page">
    <div class="switch-row">
      <Button size="small" :variant="validateTrigger.length === 2 ? 'solid' : 'outline'" @click="validateTrigger = ['blur', 'change']">
        失焦 + 输入校验
      </Button>
      <Button size="small" :variant="validateTrigger.length === 1 ? 'solid' : 'outline'" @click="validateTrigger = ['blur']">
        仅失焦校验
      </Button>
    </div>

    <Form
      ref="formRef"
      :model="model"
      :validate-trigger="validateTrigger"
      scroll-to-error
      label-width="88"
      colon
      @submit="onSubmit"
      @failed="onFailedTip"
    >
      <FormItem name="username" label="用户名" :rules="usernameRules">
        <Input v-model="model.username" placeholder="试试 admin（异步查重 700ms）" clearable />
      </FormItem>

      <FormItem name="password" label="密码" :rules="passwordRules">
        <Input v-model="model.password" type="password" placeholder="至少 6 位，含字母和数字" clearable />
      </FormItem>

      <FormItem name="confirm" label="确认密码" :rules="confirmRules">
        <Input v-model="model.confirm" type="password" placeholder="跨字段校验：须与密码一致" clearable />
      </FormItem>

      <FormItem name="phone" label="手机号" :rules="phoneRules">
        <Input v-model="model.phone" type="tel" maxlength="11" placeholder="正则校验：1 开头 11 位" clearable />
      </FormItem>

      <div style="padding: 12px">
        <Button type="primary" block native-type="submit">提交</Button>
      </div>
    </Form>

    <p class="demo-tip">{{ result }}</p>
    <p v-if="submitted" class="demo-tip">{{ submitted }}</p>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 10px;
}

.switch-row {
  display: flex;
  gap: 8px;
  padding: 0 12px;
}

.demo-tip {
  padding: 0 12px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-color-primary-text);
  word-break: break-all;
}
</style>
