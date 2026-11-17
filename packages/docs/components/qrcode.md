---
title: QRCode 二维码
description: 纯前端二维码生成，支持纠错级别、渐变色、圆点/圆角码点样式、中心 Logo、PNG 导出。
---

# QRCode 二维码

纯 TS 实现的二维码生成器（内置编码器，无第三方依赖）：版本 1~40 自动选型、字节模式（UTF-8 中文直出）、四种纠错级别、掩码按罚分自动择优。参照草料二维码常用的配置项，提供**码点样式、渐变前景色、中心 Logo** 等美化能力，内容变化实时重绘。

::: tip 正确性保障
编码器通过了两组验证：① jsQR 对 9 种长度（5~1200 字符、含中文/JSON）× 4 个纠错级别的解码回环 36/36；② 与 Nayuki QR-Code-generator 参考实现在全部版本 × 级别 × 8 种掩码下的逐模块矩阵比对完全一致。
:::

## 基础用法

<DemoBlock src="/demos/qrcode/basic.vue" title="实时生成 / 级别 / 样式 / 渐变 / Logo / 导出" desc="修改内容实时刷新；L/M/Q/H 对应 7%/15%/25%/30% 可纠正量；square/rounded/dots 三种码点；支持双色渐变与中心 Logo；ref.toDataURL 导出 PNG。" />

```vue
<jm-qrcode value="https://cli.im/" :size="180" />
```

## 纠错级别与 Logo

纠错级别越高，码点越密、抗遮挡越强。要放中心 Logo 请用 `H`（30% 可纠正），Logo 面积建议 ≤ 二维码的 1/5：

```vue
<jm-qrcode value="https://cli.im/" level="H" logo="/logo.png" :logo-width="0.22" :logo-radius="10" />
```

## 样式定制

| 能力 | 属性 |
| --- | --- |
| 码点形状 | `dot-style`：`square`（默认）/ `rounded` / `dots`，非 square 时定位图形自动换成圆角三层块 |
| 渐变前景 | `fg-color` + `fg-color2`（`gradient-direction` 控制方向） |
| 透明底 | `bg-color="transparent"` |
| 静区 | `margin`（模块数，默认 4，扫码器普遍要求 ≥ 4） |

## 导出

```ts
const qr = ref()
qr.value.toDataURL()      // 当前尺寸 PNG
qr.value.toDataURL(3)     // 3 倍放大导出（打印用）
```

## API

### Props

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 二维码内容 | `string` | - |
| size | 显示尺寸（CSS 像素，内部按 DPR 高清渲染） | `number` | `200` |
| level | 纠错级别 `L` `M` `Q` `H` | `string` | `'M'` |
| margin | 四周静区模块数 | `number` | `4` |
| fgColor | 前景色 | `string` | `'#000000'` |
| fgColor2 | 渐变第二色（不传则纯色） | `string` | - |
| gradientDirection | 渐变方向 `lt-br` `rt-bl` `top-bottom` `left-right` | `string` | `'lt-br'` |
| bgColor | 背景色，`transparent` 为透明底 | `string` | `'#ffffff'` |
| dotStyle | 码点样式 `square` `rounded` `dots` | `string` | `'square'` |
| logo | 中心 Logo 图片地址 | `string` | - |
| logoWidth | Logo 宽度占比 | `number` | `0.22` |
| logoRadius | Logo 圆角（px） | `number` | `8` |

### 方法

| 方法 | 说明 | 返回 |
| --- | --- | --- |
| toDataURL(scale?) | 导出 PNG，scale 放大倍数 | `string` |
