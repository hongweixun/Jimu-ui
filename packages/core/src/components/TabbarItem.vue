<script setup lang="ts">
import { computed, inject } from 'vue'
import { TABBAR_KEY, type TabbarName } from './tabbar-context'

defineOptions({ name: 'JmTabbarItem' })

const props = withDefaults(
  defineProps<{
    name: TabbarName
    text?: string
    badge?: string | number
    dot?: boolean
    disabled?: boolean
    icon?: string
    /** 选中时图标落入渐变圆盘并向上凸起（气泡样式） */
    bubble?: boolean
    /** 圆盘外加一圈描边环（bubble / float 通用），粗细与颜色走 CSS 变量 */
    ring?: boolean
    /** 圆盘阴影，shadow=false 关掉；阴影值走 --jm-tabbar-disc-shadow / --jm-tabbar-float-shadow */
    shadow?: boolean
    /** 悬浮按钮：整个图标变成浮出栏外的圆形 FAB（一般给 5 个 tab 的中间项） */
    float?: boolean
  }>(),
  {
    shadow: true,
  },
)

const emit = defineEmits<{ click: [name: TabbarName] }>()

const ctx = inject(TABBAR_KEY, null)
const active = computed(() => ctx?.active !== undefined && ctx.active === props.name)

const styles = computed(() => {
  const s: Record<string, string> = {}
  if (active.value && ctx?.activeColor) s['--jm-tabbar-item-color'] = ctx.activeColor
  if (!active.value && ctx?.inactiveColor) s['--jm-tabbar-item-color'] = ctx.inactiveColor
  return s
})

const showBadge = computed(() => props.dot || props.badge !== undefined)

function onClick() {
  if (props.disabled) return
  ctx?.setActive(props.name)
  emit('click', props.name)
}
</script>

<template>
  <div
    class="jm-tabbar-item"
    :class="{
      'is-active': active,
      'is-disabled': disabled,
      'is-bubble': bubble,
      'is-float': float,
      'is-ring': ring,
      'is-shadow': shadow,
    }"
    :style="styles"
    role="tab"
    :aria-selected="active ? 'true' : 'false'"
    :aria-disabled="disabled || undefined"
    :tabindex="disabled ? undefined : 0"
    @click="onClick"
    @keydown.enter="onClick"
  >
    <div class="jm-tabbar-item__icon">
      <slot name="icon">
        <i v-if="icon" :class="icon" aria-hidden="true" />
      </slot>
      <span v-if="showBadge" class="jm-tabbar-item__badge" :class="{ 'is-dot': dot }">
        <template v-if="!dot">{{ badge }}</template>
      </span>
    </div>
    <div v-if="text" class="jm-tabbar-item__text">{{ text }}</div>
  </div>
</template>

<style>
.jm-tabbar-item {
  position: relative;
  display: flex;
  flex: 1 1 0;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  min-width: 0;
  padding: 4px 2px;
  color: var(--jm-tabbar-item-color, var(--jm-text-color-3));
  background: transparent;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
  transition: color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

.jm-tabbar-item.is-active {
  color: var(--jm-tabbar-item-color, var(--jm-color-primary));
}

.jm-tabbar-item.is-disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.jm-tabbar-item__icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 22px;
  font-size: 22px;
  transition: transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease);
}

/* 选中时图标微微抬起：给"当前所在页面"一个不依赖颜色的线索 */
.jm-tabbar-item.is-active .jm-tabbar-item__icon {
  transform: translateY(calc(var(--jm-motion-distance-xs) * -0.5)) scale(1.08);
}

.jm-tabbar-item:not(.is-disabled):active .jm-tabbar-item__icon {
  transform: scale(0.9);
}

/* ---------- 气泡样式：选中时图标落入渐变圆盘并向上凸起 ----------
   圆盘用 ::before 画，绝对定位不占布局高度，栏高保持 50px 不被撑破 */
.jm-tabbar-item.is-bubble .jm-tabbar-item__icon::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: calc(var(--jm-tabbar-bubble-size, 36px) * var(--jm-size-scale));
  height: calc(var(--jm-tabbar-bubble-size, 36px) * var(--jm-size-scale));
  border-radius: var(--jm-radius-round);
  transform: translate(-50%, -50%);
  background: transparent;
  z-index: 0;
  transition:
    transform var(--jm-motion-spring-duration) var(--jm-motion-spring-ease),
    background-color var(--jm-motion-transition-duration) var(--jm-motion-transition-ease),
    box-shadow var(--jm-motion-transition-duration) var(--jm-motion-transition-ease);
}

