<script setup lang="ts">
import { computed } from 'vue'
import { toCssSize } from '../utils'

defineOptions({ name: 'JmScanner' })

/**
 * 扫描动效（Scanner）
 * ---------------------------------------------------------------------------
 * AI 识图场景的「正在扫描」视觉：一条亮线在框内往复扫动 + 四角取景框。
 * 典型用法：拍完作业题正在 OCR、上传证件照正在核验、扫动物/植物识别。
 *
 * 为什么做成独立组件而不是塞进 Uploader：
 *   - 扫描的是"画面"而不是"文件列表"：上游可能是相机取景框、img、canvas
 *     或任意合成内容，Uploader 塞不下这个抽象层级；
 *   - 动效是纯视觉职责：active 开关、时长、颜色都交给宿主，识别逻辑
 *     （模型推理、进度回调）留在业务侧——组件只回答"现在扫到哪了"。
 *
 * 动效降级：data-motion="off" 或系统减少动效时，扫描线停在中线不动，
 * 框与角标保留——功能语义还在，只是不再动。
 */

const props = withDefaults(
  defineProps<{
    /** 是否扫描中；false 时扫描线淡出停止 */
    active?: boolean
    /** 单次扫描时长（ms），线从顶扫到底再返回 */
    duration?: number
    /** 扫描线颜色 */
    lineColor?: string
    /** 扫描线厚度，数字按 px */
    lineWidth?: number | string
    /** 显示四角取景框 */
    corners?: boolean
    /** 角标颜色 */
    cornerColor?: string
    /** 角标边长，数字按 px */
    cornerSize?: number | string
    /** 角标粗细，数字按 px */
    cornerWidth?: number | string
    /** 容器圆角 */
    radius?: number | string
    /** 显示斜向网格暗纹（取景器的"科技感"底纹） */
    showGrid?: boolean
    /** 容器最小高度，数字按 px；不放内容时兜底 */
    height?: number | string
  }>(),
  {
    active: true,
    duration: 1800,
    lineColor: '',
    lineWidth: 2,
    corners: true,
    cornerColor: '',
    cornerSize: 22,
    cornerWidth: 3,
    radius: 12,
    showGrid: false,
    height: 200,
  },
)

const styles = computed(() => {
  const s: Record<string, string> = {}
  const r = toCssSize(props.radius)
  if (r) s['--jm-scanner-radius'] = r
  const h = toCssSize(props.height)
  if (h) s['--jm-scanner-height'] = h
  const lw = toCssSize(props.lineWidth)
  if (lw) s['--jm-scanner-line-width'] = lw
  if (props.lineColor) s['--jm-scanner-line-color'] = props.lineColor
  const cs = toCssSize(props.cornerSize)
  if (cs) s['--jm-scanner-corner-size'] = cs
  const cw = toCssSize(props.cornerWidth)
  if (cw) s['--jm-scanner-corner-width'] = cw
  if (props.cornerColor) s['--jm-scanner-corner-color'] = props.cornerColor
  s['--jm-scanner-duration'] = `${props.duration}ms`
  return s
})

const classes = computed(() => [
  'jm-scanner',
  {
    'is-active': props.active,
    'has-grid': props.showGrid,
    'no-corners': !props.corners,
  },
])
</script>

<template>
  <div :class="classes" :style="styles">
    <div class="jm-scanner__viewport">
      <slot>
        <div class="jm-scanner__placeholder">把要识别的内容对准取景框</div>
      </slot>

      <span v-if="showGrid" class="jm-scanner__grid" aria-hidden="true" />

      <!-- 四角取景框 -->
      <span v-if="corners" class="jm-scanner__corner jm-scanner__corner--tl" aria-hidden="true" />
      <span v-if="corners" class="jm-scanner__corner jm-scanner__corner--tr" aria-hidden="true" />
      <span v-if="corners" class="jm-scanner__corner jm-scanner__corner--bl" aria-hidden="true" />
      <span v-if="corners" class="jm-scanner__corner jm-scanner__corner--br" aria-hidden="true" />

      <!-- 扫描线：亮线 + 前方渐变拖尾 -->
      <span class="jm-scanner__line" aria-hidden="true" />

      <span
        v-if="active"
        class="jm-scanner__status"
        role="status"
        aria-label="正在扫描识别"
      >扫描中…</span>
    </div>
  </div>
</template>

<style>
/**
 * Scanner
 * ---------------------------------------------------------------------------
 * 覆盖层与内容分层：viewport 是定位容器，扫描线/角标绝对定位盖在上面；
 * 动效只跑 transform + opacity（合成层），不触发布局。
 */
.jm-scanner {
  width: 100%;
  font-family: var(--jm-font-family);
}

