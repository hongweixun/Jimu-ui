import type { InjectionKey } from 'vue'

export type StepStatus = 'wait' | 'process' | 'finish' | 'error'

export interface StepsContext {
  readonly active: number
  readonly direction: 'horizontal' | 'vertical'
  readonly activeColor?: string
  readonly doneColor?: string
  register: () => number
  unregister: () => void
  getStatus: (index: number) => StepStatus
}

export const STEPS_KEY: InjectionKey<StepsContext> = Symbol('jm-steps')
