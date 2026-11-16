/** 日历公共类型 */

export type CalendarType = 'single' | 'range' | 'multiple'

/** 选中态形状：圆形（默认）/ 方形（整格色块，TDesign 风格） */
export type CalendarShape = 'circle' | 'square'

/** 月份切换方式：none 仅箭头翻月 / month 点标题选月份 / year-month 点标题选年月 */
export type CalendarSwitchMode = 'none' | 'month' | 'year-month'

export type CalendarDayType = 'prev' | 'current' | 'next'

export interface CalendarDay {
  /** 这一天对应的真实日期（已归零到 00:00） */
  date: Date
  /** 几号 */
  day: number
  /** 属于上个月 / 本月 / 下个月 */
  type: CalendarDayType
  /** 显示文字，默认就是 day */
  text: string
  /** 日期上方的补充文案（如"今天"） */
  topInfo?: string
  /** 日期下方的补充文案（如"已签"） */
  bottomInfo?: string
  /** 追加自定义类名 */
  className?: string
  disabled?: boolean
  /** 以下由组件计算，formatter 里读不到最终选中态 */
  selected?: boolean
  inRange?: boolean
  isStart?: boolean
  isEnd?: boolean
  /** 是否为今天（组件计算，formatter 无需关心） */
  today?: boolean
}

export type CalendarFormatter = (day: CalendarDay) => Partial<CalendarDay> | void

export type CalendarValue = Date | Date[] | string | string[]
