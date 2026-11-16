<script setup lang="ts">
import { computed, provide } from 'vue'
import { STEPS_KEY, type StepStatus } from './steps-context'

defineOptions({ name: 'JmSteps' })

let seed = 0

const props = withDefaults(
  defineProps<{
    /** 当前进行到第几步，从 0 开始 */
    active?: number
    direction?: 'horizontal' | 'vertical'
    activeColor?: string
    doneColor?: string
  }>(),
  { active: 0, direction: 'horizontal' },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (props.activeColor) s['--jm-step-active'] = props.activeColor
  if (props.doneColor) s['--jm-step-done'] = props.doneColor
  return s
})

function getStatus(index: number): StepStatus {
  if (index < props.active) return 'finish'
  if (index === props.active) return 'process'
  return 'wait'
}

provide(STEPS_KEY, {
  get active() {
    return props.active
  },
  get direction() {
    return props.direction
  },
  get activeColor() {
    return props.activeColor
  },
  get doneColor() {
    return props.doneColor
  },
  register() {
    return seed++
  },
  unregister() {
    seed = Math.max(0, seed - 1)
  },
  getStatus,
})
</script>

<template>
  <div class="jm-steps" :class="`jm-steps--${direction}`" :style="styles">
    <slot />
  </div>
</template>

<style>
.jm-steps {
  display: flex;
  width: 100%;
  font-family: var(--jm-font-family);
  --jm-step-line: var(--jm-border-color-2);
}

.jm-steps--horizontal {
  flex-direction: row;
  align-items: flex-start;
}

.jm-steps--vertical {
  flex-direction: column;
}
</style>
