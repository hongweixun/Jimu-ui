<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { STEPS_KEY, type StepStatus } from './steps-context'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmStep' })

const props = withDefaults(
  defineProps<{
    title?: string
    description?: string
    /** 手动指定状态，不传则按父级 active 推导 */
    status?: StepStatus
  }>(),
  {},
)

const ctx = inject(STEPS_KEY, null)
const index = ref(0)

onMounted(() => {
  index.value = ctx ? ctx.register() : 0
})

const status = computed<StepStatus>(() => props.status ?? ctx?.getStatus(index.value) ?? 'wait')
</script>

<template>
  <div
    class="jm-step"
    :class="[`is-${status}`]"
    :aria-current="status === 'process' ? 'step' : undefined"
  >
    <div class="jm-step__head">
      <span class="jm-step__dot">
        <slot name="icon" :status="status" :index="index">
          <jm-icon v-if="status === 'finish'" name="check" size="60%" :stroke-width="2.4" />
          <jm-icon v-else-if="status === 'error'" name="close" size="60%" :stroke-width="2.4" />
          <template v-else>{{ index + 1 }}</template>
        </slot>
      </span>
      <span class="jm-step__line" aria-hidden="true" />
    </div>

    <div class="jm-step__body">
      <div class="jm-step__title">
        <slot name="title">{{ title }}</slot>
      </div>
      <div v-if="description || $slots.description" class="jm-step__desc">
        <slot name="description">{{ description }}</slot>
      </div>
    </div>
  </div>
</template>

<style>
.jm-step {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  color: var(--jm-text-color-3);
}

.jm-step__head {
  display: flex;
  align-items: center;
  width: 100%;
}

.jm-step__dot {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1.5px solid var(--jm-step-line, var(--jm-border-color-2));
  background: var(--jm-bg-container);
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  font-weight: var(--jm-font-weight-medium);
  font-variant-numeric: tabular-nums;
  box-sizing: border-box;
  transition: var(--jm-motion-color);
}

.jm-step__dot svg {
  width: 60%;
  height: 60%;
}

.jm-step__line {
  flex: 1 1 auto;
  height: 2px;
  margin: 0 6px;
  background: var(--jm-border-color-2);
  border-radius: 1px;
  transition: background-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

/* 最后一项不画连接线，靠结构判断，避免 SSR 与挂载后不一致 */
.jm-step:last-child .jm-step__line {
  display: none;
}

.jm-step.is-finish .jm-step__dot {
  border-color: var(--jm-step-done, var(--jm-color-primary));
  background: var(--jm-step-done, var(--jm-color-primary));
  color: var(--jm-color-primary-contrast);
}

.jm-step.is-finish .jm-step__line {
  background: var(--jm-step-done, var(--jm-color-primary));
}

.jm-step.is-process .jm-step__dot {
  border-color: var(--jm-step-active, var(--jm-color-primary));
  color: var(--jm-step-active, var(--jm-color-primary));
  box-shadow: 0 0 0 3px var(--jm-ring-color);
}

.jm-step.is-error .jm-step__dot {
  border-color: var(--jm-color-danger);
  background: var(--jm-color-danger);
  color: var(--jm-color-danger-contrast);
}

.jm-step__body {
  min-width: 0;
  padding: 6px 6px 0 0;
}

.jm-step__title {
  font-size: var(--jm-font-size-sm);
  line-height: 1.35;
  color: var(--jm-text-color);
}

.jm-step.is-process .jm-step__title {
  color: var(--jm-step-active, var(--jm-color-primary));
  font-weight: var(--jm-font-weight-medium);
}

.jm-step.is-error .jm-step__title {
  color: var(--jm-color-danger);
}

.jm-step__desc {
  margin-top: 2px;
  font-size: var(--jm-font-size-xs);
  line-height: 1.4;
  color: var(--jm-text-color-3);
  word-break: break-word;
}

/* ---------- 纵向 ---------- */
.jm-steps--vertical .jm-step {
  flex: 0 0 auto;
  flex-direction: row;
  align-items: stretch;
  min-height: 64px;
}

.jm-steps--vertical .jm-step__head {
  flex: 0 0 auto;
  flex-direction: column;
  width: 24px;
  align-items: center;
}

.jm-steps--vertical .jm-step__line {
  width: 2px;
  height: auto;
  flex: 1 1 auto;
  margin: 6px 0;
}

.jm-steps--vertical .jm-step:last-child .jm-step__line {
  display: none;
}

.jm-steps--vertical .jm-step__body {
  flex: 1 1 auto;
  padding: 2px 0 18px var(--jm-space-3);
}

.jm-steps--vertical .jm-step:last-child .jm-step__body {
  padding-bottom: 0;
}
</style>
