<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { toCssSize } from '../utils'
import Icon from './Icon.vue'

defineOptions({ name: 'JmAvatar' })

const props = withDefaults(
  defineProps<{
    /** 图片地址 */
    src?: string
    /** 图片替代文本；不传按纯装饰处理 */
    alt?: string
    /** 无图时的文字（取首字或直接传全称，超过 2 字自动截断） */
    text?: string
    /** 无图时的图标名 */
    icon?: string
    /** 尺寸：预设或数字(px)/任意长度 */
    size?: 'small' | 'medium' | 'large' | number | string
    /** 形状 */
    shape?: 'circle' | 'square'
    /** 圆角，square 时生效；数字按 px */
    radius?: number | string
    /** 图片裁切方式 */
    fit?: 'cover' | 'contain' | 'fill'
    /** 描边（叠放头像、深色背景上更清晰） */
    bordered?: boolean
    /** 文字头像背景色 */
    background?: string
    /** 文字颜色 */
    color?: string
    /** 图片加载失败时是否保留加载前的状态（默认回退到文字/图标） */
    keepOnError?: boolean
  }>(),
  { size: 'medium', shape: 'circle', fit: 'cover' },
)

const emit = defineEmits<{
  load: [event: Event]
  error: [event: Event]
}>()

const PRESET: Record<string, string> = {
  small: '32px',
  medium: '40px',
  large: '56px',
}

const failed = ref(false)

watch(
  () => props.src,
  () => {
    failed.value = false
  },
)

function onError(e: Event) {
  failed.value = true
  emit('error', e)
}

function onLoad(e: Event) {
  emit('load', e)
}

const showImage = computed(() => Boolean(props.src) && !failed.value)

/** 文字头像最多显示 2 个字，中文两字 / 英文首字母都合适 */
const displayText = computed(() => {
  const t = (props.text ?? '').trim()
  if (!t) return ''
  return t.length > 2 ? t.slice(0, 2) : t
})

const styles = computed(() => {
  const s: Record<string, string> = {}
  const size =
    typeof props.size === 'string' && PRESET[props.size]
      ? PRESET[props.size]
      : toCssSize(props.size)
  if (size) s['--jm-avatar-size'] = size
  const r = toCssSize(props.radius)
  if (r) s['--jm-avatar-radius'] = r
  if (props.background) s['--jm-avatar-bg'] = props.background
  if (props.color) s['--jm-avatar-color'] = props.color
  return s
})
</script>

<template>
  <div
    class="jm-avatar"
    :class="[`jm-avatar--${shape}`, { 'is-bordered': bordered }]"
    :style="styles"
  >
    <img
      v-if="showImage"
      class="jm-avatar__img"
      :src="src"
      :alt="alt"
      :style="{ objectFit: fit }"
      @load="onLoad"
      @error="onError"
    />
    <slot v-else>
      <span v-if="displayText" class="jm-avatar__text">{{ displayText }}</span>
      <Icon v-else-if="icon" class="jm-avatar__icon" :name="icon" />
      <Icon v-else class="jm-avatar__icon" name="user" />
    </slot>
  </div>
</template>

<style>
.jm-avatar {
  position: relative;
  display: inline-flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: var(--jm-avatar-size, 40px);
  height: var(--jm-avatar-size, 40px);
  border-radius: var(--jm-avatar-radius, var(--jm-radius-round));
  overflow: hidden;
  background: var(--jm-avatar-bg, var(--jm-bg-input));
  color: var(--jm-avatar-color, var(--jm-text-secondary));
  font-family: var(--jm-font-family);
  font-size: calc(var(--jm-avatar-size, 40px) * 0.36);
  font-weight: var(--jm-font-weight-medium, 500);
  line-height: 1;
  vertical-align: middle;
  user-select: none;
}

.jm-avatar--square {
  border-radius: var(--jm-avatar-radius, var(--jm-radius-md));
}

.jm-avatar.is-bordered {
  box-shadow: 0 0 0 2px var(--jm-bg-container);
}

.jm-avatar__img {
  width: 100%;
  height: 100%;
  display: block;
}

.jm-avatar__text {
  padding: 0 2px;
  white-space: nowrap;
  transform: translateZ(0);
}

.jm-avatar__icon {
  opacity: 0.7;
}
</style>
