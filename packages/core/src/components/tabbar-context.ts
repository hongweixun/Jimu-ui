import type { InjectionKey } from 'vue'

export type TabbarName = string | number

export interface TabbarContext {
  get active(): TabbarName | undefined
  setActive: (name: TabbarName) => void
  activeColor?: string
  inactiveColor?: string
}

export const TABBAR_KEY: InjectionKey<TabbarContext> = Symbol('jm-tabbar')
