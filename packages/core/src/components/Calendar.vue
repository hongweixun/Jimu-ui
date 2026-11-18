<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import JmIcon from './Icon.vue'
import Picker from './Picker.vue'
import type {
  CalendarDay,
  CalendarFormatter,
  CalendarShape,
  CalendarSwitchMode,
  CalendarType,
  CalendarValue,
} from './calendar-context'

defineOptions({ name: 'JmCalendar' })

const props = withDefaults(
  defineProps<{
    /** 选中值：single 为 Date，range/multiple 为 Date[] */
    modelValue?: CalendarValue
    type?: CalendarType
    title?: string
    /** 副标题（默认显示当前月份） */
    subtitle?: string
    showTitle?: boolean
    showSubtitle?: boolean
    showConfirm?: boolean
    confirmText?: string
    /** 超出范围时确认按钮的文案（不传则按钮置灰但文案不变） */
    confirmDisabledText?: string
    minDate?: Date | string
    maxDate?: Date | string
    /** 一周从周几开始：0=周日，1=周一 */
    firstDayOfWeek?: 0 | 1
    /** 每行高度 */
    rowHeight?: number | string
    /** 选中色 */
    color?: string
    /** 逐日定制：返回的字段会覆盖默认值 */
    formatter?: CalendarFormatter
    /** 选中态形状：circle 圆形（默认）/ square 方形（TDesign 风格，整格色块） */
    shape?: CalendarShape
    /** 只读：可以翻月，但不能改选日期 */
    readonly?: boolean
    /** 区间选择时允许起止为同一天 */
    allowSameDay?: boolean
    /** 自定义禁用规则，与 min/max 取并集 */
    disableDate?: (date: Date) => boolean
    /** 月份切换方式：none 只看箭头 / month 点标题选月份 / year-month 点标题选年月 */
    switchMode?: CalendarSwitchMode
    /** 自定义月份标题文案（默认「YYYY年M月」） */
    format?: (date: Date) => string
  }>(),
  {
    type: 'single',
    showTitle: true,
    showSubtitle: true,
    showConfirm: true,
    confirmText: '确定',
    firstDayOfWeek: 0,
    rowHeight: 64,
    shape: 'circle',
    readonly: false,
    allowSameDay: true,
    switchMode: 'none',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: Date | Date[]]
  select: [date: Date]
  confirm: [value: Date | Date[]]
  /** 当前展示的月份变化（箭头、横滑、月份面板都会触发） */
  'month-change': [month: Date]
}>()

/* ---------------- 日期工具 ---------------- */
const startOfDay = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate())
const addDays = (d: Date, n: number) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n)
const addMonths = (d: Date, n: number) => new Date(d.getFullYear(), d.getMonth() + n, 1)
const sameDay = (a: Date, b: Date) =>
  a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()

function parseDate(v: Date | string | undefined): Date | undefined {
  if (!v) return undefined
  const d = v instanceof Date ? new Date(v.getTime()) : new Date(v)
  if (Number.isNaN(d.getTime())) return undefined
  return startOfDay(d)
}

const min = computed(() => parseDate(props.minDate))
const max = computed(() => parseDate(props.maxDate))

/* ---------------- 选中值 ---------------- */
function normalize(value: CalendarValue | undefined): Date[] {
  if (value === undefined || value === null || value === '') return []
  const arr = Array.isArray(value) ? value : [value]
  return arr.map((v) => parseDate(v as Date | string)).filter((d): d is Date => !!d)
}

const selected = ref<Date[]>(normalize(props.modelValue))

watch(
  () => props.modelValue,
  (v) => {
    selected.value = normalize(v)
  },
  { deep: true },
)

const currentMonth = ref<Date>(addMonths(selected.value[0] ?? new Date(), 0))

/* 选中值变化时若跨月，跟着翻到那一页 */
watch(
  () => selected.value[0],
  (d) => {
    if (d && (d.getMonth() !== currentMonth.value.getMonth() || d.getFullYear() !== currentMonth.value.getFullYear())) {
      currentMonth.value = addMonths(d, 0)
    }
  },
)

