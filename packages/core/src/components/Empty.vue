<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'JmEmpty' })

const props = withDefaults(
  defineProps<{
    description?: string
    size?: 'small' | 'medium' | 'large'
    /** 图标宽度，数字按 px */
    imageSize?: number | string
  }>(),
  { description: '暂无数据', size: 'medium' },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.imageSize !== undefined) {
    s['--jm-empty-image-size'] = typeof props.imageSize === 'number' ? `${props.imageSize}px` : props.imageSize
  }
  return s
})
</script>

<template>
  <div class="jm-empty" :class="`jm-empty--${size}`" :style="styles" role="status">
    <div class="jm-empty__image">
      <slot name="image">
        <svg viewBox="0 0 120 120" fill="none" aria-hidden="true">
          <rect
            x="18"
            y="42"
            width="84"
            height="58"
            rx="10"
            style="fill: var(--jm-color-primary-light); stroke: var(--jm-color-primary-border)"
            stroke-width="1.5"
          />
          <path
            d="M18 58h84"
            style="stroke: var(--jm-color-primary-border)"
            stroke-width="1.5"
            stroke-dasharray="4 5"
          />
          <rect
            x="34"
            y="22"
            width="52"
            height="22"
            rx="6"
            style="fill: var(--jm-bg-container); stroke: var(--jm-color-primary-border)"
            stroke-width="1.5"
          />
          <path
            d="M34 34h52"
            style="stroke: var(--jm-color-primary-border)"
            stroke-width="1.5"
            opacity="0.6"
          />
          <circle cx="60" cy="72" r="9" style="fill: var(--jm-color-primary)" opacity="0.18" />
          <path
            d="M56 72h8M60 68v8"
            style="stroke: var(--jm-color-primary)"
            stroke-width="1.8"
            stroke-linecap="round"
          />
        </svg>
      </slot>
    </div>
    <div v-if="description || $slots.description" class="jm-empty__description">
      <slot name="description">{{ description }}</slot>
    </div>
    <div v-if="$slots.default" class="jm-empty__action">
      <slot />
    </div>
  </div>
</template>

<style>
.jm-empty {
  --jm-empty-image-size: 110px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--jm-space-7) var(--jm-space-4);
  font-family: var(--jm-font-family);
  text-align: center;
}

.jm-empty__image {
  width: var(--jm-empty-image-size);
  height: var(--jm-empty-image-size);
  color: var(--jm-color-primary);
}

.jm-empty__image svg {
  width: 100%;
  height: 100%;
}

.jm-empty__description {
  margin-top: var(--jm-space-3);
  font-size: var(--jm-font-size-sm);
  line-height: var(--jm-line-height);
  color: var(--jm-text-color-3);
}

.jm-empty__action {
  margin-top: var(--jm-space-4);
}

.jm-empty--small {
  --jm-empty-image-size: 76px;
  padding: var(--jm-space-5) var(--jm-space-3);
}

.jm-empty--large {
  --jm-empty-image-size: 150px;
  padding: var(--jm-space-8) var(--jm-space-4);
}
</style>
