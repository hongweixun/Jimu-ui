<script setup lang="ts">
const cells = [
  { span: 24, text: 'span 24' },
  { span: 12, text: 'span 12' },
  { span: 12, text: 'span 12' },
  { span: 8, text: 'span 8' },
  { span: 8, text: 'span 8' },
  { span: 8, text: 'span 8' },
]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">24 栅格 + 12px 横向间距</p>
    <jm-row :gutter="12">
      <jm-col v-for="(c, i) in cells" :key="i" :span="c.span">
        <div class="cell">{{ c.text }}</div>
      </jm-col>
    </jm-row>

    <p class="demo-label">纵向间距 gutter=[12, 10]</p>
    <jm-row :gutter="[12, 10]">
      <jm-col v-for="n in 4" :key="n" :span="12">
        <div class="cell">{{ n }}</div>
      </jm-col>
    </jm-row>

    <p class="demo-label">偏移 offset + 垂直居中</p>
    <jm-row :gutter="8" align="middle">
      <jm-col :span="6">
        <div class="cell">6</div>
      </jm-col>
      <jm-col :span="6" :offset="6">
        <div class="cell">6 offset 6</div>
      </jm-col>
    </jm-row>

    <p class="demo-label">主轴分布 justify</p>
    <jm-row justify="between" class="tall">
      <jm-col :span="6"><div class="cell">A</div></jm-col>
      <jm-col :span="6"><div class="cell">B</div></jm-col>
      <jm-col :span="6"><div class="cell">C</div></jm-col>
    </jm-row>
  </div>
</template>

<style scoped>
.cell {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  border-radius: 8px;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 12px;
}

.tall {
  height: 120px;
  padding: 12px 0;
  border-radius: 12px;
  background: var(--jm-bg-container);
}

.jm-col + .jm-col .cell {
  margin-top: 0;
}

.jm-row + .jm-row {
  margin-top: 4px;
}
</style>
