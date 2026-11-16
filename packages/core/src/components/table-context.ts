/** 表格列定义 */
export interface TableColumn {
  /** 取值字段；不传则用 index 作列标识 */
  key: string
  /** 表头文案 */
  title?: string
  /** 列宽（数字按 px），不传按内容自适应 */
  width?: number | string
  /** 最小列宽 */
  minWidth?: number | string
  /** 对齐方式 */
  align?: 'left' | 'center' | 'right'
  /** 固定在左侧（横向滚动时不跟着走），只对第一列有意义 */
  fixed?: 'left'
  /** 省略号截断（需要同时给 width 或 minWidth 才会生效） */
  ellipsis?: boolean
  /** 自定义文本：返回值会作为单元格内容 */
  formatter?: (value: unknown, row: Record<string, any>, index: number) => string
  /** 表头额外类名 */
  className?: string
}
