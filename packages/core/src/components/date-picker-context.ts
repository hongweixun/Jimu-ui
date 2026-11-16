/** 日期选择器的公共类型 */

export type DatePickerType = 'date' | 'time' | 'year-month' | 'datetime'

/** 列单位：决定 formatter 的第一个参数 */
export type DatePickerUnit = 'year' | 'month' | 'day' | 'hour' | 'minute'

/** 自定义每列文案，例如 (type, value) => `${value}月` */
export type DatePickerFormatter = (type: DatePickerUnit, value: string) => string

export interface DatePickerConfirmPayload {
  /** 各列选中的值，按列顺序，如 ['2024','05','12'] */
  selectedValues: string[]
  /** 合成后的日期对象 */
  selectedDate: Date
}
