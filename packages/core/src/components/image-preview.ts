import { createVNode, reactive, render } from 'vue'
import ImagePreviewHost from './ImagePreviewHost.vue'
import { nextZIndex } from '../utils/z-index'

export interface ImagePreviewOptions {
  images: string[]
  /** 起始下标 */
  startPosition?: number
  showIndex?: boolean
  closeable?: boolean
  closeOnClickMask?: boolean
  closeOnClickImage?: boolean
  /** 开启双击 / 双指缩放 */
  zoomable?: boolean
  /** 最大放大倍数 */
  maxScale?: number
  /** 双击放大到的倍数 */
  doubleTapScale?: number
  /** 缩放到指定倍率时回调 */
  onZoom?: (scale: number) => void
  /** 指定挂载容器，预览会限制在这个容器内显示（手机模拟框、弹窗内演示） */
  target?: HTMLElement | null
  onChange?: (index: number) => void
  onClose?: () => void
}

export const imagePreviewState = reactive({
  visible: false,
  images: [] as string[],
  startPosition: 0,
  showIndex: true,
  closeable: true,
  closeOnClickMask: true,
  closeOnClickImage: false,
  zoomable: true,
  maxScale: 4,
  doubleTapScale: 2.5,
  zIndex: 2200,
  onChange: undefined as ((index: number) => void) | undefined,
  onZoom: undefined as ((scale: number) => void) | undefined,
  onClose: undefined as (() => void) | undefined,
})

let container: HTMLElement | null = null

function mountHost(target?: HTMLElement | null) {
  if (typeof document === 'undefined') return
  const parent = target ?? document.body
  if (container && container.parentElement === parent) return
  if (container) {
    render(null, container)
    container.remove()
    container = null
  }
  container = document.createElement('div')
  container.setAttribute('data-jm-preview-host', '')
  if (target) {
    container.style.position = 'absolute'
    container.style.top = '0'
    container.style.right = '0'
    container.style.bottom = '0'
    container.style.left = '0'
  }
  parent.appendChild(container)
  render(createVNode(ImagePreviewHost), container)
}

export function closeImagePreview(): void {
  if (!imagePreviewState.visible) return
  imagePreviewState.visible = false
  imagePreviewState.onClose?.()
}

/** 函数式调起图片预览：showImagePreview({ images, startPosition }) */
export function showImagePreview(options: ImagePreviewOptions): void {
  if (!options?.images?.length) {
    console.warn('[JimuUI] showImagePreview 需要至少一张图片')
    return
  }
  mountHost(options.target)
  imagePreviewState.images = [...options.images]
  imagePreviewState.startPosition = options.startPosition ?? 0
  imagePreviewState.showIndex = options.showIndex ?? true
  imagePreviewState.closeable = options.closeable ?? true
  imagePreviewState.closeOnClickMask = options.closeOnClickMask ?? true
  imagePreviewState.closeOnClickImage = options.closeOnClickImage ?? false
  imagePreviewState.zoomable = options.zoomable ?? true
  imagePreviewState.maxScale = options.maxScale ?? 4
  imagePreviewState.doubleTapScale = options.doubleTapScale ?? 2.5
  imagePreviewState.onChange = options.onChange
  imagePreviewState.onZoom = options.onZoom
  imagePreviewState.onClose = options.onClose
  imagePreviewState.zIndex = nextZIndex(2200)
  imagePreviewState.visible = true
}
