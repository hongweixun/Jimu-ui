/** 令牌的 TS 出口，方便在 JS 里读取（图表、Canvas、动态样式等场景） */
import './index.css'

export const brand = {
  primary: '#00A0E9',
  success: '#00B98A',
  warning: '#FF9F1C',
  danger: '#E8344B',
} as const

export const palette = {
  blue: {
    50: '#e7f6fd',
    100: '#c4ebfb',
    200: '#8ed9f7',
    300: '#55c5f2',
    400: '#1fb2ed',
    500: '#00a0e9',
    600: '#0087c6',
    700: '#006ea3',
    800: '#005680',
    900: '#003d5c',
  },
  green: {
    50: '#e5faf4',
    100: '#b5f0df',
    200: '#7be2c6',
    300: '#3dd2ad',
    400: '#0acb9c',
    500: '#00b98a',
    600: '#009e75',
    700: '#00825f',
    800: '#00664a',
    900: '#004a35',
  },
  amber: {
    50: '#fff6e8',
    100: '#ffe6bf',
    200: '#ffd08c',
    300: '#ffb954',
    400: '#ffa72e',
    500: '#ff9f1c',
    600: '#e28200',
    700: '#b96700',
    800: '#8f4e00',
    900: '#663700',
  },
  red: {
    50: '#feecee',
    100: '#fcc9cf',
    200: '#f99aa5',
    300: '#f66c7c',
    400: '#f34a5f',
    500: '#e8344b',
    600: '#c92539',
    700: '#a61a2c',
    800: '#831220',
    900: '#600b16',
  },
} as const

export type BrandColor = keyof typeof brand
export type PaletteName = keyof typeof palette
export type PaletteLevel = keyof (typeof palette)['blue']
