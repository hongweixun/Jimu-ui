---
title: Uploader 上传
description: 图片选择、缩略图网格、数量与体积限制、删除与放大预览。
---

# Uploader 上传

只负责「选文件 + 展示 + 删除」，**不发请求**。上传时机由业务决定（选完就传、提交时统一传），因此 `change` 里拿到的每个对象都带着原始 `File`。

## 基础用法

<DemoBlock src="/demos/uploader/basic.vue" title="多选、限制数量与体积、只读、三列大图" desc="max-count 限制数量，max-size 限制单张体积；exceed / oversize 分别派发；readonly 只展示不可增删。" />

## 图片压缩

移动端拍照动辄 3~5MB，选择后先在端上压一遍能显著省流量。`compress` 开启后用 canvas 重绘：长边压到 `compress-max-size`（默认 1280px）、质量 `compress-quality`（默认 0.8）；png 保留透明通道，gif / svg 不压缩。压完体积反而变大时自动回退原图，`file` 字段指向压缩后的文件：

<DemoBlock src="/demos/uploader/compress.vue" title="自动压缩开关" desc="开关切到开，选完图立即可在 file 里看到压缩后的体积；压缩失败不拦截，回退原文件。" />

## 拖拽排序

`sortable` 开启长按排序：长按 420ms 抬起（放大 + 投影），拖动时其他格子实时让位，松手落位并把新顺序通过 `change` 派发。拖拽期间锁住页面滚动，拖完的这一次点击不会误开预览：

<DemoBlock src="/demos/uploader/sortable.vue" title="长按拖拽排序" desc="长按任意缩略图抬起拖动，其他格子实时让位；松手后下方实时显示当前顺序。" />

## 数据流

```
用户选择 → 校验数量 → 校验体积 → 生成 blob 预览地址 → emit update:modelValue
```

- 列表元素既可以是字符串（已有图片的 URL），也可以是对象 `{ url, name, status, file }`；
- 新选文件的 `url` 是 `URL.createObjectURL` 生成的 blob 地址，删除或组件卸载时会 `revokeObjectURL`，不会泄漏；
- 上传过程中的进度由业务把 `status` 改成 `'uploading'` 展示（左下角会出现「上传中」条）。

## 校验与反馈

| 情况 | 行为 |
| --- | --- |
| 超出 `max-count` | 只接收剩余名额，多余的通过 `exceed` 派发 |
| 超出 `max-size` | 该文件被跳过，通过 `oversize` 派发 |
| `disabled` | 不显示添加按钮，也不能删除 |
| `readonly` | 同上，但保留缩略图（用于「仅查看」场景） |

组件本身不弹提示，`oversize` / `exceed` 交给业务用 Toast 或内联文案表达——这类提示的措辞因项目而异，内置反而限制表达。

## 上传进度与失败重试

<DemoBlock src="/demos/uploader/upload.vue" title="自动上传、进度环与失败重试" desc="文件名带 fail 的文件第一次会失败，点重试即可重传成功。" />

传一个 `upload` 函数，组件就接管「上传中 / 成功 / 失败」三态：格子盖上进度环和百分比，完成后自动摘掉；失败盖上红色「重试」，点一下用同一个 File 重传。

```vue
<script setup>
async function upload(file, { onProgress }) {
  const form = new FormData()
  form.append('file', file)
  // 用 XHR 才能拿到进度，fetch 没有上传进度事件
  return await new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api/upload')
    xhr.upload.onprogress = (e) => onProgress((e.loaded / e.total) * 100)
    xhr.onload = () => (xhr.status === 200 ? resolve(xhr.responseText) : reject(new Error('上传失败')))
    xhr.onerror = () => reject(new Error('网络异常'))
    xhr.send(form)
  })
}
</script>

<jm-uploader v-model="files" :upload="upload" @success="onSuccess" @error="onError" />
```

`upload` 返回远程地址（字符串）时，列表里的本地 blob 预览会替换成远程图，同时回收 blob；返回空则保留本地预览。抛错即进入失败态，`error` 事件带上原始错误。

**手动上传**：`auto-upload="false"` 时选完只挂「待上传」角标，等业务调用 `submit()` 再统一提交——适合作业提交页这种「先攒图、最后一起交」的场景。

```vue
<jm-uploader ref="uploaderRef" v-model="files" :upload="upload" :auto-upload="false" />
<jm-button @click="uploaderRef.submit()">提交作业</jm-button>
```

