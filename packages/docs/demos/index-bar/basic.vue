<script setup lang="ts">
const groups = [
  { letter: 'A', people: ['安琪', '敖子逸'] },
  { letter: 'B', people: ['白露', '薄靳言', '毕方'] },
  { letter: 'C', people: ['蔡文姬', '曹禺', '陈景润', '程一帆'] },
  { letter: 'D', people: ['邓稼先', '丁一'] },
  { letter: 'F', people: ['范仲淹', '冯唐'] },
  { letter: 'G', people: ['高适', '顾城', '郭靖'] },
  { letter: 'H', people: ['韩愈', '胡适'] },
  { letter: 'J', people: ['贾岛', '金庸'] },
  { letter: 'L', people: ['李白', '李清照', '林徽因'] },
  { letter: 'M', people: ['孟子', '莫言'] },
  { letter: 'S', people: ['苏轼', '沈从文'] },
  { letter: 'W', people: ['王安石', '汪曾祺'] },
  { letter: 'Z', people: ['张岱', '朱自清'] },
]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">通讯录（右侧字母索引，点击或按住拖动定位）</p>
    <div id="idx-scroll" class="contact">
      <jm-index-bar scroll-container="#idx-scroll" highlight-color="#00A0E9">
        <jm-index-anchor v-for="g in groups" :key="g.letter" :index="g.letter">
          <jm-cell v-for="p in g.people" :key="p" :title="p" clickable>
            <template #icon>
              <span class="avatar">{{ p.slice(0, 1) }}</span>
            </template>
          </jm-cell>
        </jm-index-anchor>
      </jm-index-bar>
    </div>
    <p class="demo-note">分组标题会吸顶，索引条的当前字母跟随滚动高亮。</p>
  </div>
</template>

<style scoped>
.contact {
  height: 340px;
  overflow-y: auto;
  border-radius: 12px;
  background: var(--jm-bg-container);
  -webkit-overflow-scrolling: touch;
}

.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  margin-right: 10px;
  border-radius: 50%;
  background: var(--jm-color-primary-light);
  color: var(--jm-color-primary);
  font-size: 13px;
}
</style>
