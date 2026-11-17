/**
 * 二维码编码器（字节模式 UTF-8，版本 1~40 自动选型，掩码按罚分自动择优）
 * 规格：ISO/IEC 18004。算法结构与 Nayuki QR-Code-generator 一致，
 * 宿主组件据此绘制，可自定义码点样式 / 渐变 / Logo。
 */

export type QrEccLevel = 'L' | 'M' | 'Q' | 'H'

// 每个版本、每个纠错级别的：每个块纠错码字数 / 块数
// prettier-ignore
const ECC_CODEWORDS_PER_BLOCK: Record<QrEccLevel, readonly number[]> = {
  L: [-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
  M: [-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
  Q: [-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
  H: [-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
}
// prettier-ignore
const NUM_ECC_BLOCKS: Record<QrEccLevel, readonly number[]> = {
  L: [-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
  M: [-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
  Q: [-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],
  H: [-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81],
}

const ECL_FORMAT_BITS: Record<QrEccLevel, number> = { L: 1, M: 0, Q: 3, H: 2 }

/* ---------- GF(256) 运算（本原多项式 0x11d） ---------- */
function gfMul(x: number, y: number): number {
  let z = 0
  for (let i = 7; i >= 0; i--) {
    z = (z << 1) ^ ((z >>> 7) * 0x11d)
    z ^= ((y >>> i) & 1) * x
  }
  return z & 0xff
}

/** RS 生成多项式，系数从高次到低次存储，不含恒为 1 的首项（共 degree 项） */
function rsDivisor(degree: number): number[] {
  const result: number[] = new Array(degree - 1).fill(0)
  result.push(1)
  let root = 1
  for (let i = 0; i < degree; i++) {
    for (let j = 0; j < result.length; j++) {
      result[j] = gfMul(result[j], root)
      if (j + 1 < result.length) result[j] ^= result[j + 1]
    }
    root = gfMul(root, 0x02)
  }
  return result
}

function rsRemainder(data: Uint8Array, divisor: readonly number[]): number[] {
  const result = new Array<number>(divisor.length).fill(0)
  for (const b of data) {
    const factor = b ^ result.shift()!
    result.push(0)
    for (let i = 0; i < divisor.length; i++) result[i] ^= gfMul(divisor[i], factor)
  }
  return result
}

/* ---------- 容量与结构 ---------- */
function getNumRawDataModules(ver: number): number {
  let result = (16 * ver + 128) * ver + 64
  if (ver >= 2) {
    const numAlign = Math.floor(ver / 7) + 2
    result -= (25 * numAlign - 10) * numAlign - 55
    if (ver >= 7) result -= 36
  }
  return result
}

function getNumDataCodewords(ver: number, ecl: QrEccLevel): number {
  return Math.floor(getNumRawDataModules(ver) / 8) - ECC_CODEWORDS_PER_BLOCK[ecl][ver] * NUM_ECC_BLOCKS[ecl][ver]
}

function alignmentPositions(ver: number, size: number): number[] {
  if (ver === 1) return []
  const numAlign = Math.floor(ver / 7) + 2
  const step = Math.floor((ver * 8 + numAlign * 3 + 5) / (numAlign * 4 - 4)) * 2
  const result: number[] = [6]
  for (let pos = size - 7; result.length < numAlign; pos -= step) result.splice(1, 0, pos)
  return result
}

/* ---------- 矩阵 ---------- */
interface QrMatrix {
  size: number
  modules: Uint8Array[]
  isFunction: Uint8Array[]
}

const MASK_FUNCTIONS: Array<(x: number, y: number) => boolean> = [
  (x, y) => (x + y) % 2 === 0,
  (_x, y) => y % 2 === 0,
  (x, _y) => x % 3 === 0,
  (x, y) => (x + y) % 3 === 0,
  (x, y) => (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0,
  (x, y) => ((x * y) % 2) + ((x * y) % 3) === 0,
  (x, y) => (((x * y) % 2) + ((x * y) % 3)) % 2 === 0,
  (x, y) => (((x + y) % 2) + ((x * y) % 3)) % 2 === 0,
]

function makeMatrix(ver: number, ecl: QrEccLevel, dataCodewords: Uint8Array, mask: number): QrMatrix {
  const size = ver * 4 + 17
  const modules: Uint8Array[] = []
  const isFunction: Uint8Array[] = []
  for (let i = 0; i < size; i++) {
    modules.push(new Uint8Array(size))
    isFunction.push(new Uint8Array(size))
  }

  function setFunction(x: number, y: number, isDark: boolean) {
    modules[y][x] = isDark ? 1 : 0
    isFunction[y][x] = 1
  }

  // 定位图形（3 个角）
  function drawFinder(cx: number, cy: number) {
    for (let dy = -4; dy <= 4; dy++) {
      for (let dx = -4; dx <= 4; dx++) {
        const dist = Math.max(Math.abs(dx), Math.abs(dy))
        const x = cx + dx
        const y = cy + dy
        if (x >= 0 && x < size && y >= 0 && y < size) setFunction(x, y, dist !== 2 && dist !== 4)
      }
    }
  }
  drawFinder(3, 3)
  drawFinder(size - 4, 3)
  drawFinder(3, size - 4)

  // 时序图形
  for (let i = 8; i < size - 8; i++) {
    const dark = i % 2 === 0
    if (!isFunction[6][i]) setFunction(i, 6, dark)
    if (!isFunction[i][6]) setFunction(6, i, dark)
  }

  // 校正图形
  const align = alignmentPositions(ver, size)
  for (const cx of align) {
    for (const cy of align) {
      if ((cx === 6 && cy === 6) || (cx === 6 && cy === size - 7) || (cx === size - 7 && cy === 6)) continue
      for (let dy = -2; dy <= 2; dy++) {
        for (let dx = -2; dx <= 2; dx++) {
          const dist = Math.max(Math.abs(dx), Math.abs(dy))
          setFunction(cx + dx, cy + dy, dist !== 1)
        }
      }
    }
  }

  // 版本信息
  if (ver >= 7) {
    let rem = ver
    for (let i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25)
    const bits = (ver << 12) | rem
    for (let i = 0; i < 18; i++) {
      const bit = ((bits >>> i) & 1) === 1
      const a = size - 11 + (i % 3)
      const b = Math.floor(i / 3)
      setFunction(a, b, bit)
      setFunction(b, a, bit)
    }
  }

  // 格式信息
  const data = (ECL_FORMAT_BITS[ecl] << 3) | mask
  let rem = data
  for (let i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537)
  const fmtBits = ((data << 10) | rem) ^ 0x5412

  for (let i = 0; i <= 5; i++) setFunction(8, i, ((fmtBits >>> i) & 1) === 1)
  setFunction(8, 7, ((fmtBits >>> 6) & 1) === 1)
  setFunction(8, 8, ((fmtBits >>> 7) & 1) === 1)
  setFunction(7, 8, ((fmtBits >>> 8) & 1) === 1)
  for (let i = 9; i < 15; i++) setFunction(14 - i, 8, ((fmtBits >>> i) & 1) === 1)
  for (let i = 0; i < 8; i++) setFunction(size - 1 - i, 8, ((fmtBits >>> i) & 1) === 1)
  for (let i = 8; i < 15; i++) setFunction(8, size - 15 + i, ((fmtBits >>> i) & 1) === 1)
  setFunction(8, size - 8, true) // 常亮模块（左下格式区上方，ISO 规定 col=8）

  // 数据放置（之字形，右下开始向上）
  let bitIndex = 0
  for (let right = size - 1; right >= 1; right -= 2) {
    if (right === 6) right = 5
    for (let vert = 0; vert < size; vert++) {
      for (let j = 0; j < 2; j++) {
        const x = right - j
        const upward = ((right + 1) & 2) === 0
        const y = upward ? size - 1 - vert : vert
        if (!isFunction[y][x] && bitIndex < dataCodewords.length * 8) {
          modules[y][x] = ((dataCodewords[bitIndex >>> 3] >>> (7 - (bitIndex & 7))) & 1) === 1 ? 1 : 0
          bitIndex++
        }
      }
    }
  }

  // 掩码
  const maskFn = MASK_FUNCTIONS[mask]
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (!isFunction[y][x] && maskFn(x, y)) modules[y][x] ^= 1
    }
  }

  return { size, modules, isFunction }
}

/** 掩码罚分评估（ISO 规则 1~4） */
function penaltyScore(m: QrMatrix): number {
  const size = m.size
  let result = 0

  // 规则 1：同色连续段
  for (let y = 0; y < size; y++) {
    let runColor = m.modules[y][0]
    let runLen = 1
    for (let x = 1; x < size; x++) {
      if (m.modules[y][x] === runColor) {
        runLen++
        if (runLen === 5) result += 3
        else if (runLen > 5) result++
      } else {
        runColor = m.modules[y][x]
        runLen = 1
      }
    }
  }
  for (let x = 0; x < size; x++) {
    let runColor = m.modules[0][x]
    let runLen = 1
    for (let y = 1; y < size; y++) {
      if (m.modules[y][x] === runColor) {
        runLen++
        if (runLen === 5) result += 3
        else if (runLen > 5) result++
      } else {
        runColor = m.modules[y][x]
        runLen = 1
      }
    }
  }

  // 规则 2：2x2 同色块
  for (let y = 0; y < size - 1; y++) {
    for (let x = 0; x < size - 1; x++) {
      const c = m.modules[y][x]
      if (c === m.modules[y][x + 1] && c === m.modules[y + 1][x] && c === m.modules[y + 1][x + 1]) result += 3
    }
  }

  // 规则 3：1:1:3:1:1 特征
  const pattern = [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
  const matches = (get: (i: number) => number) => {
    for (let i = 0; i < 11; i++) if (get(i) !== pattern[i]) return false
    return true
  }
  for (let y = 0; y < size; y++) {
    for (let x = 0; x <= size - 11; x++) {
      if (matches((i) => m.modules[y][x + i])) result += 40
      if (matches((i) => m.modules[x + i][y])) result += 40
    }
  }

  // 规则 4：暗模块占比
  let dark = 0
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) dark += m.modules[y][x]
  const k = Math.ceil(Math.abs((dark * 20) / (size * size) - 10))
  result += k * 10

  return result
}

export interface QrEncodeResult {
  size: number
  /** true 为暗模块 */
  get: (x: number, y: number) => boolean
  version: number
}

const encodeCache = new Map<string, QrEncodeResult>()

export function encodeQRCode(text: string, ecl: QrEccLevel = 'M'): QrEncodeResult {
  const cacheKey = `${ecl}\n${text}`
  const cached = encodeCache.get(cacheKey)
  if (cached) return cached

  const bytes = new TextEncoder().encode(text)

  // 自动选版本
  let ver = 0
  for (let v = 1; v <= 40; v++) {
    const usedBits = 4 + (v <= 9 ? 8 : 16) + bytes.length * 8
    if (usedBits <= getNumDataCodewords(v, ecl) * 8) {
      ver = v
      break
    }
  }
  if (!ver) throw new Error('[QRCode] 内容太长，即使最高纠错容量的版本也放不下')

  const capBits = getNumDataCodewords(ver, ecl) * 8

  // 位流：模式 + 字符数 + 数据 + 终止符 + 对齐 + 补齐字节
  const bits: number[] = []
  const push = (value: number, len: number) => {
    for (let i = len - 1; i >= 0; i--) bits.push((value >>> i) & 1)
  }
  push(4, 4) // byte mode
  push(bytes.length, ver <= 9 ? 8 : 16)
  for (const b of bytes) push(b, 8)

  push(0, Math.min(4, capBits - bits.length)) // 终止符
  while (bits.length % 8 !== 0) bits.push(0) // 字节对齐
  for (let i = 0; bits.length < capBits; i++) {
    const pad = i % 2 === 0 ? 0xec : 0x11
    for (let j = 7; j >= 0 && bits.length < capBits; j--) bits.push((pad >>> j) & 1)
  }

  const codewordCount = capBits / 8
  const codewords = new Uint8Array(codewordCount)
  for (let i = 0; i < codewordCount; i++) {
    let byte = 0
    for (let j = 0; j < 8; j++) byte = (byte << 1) | bits[i * 8 + j]
    codewords[i] = byte
  }

  // 分块 + 纠错 + 交错
  const numBlocks = NUM_ECC_BLOCKS[ecl][ver]
  const eccLen = ECC_CODEWORDS_PER_BLOCK[ecl][ver]
  const rawCodewords = Math.floor(getNumRawDataModules(ver) / 8)
  const shortBlockLen = Math.floor(rawCodewords / numBlocks)
  const numShortBlocks = numBlocks - (rawCodewords % numBlocks)

  const blocks: Uint8Array[] = []
  const eccBlocks: number[][] = []
  for (let i = 0, k = 0; i < numBlocks; i++) {
    const datLen = shortBlockLen - eccLen + (i < numShortBlocks ? 0 : 1)
    const dat = codewords.slice(k, k + datLen)
    k += datLen
    blocks.push(dat)
    eccBlocks.push(rsRemainder(dat, rsDivisor(eccLen)))
  }

  const interleaved = new Uint8Array(rawCodewords)
  let ik = 0
  for (let i = 0; i < shortBlockLen - eccLen + 1; i++) {
    for (let b = 0; b < numBlocks; b++) {
      if (i < blocks[b].length) interleaved[ik++] = blocks[b][i]
    }
  }
  for (let i = 0; i < eccLen; i++) {
    for (let b = 0; b < numBlocks; b++) interleaved[ik++] = eccBlocks[b][i]
  }

  // 掩码择优
  let bestMask = 0
  let bestScore = Infinity
  let bestMatrix: QrMatrix | null = null
  for (let m = 0; m < 8; m++) {
    const mat = makeMatrix(ver, ecl, interleaved, m)
    const score = penaltyScore(mat)
    if (score < bestScore) {
      bestScore = score
      bestMatrix = mat
      bestMask = m
    }
  }
  void bestMask

  const result: QrEncodeResult = {
    size: bestMatrix!.size,
    get: (x, y) => bestMatrix!.modules[y][x] === 1,
    version: ver,
  }
  if (encodeCache.size > 50) encodeCache.clear()
  encodeCache.set(cacheKey, result)
  return result
}

/** @internal 仅供本地验证使用 */
export function __debugMatrix(text: string, ecl: QrEccLevel, mask: number): QrEncodeResult & { rawSize: number } {
  const { interleaved, ver } = __debugCodewords(text, ecl)
  const mat = makeMatrix(ver, ecl, interleaved, mask)
  return { size: mat.size, get: (x, y) => mat.modules[y][x] === 1, version: ver, rawSize: mat.size }
}

/** @internal 仅供本地验证使用 */
export function __debugCodewords(
  text: string,
  ecl: QrEccLevel,
): { codewords: Uint8Array; interleaved: Uint8Array; ver: number; numBlocks: number; eccLen: number; shortBlockLen: number } {
  const bytes = new TextEncoder().encode(text)
  let ver = 0
  for (let v = 1; v <= 40; v++) {
    const usedBits = 4 + (v <= 9 ? 8 : 16) + bytes.length * 8
    if (usedBits <= getNumDataCodewords(v, ecl) * 8) {
      ver = v
      break
    }
  }
  const capBits = getNumDataCodewords(ver, ecl) * 8
  const bits: number[] = []
  const push = (value: number, len: number) => {
    for (let i = len - 1; i >= 0; i--) bits.push((value >>> i) & 1)
  }
  push(4, 4)
  push(bytes.length, ver <= 9 ? 8 : 16)
  for (const b of bytes) push(b, 8)
  push(0, Math.min(4, capBits - bits.length))
  while (bits.length % 8 !== 0) bits.push(0)
  for (let i = 0; bits.length < capBits; i++) {
    const pad = i % 2 === 0 ? 0xec : 0x11
    for (let j = 7; j >= 0 && bits.length < capBits; j--) bits.push((pad >>> j) & 1)
  }
  const codewordCount = capBits / 8
  const codewords = new Uint8Array(codewordCount)
  for (let i = 0; i < codewordCount; i++) {
    let byte = 0
    for (let j = 0; j < 8; j++) byte = (byte << 1) | bits[i * 8 + j]
    codewords[i] = byte
  }
  const numBlocks = NUM_ECC_BLOCKS[ecl][ver]
  const eccLen = ECC_CODEWORDS_PER_BLOCK[ecl][ver]
  const rawCodewords = Math.floor(getNumRawDataModules(ver) / 8)
  const shortBlockLen = Math.floor(rawCodewords / numBlocks)
  const numShortBlocks = numBlocks - (rawCodewords % numBlocks)
  const blocks: Uint8Array[] = []
  const eccBlocks: number[][] = []
  for (let i = 0, k = 0; i < numBlocks; i++) {
    const datLen = shortBlockLen - eccLen + (i < numShortBlocks ? 0 : 1)
    const dat = codewords.slice(k, k + datLen)
    k += datLen
    blocks.push(dat)
    eccBlocks.push(rsRemainder(dat, rsDivisor(eccLen)))
  }
  const interleaved = new Uint8Array(rawCodewords)
  let ik = 0
  for (let i = 0; i < shortBlockLen - eccLen + 1; i++) {
    for (let b = 0; b < numBlocks; b++) {
      if (i < blocks[b].length) interleaved[ik++] = blocks[b][i]
    }
  }
  for (let i = 0; i < eccLen; i++) {
    for (let b = 0; b < numBlocks; b++) interleaved[ik++] = eccBlocks[b][i]
  }
  return { codewords, interleaved, ver, numBlocks, eccLen, shortBlockLen }
}
