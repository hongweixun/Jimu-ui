<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormRule } from 'jimu-ui'

/* ---------- 基础表单 ---------- */
const basicRef = ref<any>(null)
const basic = reactive({ username: '', phone: '', mail: '', note: '' })

const basicRules: Record<string, FormRule[]> = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 10, message: '用户名需 2~10 个字符', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号' },
    { type: 'tel', message: '手机号格式不正确', trigger: 'change' },
  ],
  mail: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  note: [{ max: 20, message: '备注不超过 20 字', trigger: 'change' }],
}

const log = ref('')
function onSubmit(model: Record<string, unknown>) {
  log.value = `✓ 校验通过：${JSON.stringify(model)}`
}
function onFailed(info: { errors: Array<{ name?: string }> }) {
  log.value = `✗ 校验失败：${info.errors.map((e) => e.name).join('、')}`
}
function resetBasic() {
  basicRef.value?.resetFields()
  log.value = ''
}

/* ---------- 规则总览：自定义 + 异步 ---------- */
const ruleForm = reactive({ code: '', account: '' })
const taken = ['admin', 'jimu', 'test']
const ruleRules: Record<string, FormRule[]> = {
  code: [
    { required: true, message: '请输入邀请码', trigger: 'blur' },
    {
      message: '邀请码格式为 JM + 4 位数字',
      pattern: /^JM\d{4}$/,
      trigger: 'change',
    },
  ],
  account: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    {
      trigger: 'blur',
      validator: async (value) => {
        await new Promise((r) => setTimeout(r, 600))
        return taken.includes(String(value)) ? '该账号已被占用' : true
      },
    },
  ],
}
const ruleRef = ref<any>(null)
const ruleLog = ref('')
const checking = ref(false)
async function submitRule() {
  checking.value = true
  const ok = await ruleRef.value?.validate()
  checking.value = false
  ruleLog.value = ok ? '✓ 两项均通过（异步校验完成）' : '✗ 还有字段未通过'
}

/* ---------- 非输入控件 ---------- */
const switchForm = reactive({ agree: false, score: 0 })
const switchRules: Record<string, FormRule[]> = {
  agree: [{ validator: (v) => v === true || '请先阅读并同意用户协议', trigger: 'change' }],
  score: [{ min: 1, message: '请至少给 1 星', trigger: 'change' }],
}
const switchLog = ref('')
const switchRef = ref<any>(null)
async function submitSwitch() {
  const ok = await switchRef.value?.validate()
  switchLog.value = ok ? '✓ 通过' : '✗ 未通过'
}

/* ---------- label 在上 ---------- */
const topForm = reactive({ name: '', school: '' })
const topRules: Record<string, FormRule[]> = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  school: [{ required: true, message: '请输入学校', trigger: 'blur' }],
}
const topRef = ref<any>(null)
const topLog = ref('')
async function submitTop() {
  const ok = await topRef.value?.validate()
  topLog.value = ok ? '✓ 通过' : '✗ 未通过'
}

