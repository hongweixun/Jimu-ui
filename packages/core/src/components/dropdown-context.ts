import type { InjectionKey, Ref } from 'vue'

export interface DropdownMenuContext {
  /** 当前展开项的下标，null 表示全部收起 */
  active: Ref<number | null>
  /** 挂载时领号，保证与 DOM 顺序一致 */
  register: () => number
  toggle: (index: number) => void
  close: () => void
  activeColor: Ref<string | undefined>
  /** 选项点击后是否收起 */
  closeOnClickOption: Ref<boolean>
}

export const DROPDOWN_MENU_KEY: InjectionKey<DropdownMenuContext> = Symbol('jmDropdownMenu')

export interface DropdownOption {
  text: string
  value: string | number
  /** 图标名（jm-icon） */
  icon?: string
  disabled?: boolean
}
