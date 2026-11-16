/** 描述列表的公共类型与 context */

import type { InjectionKey, Ref } from 'vue'

export type DescriptionsDirection = 'horizontal' | 'vertical'
export type DescriptionsAlign = 'left' | 'right'
export type DescriptionsSize = 'small' | 'medium' | 'large'

export interface DescriptionsContext {
  direction: Readonly<Ref<DescriptionsDirection>>
  /** 一行放几项 */
  column: Readonly<Ref<number>>
  border: Readonly<Ref<boolean>>
  colon: Readonly<Ref<boolean>>
  labelAlign: Readonly<Ref<DescriptionsAlign>>
  size: Readonly<Ref<DescriptionsSize>>
}

export const descriptionsContextKey: InjectionKey<DescriptionsContext> = Symbol('jm-descriptions')
