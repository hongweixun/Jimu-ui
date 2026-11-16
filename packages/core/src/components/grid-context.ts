import type { InjectionKey, Ref } from 'vue'

/** Grid 向 GridItem 下发的上下文 */
export interface GridContext {
  /** 每行列数（direction=row 时含义相同，仅排列方向不同） */
  columns: Ref<number>
  /** 每格强制正方形 */
  square: Ref<boolean>
  /** 整组可点击 */
  clickable: Ref<boolean>
  /** 内容是否居中 */
  center: Ref<boolean>
  /** 是否显示格子之间的细线 */
  border: Ref<boolean>
  /** 内部排列方向：row=图标在上，column=图标在左 */
  direction: Ref<'row' | 'column'>
  /** 由 Grid 统一派发点击，item 只需上报自身下标 */
  onItemClick: (index: number) => void
  /** 未显式传 index 时按挂载顺序领取下标 */
  claimIndex: () => number
}

export const GRID_KEY: InjectionKey<GridContext> = Symbol('jm-grid')
