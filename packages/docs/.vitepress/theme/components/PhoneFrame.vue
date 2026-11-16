<script setup lang="ts">
withDefaults(
  defineProps<{
    width?: number
    height?: number
    /** 状态栏显示的时间 */
    time?: string
    /** 是否画刘海 */
    notch?: boolean
  }>(),
  { width: 360, height: 620, time: '9:41', notch: true },
)
</script>

<template>
  <div class="phone" :style="{ width: `${width}px` }">
    <div class="phone__shell">
      <div class="phone__screen" data-jm-preview-scope :style="{ height: `${height}px` }">
        <div class="phone__status">
          <span class="phone__time">{{ time }}</span>
          <span class="phone__icons" aria-hidden="true">
            <svg viewBox="0 0 18 12" class="phone__icon">
              <rect x="0" y="8" width="3" height="4" rx="1" fill="currentColor" />
              <rect x="5" y="5.5" width="3" height="6.5" rx="1" fill="currentColor" />
              <rect x="10" y="3" width="3" height="9" rx="1" fill="currentColor" />
              <rect x="15" y="0" width="3" height="12" rx="1" fill="currentColor" opacity="0.35" />
            </svg>
            <svg viewBox="0 0 16 12" class="phone__icon">
              <path
                d="M8 10.5l1.8-2.1a2.6 2.6 0 00-3.6 0L8 10.5zM8 6.4a5.6 5.6 0 014 1.7l1.3-1.5A7.7 7.7 0 008 4.2a7.7 7.7 0 00-5.3 2.4L4 8.1a5.6 5.6 0 014-1.7z"
                fill="currentColor"
              />
            </svg>
            <svg viewBox="0 0 26 12" class="phone__icon">
              <rect x="0.5" y="1" width="21" height="10" rx="3" fill="none" stroke="currentColor" stroke-opacity="0.4" />
              <rect x="2.5" y="3" width="16" height="6" rx="1.5" fill="currentColor" />
              <path d="M23 4.5v3a2 2 0 000-3z" fill="currentColor" opacity="0.5" />
            </svg>
          </span>
        </div>

        <div v-if="notch" class="phone__notch" aria-hidden="true" />

        <div class="phone__content">
          <slot />
        </div>

        <div class="phone__home" aria-hidden="true" />
      </div>
    </div>
    <div class="phone__meta">
      <span>{{ width }} × {{ height }}</span>
      <span class="phone__meta-dot" />
      <span>iPhone / Android 通用</span>
    </div>
  </div>
</template>

<style scoped>
.phone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  max-width: 100%;
}

.phone__shell {
  /* 必须显式定宽：.phone 是 align-items:center 的列 flex，shell 是 shrink-to-fit，
     内容里若有 max-content（如跑马灯轨道）会把壳撑到全卡宽 */
  width: 100%;
  padding: 10px;
  border-radius: 44px;
  box-sizing: border-box;
  background: linear-gradient(160deg, #2c3238, #14181c 55%, #23292f);
  box-shadow:
    0 18px 40px -12px rgba(16, 21, 26, 0.35),
    0 0 0 1px rgba(255, 255, 255, 0.08) inset;
}

.phone__screen {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 34px;
  background: var(--jm-bg-page);
  color: var(--jm-text-color);
  font-family: var(--jm-font-family);
  transition: background-color 0.3s;
}

.phone__status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 44px;
  padding: 0 22px;
  flex: 0 0 auto;
  font-size: 12px;
  font-weight: 500;
  color: var(--jm-text-color);
  letter-spacing: 0.2px;
}

.phone__icons {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--jm-text-color);
}

.phone__icon {
  height: 10px;
  width: auto;
}

.phone__notch {
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 96px;
  height: 22px;
  border-radius: 999px;
  background: #0b0e11;
}

.phone__content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 4px 0 8px;
  -webkit-overflow-scrolling: touch;
  position: relative;
}

.phone__content::-webkit-scrollbar {
  width: 4px;
}

.phone__content::-webkit-scrollbar-thumb {
  border-radius: 2px;
  background: var(--jm-border-color-2);
}

.phone__home {
  position: absolute;
  bottom: 7px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 4px;
  border-radius: 999px;
  background: var(--jm-text-color-4);
  opacity: 0.4;
}

.phone__meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
}

.phone__meta-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--vp-c-text-3);
  opacity: 0.6;
}
</style>
