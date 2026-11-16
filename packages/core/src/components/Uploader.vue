<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import { FORM_KEY } from './form-context'
import JmIcon from './Icon.vue'
import Popup from './Popup.vue'
import type { UploaderFile, UploaderRequest } from '../types'

defineOptions({ name: 'JmUploader' })

const props = withDefaults(
  defineProps<{
    /** 文件列表，元素可以是 URL 字符串或对象 */
    modelValue?: (string | UploaderFile)[]
    /** 最多上传数量 */
    maxCount?: number
    multiple?: boolean
    /** input accept，如 image/* */
    accept?: string
    /** 单文件大小上限（字节），0 表示不限制 */
    maxSize?: number
    /** 选中后自动压缩图片（canvas 重绘，输出同类型 blob） */
    compress?: boolean
    /** 压缩质量 0~1，png 除外 */
    compressQuality?: number
    /** 压缩后长边上限（像素），超出按比例缩小 */
    compressMaxSize?: number
    /** 移动端直接调起相机：user / environment */
    capture?: 'user' | 'environment'
    disabled?: boolean
    readonly?: boolean
    /** 显示删除按钮 */
    deletable?: boolean
    /** 点缩略图放大预览 */
    previewImage?: boolean
    /** 上传区域文案 */
    uploadText?: string
    /** 每行列数 */
    columns?: number
    /** 格子尺寸 */
    size?: number | string
    /** 圆角 */
    radius?: number | string
    /** 开启长按拖拽排序 */
    sortable?: boolean
    name?: string
    /** 预览弹层挂载位置，内嵌在手机框里演示时传 false */
    previewTeleport?: boolean | string | Element
    /** 自定义上传函数：拿到 File 与进度回调，返回远程地址则替换本地预览 */
    upload?: UploaderRequest
    /** 选完是否立即上传；配合 upload 使用，false 时需手动调 submit() */
    autoUpload?: boolean
    /** 待上传徽标文案 */
    pendingText?: string
    /** 失败重试文案 */
    retryText?: string
  }>(),
  {
    modelValue: () => [],
    maxCount: 9,
    multiple: false,
    accept: 'image/*',
    maxSize: 0,
    compress: false,
    compressQuality: 0.8,
    compressMaxSize: 1280,
    deletable: true,
    previewImage: true,
    uploadText: '上传',
    columns: 4,
    size: 80,
    sortable: false,
    name: 'file',
    previewTeleport: true,
    autoUpload: true,
    pendingText: '待上传',
    retryText: '重试',
  },
)

const form = inject(FORM_KEY, null)
const disabled = computed(() => props.disabled || form?.disabled.value || false)

const emit = defineEmits<{
  'update:modelValue': [files: (string | UploaderFile)[]]
  change: [files: (string | UploaderFile)[]]
  /** 超过 maxCount */
  exceed: [files: File[]]
  /** 超过 maxSize */
  oversize: [files: File[]]
  delete: [file: string | UploaderFile, index: number]
  'click-preview': [file: string | UploaderFile, index: number]
  'click-upload': []
  /** 单个文件上传成功 */
  success: [file: UploaderFile, index: number]
  /** 单个文件上传失败 */
  error: [file: UploaderFile, index: number, reason: unknown]
  /** 上传进度（0~100） */
  progress: [percent: number, index: number]
}>()

const input = ref<HTMLInputElement | null>(null)
const previewIndex = ref(-1)

/** 本组件创建的 blob URL，移除或卸载时回收，避免内存泄漏 */
const objectUrls = new Set<string>()

/**
 * 本地最后一次发出的数组。自定义上传是异步的，成功后要把远程地址写回列表，
 * 此时 props.modelValue 可能还没同步过来，用 lastEmitted 兜住这个时间差。
 */
const lastEmitted = ref<(string | UploaderFile)[] | null>(null)
const list = computed(() => lastEmitted.value ?? props.modelValue ?? [])

watch(
  () => props.modelValue,
  (v) => {
    // 父级把我们发出的数组原样回灌时保持引用，否则说明外部改了数据，以外部为准
    if (v !== lastEmitted.value) lastEmitted.value = null
  },
)

const canAdd = computed(() => !disabled.value && !props.readonly && list.value.length < props.maxCount)

