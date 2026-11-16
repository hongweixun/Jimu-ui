<script setup lang="ts">
import { computed } from 'vue'
import Icon from './Icon.vue'

defineOptions({ name: 'JmResult' })

const props = withDefaults(
  defineProps<{
    /** 状态，决定图标与配色 */
    status?: 'success' | 'error' | 'warning' | 'info' | 'waiting'
    /** 自定义图标名（优先于 status） */
    icon?: string
    title?: string
    description?: string
  }>(),
  {
    status: 'info',
  },
)

const iconName = computed(() => {
  if (props.icon) return props.icon
  switch (props.status) {
    case 'success':
      return 'check'
    case 'error':
      return 'close'
    case 'warning':
      return 'warning'
    case 'waiting':
      return 'loading'
    default:
      return 'info'
  }
})

const spinning = computed(() => props.status === 'waiting' && !props.icon)
</script>

<template>
  <div class="jm-result" :class="`jm-result--${status}`" role="status">
    <div class="jm-result__icon">
      <slot name="icon">
        <Icon :name="iconName" :size="38" :spin="spinning" />
      </slot>
    </div>

    <div v-if="title || $slots.title" class="jm-result__title">
      <slot name="title">{{ title }}</slot>
    </div>

    <div v-if="description || $slots.description" class="jm-result__desc">
      <slot name="description">{{ description }}</slot>
    </div>

    <div v-if="$slots.default" class="jm-result__extra">
      <slot />
    </div>
  </div>
</template>

<style>
.jm-result {
  --jm-result-color: var(--jm-color-primary);
  --jm-result-bg: var(--jm-color-primary-light);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--jm-space-8) var(--jm-space-6);
  text-align: center;
  font-family: var(--jm-font-family);
}

.jm-result--success {
  --jm-result-color: var(--jm-color-success);
  --jm-result-bg: var(--jm-color-success-light);
}

.jm-result--error {
  --jm-result-color: var(--jm-color-danger);
  --jm-result-bg: var(--jm-color-danger-light);
}

.jm-result--warning {
  --jm-result-color: var(--jm-color-warning);
  --jm-result-bg: var(--jm-color-warning-light);
}

.jm-result--waiting {
  --jm-result-color: var(--jm-text-color-3);
  --jm-result-bg: var(--jm-bg-input);
}

.jm-result__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin-bottom: var(--jm-space-4);
  border-radius: 50%;
  background: var(--jm-result-bg);
  color: var(--jm-result-color);
}

.jm-result__title {
  font-size: var(--jm-font-size-xl);
  font-weight: var(--jm-font-weight-medium);
  line-height: var(--jm-line-height-tight);
  color: var(--jm-text-color);
}

.jm-result__desc {
  margin-top: var(--jm-space-2);
  font-size: var(--jm-font-size-sm);
  line-height: 1.6;
  color: var(--jm-text-color-3);
}

.jm-result__extra {
  display: flex;
  gap: var(--jm-space-3);
  margin-top: var(--jm-space-6);
  width: 100%;
  justify-content: center;
}
</style>
