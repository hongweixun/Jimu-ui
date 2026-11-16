<script setup lang="ts">
import { useAppearance } from 'jimu-ui'

const { appearance, setElder, setMotion } = useAppearance()
</script>

<template>
  <div class="nav-tools">
    <button
      type="button"
      class="nav-tools__btn"
      :class="{ 'is-on': appearance.elder }"
      :aria-pressed="appearance.elder"
      title="放大字号、加厚对比，模拟长辈使用"
      @click="setElder(!appearance.elder)"
    >
      <svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true">
        <circle cx="9" cy="6.5" r="3" fill="none" stroke="currentColor" stroke-width="1.7" />
        <path
          d="M3.5 20c0-3.4 2.5-5.8 5.5-5.8s5.5 2.4 5.5 5.8"
          fill="none"
          stroke="currentColor"
          stroke-width="1.7"
          stroke-linecap="round"
        />
        <path
          d="M17 9.5h5M19.5 7v5M18 20l1.5-5 1.5 5"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
        />
      </svg>
      <span>适老</span>
    </button>

    <button
      type="button"
      class="nav-tools__btn"
      :class="{ 'is-on': !appearance.motion }"
      :aria-pressed="!appearance.motion"
      title="关闭所有过渡与动效"
      @click="setMotion(!appearance.motion)"
    >
      <svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true">
        <path
          d="M13 2L4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5z"
          fill="none"
          stroke="currentColor"
          stroke-width="1.6"
          stroke-linejoin="round"
        />
      </svg>
      <span>{{ appearance.motion ? '动效开' : '动效关' }}</span>
    </button>
  </div>
</template>

<style scoped>
.nav-tools {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-right: 8px;
}

.nav-tools__btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 30px;
  padding: 0 9px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: transparent;
  color: var(--vp-c-text-2);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-tools__btn:hover {
  border-color: var(--vp-c-brand-2);
  color: var(--vp-c-brand-1);
}

.nav-tools__btn.is-on {
  border-color: var(--vp-c-brand-2);
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

@media (max-width: 768px) {
  .nav-tools__btn span {
    display: none;
  }
}
</style>
