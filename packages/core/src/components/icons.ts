/**
 * 内置图标注册表。
 *
 * 统一规格：24×24 视区、描边式（stroke: currentColor），个别实心图标用 filled 标记。
 * 新增图标直接往 `icons` 里加，或用 `registerIcon()` 在业务侧注册，避免各组件各写一份内联 SVG。
 */
export interface IconDefinition {
  /** path 的 d 值，一个图标可拆成多段（例如「圆 + 对勾」） */
  paths: string[]
  /** 实心图标：填充 currentColor，不描边 */
  filled?: boolean
  /** 覆盖默认视区，默认 '0 0 24 24' */
  viewBox?: string
}

export const icons: Record<string, IconDefinition> = {
  /* ---------- 方向 ---------- */
  'chevron-left': { paths: ['M15 5l-7 7 7 7'] },
  'chevron-right': { paths: ['M9 5l7 7-7 7'] },
  'chevron-up': { paths: ['M5 15l7-7 7 7'] },
  'chevron-down': { paths: ['M5 9l7 7 7-7'] },
  'arrow-left': { paths: ['M19 12H5', 'M11 6l-6 6 6 6'] },
  'arrow-right': { paths: ['M5 12h14', 'M13 6l6 6-6 6'] },
  'arrow-up': { paths: ['M12 19V5', 'M6 11l6-6 6 6'] },
  'arrow-down': { paths: ['M12 5v14', 'M6 13l6 6 6-6'] },
  'arrow-up-left': { paths: ['M18 18L6 6', 'M6 14V6h8'] },

  /* ---------- 基础操作 ---------- */
  check: { paths: ['M20 6L9 17l-5-5'] },
  close: { paths: ['M18 6L6 18', 'M6 6l12 12'] },
  plus: { paths: ['M12 5v14', 'M5 12h14'] },
  minus: { paths: ['M5 12h14'] },
  /* 退格：左侧三角 + 内部叉 */
  backspace: { paths: ['M9 5h10a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H9l-6-7z', 'M13 9l4 6', 'M17 9l-4 6'] },
  search: { paths: ['M18 11a7 7 0 1 1-14 0 7 7 0 0 1 14 0', 'M16.4 16.4L21 21'] },
  'more-horizontal': { paths: ['M5 12h.01', 'M12 12h.01', 'M19 12h.01'] },
  'more-vertical': { paths: ['M12 5h.01', 'M12 12h.01', 'M12 19h.01'] },
  refresh: { paths: ['M20.5 12a8.5 8.5 0 1 1-2.6-6.1', 'M20.5 4v4.6h-4.6'] },
  'arrow-clockwise': { paths: ['M20.5 12a8.5 8.5 0 1 1-2.6-6.1', 'M20.5 4v4.6h-4.6'] },
  loading: { paths: ['M12 3a9 9 0 1 0 9 9'] },
  /* 通知喇叭：主体 + 两道声波 */
  horn: {
    paths: [
      'M4 10v4a1 1 0 001 1h2l4.5 3.4A1 1 0 0013 17.6V6.4a1 1 0 00-1.5-.8L7 9H5a1 1 0 00-1 1z',
      'M17 9.5a3.5 3.5 0 010 5',
      'M19.5 7a7 7 0 010 10',
    ],
  },

  /* ---------- 状态 ---------- */
  'check-circle': { paths: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0', 'M8 12.4l2.6 2.6L16 9.6'] },
  'close-circle': { paths: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0', 'M9.6 9.6l4.8 4.8', 'M14.4 9.6l-4.8 4.8'] },
  warning: { paths: ['M12 4.2l8.4 15.1H3.6z', 'M12 10v4.2', 'M12 17.1h.01'] },
  info: { paths: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0', 'M12 11v6', 'M12 7.6h.01'] },
  success: { paths: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0', 'M8 12.4l2.6 2.6L16 9.6'] },

  /* ---------- 常用业务 ---------- */
  star: { paths: ['M12 3.6l2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z'] },
  'star-fill': { paths: ['M12 3.6l2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z'], filled: true },
  heart: { paths: ['M12 20s-7-4.4-7-9a3.9 3.9 0 0 1 7-2.4A3.9 3.9 0 0 1 19 11c0 4.6-7 9-7 9z'] },
  'heart-fill': { paths: ['M12 20s-7-4.4-7-9a3.9 3.9 0 0 1 7-2.4A3.9 3.9 0 0 1 19 11c0 4.6-7 9-7 9z'], filled: true },
  user: { paths: ['M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z', 'M4.6 20a7.4 7.4 0 0 1 14.8 0'] },
  users: { paths: ['M9 12a3.6 3.6 0 1 0 0-7.2A3.6 3.6 0 0 0 9 12z', 'M2.6 19.6a6.4 6.4 0 0 1 12.8 0', 'M16 5.2a3.6 3.6 0 0 1 0 6.6', 'M17.6 13.6a6.4 6.4 0 0 1 3.8 5.9'] },
  phone: { paths: ['M6.6 3.5h2.9l1.5 3.9-2 1.4a11 11 0 0 0 6.2 6.1l1.4-2 3.9 1.5v2.9a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z'] },
  mail: { paths: ['M3.6 6.4h16.8v11.2H3.6z', 'M4 7l8 6 8-6'] },
  location: { paths: ['M12 21s7-5.4 7-11a7 7 0 1 0-14 0c0 5.6 7 11 7 11z', 'M14.5 10a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0'] },
  calendar: { paths: ['M4 6.6h16v13.8H4z', 'M4 10.8h16', 'M8 3.6v4', 'M16 3.6v4'] },
  clock: { paths: ['M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0', 'M12 7.4V12l3.2 2'] },
  home: { paths: ['M4 10.6L12 4l8 6.6V20H4z', 'M9.6 20v-5.6h4.8V20'] },
  setting: { paths: ['M4 8.2h5', 'M13 8.2h7', 'M4 15.8h9', 'M17 15.8h3', 'M11 5.7v5', 'M15 13.3v5'] },
  bell: { paths: ['M18 8.6a6 6 0 1 0-12 0c0 4.8-2 6.4-2 6.4h16s-2-1.6-2-6.4z', 'M10.2 18.6a2 2 0 0 0 3.6 0'] },
  camera: { paths: ['M4 8.6h3.2L8.6 6.4h6.8l1.4 2.2H20v11H4z', 'M15.5 13.9a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0'] },
  image: { paths: ['M4 5.6h16v12.8H4z', 'M4 15.2l4.6-4.6 3.9 3.9 3.9-3.9L20 15.1', 'M9.3 9.7a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0'] },
  file: { paths: ['M6 3.6h8l4 4v12.8H6z', 'M14 3.6v4h4'] },
  download: { paths: ['M12 4v10.4', 'M7.8 10.6l4.2 4.2 4.2-4.2', 'M5 19.6h14'] },
  upload: { paths: ['M12 15.4V5', 'M7.8 8.8L12 4.6l4.2 4.2', 'M5 19.6h14'] },
  undo: { paths: ['M9.4 14.2L4 8.8l5.4-5.4', 'M4 8.8h9.6a6.2 6.2 0 0 1 0 12.4H9.8'] },
  trash: { paths: ['M4.8 7h14.4', 'M9.2 7V4.8h5.6V7', 'M6.8 7l1 12.8h8.4l1-12.8', 'M10.4 10.8v5.6', 'M13.6 10.8v5.6'] },
  edit: { paths: ['M4 20h4L20 8l-4-4L4 16z', 'M14.5 5.5l4 4'] },
  filter: { paths: ['M4 6h16l-6.2 7.2v6.4L10.2 21v-7.8z'] },
  sort: { paths: ['M8 5v14', 'M4.8 15.2L8 19l3.2-3.8', 'M16 19V5', 'M12.8 8.8L16 5l3.2 3.8'] },
  cart: { paths: ['M3.4 4.4h2.2l2.1 9.8h10.6', 'M8.4 14.2h10.4l1.8-6.6H6.2', 'M9.4 18.6h.01', 'M17.6 18.6h.01'] },
  gift: { paths: ['M4.4 9.6h15.2V20H4.4z', 'M2.8 6h18.4v3.6H2.8z', 'M12 6v14', 'M12 6S10.6 2.6 8.2 3.6 8.6 6 12 6z', 'M12 6s1.4-3.4 3.8-2.4S15.4 6 12 6z'] },
  wallet: { paths: ['M3.6 6.4h16.8v12.2H3.6z', 'M3.6 9.8h16.8', 'M16 13.9h2'] },
  'qr-code': { paths: ['M4 4h6v6H4z', 'M14 4h6v6h-6z', 'M4 14h6v6H4z', 'M14 14h2.4v2.4H14z', 'M17.6 14H20v2.4h-2.4z', 'M14 17.6h2.4V20H14z', 'M17.6 17.6H20V20h-2.4z'] },
  share: { paths: ['M12 3.4v11', 'M8.2 7.2L12 3.4l3.8 3.8', 'M5 12.6V20h14v-7.4'] },
  link: { paths: ['M10.2 13.8a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.2 1.2', 'M13.8 10.2a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.2-1.2'] },
  lock: { paths: ['M5.8 10.4h12.4v9.6H5.8z', 'M8.4 10.4V8a3.6 3.6 0 0 1 7.2 0v2.4'] },
  unlock: { paths: ['M5.8 10.4h12.4v9.6H5.8z', 'M8.4 10.4V8a3.6 3.6 0 0 1 6.9-1.4'] },
  scan: { paths: ['M4 8.4V4h4.4', 'M20 8.4V4h-4.4', 'M4 15.6V20h4.4', 'M20 15.6V20h-4.4', 'M3.2 12h17.6'] },
  mic: { paths: ['M12 4a3 3 0 0 1 3 3v4.6a3 3 0 0 1-6 0V7a3 3 0 0 1 3-3z', 'M6.2 11.4a5.8 5.8 0 0 0 11.6 0', 'M12 17.4V21'] },
  play: { paths: ['M7.4 4.6L19.4 12 7.4 19.4z'], filled: true },
  pause: { paths: ['M7.4 4.8h3.4v14.4H7.4z', 'M13.2 4.8h3.4v14.4h-3.4z'], filled: true },
  volume: { paths: ['M4 9.6h3.2L12 5.2v13.6L7.2 14.4H4z', 'M15.4 9.2a4 4 0 0 1 0 5.6'] },
  wifi: { paths: ['M3.2 9.4a13.6 13.6 0 0 1 17.6 0', 'M6.6 12.8a9 9 0 0 1 10.8 0', 'M10 16.2a4 4 0 0 1 4 0', 'M12 19.4h.01'] },
  book: { paths: ['M5 4.6h6.4V20H5z', 'M12.6 4.6H19V20h-6.4z'] },
  'graduation-cap': { paths: ['M3 9.6L12 5l9 4.6-9 4.6z', 'M7 12v4.4c0 1.4 2.2 2.6 5 2.6s5-1.2 5-2.6V12'] },
  eye: { paths: ['M2.6 12S6.2 6.2 12 6.2 21.4 12 21.4 12 17.8 17.8 12 17.8 2.6 12 2.6 12z', 'M14.8 12a2.8 2.8 0 1 1-5.6 0 2.8 2.8 0 0 1 5.6 0'] },
  'eye-close': { paths: ['M4 4l16 16', 'M9.6 5.4A9.7 9.7 0 0 1 12 5.1c5.8 0 9.4 6.9 9.4 6.9a17 17 0 0 1-3.2 3.9', 'M6.4 7.6A16.6 16.6 0 0 0 2.6 12S6.2 18.9 12 18.9c1 0 2-.2 2.9-.5'] },
  sun: { paths: ['M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0', 'M12 2.6v2', 'M12 19.4v2', 'M2.6 12h2', 'M19.4 12h2', 'M5.3 5.3l1.4 1.4', 'M17.3 17.3l1.4 1.4', 'M18.7 5.3l-1.4 1.4', 'M6.7 17.3l-1.4 1.4'] },
  moon: { paths: ['M20 14.6A8.6 8.6 0 0 1 9.4 4 8.6 8.6 0 1 0 20 14.6z'] },
  lightning: { paths: ['M13.4 2.6L4.8 13.4h5.8l-1 8 8.6-10.8h-5.8z'] },
}

/** 语义别名：让业务侧用更直观的名字 */
const aliases: Record<string, string> = {
  arrow: 'chevron-right',
  back: 'chevron-left',
  clear: 'close-circle',
  delete: 'trash',
  add: 'plus',
  remove: 'minus',
  photo: 'image',
  mobile: 'phone',
  successful: 'check-circle',
  error: 'close-circle',
  warn: 'warning',
  thunderbolt: 'lightning',
}

const warned = new Set<string>()

/** 解析图标名（含别名） */
export function getIcon(name: string | undefined): IconDefinition | undefined {
  if (!name) return undefined
  const key = aliases[name] ?? name
  return icons[key]
}

/** 是否已注册某个图标（含别名） */
export function hasIcon(name: string): boolean {
  return Boolean(getIcon(name))
}

/**
 * 注册自定义图标。
 *
 * ```ts
 * registerIcon('logo', 'M4 4h16v16H4z')
 * registerIcon('logo', { paths: ['...'], filled: true })
 * ```
 */
export function registerIcon(
  name: string,
  def: string | string[] | IconDefinition,
): void {
  const normalized: IconDefinition =
    typeof def === 'string'
      ? { paths: [def] }
      : Array.isArray(def)
        ? { paths: def }
        : { ...def, paths: [...def.paths] }
  icons[name] = normalized
  warned.delete(name)
}

/** 未注册图标只警告一次，避免列表里刷屏 */
export function warnMissingIcon(name: string): void {
  if (warned.has(name)) return
  warned.add(name)
  if (typeof console !== 'undefined') {
    console.warn(`[Jimu UI] 图标 "${name}" 未注册，可用 registerIcon() 自行注册`)
  }
}

/** 全部图标名，便于做图标选择器 / 文档表格 */
export function iconNames(): string[] {
  return Object.keys(icons).sort()
}
