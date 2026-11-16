import type { InjectionKey } from 'vue'

export type CollapseName = string | number

export interface CollapseContext {
  isExpanded: (name: CollapseName) => boolean
  toggle: (name: CollapseName) => void
  readonly accordion: boolean
}

export const COLLAPSE_KEY: InjectionKey<CollapseContext> = Symbol('jm-collapse')
