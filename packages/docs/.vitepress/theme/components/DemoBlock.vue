<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Component } from 'vue'
import { highlight } from '../highlight'

const props = withDefaults(
  defineProps<{
    /** 示例文件路径，相对 docs 根目录，如 /demos/button/type.vue */
    src: string
    title?: string
    desc?: string
    /** 是否套手机模拟框 */
    phone?: boolean
    /** 模拟框高度 */
    height?: number
    /** 代码区默认展开 */
    open?: boolean
    /** 示例区用白底 */
    plain?: boolean
  }>(),
  { phone: true, height: 620, open: false, plain: false },
)

const modules = import.meta.glob('/demos/**/*.vue', { eager: true }) as Record<
  string,
  { default: Component }
>
const sources = import.meta.glob('/demos/**/*.vue', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>

const key = computed(() => (props.src.startsWith('/') ? props.src : `/${props.src}`))
const demo = computed(() => modules[key.value]?.default)
const code = computed(() => (sources[key.value] ?? '').trim())
const highlighted = computed(() => highlight(code.value))

const open = ref(props.open)
const copied = ref(false)

async function copy() {
  try {
    await navigator.clipboard.writeText(code.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1600)
  } catch {
    copied.value = false
  }
}
</script>

<template>
  <section class="demo">
    <header v-if="title || desc" class="demo__head">
      <h3 v-if="title" class="demo__title">{{ title }}</h3>
      <p v-if="desc" class="demo__desc">{{ desc }}</p>
    </header>

    <div class="demo__stage" :class="{ 'is-plain': plain }">
      <PhoneFrame v-if="phone" :height="height">
        <component :is="demo" v-if="demo" />
        <p v-else class="demo__missing">未找到示例：{{ src }}</p>
      </PhoneFrame>
      <component :is="demo" v-else-if="demo" />
    </div>

    <div class="demo__bar">
      <button type="button" class="demo__toggle" :aria-expanded="open" @click="open = !open">
        <span>{{ open ? '收起代码' : '查看代码' }}</span>
        <svg viewBox="0 0 24 24" width="14" height="14" :class="{ 'is-open': open }" aria-hidden="true">
          <path
            d="M6 9l6 6 6-6"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
      <button type="button" class="demo__copy" @click="copy">
        {{ copied ? '已复制' : '复制代码' }}
      </button>
    </div>

    <div v-show="open" class="demo__code">
      <pre><code v-html="highlighted" /></pre>
    </div>
  </section>
</template>

<style scoped>
.demo {
  margin: 20px 0 28px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
  background: var(--vp-c-bg);
}

.demo__head {
  padding: 14px 18px 0;
}

.demo__title {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-text-1);
}

.demo__desc {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.demo__stage {
  display: flex;
  justify-content: center;
  padding: 20px;
  background: var(--vp-c-bg-soft);
}

/* 示例内容（如跑马灯的 max-content 轨道）不允许把手机框撑破 */
.demo__stage > * {
  min-width: 0;
}

.demo__stage.is-plain {
  background: var(--vp-c-bg);
}

.demo__bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  height: 42px;
  padding: 0 10px;
  border-top: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
}

.demo__toggle,
.demo__copy {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 28px;
  padding: 0 10px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  color: var(--vp-c-text-2);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.demo__toggle:hover,
.demo__copy:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-brand-1);
}

.demo__toggle svg {
  transition: transform 0.2s;
}

.demo__toggle svg.is-open {
  transform: rotate(180deg);
}

.demo__code {
  border-top: 1px solid var(--vp-c-divider);
  background: var(--vp-code-block-bg);
  max-height: 460px;
  overflow: auto;
}

.demo__code pre {
  margin: 0;
  padding: 16px 18px;
  font-size: 12.5px;
  line-height: 1.7;
}

.demo__code code {
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-text-1);
}

.demo__missing {
  color: var(--vp-c-danger-1);
  font-size: 13px;
}

:deep(.tok-comment) {
  color: #8b98a5;
  font-style: italic;
}

:deep(.tok-tag) {
  color: #00a0e9;
}

:deep(.tok-attr) {
  color: #b07aff;
}

:deep(.tok-str) {
  color: #00b98a;
}

:deep(.tok-punc) {
  color: #93a1ae;
}

:deep(.tok-mustache) {
  color: #ff9f1c;
}
</style>