/* ---------- 手动控制 + 报错开关 ---------- */
const manualForm = reactive({ mail: '' })
const showError = ref(true)
const manualLog = ref('')
const manualRef = ref<any>(null)
async function doValidateAll() {
  const ok = await manualRef.value?.validate()
  manualLog.value = `validate() → ${ok}`
}
async function doValidateField() {
  const ok = await manualRef.value?.validateField('mail')
  manualLog.value = `validateField('mail') → ${ok}`
}
function doClear() {
  manualRef.value?.clearValidate()
  manualLog.value = 'clearValidate() → 已清空校验状态（数据保留）'
}
function doReset() {
  manualRef.value?.resetFields()
  manualLog.value = 'resetFields() → 数据已恢复初始值与校验状态'
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础表单：行式卡片 + 实时校验 + 提交校验</p>
    <jm-form
      ref="basicRef"
      :model="basic"
      :rules="basicRules"
      scroll-to-error
      @submit="onSubmit"
      @failed="onFailed"
    >
      <div class="form-card">
        <jm-form-item name="username">
          <jm-input v-model="basic.username" label="用户名" label-placement="left" variant="plain" placeholder="2~10 个字符" />
        </jm-form-item>
        <jm-form-item name="phone">
          <jm-input v-model="basic.phone" label="手机号" label-placement="left" variant="plain" type="tel" placeholder="输入手机号" />
        </jm-form-item>
        <jm-form-item name="mail">
          <jm-input v-model="basic.mail" label="邮箱" label-placement="left" variant="plain" placeholder="name@example.com" />
        </jm-form-item>
        <jm-form-item name="note">
          <jm-input
            v-model="basic.note"
            label="备注"
            label-placement="top"
            variant="plain"
            type="textarea"
            :autosize="true"
            :maxlength="20"
            show-word-limit
            placeholder="选填，20 字以内"
          />
        </jm-form-item>
      </div>

      <div class="form-actions">
        <jm-button type="primary" native-type="submit" block>提交</jm-button>
        <jm-button native-type="button" block @click="resetBasic">重置</jm-button>
      </div>
      <p v-if="log" class="demo-note">{{ log }}</p>
    </jm-form>

    <p class="demo-label">规则总览：required / pattern / 异步 validator</p>
    <jm-form ref="ruleRef" :model="ruleForm" :rules="ruleRules">
      <div class="form-card">
        <jm-form-item name="code">
          <jm-input v-model="ruleForm.code" label="邀请码" label-placement="left" variant="plain" placeholder="JM0000" />
        </jm-form-item>
        <jm-form-item name="account">
          <jm-input v-model="ruleForm.account" label="账号" label-placement="left" variant="plain" placeholder="admin / jimu 会占用" />
        </jm-form-item>
      </div>
      <div class="form-actions">
        <jm-button type="primary" block :loading="checking" @click="submitRule">校验（含异步）</jm-button>
      </div>
      <p v-if="ruleLog" class="demo-note">{{ ruleLog }}</p>
    </jm-form>

    <p class="demo-label">非输入控件：FormItem 负责行排版，值右对齐</p>
    <jm-form ref="switchRef" :model="switchForm" :rules="switchRules">
      <div class="form-card">
        <jm-form-item name="agree" label="用户协议">
          <jm-switch v-model="switchForm.agree" />
        </jm-form-item>
        <jm-form-item name="score" label="课程评分">
          <jm-rate v-model="switchForm.score" />
        </jm-form-item>
      </div>
      <div class="form-actions">
        <jm-button type="primary" block @click="submitSwitch">提交</jm-button>
      </div>
      <p v-if="switchLog" class="demo-note">{{ switchLog }}</p>
    </jm-form>

    <p class="demo-label">label 在上（label-align="top"）</p>
    <jm-form ref="topRef" :model="topForm" :rules="topRules" label-width="88px">
      <div class="form-card">
        <jm-form-item name="name" label="姓名" label-align="top">
          <jm-input v-model="topForm.name" variant="plain" placeholder="最多 10 个字" />
        </jm-form-item>
        <jm-form-item name="school" label="学校" label-align="top" colon>
          <jm-input v-model="topForm.school" variant="plain" placeholder="学校全称" />
        </jm-form-item>
      </div>
      <div class="form-actions">
        <jm-button type="primary" block @click="submitTop">提交</jm-button>
      </div>
      <p v-if="topLog" class="demo-note">{{ topLog }}</p>
    </jm-form>

    <p class="demo-label">手动控制：validate / validateField / resetFields + 报错开关</p>
    <div class="form-toolbar">
      <span class="form-toolbar__text">show-error</span>
      <jm-switch v-model="showError" size="small" />
    </div>
    <jm-form ref="manualRef" :model="manualForm" :show-error="showError" label-width="72px">
      <div class="form-card">
        <jm-form-item name="mail" label="邮箱" :rules="[{ required: true, message: '请输入邮箱', trigger: 'blur' }]">
          <jm-input v-model="manualForm.mail" variant="plain" placeholder="关掉 show-error 后只剩红框" />
        </jm-form-item>
      </div>
    </jm-form>
    <div class="form-actions">
      <jm-button block @click="doValidateAll">validate()</jm-button>
      <jm-button block @click="doValidateField">validateField('mail')</jm-button>
      <jm-button block @click="doClear">clearValidate()</jm-button>
      <jm-button block @click="doReset">resetFields()</jm-button>
    </div>
    <p v-if="manualLog" class="demo-note">{{ manualLog }}</p>
  </div>
</template>

<style>
.form-card {
  overflow: hidden;
  background: var(--jm-bg-container);
  border-radius: var(--jm-radius);
}

/* 行与行之间的细分隔线（跨行全宽，与 Vant Field 列表一致） */
.form-card .jm-form-item + .jm-form-item {
  border-top: 1px solid var(--jm-border-color);
}

/* 行式卡片里的 plain Input 与 FormItem 行高等高 */
.form-card .jm-input__box {
  min-height: calc(48px * var(--jm-size-scale));
}

.form-actions {
  display: flex;
  gap: var(--jm-space-2);
  margin-top: var(--jm-space-3);
}

.form-toolbar {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  margin-bottom: var(--jm-space-2);
}

.form-toolbar__text {
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
}
</style>
