<script setup lang="ts">
import { ref } from 'vue'

const rate = ref(66)
const correct = ref(42)
const total = 60

function randomize() {
  rate.value = Math.round(Math.random() * 100)
  correct.value = Math.round(Math.random() * total)
}

const gradient = [
  { color: '#00A0E9', percentage: 0 },
  { color: '#1D9E75', percentage: 1 },
]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">基础</p>
    <div class="row">
      <jm-circle :percentage="rate" :size="100" />
      <jm-circle :percentage="rate" :size="100" color="#1D9E75" :stroke-width="6" />
      <jm-circle :percentage="rate" :size="100" color="#FF6430" clockwise :stroke-linecap="'butt'" />
    </div>
    <div class="actions">
      <jm-button size="small" type="primary" plain @click="randomize">随机换个值</jm-button>
    </div>

    <p class="demo-label">渐变 + 自定义中心内容</p>
    <div class="row">
      <jm-circle :percentage="(correct / total) * 100" :size="120" :color="gradient" :speed="800">
        <template #default>
          <div class="center">
            <span class="center__num">{{ correct }}/{{ total }}</span>
            <span class="center__label">答对题数</span>
          </div>
        </template>
      </jm-circle>

      <jm-circle
        :percentage="rate"
        :size="120"
        :stroke-width="10"
        color="#7C5CFC"
        :clockwise="false"
        text="学习进度"
        text-color="#7C5CFC"
      />
    </div>

    <p class="demo-label">尺寸与线宽</p>
    <div class="row">
      <jm-circle :percentage="30" :size="56" :stroke-width="5" />
      <jm-circle :percentage="55" :size="76" :stroke-width="7" color="#FFA940" />
      <jm-circle :percentage="80" :size="96" :stroke-width="9" color="#F5222D" />
    </div>
    <p class="demo-note">percentage 超出 0~100 会被收敛到边界，并在控制台给出提示。</p>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
}

.actions {
  margin-top: 10px;
}

.center {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
}

.center__num {
  font-size: 18px;
  font-weight: 600;
  color: var(--jm-text-color);
}

.center__label {
  margin-top: 2px;
  font-size: 11px;
  color: var(--jm-text-color-3);
}
</style>
