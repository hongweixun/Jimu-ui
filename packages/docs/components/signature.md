---
title: Signature 手写签名
description: Canvas 手写签名板，支持撤销、清空、透明底导出与空白裁剪，移动端书写不误触滚动。
---

# Signature 手写签名

家长签字、学员签到、合同确认——移动端绕不开「用手指写个字」。`jm-signature` 用 Canvas 承接手写笔迹，处理了三件容易出错的事：

1. **书写时页面不跟着滚**：Canvas 上 `touch-action: none`，手指落下后纵向滑动只画线，不会带动页面。
2. **高分屏不糊**：按 `devicePixelRatio` 放大位图再缩回 CSS 尺寸，笔迹边缘是清晰的。
3. **导出的是笔迹本身**：默认裁掉签名四周的空白，`png` 透明底，直接能贴进 PDF 或上传。

## 基础用法

<DemoBlock src="/demos/signature/basic.vue" title="书写、撤销、导出与只读回显" desc="松手后 v-model 拿到的是裁剪过的 dataURL。" />

```vue
<jm-signature v-model="value" :height="180" show-toolbar />

<jm-signature :model-value="value" :height="120" readonly />
```

`v-model` 绑定的是 `dataURL` 字符串，可以直接塞进表单、传给后端或存进 localStorage。空画布时值为 `''`，不会导出空白图。

## 撤销与清空

`show-toolbar` 打开内置工具栏（撤销 / 清空），按钮在无可撤销内容时自动置灰。工具栏不是必需——大多数场景希望按钮跟着业务按钮走，那就关掉它，用 ref 调方法：

```vue
<jm-signature ref="pad" v-model="value" />

<jm-button @click="pad.undo()">撤销</jm-button>
<jm-button @click="pad.clear()">重签</jm-button>
<jm-button type="primary" @click="submit(pad.toDataURL())">提交</jm-button>
```

| 方法 | 说明 |
| --- | --- |
| `clear()` | 清空画布，触发 `update:modelValue('')` 与 `clear` 事件 |
| `undo()` | 撤销上一笔，触发 `change` |
| `toDataURL(format?)` | 按当前 `trim` 设置导出，可临时指定 `'png' \| 'jpeg'` |
| `isEmpty()` | 是否没有任何笔迹（含未书写但已回显图片的情况） |

## 裁剪与格式

`trim`（默认 `true`）会按所有笔迹的包围盒裁掉四周留白，再留 `lineWidth + 4px` 的呼吸边。裁剪后的图宽高比就是笔迹本身的宽高比，贴到合同落款处不会出现一块大白底。

| 场景 | 建议 |
| --- | --- |
| 电子合同、审批单 | `format="png"` + `backgroundColor=""`（透明底） |
| 需要白底照片感 | 保持默认 `backgroundColor="#ffffff"` |
| 体积敏感 | `format="jpeg"`，质量固定 0.92 |

## 回显与只读

把之前存下的 `dataURL` 传回 `modelValue`，组件会按 contain 居中渲染到画布上；同时置 `readonly` 挡住书写。`readonly` 下仍允许从外部替换 `modelValue` 换图，只是不接受手指输入。

## 尺寸与适配

`height` 传数字按 px、传字符串按原样（如 `'40vh'`）。宽度始终撑满父容器。容器宽度变化时（横竖屏切换、侧边栏展开），已有笔迹会按比例缩放后重绘，不会跑位或丢失。

`lineWidth` 默认 3px，`penColor` 默认近黑 `#1f2937`——纯黑在手机上显得生硬。`maxStrokes`（默认 200）限制笔画总量，超出后丢弃最早的笔画，防止长时间涂写把内存吃满。

## 注意

- 画布是**位图**，导出后再放大就会糊。需要矢量签名的场景（如 PDF 矢量绘制）请自行解析笔迹，本组件不提供。
- iOS Safari 上，双指缩放会打断书写；如果页面本身允许缩放，建议在签名弹层打开期间锁滚动（`lockScroll`）。
- 未做手写轨迹压感/笔锋模拟，笔迹粗细恒定。

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| modelValue | 签名图 dataURL（`v-model`） | `string` | `''` |
| height | 画布高度，数字按 px | `number \| string` | `200` |
| penColor | 笔迹颜色 | `string` | `'#1f2937'` |
| lineWidth | 笔迹粗细（px） | `number` | `3` |
| backgroundColor | 画布底色，传 `''` 为透明 | `string` | `'#ffffff'` |
| readonly | 只读，不接受书写 | `boolean` | `false` |
| trim | 导出时裁剪四周空白 | `boolean` | `true` |
| format | 导出格式 | `'png' \| 'jpeg'` | `'png'` |
| maxStrokes | 笔画上限，超出丢弃最早的 | `number` | `200` |
| showToolbar | 显示内置撤销 / 清空工具栏 | `boolean` | `false` |
| placeholder | 空状态提示文字 | `string` | `'请在此处签名'` |
| undoText / clearText | 工具栏按钮文案 | `string` | `'撤销'` / `'清空'` |

### Events

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| update:modelValue | 笔迹变化后的 dataURL | `string` |
| change | 同上（撤销、落笔都会触发） | `string` |
| start | 落笔 | - |
| end | 抬笔 | - |
| clear | 清空 | - |

### 方法

见上文「撤销与清空」。所有方法通过组件 ref 调用。

## 无障碍

画布带 `role="img"` 与 `aria-label="手写签名画布"`，读屏能识别这是一个图像区域。手写本身对读屏用户不可用，业务侧应同时提供「上传已有签名图片」的替代路径；确认按钮不要做成「签完自动提交」，留一次显式确认。
