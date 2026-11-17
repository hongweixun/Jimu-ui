<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmPagination' })

const props = withDefaults(
  defineProps<{
    modelValue?: number
    /** 总条数；也可直接用 pageCount 指定总页数 */
    total?: number
    pageSize?: number
    pageCount?: number
    /** simple：只显示“箭头 / 当前页 共 N 页 / 箭头” */
    simple?: boolean
    /** 中间最多连续显示几个数字页码（含首尾与省略号） */
    pagerCount?: number
    disabled?: boolean
    /** 上一页 / 下一页只显示箭头时不带文字 */
    iconOnly?: boolean
    prevText?: string
    nextText?: string
    /** 只有一页时隐藏整个分页器 */
    hideOnSinglePage?: boolean
    /** 显示每页条数切换器 */
    showSizeChanger?: boolean
    /** 每页条数可选项 */
    sizeOption?: number[]
    /** 开启页码快速跳转（普通模式） */
    showQuickJumper?: boolean
  }>(),
  {
    modelValue: 1,
    total: 0,
    pageSize: 10,
    pagerCount: 5,
    prevText: '上一页',
    nextText: '下一页',
    showSizeChanger: false,
    sizeOption: () => [10, 20, 50, 100],
    showQuickJumper: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [page: number]
  'update:pageSize': [size: number]
  change: [page: number, size: number]
}>()

const size = ref(props.pageSize)
watch(
  () => props.pageSize,
  (v) => {
    size.value = v
  },
)

const count = computed(() => {
  if (props.pageCount !== undefined) return Math.max(1, Math.floor(props.pageCount))
  return Math.max(1, Math.ceil(props.total / Math.max(1, size.value)))
})

const current = computed(() => Math.min(Math.max(1, props.modelValue), count.value))

const hidden = computed(() => props.hideOnSinglePage && count.value <= 1)

const rangeStart = computed(() => (current.value - 1) * size.value + 1)
const rangeEnd = computed(() => Math.min(current.value * size.value, props.total || count.value * size.value))

type Token = number | 'prev-more' | 'next-more'

/**
 * 页码折叠：首尾页常驻，中间按当前页位置滑动。
 * pagerCount 是数字页码的最大个数（默认 5），超出部分用省略号代替，
 * 省略号可以直接点，前后各跳一屏。
 */
const tokens = computed<Token[]>(() => {
  const total = count.value
  const cur = current.value
  const slots = Math.max(3, props.pagerCount)
  if (total <= slots) return Array.from({ length: total }, (_, i) => i + 1)

  // 贴着首端：1 2 3 4 … N
  if (cur <= slots - 2) {
    const list: Token[] = Array.from({ length: slots - 1 }, (_, i) => i + 1)
    list.push('next-more', total)
    return list
  }

  // 贴着末端：1 … N-3 N-2 N-1 N
  if (cur >= total - (slots - 3)) {
    const list: Token[] = [1, 'prev-more']
    for (let i = total - (slots - 2); i <= total; i++) list.push(i)
    return list
  }

  // 中间：1 … cur-1 cur cur+1 … N
  return [1, 'prev-more', cur - 1, cur, cur + 1, 'next-more', total]
})

function emitChange(page: number) {
  emit('update:modelValue', page)
  emit('change', page, size.value)
}

function go(page: number) {
  if (props.disabled) return
  const next = Math.min(Math.max(1, page), count.value)
  if (next === current.value) return
  emitChange(next)
}

function onToken(token: Token) {
  if (token === 'prev-more') go(current.value - Math.max(2, props.pagerCount - 2))
  else if (token === 'next-more') go(current.value + Math.max(2, props.pagerCount - 2))
  else go(token)
}

function onSizeChange(e: Event) {
  if (props.disabled) return
  const next = Number((e.target as HTMLSelectElement).value)
  if (next === size.value) return
  size.value = next
  emit('update:pageSize', next)
  const page = Math.min(current.value, count.value)
  emit('update:modelValue', page)
  emit('change', page, next)
}

/* ---------- 快速跳转 ---------- */
const jumper = ref('')
const jumperError = ref(false)

function onJumper() {
  if (props.disabled) return
  const n = Number(jumper.value)
  if (!jumper.value || Number.isNaN(n)) return
  if (n < 1 || n > count.value) {
    jumperError.value = true
    setTimeout(() => (jumperError.value = false), 800)
    jumper.value = ''
    return
  }
  jumper.value = ''
  go(n)
}
</script>

<template>
  <nav
    v-if="!hidden"
    class="jm-pagination"
    :class="{ 'is-simple': simple, 'is-disabled': disabled }"
  >
    <p v-if="$slots.total" class="jm-pagination__total">
      <slot name="total" :total="total" :range="[rangeStart, rangeEnd]" />
    </p>

    <template v-if="simple">
      <button
        type="button"
        class="jm-pagination__arrow"
        :disabled="disabled || current <= 1"
        aria-label="上一页"
        @click="go(current - 1)"
      >
        <jm-icon name="chevron-left" size="16px" :stroke-width="2.2" />
      </button>
      <span class="jm-pagination__summary">
        <b>{{ current }}</b>
        <span class="jm-pagination__slash">/</span>
        {{ count }}
      </span>
      <button
        type="button"
        class="jm-pagination__arrow"
        :disabled="disabled || current >= count"
        aria-label="下一页"
        @click="go(current + 1)"
      >
        <jm-icon name="chevron-right" size="16px" :stroke-width="2.2" />
      </button>
    </template>

    <template v-else>
      <button
        type="button"
        class="jm-pagination__prev"
        :class="{ 'is-icon-only': iconOnly }"
        :disabled="disabled || current <= 1"
        aria-label="上一页"
        @click="go(current - 1)"
      >
        <jm-icon name="chevron-left" size="16px" :stroke-width="2.2" />
        <span v-if="!iconOnly">{{ prevText }}</span>
      </button>

      <ul class="jm-pagination__pages">
        <li v-for="(token, i) in tokens" :key="`${token}-${i}`">
          <button
            v-if="typeof token === 'string'"
            type="button"
            class="jm-pagination__more"
            :aria-label="token === 'prev-more' ? '向前翻页' : '向后翻页'"
            :disabled="disabled"
            @click="onToken(token)"
          >
            <jm-icon name="more-horizontal" size="16px" :stroke-width="2.4" />
          </button>
          <button
            v-else
            type="button"
            class="jm-pagination__page"
            :class="{ 'is-active': token === current }"
            :aria-current="token === current ? 'page' : undefined"
            :disabled="disabled"
            @click="onToken(token)"
          >
            {{ token }}
          </button>
        </li>
      </ul>

      <button
        type="button"
        class="jm-pagination__next"
        :class="{ 'is-icon-only': iconOnly }"
        :disabled="disabled || current >= count"
        aria-label="下一页"
        @click="go(current + 1)"
      >
        <span v-if="!iconOnly">{{ nextText }}</span>
        <jm-icon name="chevron-right" size="16px" :stroke-width="2.2" />
      </button>
    </template>

    <label v-if="showSizeChanger && !pageCount" class="jm-pagination__size" :class="{ 'is-disabled': disabled }">
      <select :value="size" :disabled="disabled" @change="onSizeChange">
        <option v-for="opt in sizeOption" :key="opt" :value="opt">{{ opt }} 条/页</option>
      </select>
    </label>

    <div v-if="showQuickJumper && !simple" class="jm-pagination__jumper" :class="{ 'is-error': jumperError }">
      <span>{{ jumperError ? `请输入 1 ~ ${count}` : '跳至' }}</span>
      <input
        v-model="jumper"
        type="number"
        inputmode="numeric"
        :disabled="disabled"
        :placeholder="String(current)"
        @keyup.enter="onJumper"
        @blur="onJumper"
      />
      <span>页</span>
    </div>

    <slot />
  </nav>
</template>

<style>
.jm-pagination {
  /* 组件自身作为容器：宽度不够时按容器（而非视口）收缩，
     放进手机模拟框、侧栏等窄容器里也能正确收缩 */
  container-type: inline-size;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
  box-sizing: border-box;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
  -webkit-tap-highlight-color: transparent;
}

.jm-pagination button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  height: 32px;
  padding: 0 10px;
  box-sizing: border-box;
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: none;
  color: inherit;
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
  transition:
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-pagination button:disabled {
  opacity: 0.38;
  cursor: not-allowed;
}

/* ---------- 总数（total 插槽） ---------- */
.jm-pagination__total {
  flex: 1 1 100%;
  margin: 0;
  font-size: var(--jm-font-size-sm);
  line-height: 24px;
  color: var(--jm-text-color-2);
}

/* ---------- 普通模式：Varlet 风格悬浮条 ---------- */
.jm-pagination:not(.is-simple) {
  padding: 6px 10px;
  border-radius: var(--jm-radius-md);
  background: var(--jm-bg-elevated);
  box-shadow: var(--jm-shadow-1);
}

.jm-pagination__pages {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-width: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}

.jm-pagination__pages li {
  display: flex;
}

.jm-pagination__page {
  min-width: 32px;
  height: 32px;
  padding: 0 4px;
  border-radius: var(--jm-radius-sm);
  font-variant-numeric: tabular-nums;
}

.jm-pagination__page:not(:disabled):not(.is-active):hover {
  background: var(--jm-bg-hover);
}

/* 当前页：主色实底 + 白字（Varlet 风格） */
.jm-pagination__page.is-active {
  background: var(--jm-color-primary);
  color: var(--jm-color-primary-contrast);
  font-weight: var(--jm-font-weight-medium);
  box-shadow: 0 2px 8px color-mix(in srgb, var(--jm-color-primary) 35%, transparent);
}

.jm-pagination button:not(:disabled):active {
  background: var(--jm-bg-hover);
}

.jm-pagination__page.is-active:not(:disabled):active {
  background: var(--jm-color-primary);
}

.jm-pagination__more {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  color: var(--jm-text-color-3);
  cursor: pointer;
}

.jm-pagination__more:not(:disabled):hover {
  background: var(--jm-bg-hover);
}

.jm-pagination__more:not(:disabled):active {
  color: var(--jm-color-primary);
}

.jm-pagination__prev,
.jm-pagination__next {
  flex: 0 0 auto;
  color: var(--jm-text-color);
}

.jm-pagination__prev:not(:disabled):hover,
.jm-pagination__next:not(:disabled):hover {
  background: var(--jm-bg-hover);
}

/* ---------- 简单模式 ---------- */
.jm-pagination.is-simple {
  justify-content: center;
  gap: var(--jm-space-3);
}

.jm-pagination__arrow {
  width: 32px;
  padding: 0;
  border-radius: 50%;
  color: var(--jm-text-color);
}

.jm-pagination__arrow:not(:disabled):hover {
  background: var(--jm-bg-hover);
}

.jm-pagination__summary {
  font-variant-numeric: tabular-nums;
  color: var(--jm-text-color-2);
}

.jm-pagination__summary b {
  color: var(--jm-text-color);
  font-weight: var(--jm-font-weight-medium);
}

.jm-pagination__slash {
  margin: 0 2px;
  opacity: 0.5;
}

/* ---------- 每页条数切换 ---------- */
.jm-pagination__size select {
  height: 32px;
  padding: 0 4px 0 8px;
  box-sizing: border-box;
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: transparent;
  color: var(--jm-text-color-2);
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
  outline-offset: 2px;
}

.jm-pagination__size select:focus-visible {
  outline: 2px solid var(--jm-color-primary);
}

/* ---------- 快速跳转 ---------- */
.jm-pagination__jumper {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--jm-text-color-2);
}