/* 展示月份变化统一从这里派发 */
watch(currentMonth, (m) => {
  emit('month-change', new Date(m.getTime()))
})

const rangeStart = computed(() =>
  props.type === 'range' && selected.value.length > 0 ? selected.value[0] : undefined,
)
const rangeEnd = computed(() =>
  props.type === 'range' && selected.value.length > 1 ? selected.value[1] : undefined,
)

/* ---------------- 月份格子 ---------------- */
const weekDays = computed(() => {
  const base = ['日', '一', '二', '三', '四', '五', '六']
  return props.firstDayOfWeek === 1 ? [...base.slice(1), base[0]] : base
})

const monthLabel = computed(() => {
  if (props.subtitle) return props.subtitle
  if (props.format) return props.format(currentMonth.value)
  return `${currentMonth.value.getFullYear()}年${currentMonth.value.getMonth() + 1}月`
})

const days = computed<CalendarDay[]>(() => {
  const y = currentMonth.value.getFullYear()
  const m = currentMonth.value.getMonth()
  const first = new Date(y, m, 1)
  const offset = (first.getDay() - props.firstDayOfWeek + 7) % 7
  const gridStart = addDays(first, -offset)
  const today = startOfDay(new Date())

  return Array.from({ length: 42 }, (_, i) => {
    const date = addDays(gridStart, i)
    const type = date.getMonth() === m ? 'current' : date < first ? 'prev' : 'next'

    const base: CalendarDay = {
      date,
      day: date.getDate(),
      type,
      text: String(date.getDate()),
    }
    if (sameDay(date, today)) {
      base.today = true
      // 对齐 TDesign：当天用「今天」二字替代数字（formatter 可覆盖 text / bottomInfo），
      // 避免「今」字压在数字下面、选中实底时还得反色的别扭布局
      base.text = '今天'
    }

    const patched = props.formatter ? props.formatter({ ...base }) : undefined
    const day: CalendarDay = { ...base, ...(patched ?? {}) }

    if (min.value && date < min.value) day.disabled = true
    if (max.value && date > max.value) day.disabled = true
    if (props.disableDate?.(date)) day.disabled = true

    if (props.type === 'range') {
      const s = rangeStart.value
      const e = rangeEnd.value
      day.isStart = !!s && sameDay(date, s)
      day.isEnd = !!e && sameDay(date, e)
      day.inRange = !!s && !!e && date > s && date < e
      day.selected = day.isStart || day.isEnd
    } else {
      day.selected = selected.value.some((d) => sameDay(d, date))
    }
    return day
  })
})

/* ---------------- 交互 ---------------- */
function pick(day: CalendarDay, e?: Event) {
  /* 触摸/触控笔的 click 已在 pointerup 里处理过，这里只放行鼠标与键盘 */
  if (e instanceof PointerEvent && e.pointerType && e.pointerType !== 'mouse') return
  if (props.readonly) return
  if (day.disabled) return
  const date = day.date

  if (props.type === 'single') {
    selected.value = [date]
  } else if (props.type === 'multiple') {
    selected.value = day.selected
      ? selected.value.filter((d) => !sameDay(d, date))
      : [...selected.value, date]
  } else {
    // range：第一次点起点，第二次点终点；已有完整区间时重新开始
    if (selected.value.length === 0 || selected.value.length === 2) {
      selected.value = [date]
    } else if (sameDay(selected.value[0], date)) {
      // 起止同一天：allowSameDay 时直接成区间，否则重新以这一天为起点
      selected.value = props.allowSameDay ? [date, date] : [date]
    } else if (date < selected.value[0]) {
      selected.value = [date, selected.value[0]]
    } else {
      selected.value = [selected.value[0], date]
    }
  }

  emit('select', date)
  emitValue()
}

function emitValue() {
  if (props.type === 'single') {
    // 没选日期就不派发，避免把 Invalid Date 传给业务
    if (!selected.value[0]) return
    emit('update:modelValue', selected.value[0])
    return
  }
  emit('update:modelValue', selected.value.slice())
}

function onConfirm() {
  if (props.readonly) return
  emitValue()
  if (props.type === 'single') {
    if (selected.value[0]) emit('confirm', selected.value[0])
    return
  }
  emit('confirm', selected.value.slice())
}

