<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { encodeQRCode, type QrEccLevel } from '../utils/qrcode'

defineOptions({ name: 'JmQrcode' })

const props = withDefaults(
  defineProps<{
    /** 二维码内容（URL、文本、JSON 等） */
    value: string
    /** 显示尺寸（CSS 像素） */
    size?: number
    /** 纠错级别：L 7% / M 15% / Q 25% / H 30%，放 Logo 建议 H */
    level?: QrEccLevel
    /** 静区（四周留白的模块数） */
    margin?: number
    /** 前景色（码点颜色） */
    fgColor?: string
    /** 渐变第二色，不传则纯色 */
    fgColor2?: string
    /** 渐变方向：默认左上→右下 */
    gradientDirection?: 'lt-br' | 'rt-bl' | 'top-bottom' | 'left-right'
    /** 背景色，传 'transparent' 为透明底 */
    bgColor?: string
    /** 码点样式 */
    dotStyle?: 'square' | 'rounded' | 'dots'
    /** Logo 图片地址（自动带白底衬垫，建议 level=H） */
    logo?: string
    /** Logo 宽度占二维码的比例 */
    logoWidth?: number
    /** Logo 圆角（CSS 像素） */
    logoRadius?: number
  }>(),
  {
    size: 200,
    level: 'M',
    margin: 4,
    fgColor: '#000000',
    bgColor: '#ffffff',
    dotStyle: 'square',
    logoWidth: 0.22,
    logoRadius: 8,
  },
)

const canvasRef = ref<HTMLCanvasElement | null>(null)
let logoImg: HTMLImageElement | null = null
let logoLoaded = false

function hexToRgba(hex: string): [number, number, number, number] {
  let h = hex.trim()
  if (h === 'transparent') return [0, 0, 0, 0]
  if (h.startsWith('rgba') || h.startsWith('rgb')) {
    const m = h.match(/[\d.]+/g) || []
    return [Number(m[0] || 0), Number(m[1] || 0), Number(m[2] || 0), m[3] !== undefined ? Number(m[3]) : 1]
  }
  if (h.startsWith('#')) {
    h = h.slice(1)
    if (h.length === 3 || h.length === 4) h = [...h].map((c) => c + c).join('')
    const n = parseInt(h.slice(0, 6), 16)
    const a = h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1
    return [(n >>> 16) & 255, (n >>> 8) & 255, n & 255, a]
  }
  return [0, 0, 0, 1]
}

function roundRect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.arcTo(x + w, y, x + w, y + h, r)
  ctx.arcTo(x + w, y + h, x, y + h, r)
  ctx.arcTo(x, y + h, x, y, r)
  ctx.arcTo(x, y, x + w, y, r)
  ctx.closePath()
  ctx.fill()
}