进度百分比不会每帧 emit（避免父组件高频重渲染），只在 `progress` 事件里按整数变化回调一次。

## 预览

默认点击缩略图打开内置放大预览（基于 `Popup`）。文档示例传了 `:preview-teleport="false"` 让弹层留在手机框内；真实项目默认挂到 body 即可。需要接自己的图片查看器时，关掉 `preview-image` 并监听 `click-preview`。

## 自定义格子比例

`ratio` 控制格子的宽高比——不只是正方形：寸照用 `'3:4'`，横图用 `'16:9'`，数字表示宽/高比（`0.75` 等价 `'3:4'`）。配合 `columns` / `size` / `radius` 可以拼出任何版式。

## 附件列表布局

`layout="list"` 把九宫格换成**附件列表**：文字性的「上传附件」按钮、每行文件名 + 大小 + 状态（上传中百分比 / 失败重试 / 待上传）+ 删除按钮，标题行显示计数。文档类作业材料、报销凭证这类"要的是清单不是照片墙"的场景更清爽。

<DemoBlock src="/demos/uploader/layout.vue" title="三种形态平铺对比（不在手机框内）" desc="寸照 3:4、横图 16:9、附件列表——同一格子系统，比例与布局随内容走。" :phone="false" />

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 文件列表 | `(string \| UploaderFile)[]` | `[]` |
| max-count | 最多上传数量 | `number` | `9` |
| multiple | 允许一次选多个 | `boolean` | `false` |
| accept | input 的 accept | `string` | `'image/*'` |
| max-size | 单文件体积上限（字节），0 不限制 | `number` | `0` |
| compress | 选中后自动压缩图片 | `boolean` | `false` |
| compress-quality | 压缩质量 0~1（png 除外） | `number` | `0.8` |
| compress-max-size | 压缩后长边上限（像素） | `number` | `1280` |
| capture | 调起相机 `user` / `environment` | `string` | — |
| disabled | 禁用 | `boolean` | `false` |
| readonly | 只读（保留缩略图） | `boolean` | `false` |
| deletable | 显示删除按钮 | `boolean` | `true` |
| preview-image | 点击缩略图放大预览 | `boolean` | `true` |
| upload-text | 上传区文案（list 布局为按钮文案） | `string` | `'上传'` |
| columns | 每行列数（grid 布局） | `number` | `4` |
| size | 格子尺寸（grid 布局） | `number \| string` | `80` |
| ratio | 格子宽高比：`'1:1'` / `'3:4'` / `'16:9'` / 数字（宽/高） | `number \| string` | `'1:1'` |
| layout | 布局 `'grid'` 九宫格 / `'list'` 附件列表 | `string` | `'grid'` |
| show-count | 显示计数（list 布局标题行） | `boolean` | `true` |
| count-text | 计数文案前缀 | `string` | `'已传'` |
| radius | 格子圆角 | `number \| string` | `var(--jm-radius-md)` |
| sortable | 开启长按拖拽排序（仅 grid） | `boolean` | `false` |
| name | input 的 name | `string` | `'file'` |
| preview-teleport | 预览弹层挂载位置 | `boolean \| string \| Element` | `true` |
| upload | 自定义上传函数 | `(file, { onProgress }) => Promise<string \| void>` | — |
| auto-upload | 选完立即上传，false 时需手动 `submit()` | `boolean` | `true` |
| pending-text | 待上传角标文案 | `string` | `'待上传'` |
| retry-text | 失败重试文案 | `string` | `'重试'` |

### Events

| 事件 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 文件列表变化 | `files` |
| change | 同上，语义化别名 | `files` |
| exceed | 超出数量上限 | `files: File[]` |
| oversize | 超出体积上限 | `files: File[]` |
| delete | 删除某项 | `(file, index)` |
| click-preview | 点击缩略图 | `(file, index)` |
| click-upload | 点击添加按钮 | — |
| success | 单个文件上传成功 | `(file, index)` |
| error | 单个文件上传失败 | `(file, index, reason)` |
| progress | 上传进度变化 | `(percent, index)` |

### 方法

| 方法 | 说明 |
| --- | --- |
| submit() | 提交所有「待上传 / 失败」的文件（`auto-upload=false` 时用） |
| retry(index) | 重试指定下标的失败项 |

### Slots

| 名称 | 说明 |
| --- | --- |
| upload | 自定义添加按钮内容 |
