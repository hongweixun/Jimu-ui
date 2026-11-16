<script setup lang="ts">
import { computed } from 'vue'
import { hexToRgba, toCssSize } from '../utils'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmTag' })

type TagType = 'default' | 'primary' | 'success' | 'warning' | 'danger'

const props = withDefaults(
  defineProps<{
    type?: TagType
    size?: 'small' | 'medium' | 'large'
    plain?: boolean
    round?: boolean
    closable?: boolean
    color?: string
    textColor?: string
    radius?: number | string
  }>(),
  { type: 'primary', size: 'medium' },
)

const emit = defineEmits<{ close: [event: MouseEvent] }>()

function onClose(e: MouseEvent) {
  emit('close', e)
}

function onCloseKey(e: KeyboardEvent) {
  emit('close', e as unknown as MouseEvent)
}

const classes = computed(() => [
  `jm-tag--${props.type}`,
  `jm-tag--${props.size}`,
  `jm--${props.type}`,
  {
    'is-plain': props.plain,
    'is-round': props.round,
    'is-closable': props.closable,
  },
])

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-tag-radius'] = r
  if (props.color) {
    s['--jm-local-color'] = props.color
    s['--jm-local-light'] = hexToRgba(props.color, 0.12)
    s['--jm-local-border'] = hexToRgba(props.color, 0.4)
  }
  if (props.textColor) s['--jm-tag-text'] = props.textColor
  return s
})
</script>

<template>
  <span class="jm-tag" :class="classes" :style="styles">
    <slot />
    <span
      v-if="closable"
      class="jm-tag__close"
      role="button"
      tabindex="0"
      aria-label="移除"
      @click.stop="onClose"
      @keydown.enter="onCloseKey"
    >
      <jm-icon name="close" size="10px" :stroke-width="2.8" />
    </span>
  </span>
</template>

<style>
.jm-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  max-width: 100%;
  height: 24px;
  padding: 0 8px;
  border: var(--jm-border-width) solid transparent;
  border-radius: var(--jm-tag-radius, var(--jm-radius-sm));
  font-family: var(--jm-font-family);
  font-size: var(--jm-font-size-xs);
  line-height: 1;
  white-space: nowrap;
  background: var(--jm-local-color);
  color: var(--jm-local-contrast);
  vertical-align: middle;
  transition: var(--jm-motion-color);
}

.jm-tag.is-plain {
  background: var(--jm-local-light);
  color: var(--jm-tag-text, var(--jm-local-color));
  border-color: var(--jm-local-border);
}

.jm-tag.is-round {
  border-radius: var(--jm-radius-round);
  padding: 0 10px;
}

.jm-tag--small {
  height: 20px;
  font-size: var(--jm-font-size-xs);
  padding: 0 6px;
}

.jm-tag--large {
  height: 30px;
  font-size: var(--jm-font-size-sm);
  padding: 0 12px;
}

.jm-tag__close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  margin-right: -2px;
  border-radius: 50%;
  opacity: 0.75;
  cursor: pointer;
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-tag__close:hover {
  opacity: 1;
}

.jm-tag__close:active {
  transform: scale(0.9);
}
</style>
