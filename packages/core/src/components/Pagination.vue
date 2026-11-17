<script setup lang="ts">
import { computed } from 'vue'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmPagination' })

const props = withDefaults(
  defineProps<{
    modelValue?: number
    /** 总条数；也可直接用 pageCount 指定总页数 */
    total?: number
    pageSize?: number
    pageCount?: number
    /** simple：只显示“上一页 / 当前页 共 N 页 / 下一页” */
    simple?: boolean
    /** 中间最多连续显示几个页码（含首尾与省略号） */
    pagerCount?: number
    disabled?: boolean
    /** 上一页 / 下一页只显示箭头时不带文字 */
    iconOnly?: boolean
    prevText?: string
    nextText?: string
    /** 只有一页时隐藏整个分页器 */
    hideOnSinglePage?: boolean
  }>(),
  {
    modelValue: 1,
    total: 0,
    pageSize: 10,
    pagerCount: 5,
    prevText: '上一页',
    nextText: '下一页',
  },
)

const emit = defineEmits<{
  'update:modelValue': [page: number]
  change: [page: number]
}>()

const count = computed(() => {
  if (props.pageCount !== undefined) return Math.max(1, Math.floor(props.pageCount))
  return Math.max(1, Math.ceil(props.total / Math.max(1, props.pageSize)))
})

const current = computed(() => Math.min(Math.max(1, props.modelValue), count.value))

const hidden = computed(() => props.hideOnSinglePage && count.value <= 1)

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

function go(page: number) {
  if (props.disabled) return
  const next = Math.min(Math.max(1, page), count.value)
  if (next === current.value) return
  emit('update:modelValue', next)
  emit('change', next)
}

function onToken(token: Token) {
  if (token === 'prev-more') go(current.value - Math.max(2, props.pagerCount - 2))
  else if (token === 'next-more') go(current.value + Math.max(2, props.pagerCount - 2))
  else go(token)
}
</script>

<template>
  <nav v-if="!hidden" class="jm-pagination" :class="{ 'is-simple': simple, 'is-disabled': disabled }">
    <template v-if="simple">
      <button
        type="button"
        class="jm-pagination__arrow"
        :disabled="disabled || current <= 1"
        aria-label="上一页"
        @click="go(current - 1)"
      >
        <jm-icon name="chevron-left" size="14px" :stroke-width="2.2" />
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
        <jm-icon name="chevron-right" size="14px" :stroke-width="2.2" />
      </button>
    </template>

    <template v-else>
      <button
        type="button"
        class="jm-pagination__prev"
        :class="{ 'is-icon-only': iconOnly }"
        :disabled="disabled || current <= 1"
        @click="go(current - 1)"
      >
        <jm-icon name="chevron-left" size="14px" :stroke-width="2.2" />
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
            <jm-icon name="more-horizontal" size="14px" :stroke-width="2.4" />
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
        @click="go(current + 1)"
      >
        <span v-if="!iconOnly">{{ nextText }}</span>
        <jm-icon name="chevron-right" size="14px" :stroke-width="2.2" />
      </button>
    </template>

    <slot />
  </nav>
</template>

<style>
.jm-pagination {
  /* 组件自身作为容器：宽度不够时按容器（而非视口）收缩箭头文字，
     放进手机模拟框、侧栏等窄容器里也能正确收起 */
  container-type: inline-size;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--jm-space-2);
  width: 100%;
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

.jm-pagination__pages {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  justify-content: center;
  gap: 2px;
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
  padding: 0 4px;
  font-variant-numeric: tabular-nums;
}

.jm-pagination__page.is-active {
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-weight: var(--jm-font-weight-medium);
}

.jm-pagination button:not(:disabled):active {
  background: var(--jm-bg-hover);
}

.jm-pagination__more {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 32px;
  padding: 0;
  color: var(--jm-text-color-3);
  cursor: pointer;
}

.jm-pagination__more:not(:disabled):active {
  color: var(--jm-color-primary);
}

.jm-pagination__prev,
.jm-pagination__next {
  flex: 0 0 auto;
  color: var(--jm-text-color);
}

.jm-pagination.is-simple {
  justify-content: center;
  gap: var(--jm-space-3);
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

[data-motion='off'] .jm-pagination button {
  transition: none;
}

/* ---------- 窄容器：页面多时把箭头文字收起来，只留箭头 ---------- */
/* 容器查询：跟着组件自身宽度走（模拟框/侧栏/半屏弹层里也正确） */
@container (max-width: 420px) {
  .jm-pagination__prev span,
  .jm-pagination__next span {
    display: none;
  }

  .jm-pagination__prev,
  .jm-pagination__next {
    padding: 0 6px;
  }

  .jm-pagination {
    gap: 6px;
  }

  .jm-pagination__pages {
    gap: 0;
  }

  .jm-pagination__page {
    min-width: 28px;
    padding: 0 2px;
  }

  .jm-pagination__more {
    width: 26px;
  }
}

/* 旧浏览器兜底：按视口宽度收窄（与容器查询规则一致，不冲突） */
@supports not (container-type: inline-size) {
  @media (max-width: 420px) {
    .jm-pagination__prev span,
    .jm-pagination__next span {
      display: none;
    }

    .jm-pagination__prev,
    .jm-pagination__next {
      padding: 0 6px;
    }

    .jm-pagination__page {
      min-width: 28px;
      padding: 0 2px;
    }

    .jm-pagination__more {
      width: 26px;
    }
  }
}
</style>