const gridStyle = computed(() => {
  const s: Record<string, string> = { '--jm-uploader-columns': String(props.columns) }
  const size = toCssSize(props.size)
  if (size) s['--jm-uploader-size'] = size
  const r = toCssSize(props.radius)
  if (r) s['--jm-uploader-radius'] = r
  return s
})

function urlOf(item: string | UploaderFile): string {
  return typeof item === 'string' ? item : (item.url ?? '')
}

function nameOf(item: string | UploaderFile, index: number): string {
  if (typeof item === 'string') return item.split('/').pop() || `文件${index + 1}`
  return item.name || `文件${index + 1}`
}

function emitList(next: (string | UploaderFile)[]) {
  lastEmitted.value = next
  emit('update:modelValue', next)
  emit('change', next)
}

/* ------------------------------------------------------------------ */
/* 上传进度 / 失败重试                                                    */
/* ------------------------------------------------------------------ */

interface UploadState {
  percent: number
  status: 'pending' | 'uploading' | 'done' | 'error'
  message?: string
}

/** 运行时进度，按本地 url 作 key；不写进 modelValue，避免每帧 emit */
const states = reactive<Record<string, UploadState>>({})

function stateKey(item: string | UploaderFile): string {
  const url = urlOf(item)
  if (url) return url
  return `#${typeof item === 'string' ? item : item.name ?? ''}`
}

function statusOf(item: string | UploaderFile) {
  const st = states[stateKey(item)]
  if (st) return st.status
  if (item && typeof item === 'object') {
    if (item.status === 'failed') return 'error'
    return item.status ?? 'done'
  }
  return 'done'
}

function percentOf(item: string | UploaderFile) {
  const st = states[stateKey(item)]
  if (st) return st.percent
  if (item && typeof item === 'object' && typeof item.percent === 'number') return item.percent
  return 0
}

function revoke(url?: string) {
  if (url && objectUrls.has(url)) {
    URL.revokeObjectURL(url)
    objectUrls.delete(url)
  }
}

async function startUpload(item: UploaderFile) {
  const upload = props.upload
  if (!upload || !item.file) return
  const key = stateKey(item)
  states[key] = { percent: 0, status: 'uploading' }

  try {
    const remote = await upload(item.file, {
      onProgress: (p) => {
        const st = states[key]
        if (!st || st.status !== 'uploading') return
        const next = Math.max(0, Math.min(100, Math.round(p)))
        if (next === st.percent) return
        st.percent = next
        emit('progress', next, indexOf(item))
      },
    })

    const index = indexOf(item)
    const next = list.value.map((it) =>
      it === item
        ? {
            ...item,
            status: 'done' as const,
            percent: 100,
            url: typeof remote === 'string' && remote ? remote : item.url,
          }
        : it,
    )
    // 换成远程地址后本地 blob 就没用了，及时回收
    if (typeof remote === 'string' && remote) revoke(item.url)
    delete states[key]
    emitList(next)
    emit('success', next[index] as UploaderFile, index)
  } catch (reason) {
    const st = states[key] ?? { percent: 0, status: 'uploading' as const }
    states[key] = {
      percent: st.percent,
      status: 'error',
      message: reason instanceof Error ? reason.message : String(reason ?? ''),
    }
    const index = indexOf(item)
    const next = list.value.map((it) => (it === item ? { ...item, status: 'error' as const } : it))
    emitList(next)
    emit('error', next[index] as UploaderFile, index, reason)
  }
}

function indexOf(item: unknown) {
  return list.value.indexOf(item as string | UploaderFile)
}

/** 手动上传全部待上传 / 失败的项 */
function submit() {
  if (!props.upload) return
  list.value.forEach((it) => {
    if (typeof it === 'string') return
    const status = statusOf(it)
    if (status === 'pending' || status === 'error') {
      states[stateKey(it)] = { percent: 0, status: 'uploading' }
      void startUpload(it)
    }
  })
}

/** 重试单个失败项 */
function retry(index: number) {
  const item = list.value[index]
  if (!item || typeof item === 'string') return
  states[stateKey(item)] = { percent: 0, status: 'uploading' }
  void startUpload(item)
}