/* ---------------- 翻页（带方向滑动） ---------------- */
const slideName = ref<'jm-cal-next' | 'jm-cal-prev'>('jm-cal-next')

/** 跳到指定月份（按新旧月份差决定滑动方向） */
function jumpToMonth(target: Date) {
  const cur = currentMonth.value
  const diff =
    (target.getFullYear() - cur.getFullYear()) * 12 + (target.getMonth() - cur.getMonth())
  if (diff === 0) return
  slideName.value = diff > 0 ? 'jm-cal-next' : 'jm-cal-prev'
  // Date 是原生对象，原地 setTime 不会触发响应式，必须换新对象
  currentMonth.value = addMonths(cur, diff)
}

function prevMonth() {
  jumpToMonth(addMonths(currentMonth.value, -1))
}

function nextMonth() {
  jumpToMonth(addMonths(currentMonth.value, 1))
}

function goToday() {
  jumpToMonth(addMonths(new Date(), 0))
}

/* ---------------- 月份 / 年月面板 ---------------- */
const panelVisible = ref(false)
const panelValues = ref<(string | number)[]>([])

const yearRange = computed(() => {
  const cur = currentMonth.value.getFullYear()
  const minY = min.value ? min.value.getFullYear() : cur - 10
  const maxY = max.value ? max.value.getFullYear() : cur + 10
  const from = Math.min(minY, cur)
  const to = Math.max(maxY, cur)
  return Array.from({ length: to - from + 1 }, (_, i) => from + i)
})

const panelColumns = computed(() => {
  const months = Array.from({ length: 12 }, (_, i) => ({ text: `${i + 1}月`, value: i + 1 }))
  return props.switchMode === 'year-month' ? [yearRange.value, months] : [months]
})

function openMonthPanel() {
  if (props.switchMode === 'none' || props.readonly) return
  panelValues.value =
    props.switchMode === 'year-month'
      ? [currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1]
      : [currentMonth.value.getMonth() + 1]
  panelVisible.value = true
}

function onPanelConfirm() {
  const vals = panelValues.value
  const year =
    props.switchMode === 'year-month' ? Number(vals[0]) : currentMonth.value.getFullYear()
  const month = Number(vals[vals.length - 1])
  panelVisible.value = false
  jumpToMonth(new Date(year, month - 1, 1))
}

/* 横滑翻月 + 触摸轻点：主体区域左右滑切换月份；
   触摸轻点在 pointerup 自行派发并锁定按下的那一天——部分内嵌 WebView
   对带漂移的轻点会丢失 click 或把 click 落到相邻格，导致「点了没反应
   / 选到隔壁」，所以原生 click 只留给鼠标与键盘。 */
let swipeStart: { x: number; y: number } | null = null
let pressIndex = -1

function dayIndexFromEvent(e: Event): number {
  const el = (e.target as HTMLElement)?.closest?.('.jm-calendar__day') as HTMLElement | null
  const i = el?.getAttribute('data-day-index')
  return i === null || i === undefined ? -1 : Number(i)
}

function onBodyPointerDown(e: PointerEvent) {
  if (e.pointerType === 'mouse' && e.button !== 0) return
  swipeStart = { x: e.clientX, y: e.clientY }
  pressIndex = dayIndexFromEvent(e)
}

function onBodyPointerUp(e: PointerEvent) {
  if (!swipeStart) return
  const dx = e.clientX - swipeStart.x
  const dy = e.clientY - swipeStart.y
  const idx = pressIndex
  swipeStart = null
  pressIndex = -1

  /* 横滑翻月：位移足够且横向占优 */
  if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    jumpToMonth(addMonths(currentMonth.value, dx < 0 ? 1 : -1))
    return
  }

  /* 轻点：纵向基本没动、横向未到翻页阈值 → 选中按下位置的那一天。
     目标取 pointerdown 的格子，容差内漂移不换目标；随后浏览器补发的
     touch click 会在 pick 里被 pointerType 守卫拦掉，不会二次翻转。 */
  if (e.pointerType !== 'mouse' && Math.abs(dy) <= 10 && Math.abs(dx) <= 48 && idx >= 0) {
    const day = days.value[idx]
    if (day) pick(day)
  }
}

