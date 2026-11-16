<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'JmLoading' })

const props = withDefaults(
  defineProps<{
    type?: 'spinner' | 'circular' | 'dots' | 'pulse'
    size?: number | string
    color?: string
    text?: string
    vertical?: boolean
  }>(),
  { type: 'circular', size: 24 },
)

const sizeValue = computed(() =>
  typeof props.size === 'number' ? `${props.size}px` : props.size,
)

const styles = computed(() => ({
  '--jm-loading-size': sizeValue.value,
  ...(props.color ? { '--jm-loading-color': props.color } : {}),
}))
</script>

<template>
  <div
    class="jm-loading"
    :class="[`jm-loading--${type}`, { 'is-vertical': vertical, 'has-text': !!text }]"
    :style="styles"
    role="status"
    aria-live="polite"
  >
    <span class="jm-loading__figure" aria-hidden="true">
      <svg v-if="type === 'circular' || type === 'spinner'" viewBox="0 0 40 40" class="jm-loading__svg">
        <circle
          cx="20"
          cy="20"
          r="16"
          fill="none"
          stroke="currentColor"
          stroke-width="3"
          stroke-opacity="0.16"
        />
        <circle
          class="jm-loading__arc"
          cx="20"
          cy="20"
          r="16"
          fill="none"
          :stroke="'currentColor'"
          stroke-width="3"
          stroke-linecap="round"
          :stroke-dasharray="type === 'spinner' ? '26 74' : '72 28'"
        />
      </svg>

      <span v-else-if="type === 'dots'" class="jm-loading__dots">
        <i /><i /><i />
      </span>

      <span v-else class="jm-loading__pulse">
        <i /><i />
      </span>
    </span>

    <span v-if="text" class="jm-loading__text">{{ text }}</span>
  </div>
</template>

<style>
.jm-loading {
  --jm-loading-size: 24px;
  --jm-loading-color: var(--jm-color-primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--jm-space-2);
  color: var(--jm-loading-color);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  vertical-align: middle;
}

.jm-loading.is-vertical {
  flex-direction: column;
  gap: var(--jm-space-2);
}

.jm-loading__figure {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--jm-loading-size);
  height: var(--jm-loading-size);
  flex: 0 0 auto;
}

.jm-loading__svg {
  width: 100%;
  height: 100%;
}

.jm-loading__arc {
  transform-origin: center;
  animation: jm-loading-rotate 0.9s linear infinite;
}

.jm-loading--spinner .jm-loading__arc {
  animation-duration: 0.7s;
}

@keyframes jm-loading-rotate {
  to {
    transform: rotate(360deg);
  }
}

.jm-loading__text {
  color: var(--jm-text-color-2);
  line-height: 1.4;
}

/* 点状 */
.jm-loading__dots {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 100%;
}

.jm-loading__dots i {
  width: calc(var(--jm-loading-size) * 0.22);
  height: calc(var(--jm-loading-size) * 0.22);
  border-radius: 50%;
  background: currentColor;
  animation: jm-loading-bounce var(--jm-motion-loop-duration) var(--jm-motion-transition-ease) infinite;
}

.jm-loading__dots i:nth-child(2) {
  animation-delay: 0.15s;
}

.jm-loading__dots i:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes jm-loading-bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.45;
  }
  30% {
    transform: translateY(-35%);
    opacity: 1;
  }
}

/* 双环脉冲 */
.jm-loading__pulse {
  position: relative;
  width: 100%;
  height: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.jm-loading__pulse i {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.4;
  animation: jm-loading-pulse 1.4s var(--jm-motion-transition-ease) infinite;
}

.jm-loading__pulse i:nth-child(2) {
  width: 60%;
  height: 60%;
  opacity: 0.9;
  animation: none;
}

@keyframes jm-loading-pulse {
  0% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  100% {
    transform: scale(1.1);
    opacity: 0;
  }
}

/* 关闭动效时：加载指示属于必要动效，保留旋转但去掉弹跳与脉冲，避免视觉噪音 */
[data-motion='off'] .jm-loading__dots i,
[data-motion='off'] .jm-loading__pulse i {
  animation: none;
  opacity: 0.7;
}
</style>
