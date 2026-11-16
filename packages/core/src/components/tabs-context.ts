import type { ComputedRef, InjectionKey } from 'vue'

export type TabName = string | number

export interface TabItem {
  name: TabName
  label: string
  disabled?: boolean
  badge?: string | number
}

export interface TabsContext {
  active: ComputedRef<TabName | undefined>
  /** track 模式（animated / swipeable）：面板常驻轨道内，由外层平移切换 */
  animated: ComputedRef<boolean>
  setActive: (name: TabName) => void
  addTab: (tab: TabItem) => void
  removeTab: (name: TabName) => void
}

export const TABS_KEY: InjectionKey<TabsContext> = Symbol('jm-tabs')