.jm-scanner__viewport {
  position: relative;
  min-height: var(--jm-scanner-height, 200px);
  border-radius: var(--jm-scanner-radius, 12px);
  overflow: hidden;
  background: var(--jm-scanner-bg, #0b1220);
}

.jm-scanner__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  color: rgba(255, 255, 255, 0.45);
  font-size: var(--jm-font-size-sm);
  text-align: center;
}

.jm-scanner__viewport > img,
.jm-scanner__viewport > video,
.jm-scanner__viewport > canvas {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 斜向网格暗纹：透明度压到 0.06，只提供质感不抢内容 */
.jm-scanner__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
}

/* 四角取景框：用双边框画 L 形，颜色跟随主色 */
.jm-scanner__corner {
  position: absolute;
  width: var(--jm-scanner-corner-size, 22px);
  height: var(--jm-scanner-corner-size, 22px);
  border: var(--jm-scanner-corner-width, 3px) solid var(--jm-scanner-corner-color, var(--jm-color-primary, #00a0e9));
  pointer-events: none;
}

.jm-scanner__corner--tl {
  top: 12px;
  left: 12px;
  border-right: 0;
  border-bottom: 0;
  border-top-left-radius: 6px;
}

.jm-scanner__corner--tr {
  top: 12px;
  right: 12px;
  border-left: 0;
  border-bottom: 0;
  border-top-right-radius: 6px;
}

.jm-scanner__corner--bl {
  bottom: 12px;
  left: 12px;
  border-right: 0;
  border-top: 0;
  border-bottom-left-radius: 6px;
}

.jm-scanner__corner--br {
  bottom: 12px;
  right: 12px;
  border-left: 0;
  border-top: 0;
  border-bottom-right-radius: 6px;
}

/* 扫描线：亮线本体画在容器顶部 + 下方 44px 渐变拖尾；容器铺满视口做位移，
   translateY(calc(100% - 2px)) 把亮线推到视口底部——线从顶扫到底再折返。
   注意亮线必须锚定 top：锚 bottom 的话 span 被推出视口后线会被 overflow 裁掉 */
.jm-scanner__line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.jm-scanner__line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: var(--jm-scanner-line-width, 2px);
  border-radius: 999px;
  /* 两端渐隐渐细：水平渐变到透明，配合 drop-shadow 光晕随形状衰减 */
  background: linear-gradient(
    90deg,
    transparent,
    var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)) 14%,
    var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)) 86%,
    transparent
  );
  filter: drop-shadow(0 0 8px var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)));
}

/* 拖尾跟随运动方向：下扫时在亮线上方，上扫时翻到下方（49.9% 处切换）。
   gradient 方向同步翻转，保证贴线一侧始终着色、远端透明 */
.jm-scanner__line::after {
  content: '';
  position: absolute;
  top: -44px;
  left: 6%;
  right: 6%;
  height: 44px;
  background: linear-gradient(
    to bottom,
    transparent,
    color-mix(in srgb, var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)) 18%, transparent)
  );
}

.jm-scanner.is-active .jm-scanner__line {
  opacity: 1;
  animation: jm-scanner-sweep var(--jm-scanner-duration, 1800ms) ease-in-out infinite;
}

.jm-scanner.is-active .jm-scanner__line::after {
  animation: jm-scanner-tail var(--jm-scanner-duration, 1800ms) ease-in-out infinite;
}

@keyframes jm-scanner-sweep {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(calc(100% - 2px));
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes jm-scanner-tail {
  0%,
  49.9% {
    /* 上方：贴线一侧是底部，向下着色渐隐到上端 */
    transform: translateY(0);
    background: linear-gradient(
      to bottom,
      transparent,
      color-mix(in srgb, var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)) 18%, transparent)
    );
  }
  50%,
  100% {
    /* 翻到下方：贴线一侧是顶部 */
    transform: translateY(46px);
    background: linear-gradient(
      to bottom,
      color-mix(in srgb, var(--jm-scanner-line-color, var(--jm-color-primary, #00a0e9)) 18%, transparent),
      transparent
    );
  }
}

/* 扫描状态文案：右下角小字，不挡内容 */
.jm-scanner__status {
  position: absolute;
  right: 14px;
  bottom: 12px;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.45);
  color: rgba(255, 255, 255, 0.85);
  font-size: var(--jm-font-size-xs);
  animation: jm-scanner-blink 1.6s ease-in-out infinite;
}

@keyframes jm-scanner-blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.55;
  }
}

/* 动效降级：线停在中线、文案不再闪烁，取景框语义保留 */
@media (prefers-reduced-motion: reduce) {
  .jm-scanner.is-active .jm-scanner__line {
    animation: none;
    top: 50%;
    opacity: 1;
  }

  .jm-scanner__status {
    animation: none;
  }
}

[data-motion='off'] .jm-scanner.is-active .jm-scanner__line {
  animation: none;
  top: 50%;
  opacity: 1;
}

[data-motion='off'] .jm-scanner__status {
  animation: none;
}
</style>