function openPicker() {
  if (!canAdd.value) return
  emit('click-upload')
  input.value?.click()
}

function onChange(e: Event) {
  const el = e.target as HTMLInputElement
  const files = Array.from(el.files ?? [])
  el.value = '' // 允许重复选择同一个文件
  if (!files.length) return
  void acceptFiles(files)
}

/** 挑选 + 压缩 + 上限校验（压缩是异步的，单独拆出来） */
async function acceptFiles(files: File[]) {
  const remain = Math.max(0, props.maxCount - list.value.length)
  if (remain === 0) {
    emit('exceed', files)
    return
  }

  let accepted = files.slice(0, remain)
  if (files.length > remain) emit('exceed', files.slice(remain))

  if (props.compress) {
    const compressed: File[] = []
    for (const f of accepted) {
      if (isCompressible(f)) {
        try {
          compressed.push(await compressImage(f))
        } catch {
          compressed.push(f) // 压缩失败不拦截，回退原文件
        }
      } else {
        compressed.push(f)
      }
    }
    accepted = compressed
  }

  if (props.maxSize > 0) {
    const oversize = accepted.filter((f) => f.size > props.maxSize)
    if (oversize.length) {
      emit('oversize', oversize)
      accepted = accepted.filter((f) => f.size <= props.maxSize)
    }
  }

  const added: UploaderFile[] = accepted.map((file) => {
    const url = typeof URL !== 'undefined' && URL.createObjectURL ? URL.createObjectURL(file) : ''
    if (url) objectUrls.add(url)
    // 传了 upload 才走上传流程，否则维持「选中即完成」的老行为
    const status = props.upload ? ('pending' as const) : ('done' as const)
    return { url, name: file.name, size: file.size, status, file }
  })

  if (added.length) {
    emitList([...list.value, ...added])
    if (props.upload && props.autoUpload) {
      added.forEach((file) => {
        states[stateKey(file)] = { percent: 0, status: 'uploading' }
        void startUpload(file)
      })
    }
  }
}

/** 可压缩的位图：gif 有动帧、svg 矢量，都重绘会毁掉 */
function isCompressible(file: File): boolean {
  return file.type.startsWith('image/') && file.type !== 'image/gif' && file.type !== 'image/svg+xml'
}

function loadImage(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file)
    const img = new Image()
    img.onload = () => {
      URL.revokeObjectURL(url)
      resolve(img)
    }
    img.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('image load failed'))
    }
    img.src = url
  })
}

async function compressImage(file: File): Promise<File> {
  const maxEdge = props.compressMaxSize || 1280
  const quality = Math.min(1, Math.max(0, props.compressQuality ?? 0.8))
  const img = await loadImage(file)
  const scale = Math.min(1, maxEdge / Math.max(img.naturalWidth, img.naturalHeight))
  const w = Math.max(1, Math.round(img.naturalWidth * scale))
  const h = Math.max(1, Math.round(img.naturalHeight * scale))

  const canvas = document.createElement('canvas')
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext('2d')
  if (!ctx) return file
  ctx.drawImage(img, 0, 0, w, h)

  /* png 保留透明通道；其余统一 jpeg（拍照场景体积收益最大） */
  const type = file.type === 'image/png' ? 'image/png' : 'image/jpeg'
  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, type, quality))
  if (!blob || blob.size >= file.size) return file // 压完反而更大就用原文件

  const name = file.name.replace(/\.[^.]+$/, '') + (type === 'image/png' ? '.png' : '.jpg')
  return new File([blob], name, { type, lastModified: Date.now() })
}

function onDelete(index: number, e: MouseEvent) {
  e.stopPropagation()
  const item = list.value[index]
  const url = urlOf(item)
  revoke(url)
  if (url) delete states[url]
  emitList(list.value.filter((_, i) => i !== index))
  emit('delete', item, index)
}

function onPreview(index: number) {
  const item = list.value[index]
  emit('click-preview', item, index)
  if (props.previewImage && urlOf(item)) previewIndex.value = index
}

const previewUrl = computed(() =>
  previewIndex.value >= 0 ? urlOf(list.value[previewIndex.value] ?? '') : '',
)

