---
title: Scanner 扫描动效
description: AI 识图场景的「正在扫描」视觉：往复扫描线 + 四角取景框，拍完作业题正在 OCR、证件照核验都用得上。
---

# Scanner 扫描动效

AI 识别功能越来越多：拍作业题做 OCR、上传证件照做核验、扫动植物识别。这些场景有一个共同的"等待中的仪式感"——**一条亮线在画面里往复扫动**。它不是装饰：扫描线告诉用户"系统正在逐行读取你的图"，比转圈 spinner 更贴场景，等待焦虑明显更低。

识别逻辑（模型推理、结果回调）留在业务侧，`Scanner` 只负责"现在扫到哪了"的视觉——它覆盖在任意内容上：`img`、`canvas`、相机取景框都行。

## 基础用法

<DemoBlock src="/demos/scanner/basic.vue" title="扫描线 + 取景框" desc="默认主色扫描线；绿色自定义；顶部按钮控制 active 开关。" />

```vue
<template>
  <jm-scanner :active="scanning" :height="190">
    <img :src="image" alt="待识别内容" />
  </jm-scanner>
</template>

<script setup>
import { ref } from 'vue'
const scanning = ref(true)   // 识别完成后置 false，扫描线淡出
const image = ref('')
</script>
```

## Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| active | 是否扫描中；false 时扫描线淡出停止 | `boolean` | `true` |
| duration | 单次扫描时长（ms），线往返一次 | `number` | `1800` |
| line-color | 扫描线颜色 | `string` | 主色 |
| line-width | 扫描线厚度（数字按 px） | `number \| string` | `2` |
| corners | 显示四角取景框 | `boolean` | `true` |
| corner-color | 角标颜色 | `string` | 主色 |
| corner-size | 角标边长（数字按 px） | `number \| string` | `22` |
| corner-width | 角标粗细（数字按 px） | `number \| string` | `3` |
| radius | 容器圆角 | `number \| string` | `12` |
| show-grid | 显示斜向网格暗纹 | `boolean` | `false` |
| height | 容器最小高度（数字按 px） | `number \| string` | `200` |

::: tip 什么时候关掉 active
拿到识别结果、或进入人工确认页时置 `false`——扫描线 0.3s 淡出，比直接卸载组件多一层"扫描结束"的收尾感。长耗时识别建议配合[进度类反馈](/components/progress)在框下补一行百分比文案。
:::

## 内容与分层

默认插槽是**被扫描的内容**（图片 / 相机画面 / canvas），覆盖层依次是：网格暗纹（可选）→ 四角取景框 → 扫描线 → 右下角「扫描中…」状态胶囊。所有覆盖层 `pointer-events: none`，不挡内容的点击。

不传内容时渲染深色底 + 占位文案，适合"还没拍照先给个取景框"的初始态。

## 动效降级

与其他组件一致：`data-motion="off"` 或系统"减少动效"开启时，扫描线**停在中线不动**（不再是转圈动画），取景框与状态胶囊保留——功能语义还在，只是不晃眼。

## 配合 Uploader

识别场景常见链路：`Uploader` 传图 → 上传完成后把返回的图片地址交给 `Scanner` 扫描 → 结果页。两者职责互补：Uploader 管"文件列表与上传状态"，Scanner 管"识别中的取景与动效"。
