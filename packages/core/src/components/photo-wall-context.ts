/** 照片墙条目 */
export interface PhotoWallItem {
  /** 展示用图片地址 */
  src: string
  /** 预览用大图，不传则用 src */
  full?: string
  /** 低清缩略图 / 占位色块，懒加载完成前先显示它 */
  thumb?: string
  /** 高宽比 = height / width；不传则在图片加载完成后自动测量 */
  ratio?: number
  /** 无障碍描述 */
  alt?: string
  /** 业务附加字段，组件不关心 */
  [key: string]: unknown
}