.jm-pagination__jumper.is-error span:first-child {
  color: var(--jm-color-danger);
}

.jm-pagination__jumper input {
  width: 44px;
  height: 32px;
  box-sizing: border-box;
  border: var(--jm-border-width) solid var(--jm-border-color);
  border-radius: var(--jm-radius-sm);
  background: transparent;
  color: var(--jm-text-color);
  font-family: inherit;
  font-size: inherit;
  text-align: center;
  appearance: textfield;
}

.jm-pagination__jumper input::-webkit-outer-spin-button,
.jm-pagination__jumper input::-webkit-inner-spin-button {
  appearance: none;
}

.jm-pagination__jumper input:focus-visible {
  outline: none;
  border-color: var(--jm-color-primary);
}

.jm-pagination__jumper.is-error input {
  border-color: var(--jm-color-danger);
}

[data-motion='off'] .jm-pagination button {
  transition: none;
}

/* ---------- 窄容器：压缩页码与间距 ----------
   断点按 content-box 计（根元素左右 padding 10px×2），
   340 ≈ 视觉 360，280 ≈ 视觉 300 */
@container (max-width: 340px) {
  .jm-pagination {
    gap: 4px;
  }

  .jm-pagination__pages {
    gap: 2px;
  }

  .jm-pagination__page,
  .jm-pagination__more {
    min-width: 28px;
    width: 28px;
    height: 30px;
  }
}

@container (max-width: 280px) {
  .jm-pagination__page,
  .jm-pagination__more {
    min-width: 24px;
    width: 24px;
  }

  .jm-pagination__prev span,
  .jm-pagination__next span {
    display: none;
  }

  .jm-pagination__prev,
  .jm-pagination__next {
    padding: 0 6px;
  }
}

/* 旧浏览器兜底 */
@supports not (container-type: inline-size) {
  @media (max-width: 360px) {
    .jm-pagination__page,
    .jm-pagination__more {
      min-width: 28px;
      width: 28px;
      height: 30px;
    }
  }

  @media (max-width: 300px) {
    .jm-pagination__page,
    .jm-pagination__more {
      min-width: 24px;
      width: 24px;
    }

    .jm-pagination__prev span,
    .jm-pagination__next span {
      display: none;
    }
  }
}
</style>
