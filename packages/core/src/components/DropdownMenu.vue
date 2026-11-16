<script setup lang="ts">
import { computed, onBeforeUnmount, provide, ref } from 'vue'
import { DROPDOWN_MENU_KEY } from './dropdown-context'

defineOptions({ name: 'JmDropdownMenu' })

const props = withDefaults(
  defineProps<{
    /** 展开项标题与选项的高亮色 */
    activeColor?: string
    /** 是否显示遮罩 */
    overlay?: boolean
    /** 点击选项后收起 */
    closeOnClickOption?: boolean
    /** 层级 */
    zIndex?: number
  }>(),
  { overlay: true, closeOnClickOption: true, zIndex: 10 },
)

const emit = defineEmits<{ open: [index: number]; close: [] }>()

/* 同页多个菜单互斥：后开的把先开的收起来 */
let activeCloser: (() => void) | null = null

const active = ref<number | null>(null)
let seq = 0

function register(): number {
  return seq++
}

function toggle(index: number) {
  if (active.value === index) {
    close()
    return
  }
  if (activeCloser && activeCloser !== close) {
    const other = activeCloser
    activeCloser = null
    other()
  }
  active.value = index
  activeCloser = close
  emit('open', index)
}

function close() {
  if (active.value === null) return
  active.value = null
  if (activeCloser === close) activeCloser = null
  emit('close')
}

onBeforeUnmount(() => {
  if (activeCloser === close) activeCloser = null
})

provide(DROPDOWN_MENU_KEY, {
  active,
  register,
  toggle,
  close,
  activeColor: computed(() => props.activeColor),
  closeOnClickOption: computed(() => props.closeOnClickOption),
})

const styles = computed(() => ({ '--jm-dropdown-z': String(props.zIndex) }))
</script>

<template>
  <div class="jm-dropdown-menu" :class="{ 'is-open': active !== null }" :style="styles">
    <div class="jm-dropdown-menu__bar">
      <slot />
    </div>
    <Transition name="jm-dropdown-mask">
      <div
        v-if="overlay && active !== null"
        class="jm-dropdown-menu__mask"
        aria-hidden="true"
        @click="close"
      />
    </Transition>
  </div>
</template>

<style>
.jm-dropdown-menu {
  position: relative;
  font-family: var(--jm-font-family);
}

.jm-dropdown-menu__bar {
  position: relative;
  z-index: calc(var(--jm-dropdown-z, 10) + 1);
  /* 展开中的菜单整体抬到其他菜单栏之上，面板才不会被兄弟菜单的标题栏盖住 */
  display: flex;
  align-items: stretch;
  height: 48px;
  background: var(--jm-bg-container);
  box-shadow: 0 1px 0 var(--jm-border-color);
}

.jm-dropdown-menu.is-open .jm-dropdown-menu__bar {
  z-index: calc(var(--jm-dropdown-z, 10) + 2);
}

.jm-dropdown-menu__mask {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  height: 100vh;
  z-index: var(--jm-dropdown-z, 10);
  /* 低于展开菜单的栏（+2）、高于普通内容；兄弟菜单栏是 +1，保持可点以便直接切换 */
  background: var(--jm-mask-color, rgba(0, 0, 0, 0.5));
}

.jm-dropdown-mask-enter-active,
.jm-dropdown-mask-leave-active {
  transition: opacity 0.2s ease;
}

.jm-dropdown-mask-enter-from,
.jm-dropdown-mask-leave-to {
  opacity: 0;
}
</style>
