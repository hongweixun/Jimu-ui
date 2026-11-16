<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useFocusTrap } from '../composables/useFocusTrap'
import { lockScroll, nextZIndex, toCssSize, unlockScroll } from '../utils'
import JmIcon from './Icon.vue'

defineOptions({ name: 'JmPopup' })

const props = withDefaults(
  defineProps<{
    show?: boolean
    position?: 'bottom' | 'top' | 'left' | 'right' | 'center'
    round?: boolean
    closeable?: boolean
    mask?: boolean
    closeOnClickMask?: boolean
    safeArea?: boolean
    zIndex?: number
    /** 锁定背景滚动 */
    lock?: boolean
    radius?: number | string
    /** 挂载目标：false 在当前位置渲染（嵌入手机模拟框等场景），字符串/元素为指定容器，默认 body */
    teleport?: boolean | string | Element
    /**
     * 关闭前钩子：返回 false 或 reject 则不关闭（适合「有未保存内容，先确认」）。
     * 遮罩点击、关闭按钮都会走它，异步期间不会重复触发。
     */
    beforeClose?: () => boolean | Promise<boolean>
    /** 按 Esc 关闭（走 beforeClose，等同点遮罩） */
    closeOnEsc?: boolean
    /**
     * 把键盘焦点锁在弹层内，关闭时归还给触发元素。
     * 抽屉、表单弹层建议开；纯展示型 popup 开着也无害
     */
    trapFocus?: boolean
    /** 无障碍名称：没有可见标题时用它给读屏软件播报 */
    ariaLabel?: string
  }>(),
  {
    position: 'bottom',
    mask: true,
    closeOnClickMask: true,
    safeArea: true,
    zIndex: 1000,
    lock: true,
    teleport: true,
    closeOnEsc: false,
    trapFocus: false,
  },
)

/** 打开时领取一个递增层级：后开的弹层永远盖住先开的（Vant 同款策略） */
const zIndex = ref(props.zIndex)

const emit = defineEmits<{
  'update:show': [value: boolean]
  open: []
  opened: []
  close: []
  closed: []
  'click-mask': [event: MouseEvent]
}>()

/* teleport 语义：false 就地渲染，字符串按选择器查，元素直接用。
   必须定义在下面的 immediate watcher 之前——watcher 在 setup 阶段就会执行到它，
   放在后面会撞上 const 的暂时性死区（TDZ）。 */
const teleportDisabled = computed(() => props.teleport === false)
const teleportTarget = computed<string | Element>(() => {
  if (typeof props.teleport === 'string') return props.teleport
  if (props.teleport instanceof Element) return props.teleport
  return 'body'
})

let locked = false

const panelRef = ref<HTMLElement | null>(null)
const trap = useFocusTrap()

/** Esc 只关最上层弹层：抽屉上又开了 ActionSheet 时，底层不能抢按键 */
function onEsc(e: KeyboardEvent) {
  if (e.key !== 'Escape') return
  const panels = Array.from(document.querySelectorAll<HTMLElement>('.jm-popup'))
  const top = panels.reduce((max, el) => Math.max(max, Number(getComputedStyle(el).zIndex) || 0), 0)
  if (top > zIndex.value) return
  e.stopPropagation()
  void close()
}

function syncLock(open: boolean) {
  if (!props.lock) return
  /* inline（teleport=false）渲染在文档流内：锁 body 会把整个页面冻住。
     滚动锁只对挂 body 的弹层生效，inline 场景交给宿主容器自己管。 */
  if (teleportDisabled.value) return
  if (open && !locked) {
    lockScroll()
    locked = true
  } else if (!open && locked) {
    unlockScroll()
    locked = false
  }
}

watch(
  () => props.show,
  (v) => {
    syncLock(!!v)
    if (v) {
      zIndex.value = Math.max(zIndex.value, props.zIndex, nextZIndex())
      emit('open')
      if (props.closeOnEsc) document.addEventListener('keydown', onEsc, true)
      if (props.trapFocus) {
        nextTick(() => requestAnimationFrame(() => trap.activate(panelRef.value)))
      }
    } else {
      document.removeEventListener('keydown', onEsc, true)
      trap.deactivate()
    }
  },
  { immediate: true },
)

