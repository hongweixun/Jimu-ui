<script setup lang="ts">
import { computed } from 'vue'
import JmNotify from './Notify.vue'
import { closeNotify, notifyState } from './notify'

defineOptions({ name: 'JmNotifyHost' })

/** 后进来的排最上面：顶部通知的阅读顺序是「最新 → 最旧」 */
const list = computed(() => [...notifyState.items].reverse())

function onClose(id: number, onClose?: () => void) {
  onClose?.()
  closeNotify(id)
}
</script>

<template>
  <div
    v-if="notifyState.items.length"
    class="jm-notify-host"
    :class="{ 'is-inline': notifyState.inline }"
  >
    <TransitionGroup name="jm-notify-stack">
      <div v-for="item in list" :key="item.id" class="jm-notify-host__item">
        <jm-notify
          show
          inline
          :type="item.type"
          :title="item.title"
          :message="item.message"
          :duration="item.duration ?? 3000"
          :closeable="item.closeable ?? true"
          :icon="item.icon"
          :color="item.color"
          :background="item.background"
          :safe-area-inset-top="item.safeAreaInsetTop"
          @click="item.onClick?.($event)"
          @close="onClose(item.id, item.onClose)"
        />
      </div>
    </TransitionGroup>
  </div>
</template>

<style>
.jm-notify-host {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 2100;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

/* 挂在自定义容器里：跟随容器绝对定位，不贴浏览器视口 */
.jm-notify-host.is-inline {
  position: absolute;
}

.jm-notify-host__item {
  position: relative;
  pointer-events: auto;
}

/* 宿主里的每一条都参与流式堆叠，不受 inline 的绝对定位影响 */
.jm-notify-host .jm-notify.is-inline {
  position: relative;
  top: auto;
  right: auto;
  left: auto;
  width: 100%;
}

/* 堆叠增删：新的一条从上方落入，旧的整体下移，移除时反向收回 */
.jm-notify-stack-enter-active,
.jm-notify-stack-leave-active,
.jm-notify-stack-move {
  transition:
    transform var(--jm-duration-3) var(--jm-motion-enter-ease),
    opacity var(--jm-duration-2) var(--jm-motion-enter-ease);
}

.jm-notify-stack-enter-from {
  transform: translate3d(0, -100%, 0);
  opacity: 0;
}

.jm-notify-stack-leave-to {
  transform: translate3d(0, -12px, 0);
  opacity: 0;
}

.jm-notify-stack-leave-active {
  position: absolute;
  left: 0;
  right: 0;
}

[data-motion='off'] .jm-notify-stack-enter-active,
[data-motion='off'] .jm-notify-stack-leave-active,
[data-motion='off'] .jm-notify-stack-move {
  transition: opacity 120ms linear;
}

[data-motion='off'] .jm-notify-stack-enter-from,
[data-motion='off'] .jm-notify-stack-leave-to {
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-notify-stack-enter-active,
  .jm-notify-stack-leave-active,
  .jm-notify-stack-move {
    transition: opacity 120ms linear;
  }

  .jm-notify-stack-enter-from,
  .jm-notify-stack-leave-to {
    transform: none;
  }
}
</style>
