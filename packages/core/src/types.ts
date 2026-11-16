/** 公共类型，供组件与外部消费方共用 */

export type ComponentType = 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
export type ComponentSize = 'small' | 'medium' | 'large'

export interface ActionSheetAction {
  name?: string | number
  label: string
  /** 选项图标：SVG 的 path d 值 */
  icon?: string
  subLabel?: string
  color?: string
  disabled?: boolean
  loading?: boolean
}

/** Uploader 的文件项：新选文件为 blob URL，服务端返回的为远程地址 */
export interface UploaderFile {
  url?: string
  name?: string
  size?: number
  /** 上传状态：pending 待上传 / uploading 上传中 / done 完成 / error 失败（failed 为旧别名） */
  status?: 'pending' | 'uploading' | 'done' | 'error' | 'failed'
  /** 上传进度 0~100 */
  percent?: number
  /** 失败原因（status 为 error 时展示） */
  message?: string
  /** 原始文件，方便业务自行上传 */
  file?: File
  [key: string]: unknown
}

/** 自定义上传时回传的进度助手 */
export interface UploaderHelpers {
  /** 上报进度 0~100 */
  onProgress: (percent: number) => void
}

/** 自定义上传函数：返回远程地址则替换本地预览图，抛错则进入失败态 */
export type UploaderRequest = (
  file: File,
  helpers: UploaderHelpers,
) => Promise<string | void>

/** CountDown 的拆分结果 */
export interface CountDownTimeData {
  /** 剩余总毫秒 */
  total: number
  days: number
  hours: number
  minutes: number
  seconds: number
  milliseconds: number
}

/** Circle 的渐变色标 */
export interface CircleColorStop {
  color: string
  /** 0 ~ 1 */
  percentage: number
}

/** Segmented 的一段 */
export interface SegmentedOption {
  label?: string
  value: string | number
  /** 图标名，见 jm-icon */
  icon?: string
  disabled?: boolean
}
