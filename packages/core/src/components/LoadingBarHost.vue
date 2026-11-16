<script setup lang="ts">
import { computed } from 'vue'
import { loadingBarState } from './loading-bar'

defineOptions({ name: 'JmLoadingBar' })

const barColor = computed(() => {
  if (loadingBarState.failed) return loadingBarState.errorColor || 'var(--jm-color-danger)'
  return loadingBarState.color || 'var(--jm-color-primary)'
})
</script>

<template>
  <div
    class="jm-loading-bar"
    :class="{
      'is-visible': loadingBarState.visible,
      'is-failed': loadingBarState.failed,
      'is-inline': loadingBarState.inline,
    }"
    :style="{
      zIndex: loadingBarState.zIndex,
      '--jm-loading-bar-color': barColor,
      '--jm-loading-bar-size': `${loadingBarState.height}px`,
    }"
    role="progressbar"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="Math.round(loadingBarState.progress)"
  >
    <div class="jm-loading-bar__inner" :style="{ width: `${loadingBarState.progress}%` }">
      <span class="jm-loading-bar__glow" aria-hidden="true" />
    </div>
  </div>
</template>

<style scoped>
.jm-loading-bar {
  position: fixed;
  top: var(--jm-safe-top, 0px);
  right: 0;
  left: 0;
  height: var(--jm-loading-bar-size, 2px);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.22s ease;
}

.jm-loading-bar.is-inline {
  position: absolute;
}

.jm-loading-bar.is-visible {
  opacity: 1;
}

.jm-loading-bar__inner {
  position: relative;
  height: 100%;
  border-radius: 0 2px 2px 0;
  background: var(--jm-loading-bar-color, var(--jm-color-primary));
  transition: width 0.2s ease;
  will-change: width;
}

.jm-loading-bar__glow {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 60px;
  border-radius: 0 2px 2px 0;
  background: linear-gradient(90deg, transparent, var(--jm-loading-bar-color, var(--jm-color-primary)));
  opacity: 0.6;
  filter: blur(1px);
}

[data-motion='off'] .jm-loading-bar,
[data-motion='off'] .jm-loading-bar__inner {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-loading-bar,
  .jm-loading-bar__inner {
    transition: none;
  }

  .jm-loading-bar__glow {
    display: none;
  }
}
</style>
