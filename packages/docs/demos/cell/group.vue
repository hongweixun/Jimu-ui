<template>
  <div class="demo-page">
    <jm-cell-group title="卡片式（默认 inset）" :radius="14">
      <jm-cell title="课程名称" value="高一数学 · 函数专题" is-link size="large" />
      <jm-cell title="开课时间" value="每周三 19:00" />
      <jm-cell title="剩余名额" value="12 / 40" label="报名从速" />
    </jm-cell-group>

    <jm-cell-group title="通栏 + 自定义底色" :inset="false">
      <jm-cell title="我的订单" is-link background="var(--jm-bg-container)" />
      <jm-cell title="优惠券" value="3 张可用" is-link background="var(--jm-bg-container)" />
    </jm-cell-group>

    <jm-cell-group title="无分隔线、自定义圆角" :inset="false" :radius="0">
      <jm-cell title="学习报告" value="本周 4.5 小时" is-link :border="false" />
    </jm-cell-group>

    <p class="demo-note">CellGroup 负责圆角、底色与分割线，Cell 只负责单行布局。</p>
  </div>
</template>
