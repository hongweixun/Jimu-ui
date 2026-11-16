<script setup lang="ts">
defineOptions({ name: 'JmSwipeItem' })
</script>

<template>
  <div class="jm-swipe__item">
    <slot />
  </div>
</template>

<style>
.jm-swipe__item {
  width: 100%;
  height: 100%;
}
</style>
