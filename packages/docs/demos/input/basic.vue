<script setup lang="ts">
import { ref, watch } from 'vue'

const name = ref('')
const phone = ref('13800000000')
const phoneNew = ref('')
const note = ref('')
const search = ref('')
const account = ref('')
const amount = ref('')
const intro = ref('')
const badMail = ref('jimu@')
const codeInput = ref('')
const codeInput2 = ref('')
const codeInput3 = ref('')
const codeInput4 = ref('')
const sendLog = ref('')
const intro2 = ref('')
const rowName = ref('')
const rowPhone = ref('123')
const rowAmount = ref('')
const readOnlyVal = ref('输入框只读')
const errName = ref('')
const errMail = ref('')
const errStandalone = ref('')

/* 错误态是受控的：error / error-message 由外部校验状态驱动，输入合法后置回即可消失 */
const nameError = ref(true)
watch(errName, (v) => (nameError.value = v.trim().length === 0))

const phoneError = ref(true)
const phoneMsg = ref('手机号格式错误')
watch(rowPhone, (v) => {
  const ok = /^1[3-9]\d{9}$/.test(v)
  phoneError.value = !ok
  phoneMsg.value = ok ? '' : '手机号格式错误'
})

const mailError = ref(true)
watch(errMail, (v) => (mailError.value = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)))

/* label 顶部对齐（plain 行卡片）演示 */
const topText = ref('')
const topMail = ref('')
const topMailError = ref(true)
watch(topMail, (v) => (topMailError.value = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)))

