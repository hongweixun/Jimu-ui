<script setup lang="ts">
import ImagePreview from './ImagePreview.vue'
import { closeImagePreview, imagePreviewState } from './image-preview'

defineOptions({ name: 'JmImagePreviewHost' })
</script>

<template>
  <ImagePreview
    :show="imagePreviewState.visible"
    :images="imagePreviewState.images"
    :start-position="imagePreviewState.startPosition"
    :show-index="imagePreviewState.showIndex"
    :closeable="imagePreviewState.closeable"
    :close-on-click-mask="imagePreviewState.closeOnClickMask"
    :close-on-click-image="imagePreviewState.closeOnClickImage"
    :zoomable="imagePreviewState.zoomable"
    :max-scale="imagePreviewState.maxScale"
    :double-tap-scale="imagePreviewState.doubleTapScale"
    :z-index="imagePreviewState.zIndex"
    :teleport="false"
    @update:show="(v: boolean) => { if (!v) closeImagePreview() }"
    @change="(i: number) => imagePreviewState.onChange?.(i)"
    @zoom="(s: number) => imagePreviewState.onZoom?.(s)"
  />
</template>