const showPreview = computed({
  get: () => previewIndex.value >= 0,
  set: (v: boolean) => {
    if (!v) previewIndex.value = -1
  },
})

onBeforeUnmount(() => {
  objectUrls.forEach((url) => URL.revokeObjectURL(url))
  objectUrls.clear()
})

/* ------------------------------------------------------------------ */
/* 长按拖拽排序                                                          */
/* ------------------------------------------------------------------ */

const root = ref<HTMLElement | null>(null)

/** 拖拽起始 index（数据序），-1 表示未在拖拽 */
const dragIndex = ref(-1)
/** 拖拽项当前应处的 index：拖拽期间 DOM 不动，只有其他格子让位 */
const dragCur = ref(-1)
const dragActive = ref(false)
const dragDx = ref(0)
const dragDy = ref(0)

const PRESS_DELAY = 420
let pressTimer: ReturnType<typeof setTimeout> | undefined
let pressStart = { x: 0, y: 0 }
/** 拖拽项原格子的中心（视口坐标），curIndex 按它落点算 */
let cellCenter = { x: 0, y: 0 }
let cellW = 0
let step = 0
let cols = 1
let justDragged = false

function measureGrid() {
  const el = root.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const cs = getComputedStyle(el)
  const gap = parseFloat(cs.columnGap || cs.gap) || 0
  cols = Math.max(1, props.columns)
  cellW = (rect.width - gap * (cols - 1)) / cols
  step = cellW + gap
}

/** 格子中心（视口坐标） */
function centerOf(index: number, rect: DOMRect) {
  const col = index % cols
  const row = Math.floor(index / cols)
  return {
    x: rect.left + col * step + cellW / 2,
    y: rect.top + row * step + cellW / 2,
  }
}

/** 拖拽项中心当前落在哪个格子上 */
function curIndexFromCenter() {
  const rect = root.value?.getBoundingClientRect()
  if (!rect) return dragCur.value
  const x = cellCenter.x + dragDx.value
  const y = cellCenter.y + dragDy.value
  const col = Math.floor((x + step / 2 - rect.left) / step)
  const row = Math.floor((y + step / 2 - rect.top) / step)
  const i = row * cols + col
  return Math.max(0, Math.min(i, list.value.length - 1))
}

function onThumbPointerDown(e: PointerEvent, index: number) {
  if (!props.sortable || disabled.value || props.readonly) return
  if (e.pointerType === 'mouse' && e.button !== 0) return

  pressStart = { x: e.clientX, y: e.clientY }
  dragIndex.value = index
  dragCur.value = index
  dragDx.value = 0
  dragDy.value = 0

  pressTimer = setTimeout(() => {
    if (dragIndex.value < 0) return
    measureGrid()
    const rect = root.value?.getBoundingClientRect()
    if (!rect) return
    cellCenter = centerOf(dragIndex.value, rect)
    dragActive.value = true
    justDragged = false
    document.body.style.userSelect = 'none'
  }, PRESS_DELAY)
}

/* move/up 挂在 document：手指拖出缩略图也要跟手，且不依赖 setPointerCapture
   （合成事件没有真实 pointerId，capture 必抛 NotFoundError） */
function onDocPointerMove(e: PointerEvent) {
  if (!dragActive.value || dragIndex.value < 0) return
  dragDx.value = e.clientX - pressStart.x
  dragDy.value = e.clientY - pressStart.y
  dragCur.value = curIndexFromCenter()
}

function onThumbPointerUp() {
  clearTimeout(pressTimer)
  if (!dragActive.value) {
    dragIndex.value = -1
    return
  }

  const from = dragIndex.value
  const to = dragCur.value
  dragActive.value = false
  dragIndex.value = -1
  dragCur.value = -1
  document.body.style.userSelect = ''
  justDragged = true
  setTimeout(() => (justDragged = false), 120)

  if (from !== to) {
    const next = [...list.value]
    const [moved] = next.splice(from, 1)
    next.splice(to, 0, moved)
    emitList(next)
  }
}

function onThumbPointerCancel() {
  clearTimeout(pressTimer)
  dragActive.value = false
  dragIndex.value = -1
  dragCur.value = -1
  document.body.style.userSelect = ''
}