function onSend() {
  sendLog.value = `验证码已发送（倒计时中）`
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">浮动标签：聚焦或有值时上浮</p>
    <jm-input v-model="account" label="账号" placeholder="手机号 / 邮箱" clearable />
    <jm-input v-model="name" label="课程名称" variant="filled" placeholder="例如：初二物理" />
    <jm-input v-model="amount" label="金额" variant="underlined" placeholder="0.00" inputmode="decimal" />

    <p class="demo-label">三种外观</p>
    <jm-input v-model="name" placeholder="描边 outline（默认）" />
    <jm-input v-model="name" variant="filled" placeholder="灰底 filled" />
    <jm-input v-model="name" variant="underlined" placeholder="下划线 underlined（聚焦看高亮线展开）" />

    <p class="demo-label">尺寸</p>
    <jm-input v-model="phone" size="small" label="小号" placeholder="辅助文案" />
    <jm-input v-model="phone" label="中号" />
    <jm-input v-model="phone" size="large" label="大号" />

    <p class="demo-label">清空 + 字数限制</p>
    <jm-input v-model="note" clearable placeholder="输入点什么" :maxlength="20" show-word-limit />
    <jm-input v-model="search" clearable placeholder="搜索课程" radius="10px">
      <template #prefix>
        <svg viewBox="0 0 24 24" width="16" height="16">
          <circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.7" />
          <path d="M16 16l4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
        </svg>
      </template>
    </jm-input>

    <p class="demo-label">校验失败态</p>
    <jm-input v-model="badMail" label="邮箱" error placeholder="name@example.com" />

    <p class="demo-label">自定义圆角 / 状态</p>
    <jm-input v-model="name" :radius="0" placeholder="方角" />
    <jm-input v-model="name" radius="12px" placeholder="小圆角" />
    <jm-input model-value="只读内容" readonly label="只读" />
    <jm-input model-value="禁用状态" disabled label="禁用" />

    <p class="demo-label">textarea：autosize 跟随内容撑开（上限 120px）</p>
    <jm-input
      v-model="intro"
      type="textarea"
      autosize
      :max-height="120"
      placeholder="自我介绍，内容多高框就多高…"
    />

    <p class="demo-label">textarea：固定行数（字数统计覆盖在框内右下角）</p>
    <jm-input v-model="note" type="textarea" :rows="3" placeholder="rows=3 定高" :maxlength="100" show-word-limit />
    <jm-input v-model="name" type="textarea" :rows="2" variant="filled" placeholder="灰底 textarea" />

    <p class="demo-label">手机号：固定前缀 +86</p>
    <jm-input
      v-model="phoneNew"
      prefix-text="+86"
      type="tel"
      inputmode="numeric"
      :maxlength="11"
      placeholder="请输入手机号"
    />

    <p class="demo-label">验证码：按钮圆角跟随输入框（auto），倒计时固定两位数</p>
    <jm-input
      v-model="codeInput"
      code
      radius="999px"
      :maxlength="6"
      inputmode="numeric"
      placeholder="胶囊输入框 → 按钮自动是胶囊"
      @send="onSend"
    />
    <jm-input
      v-model="codeInput2"
      code
      :code-duration="10"
      :maxlength="6"
      inputmode="numeric"
      placeholder="普通圆角输入框 → 按钮跟随圆角"
      @send="onSend"
    />
    <jm-input
      v-model="codeInput3"
      code
      code-shape="square"
      variant="filled"
      :code-duration="10"
      :maxlength="6"
      inputmode="numeric"
      placeholder="强制方形按钮，10 秒倒计时"
      @send="onSend"
    />
    <jm-input
      v-model="codeInput4"
      code
      code-type="text"
      :code-duration="10"
      :maxlength="6"
      inputmode="numeric"
      placeholder="纯文字验证码（无底色）"
      @send="onSend"
    />
    <p class="demo-note">{{ sendLog || '点击「获取验证码」试试' }}</p>

    <p class="demo-label">label 在上 + textarea（多行输入）</p>
    <jm-input
      v-model="intro2"
      type="textarea"
      label="详细描述"
      label-placement="top"
      variant="outline"
      :rows="3"
      placeholder="标签在上，这里可以多行输入换行…"
    />
    <jm-input
      v-model="intro"
      type="textarea"
      autosize
      :max-height="120"
      label="备注"
      label-placement="top"
      variant="filled"
      placeholder="灰底 autosize，内容多高框就多高"
    />

    <p class="demo-label">label 在上（Vant Field 排版）+ 错误提示文案</p>
    <jm-input v-model="name" label="课程名称" label-placement="top" placeholder="请输入课程名称" />
    <jm-input
      v-model="badMail"
      label="邮箱"
      label-placement="top"
      error
      error-message="邮箱格式不正确，请重新输入"
      placeholder="name@example.com"
    />

    <p class="demo-label">文字对齐：左 / 居中 / 右</p>
    <jm-input v-model="name" align="left" placeholder="align=left（默认）" />
    <jm-input v-model="amount" align="center" placeholder="align=center" inputmode="decimal" />
    <jm-input v-model="amount" align="right" placeholder="align=right" inputmode="decimal" />

    <p class="demo-label">placeholder 定制（颜色 / 字号 / 字体）</p>
    <jm-input
      v-model="name"
      class="demo-ph"
      placeholder="粉色 placeholder · 衬线 · 17px"
    />

    <p class="demo-label">Vant Field 式行排版：label 在左 + plain 外观 + 必填星号 + 图标</p>
    <div class="vant-rows">
      <jm-input
        v-model="rowName"
        label="用户名"
        label-placement="left"
        required
        variant="plain"
        placeholder="请输入用户名"
      />
      <jm-input
        v-model="rowPhone"
        label="手机号"
        label-placement="left"
        required
        variant="plain"
        type="tel"
        :maxlength="11"
      />
      <jm-input
        model-value="输入框只读"
        label="文本"
        label-placement="left"
        variant="plain"
        readonly
      />
      <jm-input
        model-value="输入框禁用"
        label="文本"
        label-placement="left"
        variant="plain"
        disabled
      />
      <jm-input
        v-model="rowAmount"
        label="金额"
        label-placement="left"
        colon
        variant="plain"
        inputmode="decimal"
        placeholder="左侧图标 + 右侧图标"
      >
        <template #left-icon>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 8v.5M12 11v5" stroke-linecap="round" />
          </svg>
        </template>
        <template #suffix>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.7">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 11v5M12 8v.5" stroke-linecap="round" />
          </svg>
        </template>
      </jm-input>
    </div>

    <p class="demo-label">label 顶部对齐（plain 行卡片：label-placement="top" + variant="plain"）</p>
    <div class="vant-rows">
      <jm-input
        v-model="topText"
        label="文本"
        label-placement="top"
        variant="plain"
        placeholder="顶部对齐"
      />
      <jm-input
        v-model="rowName"
        label="用户名"
        label-placement="top"
        variant="plain"
        required
        colon
        placeholder="顶部对齐 + 必填星号 / 冒号"
      />
      <jm-input
        v-model="topMail"
        label="邮箱"
        label-placement="top"
        variant="plain"
        :error="topMailError"
        :error-message="topMailError ? '请输入正确的邮箱地址' : ''"
        placeholder="name@example.com"
      />
      <jm-input
        v-model="intro2"
        type="textarea"
        label="备注"
        label-placement="top"
        variant="plain"
        :rows="2"
        placeholder="顶部对齐 + 多行输入"
      />
    </div>

    <p class="demo-label">错误提示：默认跟随输入框对齐，也可覆盖对齐（左 / 中 / 右）与颜色</p>
    <div class="vant-rows">
      <jm-input
        v-model="errName"
        label="用户名"
        label-placement="left"
        required
        :error="nameError"
        :error-message="nameError ? '请输入用户名' : ''"
        variant="plain"
        placeholder="placeholder 也转红"
      />
      <jm-input
        v-model="rowPhone"
        label="手机号"
        label-placement="left"
        :error="phoneError"
        :error-message="phoneMsg"
        error-align="right"
        variant="plain"
        type="tel"
        :maxlength="11"
      />
      <jm-input
        v-model="errMail"
        label="邮箱"
        label-placement="left"
        :error="mailError"
        :error-message="mailError ? '邮箱格式不正确（自定义橙色）' : ''"
        error-color="#FF6430"
        error-align="center"
        variant="plain"
        placeholder="name@example.com"
      />
      <jm-input
        v-model="errStandalone"
        align="center"
        error
        error-message="错误文案默认跟随 align=center"
        placeholder="浮动标签 + 错误文案"
      />
    </div>
    <p class="demo-note">error / error-message 是受控 props：组件只负责呈现，不内置校验规则。上面三行的校验状态随输入实时更新——输入合法后报错文案即消失。Form 校验组件接入后会把这一状态自动接管。</p>
  </div>
</template>

<style>
.demo-ph {
  --jm-input-placeholder-color: #e2557b;
  --jm-input-placeholder-font-size: 17px;
  --jm-input-placeholder-font-family: Georgia, serif;
  --jm-input-placeholder-font-weight: 400;
}

/* Vant Field 式行排版：白卡 + 行间细分割线 */
.vant-rows {
  background: var(--jm-bg-container);
  border-radius: var(--jm-radius);
  overflow: hidden;
}

.vant-rows .jm-input__box {
  min-height: calc(48px * var(--jm-size-scale));
}

.vant-rows .jm-input + .jm-input {
  border-top: 1px solid var(--jm-border-color);
}
</style>
