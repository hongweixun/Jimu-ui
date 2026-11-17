<script setup lang="ts">
import { snackbarState, type SnackbarItem } from './snackbar'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmSnackbarHost' })

function iconOf(it: SnackbarItem): string {
  if (it.type === 'success') return 'check-circle'
  if (it.type === 'error') return 'close-circle'
  return ''
}

function clearItem(id: number) {
  const idx = snackbarState.items.findIndex((x) => x.id === id)
  if (idx !== -1) {
    const it = snackbarState.items[idx]
    snackbarState.items.splice(idx, 1)
    it.onClose?.()
  }
}

function onAction(it: SnackbarItem) {
  it.onAction?.()
  clearItem(it.id)
}
</script>

<template>
  <Teleport to="body">
    <!-- 禁止穿透点击的透明屏障 -->
    <Transition name="jm-snackbar-fade">
      <div
        v-if="snackbarState.items.some((it) => it.forbidClick)"
        class="jm-snackbar__blocker"
        :style="{ zIndex: Math.max(...snackbarState.items.map((i) => i.zIndex)) - 1 }"
      />
    </Transition>

    <div class="jm-snackbar-group is-top">
      <TransitionGroup name="jm-snackbar-pop">
        <div
          v-for="it in snackbarState.items.filter((i) => i.position === 'top')"
          :key="it.id"
          class="jm-snackbar"
          :class="[`jm-snackbar--${it.type}`, { 'is-vertical': it.vertical }]"
          :style="{ zIndex: it.zIndex }"
          role="alert"
          aria-live="assertive"
        >
          <span v-if="iconOf(it)" class="jm-snackbar__icon" aria-hidden="true">
            <jm-icon :name="iconOf(it)" size="18px" :stroke-width="1.8" />
          </span>
          <svg v-else-if="it.type === 'loading'" viewBox="0 0 40 40" class="jm-snackbar__spinner" aria-hidden="true">
            <circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.25" />
            <circle
              cx="20"
              cy="20"
              r="16"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-dasharray="70 30"
              class="jm-snackbar__arc"
            />
          </svg>

          <div class="jm-snackbar__content">{{ it.content }}</div>

          <button v-if="it.action" type="button" class="jm-snackbar__action" @click="onAction(it)">
            {{ it.action }}
          </button>
        </div>
      </TransitionGroup>
    </div>

    <div class="jm-snackbar-group is-center">
      <TransitionGroup name="jm-snackbar-pop">
        <div
          v-for="it in snackbarState.items.filter((i) => i.position === 'center')"
          :key="it.id"
          class="jm-snackbar"
          :class="[`jm-snackbar--${it.type}`, { 'is-vertical': it.vertical }]"
          :style="{ zIndex: it.zIndex }"
          role="alert"
        >
          <span v-if="iconOf(it)" class="jm-snackbar__icon" aria-hidden="true">
            <jm-icon :name="iconOf(it)" size="18px" :stroke-width="1.8" />
          </span>
          <svg v-else-if="it.type === 'loading'" viewBox="0 0 40 40" class="jm-snackbar__spinner" aria-hidden="true">
            <circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.25" />
            <circle
              cx="20"
              cy="20"
              r="16"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-dasharray="70 30"
              class="jm-snackbar__arc"
            />
          </svg>

          <div class="jm-snackbar__content">{{ it.content }}</div>

          <button v-if="it.action" type="button" class="jm-snackbar__action" @click="onAction(it)">
            {{ it.action }}
          </button>
        </div>
      </TransitionGroup>
    </div>

    <div class="jm-snackbar-group is-bottom">
      <TransitionGroup name="jm-snackbar-pop">
        <div
          v-for="it in snackbarState.items.filter((i) => i.position === 'bottom')"
          :key="it.id"
          class="jm-snackbar"
          :class="[`jm-snackbar--${it.type}`, { 'is-vertical': it.vertical }]"
          :style="{ zIndex: it.zIndex }"
          role="alert"
        >
          <span v-if="iconOf(it)" class="jm-snackbar__icon" aria-hidden="true">
            <jm-icon :name="iconOf(it)" size="18px" :stroke-width="1.8" />
          </span>
          <svg v-else-if="it.type === 'loading'" viewBox="0 0 40 40" class="jm-snackbar__spinner" aria-hidden="true">
            <circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.25" />
            <circle
              cx="20"
              cy="20"
              r="16"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-dasharray="70 30"
              class="jm-snackbar__arc"
            />
          </svg>

          <div class="jm-snackbar__content">{{ it.content }}</div>

          <button v-if="it.action" type="button" class="jm-snackbar__action" @click="onAction(it)">
            {{ it.action }}
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style>
.jm-snackbar-host .jm-snackbar-group,
.jm-snackbar-group {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  padding: 0 16px;
}

