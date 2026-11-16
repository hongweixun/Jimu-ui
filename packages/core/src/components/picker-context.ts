/** 选择器选项与列的公共类型 */

export interface PickerOption {
  text: string
  value: string | number
  /** 禁用后不可选，滚动吸附时会被跳过 */
  disabled?: boolean
}

/** 允许直接传字符串/数字，内部统一成 PickerOption */
export type PickerOptionInput = string | number | PickerOption

/** 多列：每一列是一组选项 */
export type PickerColumnInput = PickerOptionInput[]

export interface PickerFieldNames {
  text?: string
  value?: string
  disabled?: string
}

export interface PickerConfirmPayload {
  selectedValues: (string | number)[]
  selectedOptions: PickerOption[]
  selectedIndexes: number[]
}

/** 级联选项：children 为下一级选项 */
export interface CascadeOption {
  text: string
  value: string | number
  disabled?: boolean
  children?: CascadeOption[]
}
