/**
 * 弹层层级管理（参照 Vant 的 z-index 方案）
 * ---------------------------------------------------------------------------
 * 弹层（Popup / ActionSheet / Dialog / Toast）同时存在多个时，后开的必须盖住先开的。
 * 只靠组件默认 z-index 会出现两张 1000 平级、层级由 DOM 顺序决定的随机局面。
 * 这里用一个模块级计数器：每次有弹层打开，取下一个更大的值。
 * 初始值对齐 --jm-z-index-toast（2000），弹层陆续打开会自然超过它，
 * Toast 打开时同样走这个计数器，保证 toast 永远在当前所有弹层之上。
 */

let current = 2000

export function nextZIndex(base?: number): number {
  // 传 base 时先把计数器抬到 base，保证一类弹层（如图片预览）始终在上面一层
  if (base && base > current) current = base
  current += 1
  return current
}
