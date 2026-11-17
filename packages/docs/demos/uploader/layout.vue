<script setup lang="ts">
import { ref } from 'vue'
import type { UploaderFile } from 'jimu-ui'

function svg(text: string, from: string, to: string, w = 300, h = 400) {
  const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${from}"/><stop offset="1" stop-color="${to}"/></linearGradient></defs><rect width="${w}" height="${h}" fill="url(#g)"/><text x="50%" y="52%" font-family="system-ui,-apple-system,sans-serif" font-size="22" fill="#fff" text-anchor="middle" dominant-baseline="middle">${text}</text></svg>`
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(raw)
}

/* 寸照比例：3:4 */
const portrait = ref<(string | UploaderFile)[]>([svg('寸照 3:4', '#00A0E9', '#2B6BE4')])

/* 宽屏比例：16:9 横图 */
const wide = ref<(string | UploaderFile)[]>([svg('横图 16:9', '#22C55E', '#0E9F6E', 400, 225)])

/* 附件列表：文件对象带名称与大小 */
const attachments = ref<(string | UploaderFile)[]>([
  { name: '体检报告.pdf', size: 834211 },
  { url: svg('IMG_0219', '#7C5CFF', '#5C3BE4', 300, 300), name: 'IMG_0219.jpg', size: 152043 },
])
const tip = ref('')
</script>

<template>
  <div class="demo-page">
    <div class="panes">
      <section class="pane">
        <h4 class="pane-title">grid + ratio="3:4"（寸照比例）</h4>
        <jm-uploader v-model="portrait" :columns="3" size="76" ratio="3:4" upload-text="寸照" />
        <p class="pane-sub">正方形之外，格子里也能装下竖版内容</p>
      </section>

      <section class="pane">
        <h4 class="pane-title">grid + ratio="16:9"</h4>
        <jm-uploader v-model="wide" :columns="2" size="120" radius="10" ratio="16:9" upload-text="横图" />
        <p class="pane-sub">同款格子，比例随内容走</p>
      </section>

      <section class="pane pane--wide">
        <h4 class="pane-title">layout="list"（附件列表）</h4>
        <jm-uploader
          v-model="attachments"
          layout="list"
          upload-text="上传附件"
          max-count="5"
          @delete="() => (tip = '已删除一个附件')"
        />
        <p class="pane-sub">文字性的上传 / 删除 / 计数，适合文档类作业材料</p>
        <p v-if="tip" class="demo-tip">{{ tip }}</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.demo-page {
  max-width: 720px;
  margin: 0 auto;
}

.panes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.pane {
  min-width: 0;
  padding: 14px;
  border-radius: 12px;
  background: var(--jm-bg-container);
  border: 1px solid var(--jm-border-color);
}

.pane--wide {
  grid-column: 1 / -1;
}

.pane-title {
  margin: 0 0 10px;
  font-size: 13px;
  color: var(--jm-text-color-3);
  font-weight: 600;
}

.pane-sub {
  margin-top: 8px;
  font-size: 12px;
  color: var(--jm-text-color-4);
}

.demo-tip {
  margin-top: 8px;
  font-size: 12px;
  color: var(--jm-color-primary-text);
}
</style>