function onBodyPointerCancel() {
  swipeStart = null
  pressIndex = -1
}

/* ---------------- 文案 ---------------- */
const fmtDate = (d: Date) => `${d.getMonth() + 1}月${d.getDate()}日`

const summary = computed(() => {
  if (props.type === 'single') return selected.value[0] ? fmtDate(selected.value[0]) : ''
  if (props.type === 'multiple') return selected.value.length ? `已选 ${selected.value.length} 天` : ''
  if (selected.value.length === 0) return ''
  if (selected.value.length === 1) return `${fmtDate(selected.value[0])} 起`
  return `${fmtDate(selected.value[0])} - ${fmtDate(selected.value[1])}`
})

const confirmLabel = computed(() => {
  const empty = props.type === 'single' ? !selected.value[0] : selected.value.length === 0
  if (empty && props.confirmDisabledText) return props.confirmDisabledText
  return props.confirmText
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  const h = toCssSize(props.rowHeight)
  if (h) s['--jm-calendar-row-height'] = h
  if (props.color) {
    s['--jm-calendar-color'] = props.color
    s['--jm-calendar-color-light'] = `${props.color}1f`
  }
  return s
})

defineExpose({ currentMonth, selected, prevMonth, nextMonth, goToday, openMonthPanel })
</script>

<template>
  <div
    class="jm-calendar"
    :class="{ 'is-square': shape === 'square', 'is-readonly': readonly }"
    :style="styles"
  >
    <div v-if="showTitle || showSubtitle" class="jm-calendar__header">
      <div v-if="showTitle" class="jm-calendar__title">{{ title || '选择日期' }}</div>

      <div v-if="showSubtitle" class="jm-calendar__subtitle">
        <button type="button" class="jm-calendar__arrow" aria-label="上个月" @click="prevMonth">
          <jm-icon name="chevron-left" size="20px" :stroke-width="2" />
        </button>
        <button
          v-if="switchMode !== 'none'"
          type="button"
          class="jm-calendar__month is-switchable"
          :disabled="readonly"
          @click="openMonthPanel"
        >
          <span class="jm-calendar__month-text">{{ monthLabel }}</span>
          <jm-icon name="chevron-down" size="14px" :stroke-width="2" />
        </button>
        <span v-else class="jm-calendar__month">{{ monthLabel }}</span>
        <button type="button" class="jm-calendar__arrow" aria-label="下个月" @click="nextMonth">
          <jm-icon name="chevron-right" size="20px" :stroke-width="2" />
        </button>
      </div>

      <div v-if="summary" class="jm-calendar__summary">{{ summary }}</div>

      <!-- 月份面板：锚定在标题行下方，不依赖弹层挂载，任何容器内定位都正确 -->
      <Transition name="jm-cal-panel">
        <div
          v-if="panelVisible && switchMode !== 'none'"
          class="jm-calendar__panel"
          role="dialog"
          aria-label="选择月份"
        >
          <div class="jm-calendar__panel-toolbar">
            <button type="button" class="jm-calendar__panel-action" @click="panelVisible = false">
              取消
            </button>
            <span class="jm-calendar__panel-title">
              {{ switchMode === 'year-month' ? '选择年月' : '选择月份' }}
            </span>
            <button
              type="button"
              class="jm-calendar__panel-action is-confirm"
              @click="onPanelConfirm"
            >
              确认
            </button>
          </div>
          <jm-picker
            v-model="panelValues"
            :columns="panelColumns"
            :show-toolbar="false"
            :item-height="40"
            :visible-count="5"
          />
        </div>
      </Transition>
    </div>

    <div
      class="jm-calendar__body"
      @pointerdown="onBodyPointerDown"
      @pointerup="onBodyPointerUp"
      @pointercancel="onBodyPointerCancel"
    >
      <Transition :name="slideName">
        <div
          :key="`${currentMonth.getFullYear()}-${currentMonth.getMonth()}`"
          class="jm-calendar__page"
        >
          <div class="jm-calendar__weekdays">
            <span v-for="w in weekDays" :key="w" class="jm-calendar__weekday">{{ w }}</span>
          </div>

          <div class="jm-calendar__days">
            <button
              v-for="(day, i) in days"
              :key="i"
              type="button"
              class="jm-calendar__day"
              :data-day-index="i"
              :class="[
                `is-${day.type}`,
                day.className,
                {
                  'is-selected': day.selected,
                  'is-in-range': day.inRange,
                  'is-range-start': day.isStart,
                  'is-range-end': day.isEnd,
                  'is-disabled': day.disabled,
                  'is-today': day.today,
                },
              ]"
              :disabled="day.disabled"
              @click="pick(day, $event)"
            >
              <span class="jm-calendar__day-main">
                <span class="jm-calendar__day-text">{{ day.text }}</span>
              </span>
              <span v-if="day.topInfo" class="jm-calendar__day-info is-top">{{ day.topInfo }}</span>
              <!-- 下方备注常驻占位：没有备注也撑住行高，所有格子的数字基线保持一致 -->
              <span class="jm-calendar__day-info is-bottom">{{ day.bottomInfo }}</span>
            </button>
          </div>
        </div>
      </Transition>
    </div>

    <div v-if="showConfirm" class="jm-calendar__footer">
      <button type="button" class="jm-calendar__confirm" @click="onConfirm">{{ confirmLabel }}</button>
    </div>

    <div v-if="panelVisible" class="jm-calendar__panel-mask" @click="panelVisible = false" />
  </div>