.jm-snackbar-group.is-top {
  justify-content: flex-start;
}

.jm-snackbar-group.is-center {
  justify-content: center;
}

.jm-snackbar-group.is-bottom {
  justify-content: flex-end;
}

.jm-snackbar__blocker {
  position: fixed;
  inset: 0;
  pointer-events: auto;
}

.jm-snackbar {
  display: flex;
  align-items: center;
  width: min(var(--jm-snackbar-width, 300px), calc(100vw - 32px));
  box-sizing: border-box;
  margin: 6px 0;
  padding: 12px 14px;
  border-radius: var(--jm-radius-md);
  background: var(--jm-snackbar-background, var(--jm-text-color));
  color: var(--jm-snackbar-color, #fff);
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-sm);
  line-height: 1.5;
  pointer-events: auto;
  box-shadow: var(--jm-elevation-12);
}

.jm-snackbar--success {
  background: var(--jm-color-success);
}

.jm-snackbar--warning {
  background: var(--jm-color-warning);
}

.jm-snackbar--error {
  background: var(--jm-color-danger);
}

.jm-snackbar--info {
  background: var(--jm-color-info);
}

.jm-snackbar.is-vertical {
  flex-direction: column;
  align-items: stretch;
}

.jm-snackbar__icon {
  display: inline-flex;
  flex: 0 0 auto;
  margin-right: 10px;
}

.jm-snackbar__icon svg {
  display: block;
}

.jm-snackbar__content {
  flex: 1 1 auto;
  word-break: break-word;
}

.jm-snackbar__action {
  flex: 0 0 auto;
  margin-left: 12px;
  padding: 4px 8px;
  border: 0;
  border-radius: var(--jm-radius-sm);
  background: none;
  color: var(--jm-color-primary);
  font-family: inherit;
  font-size: inherit;
  font-weight: var(--jm-font-weight-medium);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-snackbar__action:active {
  opacity: 0.7;
}

.jm-snackbar__spinner {
  flex: 0 0 auto;
  width: 18px;
  height: 18px;
  margin-right: 10px;
}

.jm-snackbar__arc {
  transform-origin: center;
  animation: jm-snackbar-spin 0.9s linear infinite;
}

@keyframes jm-snackbar-spin {
  to {
    transform: rotate(360deg);
  }
}

/* 进出场：从对应方向滑入 */
.jm-snackbar-pop-enter-active,
.jm-snackbar-pop-leave-active {
  transition:
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-snackbar-pop-enter-from,
.jm-snackbar-pop-leave-to {
  opacity: 0;
}

.is-top .jm-snackbar-pop-enter-from,
.is-top .jm-snackbar-pop-leave-to {
  transform: translateY(-16px);
}

.is-bottom .jm-snackbar-pop-enter-from,
.is-bottom .jm-snackbar-pop-leave-to {
  transform: translateY(16px);
}

.jm-snackbar-fade-enter-active,
.jm-snackbar-fade-leave-active {
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-snackbar-fade-enter-from,
.jm-snackbar-fade-leave-to {
  opacity: 0;
}

[data-motion='off'] .jm-snackbar__arc {
  animation: none;
}
</style>
