<script setup lang="ts">
import { computed, useSlots } from 'vue'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmNavBar' })

const props = withDefaults(
  defineProps<{
    /** 标题文字，也可以用 #title 插槽 */
    title?: string
    leftText?: string
    leftArrow?: boolean
    rightText?: string
    border?: boolean
    fixed?: boolean
    /** fixed 时是否补一个等高占位块，避免内容被盖住 */
    placeholder?: boolean
    /** 是否让出状态栏安全区（刘海屏） */
    safeAreaInsetTop?: boolean
    zIndex?: number
    background?: string
    color?: string
  }>(),
  {
    leftArrow: false,
    border: true,
    fixed: false,
    placeholder: false,
    safeAreaInsetTop: true,
    zIndex: 100,
  },
)

const emit = defineEmits<{ 'click-left': []; 'click-right': [] }>()
const slots = useSlots()

const showLeft = computed(() => props.leftArrow || !!props.leftText || !!slots.left)
const showRight = computed(() => !!props.rightText || !!slots.right)

const styles = computed(() => {
  const s: Record<string, string> = { '--jm-navbar-z': String(props.zIndex) }
  if (props.background) s['--jm-navbar-bg'] = props.background
  if (props.color) s['--jm-navbar-color'] = props.color
  return s
})

function onLeft() {
  if (showLeft.value) emit('click-left')
}

function onRight() {
  if (showRight.value) emit('click-right')
}
</script>

<template>
  <div
    v-if="fixed && placeholder"
    class="jm-navbar__placeholder"
    :class="{ 'is-safe-top': safeAreaInsetTop }"
    aria-hidden="true"
  />
  <div
    class="jm-navbar"
    :class="{ 'is-fixed': fixed, 'is-border': border }"
    :style="styles"
    role="navigation"
  >
    <div class="jm-navbar__inner" :class="{ 'is-safe-top': safeAreaInsetTop }">
      <div
        class="jm-navbar__left"
        :class="{ 'is-tappable': showLeft }"
        :role="showLeft ? 'button' : undefined"
        :tabindex="showLeft ? 0 : undefined"
        @click="onLeft"
        @keydown.enter="onLeft"
      >
        <slot name="left">
          <span v-if="leftArrow" class="jm-navbar__arrow" aria-hidden="true">
            <jm-icon name="chevron-left" size="22px" :stroke-width="2" />
          </span>
          <span v-if="leftText" class="jm-navbar__text">{{ leftText }}</span>
        </slot>
      </div>

      <div class="jm-navbar__title">
        <slot name="title">{{ title }}</slot>
      </div>

      <div
        class="jm-navbar__right"
        :class="{ 'is-tappable': showRight }"
        :role="showRight ? 'button' : undefined"
        :tabindex="showRight ? 0 : undefined"
        @click="onRight"
        @keydown.enter="onRight"
      >
        <slot name="right">
          <span v-if="rightText" class="jm-navbar__text">{{ rightText }}</span>
        </slot>
      </div>
    </div>
  </div>
</template>

<style>
.jm-navbar {
  position: relative;
  z-index: var(--jm-navbar-z, 100);
  width: 100%;
  background: var(--jm-navbar-bg, var(--jm-bg-container));
  color: var(--jm-navbar-color, var(--jm-text-color));
  font-family: var(--jm-font-family);
  /* 隔离内部字号放大，避免适老模式下撑破 44px */
  --jm-navbar-height: calc(46px * var(--jm-size-scale));
}

.jm-navbar__placeholder {
  height: calc(46px * var(--jm-size-scale));
}

.jm-navbar__placeholder.is-safe-top {
  height: calc(46px * var(--jm-size-scale) + var(--jm-safe-top));
}

.jm-navbar.is-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding-left: var(--jm-safe-left);
  padding-right: var(--jm-safe-right);
}

.jm-navbar.is-border::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1px;
  background: var(--jm-border-color);
  transform: scaleY(0.5);
  transform-origin: bottom;
}

.jm-navbar__inner {
  display: flex;
  align-items: center;
  height: var(--jm-navbar-height);
  padding: 0 var(--jm-space-2);
}

.jm-navbar__inner.is-safe-top {
  height: calc(var(--jm-navbar-height) + var(--jm-safe-top));
  padding-top: var(--jm-safe-top);
}

.jm-navbar__left,
.jm-navbar__right {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 0 0 auto;
  min-width: 44px;
  height: 100%;
  font-size: var(--jm-font-size-md);
  color: var(--jm-text-color-2);
}

.jm-navbar__right {
  justify-content: flex-end;
  min-width: 44px;
}

.jm-navbar__left.is-tappable,
.jm-navbar__right.is-tappable {
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  border-radius: var(--jm-radius-sm);
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-navbar__left.is-tappable:active,
.jm-navbar__right.is-tappable:active {
  opacity: 0.5;
}

.jm-navbar__arrow {
  display: inline-flex;
  width: 22px;
  height: 22px;
  color: var(--jm-text-color);
}

.jm-navbar__arrow svg {
  width: 100%;
  height: 100%;
}

.jm-navbar__title {
  flex: 1 1 auto;
  min-width: 0;
  padding: 0 var(--jm-space-1);
  font-size: var(--jm-font-size-lg);
  font-weight: var(--jm-font-weight-medium);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.jm-navbar__text {
  font-size: var(--jm-font-size-md);
  white-space: nowrap;
}

/* 适老：标题再放大一档，左右只保留图标语义不挤压 */
[data-elder='true'] .jm-navbar__title {
  font-size: var(--jm-font-size-xl);
}
</style>
