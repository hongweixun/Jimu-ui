<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

defineOptions({ name: 'JmEllipsis' })

const props = withDefaults(
  defineProps<{
    /** 文本内容，也可用默认插槽 */
    content?: string
    /** 收起时保留的行数，1 为单行截断 */
    rows?: number
    /** 是否可展开收起；false 时纯截断 */
    expandable?: boolean
    /** 受控展开态（v-model:expanded），不传则内部维护 */
    expanded?: boolean
    /** 展开动作文案 */
    expandText?: string
    /** 收起动作文案 */
    collapseText?: string
    /** 动作位置：text 跟在文本末尾，block 独占一行靠右 */
    actionPosition?: 'text' | 'block'
  }>(),
  {
    rows: 1,
    expandable: false,
    expanded: undefined,
    expandText: '展开',
    collapseText: '收起',
    actionPosition: 'text',
  },
)

const emit = defineEmits<{
  'update:expanded': [value: boolean]
  change: [value: boolean]
}>()

/* 展开态：传了 expanded 走受控，否则内部维护 */
const innerExpanded = ref(false)
const isExpanded = computed(() => (props.expanded === undefined ? innerExpanded.value : props.expanded))

function setExpanded(v: boolean) {
  innerExpanded.value = v
  emit('update:expanded', v)
  emit('change', v)
}

function toggle() {
  setExpanded(!isExpanded.value)
}

const textRef = ref<HTMLElement | null>(null)
const rootRef = ref<HTMLElement | null>(null)
/* 容器宽度下文本是否放不下：放不下才显示展开动作 */
const overflow = ref(false)
const clampStyle = computed(() =>
  isExpanded.value ? undefined : { '-webkit-line-clamp': String(props.rows) },
)

const actionLabel = computed(() => (isExpanded.value ? props.collapseText : props.expandText))
const showAction = computed(() => props.expandable && (overflow.value || isExpanded.value))

let ro: ResizeObserver | undefined
let lastObservedWidth = 0

/** 量一次「实际放不放得下」：临时解除截断比较内容高度/宽度 */
function measure() {
  const el = textRef.value
  if (!el || props.expanded) {
    overflow.value = false
    return
  }
  const prev = el.style.getPropertyValue('-webkit-line-clamp')
  el.style.setProperty('-webkit-line-clamp', 'unset')
  if (props.rows > 1) {
    const lh = parseFloat(getComputedStyle(el).lineHeight) || 0
    overflow.value = lh > 0 && el.scrollHeight > lh * props.rows + 2
  } else {
    overflow.value = el.scrollWidth > el.clientWidth + 1
  }
  if (prev) el.style.setProperty('-webkit-line-clamp', prev)
  else el.style.removeProperty('-webkit-line-clamp')
}

watch(
  () => [props.content, props.rows, props.expanded],
  () => {
    /* 展开态变化后再收起时需要重新量，等一帧让 clamp 生效前先量原始尺寸 */
    requestAnimationFrame(measure)
  },
)

onMounted(() => {
  measure()
  /* 观察外层容器，且只在宽度变化时重测：
     测量时解除/恢复截断会改高度，否则会自己触发自己形成死循环 */
  if (typeof ResizeObserver !== 'undefined' && rootRef.value) {
    lastObservedWidth = rootRef.value.clientWidth
    ro = new ResizeObserver((entries) => {
      const w = entries[0]?.contentRect.width ?? 0
      if (Math.abs(w - lastObservedWidth) < 1) return
      lastObservedWidth = w
      measure()
    })
    ro.observe(rootRef.value)
  }
})

onBeforeUnmount(() => ro?.disconnect())

defineExpose({ measure })
</script>

<template>
  <div ref="rootRef" class="jm-ellipsis" :class="{ 'is-expanded': isExpanded }">
    <span ref="textRef" class="jm-ellipsis__text" :style="clampStyle">
      <slot>{{ content }}</slot><template v-if="showAction && actionPosition === 'text'">
        <button type="button" class="jm-ellipsis__action" @click.stop="toggle">{{ actionLabel }}</button></template>
    </span>
    <div v-if="showAction && actionPosition === 'block'" class="jm-ellipsis__action-row">
      <button type="button" class="jm-ellipsis__action" @click="toggle">{{ actionLabel }}</button>
    </div>
  </div>
</template>

<style>
.jm-ellipsis {
  min-width: 0;
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  line-height: 1.6;
  color: var(--jm-text-color);
}

.jm-ellipsis__text {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
  /* -webkit-line-clamp 由内联样式按 rows 写入，展开态解除 */
}

.jm-ellipsis__action {
  border: 0;
  padding: 0;
  margin: 0 0 0 4px;
  background: none;
  font: inherit;
  color: var(--jm-color-primary);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-ellipsis__action:active {
  opacity: 0.7;
}

.jm-ellipsis__action-row {
  margin-top: 2px;
  text-align: right;
}

.jm-ellipsis__action-row .jm-ellipsis__action {
  margin: 0;
}
</style>
