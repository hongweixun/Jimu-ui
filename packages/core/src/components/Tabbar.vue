<script setup lang="ts">
import { computed, cloneVNode, provide, useSlots, type VNode } from 'vue'
import TabbarItem from './TabbarItem.vue'
import { TABBAR_KEY, type TabbarName } from './tabbar-context'

defineOptions({ name: 'JmTabbar' })

const props = withDefaults(
  defineProps<{
    modelValue?: TabbarName
    fixed?: boolean
    border?: boolean
    /** fixed 时补等高占位 */
    placeholder?: boolean
    safeAreaInsetBottom?: boolean
    activeColor?: string
    inactiveColor?: string
    zIndex?: number
    background?: string
    /** 自动让中间那个 tab 悬浮成 FAB（5 个 tab 时即第 3 个） */
    floatCenter?: boolean
  }>(),
  {
    fixed: true,
    border: true,
    placeholder: true,
    safeAreaInsetBottom: true,
    zIndex: 100,
  },
)

const emit = defineEmits<{
  'update:modelValue': [name: TabbarName]
  change: [name: TabbarName]
}>()

const styles = computed(() => {
  const s: Record<string, string> = { '--jm-tabbar-z': String(props.zIndex) }
  if (props.background) s['--jm-tabbar-bg'] = props.background
  return s
})

/* useSlots() 在默认泛型下会被 vue-tsc 推导成 {}，显式标注避免 slots.default 报错 */
const slots = useSlots() as { default?: (...args: unknown[]) => VNode[] }

/**
 * float-center 时把中间的 jm-tabbar-item 打上 float 标记。
 * 只克隆中间且未显式传 float 的 vnode，业务自己传的 float 优先。
 */
const slotted = computed<VNode[]>(() => {
  const children = slots.default?.() ?? []
  if (!props.floatCenter) return children
  const items = children.filter((v) => v.type === TabbarItem)
  if (items.length === 0) return children
  const mid = Math.floor(items.length / 2)
  let idx = 0
  return children.map((v) => {
    if (v.type !== TabbarItem) return v
    const isMid = idx++ === mid
    if (!isMid) return v
    return v.props && 'float' in v.props ? v : cloneVNode(v, { float: true })
  })
})

provide(TABBAR_KEY, {
  get active() {
    return props.modelValue
  },
  setActive(name: TabbarName) {
    emit('update:modelValue', name)
    emit('change', name)
  },
  get activeColor() {
    return props.activeColor
  },
  get inactiveColor() {
    return props.inactiveColor
  },
})
</script>

<template>
  <div
    v-if="fixed && placeholder"
    class="jm-tabbar__placeholder"
    :class="{ 'is-safe-bottom': safeAreaInsetBottom }"
    aria-hidden="true"
  />
  <div
    class="jm-tabbar"
    :class="{ 'is-fixed': fixed, 'is-border': border }"
    :style="styles"
    role="tablist"
  >
    <div class="jm-tabbar__inner" :class="{ 'is-safe-bottom': safeAreaInsetBottom }">
      <component :is="v" v-for="(v, i) in slotted" :key="i" />
    </div>
  </div>
</template>

<style>
.jm-tabbar {
  position: relative;
  z-index: var(--jm-tabbar-z, 100);
  width: 100%;
  background: var(--jm-tabbar-bg, var(--jm-bg-container));
  font-family: var(--jm-font-family);
}

.jm-tabbar__placeholder {
  height: calc(50px * var(--jm-size-scale));
}

.jm-tabbar__placeholder.is-safe-bottom {
  height: calc(50px * var(--jm-size-scale) + var(--jm-safe-bottom));
}

.jm-tabbar.is-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-left: var(--jm-safe-left);
  padding-right: var(--jm-safe-right);
}

.jm-tabbar.is-border::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 1px;
  background: var(--jm-border-color);
  transform: scaleY(0.5);
  transform-origin: top;
}

.jm-tabbar__inner {
  display: flex;
  align-items: stretch;
  height: calc(50px * var(--jm-size-scale));
}

.jm-tabbar__inner.is-safe-bottom {
  height: calc(50px * var(--jm-size-scale) + var(--jm-safe-bottom));
  padding-bottom: var(--jm-safe-bottom);
}
</style>
