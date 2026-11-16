<script setup lang="ts">
const teachers = ['张老师', '李老师', '王老师', '赵老师', '周老师', '吴老师']

/** 用内联 SVG 当头像，避免文档离线时依赖外网图片 */
const avatar = (from: string, to: string) =>
  `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="96" height="96" fill="url(#g)"/><circle cx="48" cy="38" r="16" fill="#fff" opacity=".9"/><path d="M18 92c4-18 16-27 30-27s26 9 30 27z" fill="#fff" opacity=".9"/></svg>`,
  )}`

const broken = avatar('#c9ccd3', '#8f96a3')
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">尺寸与形状</p>
    <div class="row">
      <jm-avatar size="small" text="王" />
      <jm-avatar text="王" />
      <jm-avatar size="large" text="王" />
      <jm-avatar :size="64" text="王" />
      <jm-avatar shape="square" text="班" background="var(--jm-color-primary-light)" color="var(--jm-color-primary)" />
      <jm-avatar shape="square" :size="48" :radius="12" text="级" />
    </div>

    <p class="demo-label">图片头像 / 图标兜底</p>
    <div class="row">
      <jm-avatar :src="avatar('#7ec8f5', '#00A0E9')" alt="用户头像" />
      <jm-avatar :src="avatar('#a5d6a7', '#1D9E75')" size="large" alt="用户头像" />
      <jm-avatar icon="user" />
      <jm-avatar icon="graduation-cap" background="var(--jm-color-primary-light)" color="var(--jm-color-primary)" />
      <jm-avatar :src="broken" text="失" alt="加载失败会回退到文字" />
    </div>

    <p class="demo-label">头像组（max 折叠成 +N）</p>
    <div class="row">
      <jm-avatar-group :max="4" :total="teachers.length" :gap="26">
        <jm-avatar
          v-for="(t, i) in teachers"
          :key="t"
          :text="t.slice(0, 1)"
          :background="`hsl(${i * 48 + 190} 70% 92%)`"
          :color="`hsl(${i * 48 + 190} 55% 38%)`"
          shape="circle"
        />
      </jm-avatar-group>
    </div>

    <p class="demo-label">列表里带描述</p>
    <div class="list">
      <div v-for="(t, i) in teachers.slice(0, 3)" :key="t" class="list-row">
        <jm-avatar :text="t.slice(0, 1)" size="small" :background="`hsl(${i * 48 + 190} 70% 92%)`" :color="`hsl(${i * 48 + 190} 55% 38%)`" />
        <div class="meta">
          <p class="name">{{ t }}</p>
          <p class="desc">语文组 · 教龄 {{ 5 + i }} 年</p>
        </div>
        <jm-icon name="chevron-right" :size="16" color="var(--jm-text-tertiary)" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 0;
}

.list {
  overflow: hidden;
  border-radius: 12px;
  background: var(--jm-bg-container);
}

.list-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
}

.list-row + .list-row {
  border-top: 1px solid var(--jm-border-color);
}

.meta {
  flex: 1;
  min-width: 0;
}

.name {
  margin: 0;
  font-size: 14px;
  color: var(--jm-text-primary);
}

.desc {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--jm-text-tertiary);
}
</style>