/* 初始即打开时 ref 还没挂上，补一次激活 */
onMounted(() => {
  if (!props.show) return
  if (props.trapFocus) nextTick(() => requestAnimationFrame(() => trap.activate(panelRef.value)))
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onEsc, true)
  if (locked) {
    unlockScroll()
    locked = false
  }
})

let closing = false

async function close() {
  if (props.beforeClose && !closing) {
    closing = true
    try {
      const ok = await props.beforeClose()
      if (ok === false) return
    } catch {
      return
    } finally {
      closing = false
    }
  }
  emit('update:show', false)
  emit('close')
}

function onMask(e: MouseEvent) {
  emit('click-mask', e)
  if (props.closeOnClickMask) close()
}

const transitionName = computed(() =>
  props.position === 'center' ? 'jm-zoom' : `jm-slide-${props.position}`,
)

const panelStyle = computed(() => {
  const s: Record<string, string> = { zIndex: String(zIndex.value) }
  const r = toCssSize(props.radius)
  if (r) s['--jm-popup-radius'] = r
  return s
})

const maskStyle = computed(() => ({ zIndex: String(zIndex.value - 1) }))
</script>

<template>
  <Teleport :to="teleportTarget" :disabled="teleportDisabled">
    <!-- inline（teleport=false）时包一层裁剪根：滑入动画期间弹层被 translateY 推到容器外，
         变换后的边界会把宿主滚动容器的 scrollHeight 瞬间撑大、冒出一条滚动条，
         内容区随之变窄又复原——表现为"打开的一瞬间抖一下"。裁剪根把越界部分裁掉。 -->
    <div :class="teleportDisabled ? 'jm-popup__inline-root' : 'jm-popup__portal'">
      <Transition name="jm-fade" @after-enter="emit('opened')" @after-leave="emit('closed')">
        <div
          v-if="show && mask"
          class="jm-popup__mask"
          :class="{ 'is-inline': teleportDisabled }"
          :style="maskStyle"
          @click="onMask"
        />
      </Transition>

      <Transition :name="transitionName">
        <div
          v-if="show"
          ref="panelRef"
          class="jm-popup"
          :class="[
            `jm-popup--${position}`,
            { 'is-round': round, 'is-inline': teleportDisabled, 'has-safe-area': safeArea },
          ]"
          :style="panelStyle"
          role="dialog"
          aria-modal="true"
          tabindex="-1"
          :aria-label="ariaLabel"
        >
          <button v-if="closeable" type="button" class="jm-popup__close" aria-label="关闭" @click="close">
            <jm-icon name="close" size="18px" :stroke-width="1.8" />
          </button>
          <slot />
        </div>
      </Transition>
    </div>
  </Teleport>
</template>

<style>
/* 非 inline（挂 body）时是纯透传容器，不参与布局 */
.jm-popup__portal {
  display: contents;
}

/* inline 裁剪根：铺满宿主定位容器并裁掉动画越界部分（见模板注释） */
.jm-popup__inline-root {
  position: absolute;
  inset: 0;
  overflow: hidden;
  /* 自身不拦截点击，交互全部留给遮罩与弹层 */
  pointer-events: none;
}

.jm-popup__inline-root > * {
  pointer-events: auto;
}

.jm-popup__mask {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: var(--jm-bg-mask);
}

.jm-popup__mask.is-inline {
  position: absolute;
}

.jm-popup {
  --jm-popup-radius: var(--jm-radius-lg);
  position: fixed;
  z-index: 1000;
  background: var(--jm-bg-elevated);
  font-family: var(--jm-font-family);
  color: var(--jm-text-color);
  overflow: hidden;
  -webkit-overflow-scrolling: touch;
}

/* 面板自身是焦点落点（tabindex="-1"），焦点位置由内部控件体现 */
.jm-popup:focus-visible {
  outline: none;
}