/* 圆盘垫底，图标浮在上面 */
.jm-tabbar-item__icon > * {
  position: relative;
  z-index: 1;
}

.jm-tabbar-item.is-bubble.is-active .jm-tabbar-item__icon {
  color: var(--jm-tabbar-bubble-icon, #fff);
  transform: translateY(calc(var(--jm-tabbar-bubble-lift, 6px) * var(--jm-size-scale) * -1));
}

.jm-tabbar-item.is-bubble.is-active .jm-tabbar-item__icon::before {
  background: var(
    --jm-tabbar-bubble-bg,
    linear-gradient(
      180deg,
      var(--jm-tabbar-bubble-bg-from, #4cc3f5),
      var(--jm-tabbar-bubble-bg-to, var(--jm-color-primary))
    )
  );
}

/* 阴影独立成配置：shadow=false 时不带投影，阴影值也可整体覆盖 */
.jm-tabbar-item.is-bubble.is-active.is-shadow .jm-tabbar-item__icon::before {
  box-shadow: var(--jm-tabbar-disc-shadow, 0 6px 14px rgba(0, 0, 0, 0.16));
}

.jm-tabbar-item.is-bubble:not(.is-disabled):active .jm-tabbar-item__icon {
  transform: translateY(calc(var(--jm-tabbar-bubble-lift, 6px) * var(--jm-size-scale) * -1))
    scale(0.92);
}

/* ---------- 悬浮按钮：圆形 FAB 浮出栏顶，文字隐藏 ---------- */
.jm-tabbar-item.is-float .jm-tabbar-item__icon {
  color: var(--jm-tabbar-float-icon, #fff);
  transform: translateY(calc(var(--jm-tabbar-float-lift, 16px) * var(--jm-size-scale) * -1));
}

.jm-tabbar-item.is-float .jm-tabbar-item__icon::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: calc(var(--jm-tabbar-float-size, 50px) * var(--jm-size-scale));
  height: calc(var(--jm-tabbar-float-size, 50px) * var(--jm-size-scale));
  border-radius: var(--jm-radius-round);
  transform: translate(-50%, -50%);
  background: var(
    --jm-tabbar-float-bg,
    linear-gradient(
      180deg,
      var(--jm-tabbar-bubble-bg-from, #4cc3f5),
      var(--jm-tabbar-bubble-bg-to, var(--jm-color-primary))
    )
  );
  z-index: 0;
}

.jm-tabbar-item.is-float.is-shadow .jm-tabbar-item__icon::before {
  box-shadow: var(--jm-tabbar-float-shadow, 0 8px 18px rgba(0, 0, 0, 0.22));
}

.jm-tabbar-item.is-float:not(.is-disabled):active .jm-tabbar-item__icon {
  transform: translateY(calc(var(--jm-tabbar-float-lift, 16px) * var(--jm-size-scale) * -1))
    scale(0.92);
}

/* ---------- 描边环：bubble / float 通用，ring 属性开启 ----------
   环用 border 画，background-clip 让渐变只铺在环内。
   环色默认取标签栏自身的底色（--jm-tabbar-bg），圆盘看起来像被栏面"包"了一层框；
   想要别的框色直接覆盖 --jm-tabbar-ring-color */
.jm-tabbar-item.is-ring .jm-tabbar-item__icon::before {
  border: var(--jm-tabbar-ring-width, 3px) solid
    var(--jm-tabbar-ring-color, var(--jm-tabbar-bg, var(--jm-bg-container)));
  background-clip: padding-box;
}

.jm-tabbar-item.is-ring.is-bubble:not(.is-active) .jm-tabbar-item__icon::before {
  /* 未选中的气泡没有圆盘，环也不该出现 */
  border: 0;
}

.jm-tabbar-item.is-float .jm-tabbar-item__text {
  display: none;
}

.jm-tabbar-item__icon svg {
  width: 22px;
  height: 22px;
}

.jm-tabbar-item__text {
  font-size: var(--jm-font-size-xs);
  line-height: 1.2;
  white-space: nowrap;
}

.jm-tabbar-item__badge {
  position: absolute;
  top: -2px;
  left: 50%;
  margin-left: 4px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-danger);
  color: var(--jm-color-danger-contrast);
  font-size: 10px;
  font-weight: var(--jm-font-weight-medium);
  line-height: 16px;
  text-align: center;
  white-space: nowrap;
  box-sizing: border-box;
}

.jm-tabbar-item__badge.is-dot {
  min-width: 6px;
  width: 6px;
  height: 6px;
  padding: 0;
  top: 2px;
  margin-left: 6px;
}

[data-elder='true'] .jm-tabbar-item__text {
  font-size: var(--jm-font-size-sm);
}
</style>
