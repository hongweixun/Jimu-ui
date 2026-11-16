<script setup lang="ts">
import { computed, inject, onBeforeUnmount, ref, watch } from 'vue'
import { COLLAPSE_KEY, type CollapseName } from './collapse-context'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmCollapseItem' })

const props = withDefaults(
  defineProps<{
    name: CollapseName
    title?: string
    disabled?: boolean
    showArrow?: boolean
    /** 内容区自定义内边距，传 0 可去掉 */
    contentPadding?: string
  }>(),
  { showArrow: true, contentPadding: '0 16px 14px' },
)

const emit = defineEmits<{ click: [name: CollapseName] }>()

const ctx = inject(COLLAPSE_KEY, null)
const open = computed(() => (ctx ? ctx.isExpanded(props.name) : false))

const contentRef = ref<HTMLElement | null>(null)
const height = ref(open.value ? 'auto' : '0px')
let timer: ReturnType<typeof setTimeout> | undefined

watch(open, (expanded) => {
  const el = contentRef.value
  if (!el) {
    height.value = expanded ? 'auto' : '0px'
    return
  }
  clearTimeout(timer)
  if (expanded) {
    // 先给确定高度才能动画，动画结束后放开为 auto（内容后续变高也不会被裁）
    height.value = `${el.scrollHeight}px`
    timer = setTimeout(() => {
      if (open.value) height.value = 'auto'
    }, 360)
  } else {
    // 从 auto 收起：先固定当前高度，强制回流，再置 0
    height.value = `${el.scrollHeight}px`
    void el.offsetHeight
    requestAnimationFrame(() => {
      height.value = '0px'
    })
  }
})

onBeforeUnmount(() => clearTimeout(timer))

function onTitleClick() {
  if (props.disabled) return
  ctx?.toggle(props.name)
  emit('click', props.name)
}
</script>

<template>
  <div class="jm-collapse-item" :class="{ 'is-expanded': open, 'is-disabled': disabled }">
    <div
      class="jm-collapse-item__title"
      role="button"
      :tabindex="disabled ? undefined : 0"
      :aria-expanded="open ? 'true' : 'false'"
      :aria-disabled="disabled || undefined"
      @click="onTitleClick"
      @keydown.enter="onTitleClick"
    >
      <div class="jm-collapse-item__title-text">
        <slot name="title">{{ title }}</slot>
      </div>
      <div class="jm-collapse-item__extra">
        <slot name="extra" />
        <span v-if="showArrow" class="jm-collapse-item__arrow" aria-hidden="true">
          <jm-icon name="chevron-down" size="18px" :stroke-width="2" />
        </span>
      </div>
    </div>

    <div class="jm-collapse-item__wrapper" :style="{ height }">
      <div ref="contentRef" class="jm-collapse-item__content" :style="{ padding: contentPadding }">
        <slot />
      </div>
    </div>
  </div>
</template>

<style>
.jm-collapse-item {
  position: relative;
  background: var(--jm-bg-container);
}

.jm-collapse-item + .jm-collapse-item::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 1px;
  background: var(--jm-border-color);
  transform: scaleY(0.5);
  transform-origin: top;
}

.jm-collapse-item__title {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  min-height: var(--jm-cell-height);
  padding: 12px var(--jm-space-4);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  border-radius: var(--jm-radius-sm);
  transition: background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-collapse-item__title:active {
  background: var(--jm-bg-active);
}

.jm-collapse-item.is-disabled .jm-collapse-item__title {
  opacity: 0.45;
  cursor: not-allowed;
}

.jm-collapse-item__title-text {
  flex: 1 1 auto;
  min-width: 0;
  font-size: var(--jm-font-size-md);
  line-height: var(--jm-line-height);
  color: var(--jm-text-color);
}

.jm-collapse-item__extra {
  display: flex;
  align-items: center;
  gap: var(--jm-space-2);
  flex: 0 0 auto;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
}

.jm-collapse-item__arrow {
  display: flex;
  width: 18px;
  height: 18px;
  color: var(--jm-text-color-3);
  transition: transform var(--jm-duration-3) var(--jm-motion-transition-ease);
}

.jm-collapse-item.is-expanded .jm-collapse-item__arrow {
  transform: rotate(180deg);
}

.jm-collapse-item__arrow svg {
  width: 100%;
  height: 100%;
}

.jm-collapse-item__wrapper {
  overflow: hidden;
  /* 展开/收起是"尺寸变化"，用标准曲线 300ms：200ms 在大面板上会显得急，400ms 又拖 */
  transition: height var(--jm-duration-3) var(--jm-motion-transition-ease);
  will-change: height;
}

.jm-collapse-item__content {
  font-size: var(--jm-font-size-sm);
  line-height: var(--jm-line-height);
  color: var(--jm-text-color-2);
}

/* 动效关闭：高度直接跳变，不做 height 过渡 */
[data-motion='off'] .jm-collapse-item__wrapper,
[data-motion='off'] .jm-collapse-item__arrow {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-collapse-item__wrapper,
  .jm-collapse-item__arrow {
    transition: none;
  }
}
</style>
