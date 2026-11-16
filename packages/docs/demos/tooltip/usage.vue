<script setup lang="ts">
const rows = [
  { label: '计费方式', value: '按量计费', tip: '按实际调用次数计费，每小时结算一次，不足 1 分钱的部分累计到下个周期。' },
  { label: '免费额度', value: '1000 次 / 月', tip: '每月 1 号重置，个人开发者与企业账号共享同一份额度。' },
  { label: '超限策略', value: '自动降级', tip: '超出额度后接口返回缓存结果，不会直接报错。恢复额度后自动切回实时计算。' },
]
</script>

<template>
  <div class="demo-page">
    <p class="demo-label">字段名旁边的信息图标：长按（移动端）或鼠标移上去看解释</p>
    <jm-descriptions border>
      <jm-descriptions-item v-for="r in rows" :key="r.label" :label="r.label">
        {{ r.value }}
        <jm-tooltip :content="r.tip" trigger="longpress" :max-width="200" theme="light">
          <jm-icon name="info" class="hint" />
        </jm-tooltip>
      </jm-descriptions-item>
    </jm-descriptions>

    <p class="demo-label">操作被禁用时说明原因，比灰掉一个按钮更有用</p>
    <jm-tooltip content="本月已修改过 3 次，下月 1 号后可再次修改" placement="bottom">
      <span class="disabled-wrap">
        <jm-button size="small" disabled>修改绑定手机</jm-button>
      </span>
    </jm-tooltip>
  </div>
</template>

<style scoped>
.demo-page > * + * {
  margin-top: 16px;
}

.hint {
  margin-left: 3px;
  color: var(--jm-text-color-3);
  font-size: 14px;
  vertical-align: -2px;
}

/* 禁用元素在部分浏览器上不派发鼠标事件，用外层包一层接住 */
.disabled-wrap {
  display: inline-flex;
}
</style>
