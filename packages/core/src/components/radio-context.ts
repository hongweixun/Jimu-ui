import type { ComputedRef, InjectionKey } from 'vue'

export type RadioValue = string | number

export interface RadioGroupContext {
  value: ComputedRef<RadioValue | undefined>
  disabled: ComputedRef<boolean>
  color: ComputedRef<string | undefined>
  select: (val: RadioValue) => void
}

export const RADIO_GROUP_KEY: InjectionKey<RadioGroupContext> = Symbol('jm-radio-group')
