import { computed, ref, reactive } from 'vue'
import { isClient } from '../utils'

export type ThemeMode = 'light' | 'dark' | 'auto'

const KEYS = {
  theme: 'jm-theme',
  motion: 'jm-motion',
  elder: 'jm-elder',
}

/** 全局外观状态：主题 / 动效 / 适老 */
export const appearance = reactive({
  theme: 'auto' as ThemeMode,
  motion: true,
  elder: false,
})

const prefersDark = ref(false)
let mql: MediaQueryList | null = null
let ready = false

function apply() {
  if (!isClient) return
  const html = document.documentElement
  const dark = appearance.theme === 'dark' || (appearance.theme === 'auto' && prefersDark.value)

  html.dataset.theme = dark ? 'dark' : 'light'
  // 同时兼容 VitePress / Tailwind 的 .dark 约定
  html.classList.toggle('dark', dark)

  if (appearance.motion) html.removeAttribute('data-motion')
  else html.setAttribute('data-motion', 'off')

  if (appearance.elder) html.setAttribute('data-elder', 'true')
  else html.removeAttribute('data-elder')
}

/** 只应调用一次，通常在 main.ts 里 */
export function setupAppearance(): void {
  if (!isClient || ready) return
  ready = true

  mql = window.matchMedia('(prefers-color-scheme: dark)')
  prefersDark.value = mql.matches
  mql.addEventListener('change', (e) => {
    prefersDark.value = e.matches
    apply()
  })

  const t = localStorage.getItem(KEYS.theme) as ThemeMode | null
  if (t === 'light' || t === 'dark' || t === 'auto') appearance.theme = t
  if (localStorage.getItem(KEYS.motion) === 'off') appearance.motion = false
  if (localStorage.getItem(KEYS.elder) === 'true') appearance.elder = true

  apply()
}

export function useAppearance() {
  setupAppearance()

  const isDark = computed(
    () => appearance.theme === 'dark' || (appearance.theme === 'auto' && prefersDark.value),
  )

  const setTheme = (mode: ThemeMode) => {
    appearance.theme = mode
    if (isClient) localStorage.setItem(KEYS.theme, mode)
    apply()
  }

  const setMotion = (on: boolean) => {
    appearance.motion = on
    if (isClient) localStorage.setItem(KEYS.motion, on ? 'on' : 'off')
    apply()
  }

  const setElder = (on: boolean) => {
    appearance.elder = on
    if (isClient) localStorage.setItem(KEYS.elder, on ? 'true' : 'false')
    apply()
  }

  return {
    appearance,
    isDark,
    setTheme,
    setMotion,
    setElder,
    toggleTheme: () => setTheme(isDark.value ? 'light' : 'dark'),
    toggleMotion: () => setMotion(!appearance.motion),
    toggleElder: () => setElder(!appearance.elder),
  }
}
