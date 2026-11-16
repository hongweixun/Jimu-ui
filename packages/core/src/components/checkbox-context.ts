import type { ComputedRef, InjectionKey } from 'vue'

export type CheckboxValue = string | number

export interface CheckboxGroupContext {
  value: ComputedRef<CheckboxValue[]>
  disabled: ComputedRef<boolean>
  color: ComputedRef<string | undefined>
  toggle: (val: CheckboxValue, checked: boolean) => void
}

export const CHECKBOX_GROUP_KEY: InjectionKey<CheckboxGroupContext> = Symbol('jm-checkbox-group')
