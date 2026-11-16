import type { InjectionKey, Ref } from 'vue'

export interface IndexBarContext {
  /** 当前高亮的索引 */
  active: Ref<string>
  /** 锚点注册，返回注销函数 */
  register: (index: string, getEl: () => HTMLElement | undefined) => () => void
  /** 分组标题是否吸顶 */
  sticky: Ref<boolean>
}

export const INDEX_BAR_KEY: InjectionKey<IndexBarContext> = Symbol('jm-index-bar')