/** 其他格子按目标位置让位：走直线位移，跨行也自然 */
function itemStyle(i: number): Record<string, string> {
  const s: Record<string, string> = {}
  if (!dragActive.value || dragIndex.value < 0) return s

  if (i === dragIndex.value) {
    s.transform = `translate(${dragDx.value}px, ${dragDy.value}px) scale(1.06)`
    return s
  }

  const from = dragIndex.value
  const cur = dragCur.value
  const shouldShift = (from < cur && i > from && i <= cur) || (cur < from && i >= cur && i < from)
  if (!shouldShift) return s

  const target = cur < from ? i + 1 : i - 1
  const colA = i % cols
  const rowA = Math.floor(i / cols)
  const colB = target % cols
  const rowB = Math.floor(target / cols)
  s.transform = `translate(${(colB - colA) * step}px, ${(rowB - rowA) * step}px)`
  return s
}

/** 拖完的一次 click 不打开预览 */
function onThumbClick(index: number) {
  if (justDragged) return
  onPreview(index)
}

/* 拖拽期间锁住页面滚动（touchmove 非被动才拦得住） */
function onTouchMove(e: TouchEvent) {
  if (dragActive.value) e.preventDefault()
}

defineExpose({
  /** 手动上传全部待上传 / 失败项（autoUpload=false 时用） */
  submit,
  /** 重试指定下标的失败项 */
  retry,
})

onMounted(() => {
  document.addEventListener('touchmove', onTouchMove, { passive: false })
  document.addEventListener('pointermove', onDocPointerMove)
  document.addEventListener('pointerup', onThumbPointerUp)
  document.addEventListener('pointercancel', onThumbPointerCancel)
})

onBeforeUnmount(() => {
  clearTimeout(pressTimer)
  document.removeEventListener('touchmove', onTouchMove)
  document.removeEventListener('pointermove', onDocPointerMove)
  document.removeEventListener('pointerup', onThumbPointerUp)
  document.removeEventListener('pointercancel', onThumbPointerCancel)
  document.body.style.userSelect = ''
})
</script>

<template>
  <div
    ref="root"
    class="jm-uploader"
    :class="{ 'is-disabled': disabled, 'is-sortable': sortable }"
    :style="gridStyle"
  >
    <input
      ref="input"
      class="jm-uploader__input"
      type="file"
      :name="name"
      :accept="accept"
      :multiple="multiple"
      :capture="capture"
      :disabled="disabled"
      @change="onChange"
    />

    <div
      v-for="(item, i) in list"
      :key="urlOf(item) || i"
      class="jm-uploader__item"
      :class="{
        'is-dragging': dragActive && i === dragIndex,
        'is-dropped': dragActive && i === dragCur && i !== dragIndex,
      }"
      :style="itemStyle(i)"
    >
      <img
        class="jm-uploader__thumb"
        :src="urlOf(item)"
        :alt="nameOf(item, i)"
        draggable="false"
        @pointerdown="onThumbPointerDown($event, i)"
        @click="onThumbClick(i)"
      />
      <div
        v-if="statusOf(item) === 'uploading'"
        class="jm-uploader__progress"
        :style="{ '--jm-upload-p': `${percentOf(item)}%` }"
        role="progressbar"
        :aria-valuenow="percentOf(item)"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <span class="jm-uploader__progress-num">{{ percentOf(item) }}%</span>
      </div>
      <button
        v-else-if="statusOf(item) === 'error'"
        type="button"
        class="jm-uploader__retry"
        @click.stop="retry(i)"
      >
        <jm-icon name="refresh" size="12" :stroke-width="2.4" />
        <span>{{ retryText }}</span>
      </button>
      <span v-else-if="statusOf(item) === 'pending'" class="jm-uploader__badge">
        {{ pendingText }}
      </span>
      <button
        v-if="deletable && !readonly && !disabled"
        type="button"
        class="jm-uploader__delete"
        aria-label="删除"
        @click="onDelete(i, $event)"
      >
        <jm-icon name="close" size="12px" :stroke-width="2.4" />
      </button>
    </div>

    <button
      v-if="canAdd"
      type="button"
      class="jm-uploader__trigger"
      :aria-label="uploadText"
      @click="openPicker"
    >
      <slot name="upload">
        <jm-icon class="jm-uploader__plus" name="plus" size="24px" :stroke-width="1.8" />
        <span v-if="uploadText" class="jm-uploader__text">{{ uploadText }}</span>
      </slot>
    </button>

    <Popup
      v-model:show="showPreview"
      position="center"
      :teleport="previewTeleport"
      :radius="8"
    >
      <img v-if="previewUrl" class="jm-uploader__preview" :src="previewUrl" alt="预览" />
    </Popup>
  </div>