.jm-popup.is-inline {
  position: absolute;
}

.jm-popup--bottom {
  left: 0;
  right: 0;
  bottom: 0;
  max-height: 85%;
  overflow-y: auto;
}

.jm-popup--top {
  left: 0;
  right: 0;
  top: 0;
  max-height: 85%;
  overflow-y: auto;
}

.jm-popup--left {
  top: 0;
  bottom: 0;
  left: 0;
  width: 76%;
  max-width: 320px;
  overflow-y: auto;
}

.jm-popup--right {
  top: 0;
  bottom: 0;
  right: 0;
  width: 76%;
  max-width: 320px;
  overflow-y: auto;
}

.jm-popup--center {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 84%;
}

/* 圆角 */
.jm-popup.is-round.jm-popup--bottom {
  border-radius: var(--jm-popup-radius) var(--jm-popup-radius) 0 0;
}

.jm-popup.is-round.jm-popup--top {
  border-radius: 0 0 var(--jm-popup-radius) var(--jm-popup-radius);
}

.jm-popup.is-round.jm-popup--left {
  border-radius: 0 var(--jm-popup-radius) var(--jm-popup-radius) 0;
}

.jm-popup.is-round.jm-popup--right {
  border-radius: var(--jm-popup-radius) 0 0 var(--jm-popup-radius);
}

.jm-popup.is-round.jm-popup--center {
  border-radius: var(--jm-popup-radius);
}

/* 安全区 */
.jm-popup.has-safe-area.jm-popup--bottom {
  padding-bottom: var(--jm-safe-bottom);
}

.jm-popup.has-safe-area.jm-popup--top {
  padding-top: var(--jm-safe-top);
}

.jm-popup__close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: var(--jm-bg-input);
  color: var(--jm-text-color-3);
  cursor: pointer;
}

/* 过渡：移动端弹层节奏（参照 Varlet）
   250ms 内完成、进出对称。桌面端那套"进 300 减速 / 出 200 加速"是为大屏长距离位移设计的，
   手机上的 sheet 位移本来就短，对称的 250ms 更跟手，也不会出现"关得比开得快"的突兀感。 */
.jm-fade-enter-active,
.jm-fade-leave-active {
  transition: opacity var(--jm-motion-scrim-duration) var(--jm-motion-scrim-ease);
}

.jm-fade-enter-from,
.jm-fade-leave-to {
  opacity: 0;
}

.jm-slide-bottom-enter-active,
.jm-slide-top-enter-active,
.jm-slide-left-enter-active,
.jm-slide-right-enter-active,
.jm-slide-bottom-leave-active,
.jm-slide-top-leave-active,
.jm-slide-left-leave-active,
.jm-slide-right-leave-active {
  transition: transform var(--jm-motion-sheet-duration) var(--jm-motion-sheet-ease);
  will-change: transform;
}

.jm-slide-bottom-enter-from,
.jm-slide-bottom-leave-to {
  transform: translate3d(0, 100%, 0);
}

.jm-slide-top-enter-from,
.jm-slide-top-leave-to {
  transform: translate3d(0, -100%, 0);
}

.jm-slide-left-enter-from,
.jm-slide-left-leave-to {
  transform: translate3d(-100%, 0, 0);
}

.jm-slide-right-enter-from,
.jm-slide-right-leave-to {
  transform: translate3d(100%, 0, 0);
}

/* 居中弹层：缩放 + 淡入，不做过冲——移动端小屏上弹一下会显得廉价 */
.jm-zoom-enter-active,
.jm-zoom-leave-active {
  transition:
    transform var(--jm-motion-sheet-duration) var(--jm-motion-sheet-ease),
    opacity var(--jm-motion-scrim-duration) var(--jm-motion-scrim-ease);
}

.jm-zoom-enter-from,
.jm-zoom-leave-to {
  transform: translate(-50%, -50%) scale(var(--jm-motion-scale-pop));
  opacity: 0;
}
</style>
