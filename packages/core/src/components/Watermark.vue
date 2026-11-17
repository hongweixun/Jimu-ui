<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

defineOptions({ name: 'JmWatermark' })

const props = withDefaults(
  defineProps<{
    /** 文字水印，传数组即多行 */
    text?: string | string[]
    /** 图片水印（URL），与文字可同时使用 */
    image?: string
    /** 透明度 0 ~ 1 */
    opacity?: number
    /** 水印间距 [横, 纵]，数字表示两者相同 */
    gap?: number | [number, number]
    /** 旋转角度（deg） */
    rotate?: number
    fontSize?: number
    /** 文字颜色（配合 opacity） */
    color?: string
    /** 覆盖整个视口并固定 */
    fullscreen?: boolean
    zIndex?: number
    /** 水印层偏移，用于错行 */
    offset?: [number, number]
  }>(),
  {
    text: '',
    opacity: 0.16,
    gap: () => [80, 80] as [number, number],
    rotate: -22,
    fontSize: 14,
    color: '#000000',
    fullscreen: false,
    zIndex: 9,
  },
)

const gapX = computed(() => (Array.isArray(props.gap) ? props.gap[0] : props.gap))
const gapY = computed(() => (Array.isArray(props.gap) ? props.gap[1] : props.gap))

const tile = ref('')
const tileSize = ref({ width: 0, height: 0 })
const offset = computed(() =>
  Array.isArray(props.offset) ? `${props.offset[0]}px ${props.offset[1]}px` : '0px 0px',
)

function lines(): string[] {
  if (Array.isArray(props.text)) return props.text.filter((t) => t !== '')
  return props.text ? [props.text] : []
}

/** 用 canvas 生成一块「单元格」，再交给 background-repeat 平铺 */
function render() {
  if (typeof document === 'undefined') return
  const rows = lines()
  if (!rows.length && !props.image) {
    tile.value = ''
    return
  }

  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = Math.min(window.devicePixelRatio || 1, 3)
  const font = `${props.fontSize}px ${getComputedStyle(document.body).fontFamily || 'sans-serif'}`
  ctx.font = font

  const lineHeight = props.fontSize * 1.4
  const textWidth = Math.max(0, ...rows.map((r) => ctx.measureText(r).width))
  const textHeight = rows.length * lineHeight
  const imgSize = props.image ? props.fontSize * 3 : 0
  const contentWidth = Math.max(textWidth, imgSize)
  const contentHeight = Math.max(textHeight, imgSize)

  const angle = (Math.abs(props.rotate) * Math.PI) / 180
  const cos = Math.abs(Math.cos(angle))
  const sin = Math.abs(Math.sin(angle))
  // 旋转后外接矩形，保证旋转的水印不被裁掉
  const boxWidth = contentWidth * cos + contentHeight * sin
  const boxHeight = contentWidth * sin + contentHeight * cos

  const width = Math.ceil(boxWidth + gapX.value)
  const height = Math.ceil(boxHeight + gapY.value)

  canvas.width = Math.round(width * dpr)
  canvas.height = Math.round(height * dpr)
  ctx.scale(dpr, dpr)
  ctx.translate(width / 2, height / 2)
  ctx.rotate(((props.rotate ?? 0) * Math.PI) / 180)
  ctx.globalAlpha = Math.min(1, Math.max(0, props.opacity))
  ctx.fillStyle = props.color
  ctx.font = font
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  let cursorY = props.image ? imgSize / 2 + props.fontSize * 0.4 : -textHeight / 2 + lineHeight / 2
  rows.forEach((row) => {
    ctx.fillText(row, 0, cursorY)
    cursorY += lineHeight
  })

  if (props.image) {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      ctx.globalAlpha = Math.min(1, Math.max(0, props.opacity))
      const x = -imgSize / 2
      const y = rows.length ? -imgSize / 2 - textHeight / 2 : -imgSize / 2
      ctx.drawImage(img, x, y, imgSize, imgSize)
      try {
        tile.value = canvas.toDataURL('image/png')
      } catch {
        // 跨域图片会污染画布，静默降级成纯文字水印
        tile.value = canvas.toDataURL('image/png')
      }
      tileSize.value = { width, height }
    }
    img.src = props.image
  } else {
    tile.value = canvas.toDataURL('image/png')
    tileSize.value = { width, height }
  }
}

const layerStyle = computed(() => ({
  backgroundImage: tile.value ? `url("${tile.value}")` : 'none',
  backgroundSize: `${tileSize.value.width}px ${tileSize.value.height}px`,
  backgroundPosition: offset.value,
}))

watch(
  () => [
    props.text,
    props.image,
    props.opacity,
    props.rotate,
    props.fontSize,
    props.color,
    gapX.value,
    gapY.value,
  ],
  () => render(),
  { immediate: true },
)

let lastDpr = typeof window !== 'undefined' ? window.devicePixelRatio : 1

/** 字体加载完宽度会变、跨屏拖动 dpr 会变：两种情况都要重画 */
function onFontsReady() {
  document.fonts?.ready.then(() => render()).catch(() => {})
}

function onResize() {
  if (window.devicePixelRatio === lastDpr) return
  lastDpr = window.devicePixelRatio
  render()
}

onMounted(() => {
  onFontsReady()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => window.removeEventListener('resize', onResize))
</script>

<template>
  <div
    class="jm-watermark"
    :class="{
      'is-plain': !$slots.default,
      'is-fullscreen': fullscreen,
    }"
    :style="fullscreen ? { zIndex: String(zIndex) } : undefined"
  >
    <slot />
    <div class="jm-watermark__layer" :style="layerStyle" aria-hidden="true" />
  </div>
</template>

<style>
.jm-watermark {
  position: relative;
  font-family: var(--jm-font-family);
}

/* 不给插槽时铺满父容器，作为纯覆盖层使用 */
.jm-watermark.is-plain {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.jm-watermark.is-fullscreen {
  position: fixed;
  inset: 0;
  pointer-events: none;
}

.jm-watermark__layer {
  position: absolute;
  inset: 0;
  background-repeat: repeat;
  pointer-events: none;
  user-select: none;
  -webkit-user-select: none;
}
</style>
