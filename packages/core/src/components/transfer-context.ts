/** 穿梭框条目 */
export interface TransferItem {
  label: string
  value: string | number
  /** 次行说明，如「3 节课 · 12 分钟」 */
  desc?: string
  /** 禁用的项不可勾选、不可移动 */
  disabled?: boolean
}
