<script setup lang="ts">
import { computed, ref } from 'vue'

const grade = ref<string | number>('')
const subject = ref<string | number>('all')
const sort = ref<(string | number)[]>([])

const gradeOptions = [
  { text: '全部年级', value: '' },
  { text: '一年级', value: 1 },
  { text: '二年级', value: 2 },
  { text: '三年级', value: 3 },
  { text: '四年级', value: 4, disabled: true },
]

const subjectOptions = [
  { text: '全部科目', value: 'all' },
  { text: '语文', value: 'chinese' },
  { text: '数学', value: 'math' },
  { text: '英语', value: 'english' },
  { text: '科学', value: 'science' },
]

const sortOptions = [
  { text: '最近创建', value: 'created' },
  { text: '课时最多', value: 'lessons' },
  { text: '报名人数', value: 'students' },
]

const result = computed(() => {
  const g = grade.value === '' ? '全部年级' : `${grade.value} 年级`
  const s = subjectOptions.find((o) => o.value === subject.value)?.text ?? '全部科目'
  const st = sort.value.length
    ? sort.value
        .map((v) => sortOptions.find((o) => o.value === v)?.text)
        .filter(Boolean)
        .join('、')
    : '默认排序'
  return `${g} · ${s} · ${st}`
})

const tags = ref<string[]>(['语文'])
const allTags = ['语文', '数学', '英语', '物理', '化学', '生物']
function toggleTag(t: string) {
  tags.value = tags.value.includes(t) ? tags.value.filter((x) => x !== t) : [...tags.value, t]
}

function toggleSort(v: string | number) {
  sort.value = sort.value.includes(v) ? sort.value.filter((x) => x !== v) : [...sort.value, v]
}
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">单选 / 多选（自定义内容）</p>
    <div class="panel">
      <jm-dropdown-menu active-color="#00A0E9">
        <jm-dropdown-item v-model="grade" :options="gradeOptions" placeholder="年级" />
        <jm-dropdown-item v-model="subject" :options="subjectOptions" placeholder="科目" />
        <jm-dropdown-item v-model="sort" multiple placeholder="排序">
          <ul class="opts">
            <li
              v-for="o in sortOptions"
              :key="o.value"
              :class="{ active: sort.includes(o.value) }"
              @click="toggleSort(o.value)"
            >
              {{ o.text }}
            </li>
          </ul>
        </jm-dropdown-item>
      </jm-dropdown-menu>
    </div>
    <p class="demo-note">当前筛选：{{ result }}</p>

    <p class="demo-label">自定义面板（标签多选，关掉遮罩）</p>
    <div class="panel">
      <jm-dropdown-menu :overlay="false">
        <jm-dropdown-item :model-value="tags" :max-height="200" placeholder="兴趣标签">
          <div class="tags">
            <jm-tag
              v-for="t in allTags"
              :key="t"
              :plain="!tags.includes(t)"
              :type="tags.includes(t) ? 'primary' : 'default'"
              @click="toggleTag(t)"
            >{{ t }}</jm-tag>
          </div>
        </jm-dropdown-item>
      </jm-dropdown-menu>
    </div>
    <p class="demo-note">已选：{{ tags.join('、') || '无' }}</p>

    <p class="demo-label">禁用项</p>
    <div class="panel">
      <jm-dropdown-menu>
        <jm-dropdown-item disabled title="不可展开" />
        <jm-dropdown-item :options="gradeOptions" title="年级含禁用项" />
      </jm-dropdown-menu>
    </div>
  </div>
</template>

<style scoped>
.panel {
  border-radius: 12px;
  background: var(--jm-bg-container);
}

/* 面板和遮罩都挂在菜单栏外侧，容器不能 overflow:hidden，否则会被裁掉 */
.panel :deep(.jm-dropdown-menu__bar) {
  border-radius: 12px;
}

.opts {
  margin: 0;
  padding: 4px 0;
  list-style: none;
}

.opts li {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--jm-text-primary);
}

.opts li.active {
  color: var(--jm-color-primary);
  font-weight: 500;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 16px;
}

.tags .jm-tag {
  cursor: pointer;
}
</style>
