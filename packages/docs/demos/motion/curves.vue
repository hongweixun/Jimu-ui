<script setup lang="ts">
import { ref } from 'vue'

const replay = ref(0)

const curves = [
  {
    label: '标准 standard',
    value: 'cubic-bezier(.34,.69,.1,1)',
    ease: 'var(--jm-ease-standard)',
    use: '状态切换、位移、变色',
  },
  {
    label: '减速 decelerate',
    value: 'cubic-bezier(.4,.8,.74,1)',
    ease: 'var(--jm-ease-decelerate)',
    use: '进场落位',
  },
  {
    label: '加速 accelerate',
    value: 'cubic-bezier(.26,0,.48,.9)',
    ease: 'var(--jm-ease-accelerate)',
    use: '退场离场',
  },
  {
    label: '回弹 overshoot',
    value: 'cubic-bezier(.3,1.3,.3,1)',
    ease: 'var(--jm-ease-overshoot)',
    use: '开关、勾选',
  },
]

const durations = ['var(--jm-duration-1)', 'var(--jm-duration-2)', 'var(--jm-duration-3)', 'var(--jm-duration-5)']
const durationLabels = ['100ms 反馈', '200ms 过渡/退场', '300ms 进场', '500ms 大面积']
</script>

<template>
  <div class="motion">
    <div class="motion__head">
      <div>
        <p class="motion__title">缓动曲线</p>
        <p class="motion__sub">同一段位移、同样 700ms，只换曲线</p>
      </div>
      <button type="button" class="motion__replay" @click="replay++">重播</button>
    </div>

    <div :key="`c${replay}`" class="motion__list">
      <div v-for="c in curves" :key="c.label" class="motion__row">
        <div class="motion__meta">
          <strong>{{ c.label }}</strong>
          <code>{{ c.value }}</code>
        </div>
        <div class="motion__track">
          <span class="motion__dot" :style="{ '--ease': c.ease }" />
        </div>
        <span class="motion__use">{{ c.use }}</span>
      </div>
    </div>

    <div class="motion__head motion__head--gap">
      <div>
        <p class="motion__title">时长阶梯</p>
        <p class="motion__sub">同样标准曲线，只换时长</p>
      </div>
    </div>

    <div :key="`d${replay}`" class="motion__list">
      <div v-for="(d, i) in durations" :key="d" class="motion__row">
        <div class="motion__meta">
          <strong>{{ durationLabels[i] }}</strong>
          <code>--jm-duration-{{ [1, 2, 3, 5][i] }}</code>
        </div>
        <div class="motion__track">
          <span
            class="motion__dot motion__dot--bar"
            :style="{ '--ease': 'var(--jm-ease-standard)', '--dur': d }"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.motion {
  width: 100%;
  padding: 20px 22px 22px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg);
}

.motion__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.motion__head--gap {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px dashed var(--vp-c-divider);
}

.motion__title {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.motion__sub {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.motion__replay {
  flex: 0 0 auto;
  height: 28px;
  padding: 0 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font-size: 12px;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}

.motion__replay:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
}

.motion__list {
  margin-top: 14px;
}

.motion__row {
  display: grid;
  grid-template-columns: 210px 1fr 110px;
  align-items: center;
  gap: 14px;
  padding: 7px 0;
}

.motion__meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.motion__meta strong {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--vp-c-text-1);
}

.motion__meta code {
  font-size: 11px;
  color: var(--vp-c-text-3);
}

.motion__track {
  position: relative;
  height: 6px;
  border-radius: 999px;
  background: var(--vp-c-bg-soft);
}

.motion__dot {
  position: absolute;
  top: 50%;
  left: 0;
  width: 12px;
  height: 12px;
  margin-top: -6px;
  border-radius: 50%;
  background: var(--jm-color-primary, #00a0e9);
  box-shadow: 0 0 0 3px rgba(0, 160, 233, 0.16);
  animation: jm-demo-slide 700ms var(--ease) both;
}

.motion__dot--bar {
  width: 22px;
  margin-top: -6px;
  border-radius: 999px;
  animation: jm-demo-slide var(--dur) var(--ease) both;
}

.motion__use {
  font-size: 11.5px;
  color: var(--vp-c-text-3);
  text-align: right;
}

@keyframes jm-demo-slide {
  from {
    left: 0;
  }
  to {
    left: calc(100% - 12px);
  }
}

@media (max-width: 720px) {
  .motion__row {
    grid-template-columns: 130px 1fr;
  }

  .motion__use {
    display: none;
  }
}
</style>