</template>

<style>
.jm-calendar {
  --jm-calendar-row-height: 64px;
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--jm-bg-elevated);
  font-family: var(--jm-font-family);
  user-select: none;
}

.jm-calendar__header {
  position: relative;
  padding: var(--jm-space-4) var(--jm-space-4) var(--jm-space-2);
  text-align: center;
}

.jm-calendar__title {
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-lg);
  font-weight: var(--jm-font-weight-medium);
  line-height: 1.4;
}

.jm-calendar__subtitle {
  display: flex;
  align-items: center;
  margin-top: 6px;
}

/* 年月铺满剩余宽度，两侧各留一个翻月箭头（参照 TDesign） */
.jm-calendar__month {
  flex: 1 1 auto;
  min-width: 0;
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  font-variant-numeric: tabular-nums;
  text-align: center;
}

button.jm-calendar__month {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 4px 0;
  border: 0;
  background: transparent;
  font-family: inherit;
  cursor: pointer;
}

.jm-calendar__month.is-switchable:active {
  color: var(--jm-calendar-color, var(--jm-color-primary));
}

.jm-calendar__arrow {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: transparent;
  color: var(--jm-text-color-2);
  cursor: pointer;
}

.jm-calendar__arrow:active {
  background: var(--jm-bg-hover);
}

/* 翻月滑动容器 */
.jm-calendar__body {
  position: relative;
  overflow: hidden;
  touch-action: pan-y;
}

.jm-calendar__page {
  background: inherit;
  touch-action: pan-y;
}

/* 翻页动画：整页左右滑入滑出，离场页 absolute 叠放 */
.jm-cal-next-enter-active,
.jm-cal-next-leave-active,
.jm-cal-prev-enter-active,
.jm-cal-prev-leave-active {
  transition:
    transform 0.28s var(--jm-motion-transition-ease),
    opacity 0.28s var(--jm-motion-transition-ease);
}

.jm-cal-next-leave-active,
.jm-cal-prev-leave-active {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.jm-cal-next-enter-from {
  transform: translateX(100%);
}

.jm-cal-next-leave-to {
  transform: translateX(-28%);
  opacity: 0;
}

.jm-cal-prev-enter-from {
  transform: translateX(-100%);
}

.jm-cal-prev-leave-to {
  transform: translateX(28%);
  opacity: 0;
}

[data-motion='off'] .jm-cal-next-enter-active,
[data-motion='off'] .jm-cal-next-leave-active,
[data-motion='off'] .jm-cal-prev-enter-active,
[data-motion='off'] .jm-cal-prev-leave-active {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-cal-next-enter-active,
  .jm-cal-next-leave-active,
  .jm-cal-prev-enter-active,
  .jm-cal-prev-leave-active {
    transition: none;
  }
}

.jm-calendar__summary {
  margin-top: 4px;
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-xs);
}

