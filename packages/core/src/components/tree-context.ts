/** 树节点：知识点树、课程目录、组织架构都套这个结构 */
export interface TreeNode {
  label: string
  value: string | number
  children?: TreeNode[]
  disabled?: boolean
  /** 节点右侧的补充信息，如「12 分钟」「3 节」 */
  extra?: string
  /** 节点前的小图标（内置图标名） */
  icon?: string
  /** 异步加载时用来标记是否叶子，省掉一次「加载完发现是空的」请求 */
  isLeaf?: boolean
  /** 业务自定义字段，原样带回事件里 */
  [key: string]: unknown
}

export type TreeCheckState = 'checked' | 'indeterminate' | 'unchecked'

export interface TreeCheckInfo {
  /** 本次操作的节点 */
  node: TreeNode
  /** 本次操作后该节点是否全选 */
  checked: boolean
  /** 所有半选节点（父节点部分子节点被选中） */
  halfCheckedValues: (string | number)[]
}

export interface TreeExpandInfo {
  node: TreeNode
  expanded: boolean
}
