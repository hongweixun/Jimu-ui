<script setup lang="ts">
import { closeToast, toastState } from './toast'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmToastHost' })
</script>

<template>
  <Teleport to="body" :disabled="toastState.inline">
    <Transition name="jm-toast-pop">
      <div
        v-if="toastState.visible && toastState.mask"
        class="jm-toast__mask"
        :class="{ 'is-inline': toastState.inline }"
        :style="{ zIndex: toastState.zIndex - 1 }"
      />
    </Transition>
    <Transition name="jm-toast-pop">
      <div
        v-if="toastState.visible"
        class="jm-toast"
        :class="[
          `jm-toast--${toastState.position}`,
          `jm-toast--${toastState.type}`,
          { 'is-inline': toastState.inline, 'is-clickable': toastState.closeOnClick },
        ]"
        :style="{ zIndex: toastState.zIndex }"
        role="alert"
        aria-live="assertive"
        @click="toastState.closeOnClick && closeToast()"
      >
        <div class="jm-toast__box" :class="{ 'is-clickable': toastState.closeOnClick }">
          <span
            v-if="toastState.icon || toastState.type !== 'text'"
            class="jm-toast__icon"
            aria-hidden="true"
          >
            <jm-icon
              v-if="toastState.icon"
              :name="toastState.icon"
              size="32px"
              :stroke-width="1.6"
            />
            <jm-icon
              v-else-if="toastState.type === 'success'"
              name="check-circle"
              size="32px"
              :stroke-width="1.6"
            />
            <jm-icon
              v-else-if="toastState.type === 'fail'"
              name="close-circle"
              size="32px"
              :stroke-width="1.6"
            />
            <svg v-else viewBox="0 0 40 40" class="jm-toast__spinner">
              <circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.2" />
              <circle
                cx="20"
                cy="20"
                r="16"
                fill="none"
                stroke="currentColor"
                stroke-width="3"
                stroke-linecap="round"
                stroke-dasharray="70 30"
                class="jm-toast__arc"
              />
            </svg>
          </span>
          <span class="jm-toast__text">{{ toastState.message }}</span>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
.jm-toast {
  position: fixed;
  left: 50%;
  z-index: var(--jm-z-index-toast);
  transform: translateX(-50%);
  max-width: 70%;
  pointer-events: none;
  font-family: var(--jm-font-family);
}

.jm-toast--middle {
  top: 50%;
  transform: translate(-50%, -50%);
}

.jm-toast--top {
  top: 12%;
}

.jm-toast--bottom {
  bottom: 14%;
}

.jm-toast__box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--jm-space-2);
  padding: var(--jm-space-3) var(--jm-space-4);
  border-radius: var(--jm-radius-lg);
  /* 不加 backdrop-filter：模糊层跟随 transform 动画逐帧重采样，会产生碎块状闪烁 */
  background: rgba(16, 21, 26, 0.85);
  color: #fff;
  font-size: var(--jm-font-size-sm);
  line-height: 1.45;
  text-align: center;
  word-break: break-word;
}

.jm-toast.is-clickable {
  pointer-events: auto;
}

.jm-toast__box.is-clickable {
  cursor: pointer;
}

.jm-toast__icon {
  display: inline-flex;
  width: 32px;
  height: 32px;
}

.jm-toast__icon svg {
  width: 100%;
  height: 100%;
}

.jm-toast__arc {
  transform-origin: center;
  animation: jm-toast-spin 0.9s linear infinite;
}

@keyframes jm-toast-spin {
  to {
    transform: rotate(360deg);
  }
}

.jm-toast__mask {
  position: fixed;
  inset: 0;
  z-index: calc(var(--jm-z-index-toast) - 1);
  background: transparent;
}

.jm-toast__mask.is-inline {
  position: absolute;
}

.jm-toast.is-inline {
  position: absolute;
}

/* 过渡：由小变大弹入、由大变小弹出（用户钦定，简单好看）。
   进场 200ms 减速曲线从 0.6 放大到 1；退场 150ms 加速曲线缩回 0.6 同步淡出。
   四个位置统一只做缩放，不做位移，规则一条就够记。
   will-change 提升为合成层：文字只栅格化一次，动画期间由 GPU 整体缩放，
   不会再出现逐帧重排文字的"一粒粒"噪点。 */
.jm-toast-pop-enter-active,
.jm-toast-pop-leave-active {
  will-change: transform, opacity;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

.jm-toast-pop-enter-active {
  transition:
    opacity var(--jm-duration-2) var(--jm-motion-enter-ease),
    transform var(--jm-duration-2) var(--jm-motion-enter-ease);
}

.jm-toast-pop-leave-active {
  transition:
    opacity 150ms var(--jm-motion-exit-ease),
    transform 150ms var(--jm-motion-exit-ease);
}

.jm-toast-pop-enter-from,
.jm-toast-pop-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.6);
}

.jm-toast--middle.jm-toast-pop-enter-from,
.jm-toast--middle.jm-toast-pop-leave-to {
  transform: translate(-50%, -50%) scale(0.6);
}

.jm-toast--top.jm-toast-pop-enter-from,
.jm-toast--top.jm-toast-pop-leave-to,
.jm-toast--bottom.jm-toast-pop-enter-from,
.jm-toast--bottom.jm-toast-pop-leave-to {
  transform: translateX(-50%) scale(0.6);
}
</style>