</template>

<style>
.jm-uploader {
  display: grid;
  grid-template-columns: repeat(var(--jm-uploader-columns, 4), 1fr);
  gap: var(--jm-space-2);
  font-family: var(--jm-font-family);
}

.jm-uploader__input {
  display: none;
}

.jm-uploader__item,
.jm-uploader__trigger {
  position: relative;
  aspect-ratio: 1 / 1;
  min-width: 0;
  border-radius: var(--jm-uploader-radius, var(--jm-radius-md));
  overflow: hidden;
}

/* ---------- 拖拽排序 ---------- */
.jm-uploader.is-sortable .jm-uploader__item {
  transition: transform var(--jm-motion-transition-duration, 200ms) var(--jm-motion-transition-ease, ease-out);
}

.jm-uploader.is-sortable .jm-uploader__thumb {
  cursor: grab;
  touch-action: pan-y; /* 长按激活前仍允许页面竖向滚动 */
}

.jm-uploader__item.is-dragging {
  z-index: 3;
  transition: none;
  opacity: 0.92;
}

.jm-uploader__item.is-dragging .jm-uploader__thumb {
  cursor: grabbing;
  box-shadow: 0 6px 18px rgba(16, 21, 26, 0.28);
}

.jm-uploader__item.is-dropped {
  opacity: 0.55;
}

.jm-uploader__thumb {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: var(--jm-bg-input);
  cursor: zoom-in;
}

.jm-uploader__badge {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 2px 0;
  background: rgba(0, 0, 0, 0.55);
  color: #fff;
  font-size: 10px;
  text-align: center;
}

.jm-uploader__progress {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.42);
  color: #fff;
  pointer-events: none;
}

/* 进度环：conic-gradient 画弧，radial-gradient 掏空中间 */
.jm-uploader__progress::before {
  content: '';
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: conic-gradient(#fff var(--jm-upload-p, 0%), rgba(255, 255, 255, 0.28) 0);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px));
}

.jm-uploader__progress-num {
  position: relative;
  font-size: 10px;
  font-variant-numeric: tabular-nums;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
}

.jm-uploader__retry {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: inline-flex;
  align-items: center;
  gap: 2px;
  height: 24px;
  padding: 0 8px;
  border: 0;
  border-radius: var(--jm-radius-round);
  background: var(--jm-color-danger);
  color: #fff;
  font-family: inherit;
  font-size: 11px;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
}

.jm-uploader__retry:active {
  background: var(--jm-color-danger-active);
}

.jm-uploader__delete {
  position: absolute;
  top: 4px;
  right: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  cursor: pointer;
}

.jm-uploader__delete:active {
  background: rgba(0, 0, 0, 0.7);
}

.jm-uploader__trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border: 1px dashed var(--jm-border-color-2);
  background: var(--jm-bg-input);
  color: var(--jm-text-color-3);
  cursor: pointer;
  transition:
    border-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease),
    background-color var(--jm-motion-feedback-duration) var(--jm-motion-feedback-ease);
}

.jm-uploader__trigger:active {
  background: var(--jm-bg-active);
}

@media (hover: hover) {
  .jm-uploader__trigger:hover {
    border-color: var(--jm-color-primary);
    color: var(--jm-color-primary);
  }
}

.jm-uploader.is-disabled .jm-uploader__trigger {
  cursor: not-allowed;
  opacity: 0.5;
}

.jm-uploader__plus {
  width: 24px;
  height: 24px;
}

.jm-uploader__text {
  font-size: var(--jm-font-size-xs);
  line-height: 1.2;
}

.jm-uploader__preview {
  display: block;
  max-width: 80vw;
  max-height: 70vh;
  object-fit: contain;
}
</style>
