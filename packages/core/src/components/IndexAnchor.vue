<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, ref } from 'vue'
import { INDEX_BAR_KEY } from './index-bar-context'

defineOptions({ name: 'JmIndexAnchor' })

const props = defineProps<{
  /** 分组索引，与右侧索引条一一对应 */
  index: string
  /** 自定义标题内容，默认显示 index */
  title?: string
}>()

const ctx = inject(INDEX_BAR_KEY, null)
const sticky = computed(() => ctx?.sticky.value ?? true)
const root = ref<HTMLElement>()
let unregister: (() => void) | null = null

onMounted(() => {
  unregister = ctx?.register(props.index, () => root.value) ?? null
})

onBeforeUnmount(() => {
  unregister?.()
})
</script>

<template>
  <div ref="root" class="jm-index-anchor">
    <div class="jm-index-anchor__header" :class="{ 'is-sticky': sticky }">
      <slot name="title">{{ title ?? index }}</slot>
    </div>
    <div class="jm-index-anchor__content">
      <slot />
    </div>
  </div>
</template>

<style>
.jm-index-anchor {
  font-family: var(--jm-font-family);
}

.jm-index-anchor__header {
  display: flex;
  align-items: center;
  padding: var(--jm-space-2) var(--jm-space-4);
  background: var(--jm-bg-page);
  color: var(--jm-text-color-2);
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
}

/* 吸顶：靠原生 sticky，滚动容器是谁就贴在谁顶部 */
.jm-index-anchor__header.is-sticky {
  position: sticky;
  top: 0;
  z-index: 1;
}

.jm-index-anchor__content {
  background: var(--jm-bg-container);
}
</style>