function draw() {
  const canvas = canvasRef.value
  if (!canvas || typeof document === 'undefined') return

  let qr
  try {
    qr = encodeQRCode(props.value, props.level)
  } catch (e) {
    /* 内容太长等情况：画一个空白底并让控制台提示 */
    console.warn(e)
    qr = { size: 1, get: () => false }
  }

  const margin = Math.max(0, Math.floor(props.margin))
  const total = qr.size + margin * 2
  const dpr = Math.min(window.devicePixelRatio || 1, 3)
  const px = Math.max(1, Math.floor(props.size * dpr))

  canvas.width = px
  canvas.height = px
  canvas.style.width = `${props.size}px`
  canvas.style.height = `${props.size}px`

  const ctx = canvas.getContext('2d')
  if (!ctx) return
  ctx.clearRect(0, 0, px, px)

  // 背景
  const bg = hexToRgba(props.bgColor)
  if (bg[3] > 0) {
    ctx.fillStyle = props.bgColor
    ctx.fillRect(0, 0, px, px)
  }

  // 前景色 / 渐变
  const cell = px / total
  let fill: string | CanvasGradient = props.fgColor
  if (props.fgColor2) {
    const dirs: Record<string, [number, number, number, number]> = {
      'lt-br': [0, 0, px, px],
      'rt-bl': [px, 0, 0, px],
      'top-bottom': [0, 0, 0, px],
      'left-right': [0, 0, px, 0],
    }
    const [x0, y0, x1, y1] = dirs[props.gradientDirection ?? 'lt-br']
    const g2 = ctx.createLinearGradient(x0, y0, x1, y1)
    g2.addColorStop(0, props.fgColor)
    g2.addColorStop(1, props.fgColor2)
    fill = g2
  }
  ctx.fillStyle = fill

  const drawModule = (x: number, y: number) => {
    const cx = (x + margin) * cell
    const cy = (y + margin) * cell
    if (props.dotStyle === 'dots') {
      ctx.beginPath()
      ctx.arc(cx + cell / 2, cy + cell / 2, cell * 0.42, 0, Math.PI * 2)
      ctx.fill()
    } else if (props.dotStyle === 'rounded') {
      roundRect(ctx, cx + cell * 0.06, cy + cell * 0.06, cell * 0.88, cell * 0.88, cell * 0.3)
    } else {
      ctx.fillRect(cx, cy, cell + 0.5, cell + 0.5)
    }
  }

  for (let y = 0; y < qr.size; y++) {
    for (let x = 0; x < qr.size; x++) {
      if (!qr.get(x, y)) continue
      drawModule(x, y)
    }
  }

  // 定位图形重绘成更精致的三层圆角块（仅非 square 样式时）
  if (props.dotStyle !== 'square') {
    const drawFinder = (fx: number, fy: number) => {
      ctx.fillStyle = fill
      // 外框 7x7：外圈实心环
      roundRect(ctx, (fx - 3 + margin) * cell, (fy - 3 + margin) * cell, cell * 7, cell * 7, cell * 2)
      // 挖空中间：用背景色盖一个 5x5
      const bgs = props.bgColor
      ctx.fillStyle = bgs
      roundRect(ctx, (fx - 2 + margin) * cell + cell * 0.02, (fy - 2 + margin) * cell + cell * 0.02, cell * 5 - cell * 0.04, cell * 5 - cell * 0.04, cell * 1.4)
      // 中心 3x3
      ctx.fillStyle = fill
      roundRect(ctx, (fx - 1 + margin) * cell, (fy - 1 + margin) * cell, cell * 3, cell * 3, cell * 0.9)
    }
    drawFinder(3, 3)
    drawFinder(qr.size - 4, 3)
    drawFinder(3, qr.size - 4)
  }

  // Logo
  if (logoLoaded && logoImg) {
    const lw = px * props.logoWidth
    const pad = lw * 0.12
    const lx = (px - lw) / 2
    ctx.fillStyle = props.bgColor === 'transparent' ? '#ffffff' : props.bgColor
    roundRect(ctx, lx - pad, lx - pad, lw + pad * 2, lw + pad * 2, props.logoRadius * dpr + pad)
    ctx.save()
    roundRectPathOnly(ctx, lx, lx, lw, lw, props.logoRadius * dpr)
    ctx.clip()
    ctx.drawImage(logoImg, lx, lx, lw, lw)
    ctx.restore()
  }
}

function roundRectPathOnly(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.arcTo(x + w, y, x + w, y + h, r)
  ctx.arcTo(x + w, y + h, x, y + h, r)
  ctx.arcTo(x, y + h, x, y, r)
  ctx.arcTo(x, y, x + w, y, r)
  ctx.closePath()
}

function loadLogo() {
  logoLoaded = false
  logoImg = null
  if (!props.logo || typeof document === 'undefined') {
    draw()
    return
  }
  const img = new Image()
  img.crossOrigin = 'anonymous'
  img.onload = () => {
    logoImg = img
    logoLoaded = true
    draw()
  }
  img.onerror = () => draw()
  img.src = props.logo
}

watch(
  () => [props.value, props.level, props.margin, props.size, props.fgColor, props.fgColor2, props.bgColor, props.dotStyle, props.logo, props.logoWidth, props.logoRadius, props.gradientDirection],
  () => loadLogo(),
)

onMounted(() => {
  loadLogo()
  draw()
})

onBeforeUnmount(() => {
  logoImg = null
})

const info = computed(() => {
  try {
    const r = encodeQRCode(props.value, props.level)
    return `v${r.version} · ${r.size}×${r.size}`
  } catch {
    return ''
  }
})

/** 导出 PNG dataURL（可传倍数放大导出尺寸） */
function toDataURL(scale = 1): string {
  const canvas = canvasRef.value
  if (!canvas) return ''
  if (scale === 1) return canvas.toDataURL('image/png')
  const out = document.createElement('canvas')
  out.width = canvas.width * scale
  out.height = canvas.height * scale
  const ctx = out.getContext('2d')
  if (!ctx) return ''
  ctx.imageSmoothingEnabled = false
  ctx.drawImage(canvas, 0, 0, out.width, out.height)
  return out.toDataURL('image/png')
}

defineExpose({ toDataURL })
</script>

<template>
  <div class="jm-qrcode" :style="{ width: `${size}px`, height: `${size}px` }">
    <canvas ref="canvasRef" class="jm-qrcode__canvas" role="img" :aria-label="`二维码：${value.slice(0, 24)}`" />
  </div>
</template>

<style>
.jm-qrcode {
  position: relative;
  display: inline-block;
  font-family: var(--jm-font-family);
}

.jm-qrcode__canvas {
  display: block;
}
</style>
