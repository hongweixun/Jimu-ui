<script setup lang="ts">
import { ref } from 'vue'
import type { CascadeOption } from 'jimu-ui'

const visible = ref(false)
const value = ref<(string | number)[]>(['zj', 'hz', 'xihu'])

const region: CascadeOption[] = [
  {
    text: '浙江省',
    value: 'zj',
    children: [
      {
        text: '杭州市',
        value: 'hz',
        children: [
          { text: '西湖区', value: 'xihu' },
          { text: '拱墅区', value: 'gongshu' },
          { text: '滨江区', value: 'binjiang' },
          { text: '余杭区', value: 'yuhang' },
        ],
      },
      {
        text: '宁波市',
        value: 'nb',
        children: [
          { text: '海曙区', value: 'haishu' },
          { text: '江北区', value: 'jiangbei' },
          { text: '鄞州区', value: 'yinzhou' },
        ],
      },
    ],
  },
  {
    text: '江苏省',
    value: 'js',
    children: [
      {
        text: '南京市',
        value: 'nj',
        children: [
          { text: '鼓楼区', value: 'gulou' },
          { text: '玄武区', value: 'xuanwu' },
        ],
      },
      {
        text: '苏州市',
        value: 'sz',
        children: [
          { text: '姑苏区', value: 'gusu' },
          { text: '工业园区', value: 'sip' },
        ],
      },
    ],
  },
]

function label(path: (string | number)[]) {
  const names: string[] = []
  let nodes = region
  for (const v of path) {
    const node = nodes.find((n) => n.value === v)
    if (!node) break
    names.push(node.text)
    nodes = node.children ?? []
  }
  return names.join(' / ') || '请选择'
}

const lastChange = ref('')
</script>

<template>
  <div class="demo-page">
    <jm-cell title="所在地区" :value="label(value)" is-link clickable @click="visible = true" />

    <jm-popup v-model:show="visible" position="bottom" round :safe-area="false" :teleport="false">
      <jm-cascade-picker
        v-model="value"
        :options="region"
        title="选择地区"
        @confirm="visible = false"
        @cancel="visible = false"
        @change="(p) => (lastChange = p.selectedValues.join('/'))"
      />
    </jm-popup>

    <p class="demo-note">
      选中值：{{ value.join(' / ') }}；最近一次 change：{{ lastChange || '—' }}
    </p>
    <p class="demo-note">
      换省后，市、区两列会自动重建并回到第一项——改上层就等于放弃下层已选内容。
    </p>

    <p class="demo-label">两级级联（分类 → 子类）</p>
    <jm-cascade-picker
      v-model="value"
      :options="region"
      :show-toolbar="false"
      :visible-count="3"
      :item-height="40"
    />
  </div>
</template>
