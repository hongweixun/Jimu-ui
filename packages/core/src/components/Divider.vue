<script setup lang="ts">
defineOptions({ name: 'JmDivider' })

const props = withDefaults(
  defineProps<{
    /** 竖线分割 */
    vertical?: boolean
    dashed?: boolean
    /** 文案位置 */
    position?: 'left' | 'center' | 'right'
    /** 只留细线（0.5px 效果），适合列表内 */
    hairline?: boolean
  }>(),
  { position: 'center' },
)
</script>

<template>
  <div
    class="jm-divider"
    :class="[
      vertical ? 'jm-divider--vertical' : 'jm-divider--horizontal',
      `jm-divider--${position}`,
      { 'is-dashed': dashed, 'is-hairline': hairline, 'has-text': !!$slots.default },
    ]"
    role="separator"
  >
    <span v-if="$slots.default && !vertical" class="jm-divider__text"><slot /></span>
  </div>
</template>

<style>
.jm-divider {
  --jm-divider-color: var(--jm-border-color);
  font-family: var(--jm-font-family);
}

.jm-divider--horizontal {
  display: flex;
  align-items: center;
  width: 100%;
  margin: var(--jm-space-4) 0;
  border-top: var(--jm-border-width) solid var(--jm-divider-color);
}

.jm-divider--horizontal.is-dashed {
  border-top-style: dashed;
}

.jm-divider--horizontal.is-hairline {
  border-top-width: 0;
  height: 1px;
  background: var(--jm-divider-color);
  transform: scaleY(0.5);
}

.jm-divider--horizontal.has-text {
  border-top: none;
  gap: var(--jm-space-3);
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-3);
}

.jm-divider--horizontal.has-text::before,
.jm-divider--horizontal.has-text::after {
  content: '';
  flex: 1;
  border-top: var(--jm-border-width) solid var(--jm-divider-color);
}

.jm-divider--horizontal.has-text.is-dashed::before,
.jm-divider--horizontal.has-text.is-dashed::after {
  border-top-style: dashed;
}

.jm-divider--left.has-text::before {
  flex: 0 0 24px;
}

.jm-divider--right.has-text::after {
  flex: 0 0 24px;
}

.jm-divider__text {
  flex: 0 0 auto;
  white-space: nowrap;
}

.jm-divider--vertical {
  display: inline-block;
  width: 1px;
  height: 1em;
  margin: 0 var(--jm-space-2);
  padding: 0;
  border-left: var(--jm-border-width) solid var(--jm-divider-color);
  vertical-align: middle;
}

.jm-divider--vertical.is-dashed {
  border-left-style: dashed;
}
</style>