/* 星期表头 */
.jm-calendar__weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  padding: 0 var(--jm-space-2);
  color: var(--jm-text-color-3);
  font-size: var(--jm-font-size-sm);
  text-align: center;
}

.jm-calendar__weekday {
  padding: 8px 0 6px;
}

/* 日期格子 */
.jm-calendar__days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  padding: 0 var(--jm-space-2) var(--jm-space-2);
}

/* 日期格子：纵向排布 —— 数字一行 + 备注一行（对齐 TDesign 方格） */
.jm-calendar__day {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  height: var(--jm-calendar-row-height);
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--jm-text-color);
  font-family: inherit;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

/* 数字所在的一行：高度固定，区间带和方块都挂在这层 */
.jm-calendar__day-main {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 34px;
}

.jm-calendar__day.is-prev,
.jm-calendar__day.is-next {
  color: var(--jm-text-color-4);
}

.jm-calendar__day.is-disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* 区间底色：起止各铺一半，接缝处才不会断开 */
.jm-calendar__day.is-in-range .jm-calendar__day-main::before,
.jm-calendar__day.is-range-start .jm-calendar__day-main::before,
.jm-calendar__day.is-range-end .jm-calendar__day-main::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  background: var(--jm-calendar-color-light, var(--jm-color-primary-light));
  z-index: 0;
}

.jm-calendar__day.is-in-range .jm-calendar__day-main::before {
  left: 0;
  right: 0;
}

.jm-calendar__day.is-range-start .jm-calendar__day-main::before {
  left: 50%;
  right: 0;
}

.jm-calendar__day.is-range-end .jm-calendar__day-main::before {
  left: 0;
  right: 50%;
}

/* 起止同一天：没有区间带 */
.jm-calendar__day.is-range-start.is-range-end .jm-calendar__day-main::before {
  display: none;
}

