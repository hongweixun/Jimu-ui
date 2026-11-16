import type { InjectionKey } from 'vue'

/** 时间轴节点语义色 */
export type TimelineType = 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'

export interface TimelineContext {
  readonly lineStyle: 'solid' | 'dashed'
}

export const TIMELINE_KEY: InjectionKey<TimelineContext> = Symbol('jm-timeline')