.jm-calendar__day-text {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: var(--jm-font-size-md);
  font-variant-numeric: tabular-nums;
  transition:
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

/* 按压反馈：数字轻微缩放，让「这次点到了」看得见 */
.jm-calendar__day:not(.is-disabled):active .jm-calendar__day-text {
  transform: scale(0.88);
  opacity: 0.72;
}

[data-motion='off'] .jm-calendar__day:not(.is-disabled):active .jm-calendar__day-text {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-calendar__day:not(.is-disabled):active .jm-calendar__day-text {
    transition: none;
  }
}

/* 圆形选中（默认） */
.jm-calendar__day.is-selected .jm-calendar__day-text {
  background: var(--jm-calendar-color, var(--jm-color-primary));
  color: var(--jm-color-primary-contrast);
  font-weight: var(--jm-font-weight-medium);
}

.jm-calendar__day.is-today .jm-calendar__day-text {
  box-shadow: inset 0 0 0 1px var(--jm-calendar-color, var(--jm-color-primary));
  color: var(--jm-calendar-color, var(--jm-color-primary));
  /* 「今天」两个字比数字略小，圆里放得下也不显挤 */
  font-size: var(--jm-font-size-sm);
}

.jm-calendar__day.is-today.is-selected .jm-calendar__day-text {
  box-shadow: none;
  color: var(--jm-color-primary-contrast);
}

/* 日期描述：下方备注是独立小字行（常驻占位），与数字、选中色块互不重叠；
   上方备注少见，仍绝对定位贴格子顶缘 */
.jm-calendar__day-info {
  flex: 0 0 auto;
  width: 100%;
  height: 12px;
  color: var(--jm-text-color-3);
  font-size: 10px;
  line-height: 12px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}

.jm-calendar__day-info.is-top {
  position: absolute;
  top: 2px;
  left: 0;
  right: 0;
  height: auto;
}

.jm-calendar__day.is-selected .jm-calendar__day-info {
  color: var(--jm-calendar-color, var(--jm-color-primary));
}

/* ---------- 方形（TDesign 风格）：整格色块，起止只圆外侧 ---------- */
.jm-calendar.is-square .jm-calendar__day-main {
  border-radius: 4px;
}

.jm-calendar.is-square .jm-calendar__day.is-range-start:not(.is-range-end) .jm-calendar__day-main {
  border-radius: 4px 0 0 4px;
}

.jm-calendar.is-square .jm-calendar__day.is-range-end:not(.is-range-start) .jm-calendar__day-main {
  border-radius: 0 4px 4px 0;
}

/* 方块已盖住起止格，区间带铺满即可 */
.jm-calendar.is-square .jm-calendar__day.is-in-range .jm-calendar__day-main::before,
.jm-calendar.is-square .jm-calendar__day.is-range-start .jm-calendar__day-main::before,
.jm-calendar.is-square .jm-calendar__day.is-range-end .jm-calendar__day-main::before {
  left: 0;
  right: 0;
}

.jm-calendar.is-square .jm-calendar__day.is-range-start.is-range-end .jm-calendar__day-main::before {
  display: none;
}

.jm-calendar.is-square .jm-calendar__day.is-selected .jm-calendar__day-main {
  background: var(--jm-calendar-color, var(--jm-color-primary));
}

.jm-calendar.is-square .jm-calendar__day.is-selected .jm-calendar__day-text {
  background: transparent;
  color: var(--jm-color-primary-contrast);
}

.jm-calendar.is-square .jm-calendar__day.is-today .jm-calendar__day-main {
  box-shadow: inset 0 0 0 1px var(--jm-calendar-color, var(--jm-color-primary));
}

.jm-calendar.is-square .jm-calendar__day.is-today .jm-calendar__day-text {
  box-shadow: none;
  color: inherit;
}

.jm-calendar.is-square .jm-calendar__day.is-today.is-selected .jm-calendar__day-main {
  box-shadow: none;
}

/* 只读 */
.jm-calendar.is-readonly .jm-calendar__day {
  cursor: default;
}

/* ---------- 月份面板：锚定标题下方，盖住日期区 ---------- */
.jm-calendar__panel-mask {
  position: absolute;
  inset: 0;
  z-index: 25;
  cursor: pointer;
}

.jm-calendar__panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 26;
  border-radius: var(--jm-radius-lg);
  background: var(--jm-bg-elevated);
  box-shadow: var(--jm-shadow-lg, 0 8px 24px rgba(0, 0, 0, 0.14));
  overflow: hidden;
}

.jm-calendar__panel-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--jm-space-2) var(--jm-space-4) 0;
}

.jm-calendar__panel-action {
  padding: 4px 8px;
  border: 0;
  background: transparent;
  color: var(--jm-text-color-3);
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  cursor: pointer;
}

.jm-calendar__panel-action.is-confirm {
  color: var(--jm-calendar-color, var(--jm-color-primary));
  font-weight: var(--jm-font-weight-medium);
}

.jm-calendar__panel-title {
  color: var(--jm-text-color);
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
}

/* 入场：从标题下方轻轻落下 */
.jm-cal-panel-enter-active,
.jm-cal-panel-leave-active {
  transition:
    opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    transform var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-cal-panel-enter-from,
.jm-cal-panel-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

[data-motion='off'] .jm-cal-panel-enter-active,
[data-motion='off'] .jm-cal-panel-leave-active {
  transition: none;
}

@media (prefers-reduced-motion: reduce) {
  .jm-cal-panel-enter-active,
  .jm-cal-panel-leave-active {
    transition: none;
  }
}

/* 底部确认 */
.jm-calendar__footer {
  padding: var(--jm-space-2) var(--jm-space-4) var(--jm-space-4);
}

.jm-calendar__confirm {
  width: 100%;
  height: var(--jm-control-height-md);
  border: 0;
  border-radius: var(--jm-radius-md);
  background: var(--jm-calendar-color, var(--jm-color-primary));
  color: var(--jm-color-primary-contrast);
  font-family: inherit;
  font-size: var(--jm-font-size-md);
  font-weight: var(--jm-font-weight-medium);
  cursor: pointer;
  transition: opacity var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-calendar__confirm:active {
  opacity: 0.85;
}
</style>
