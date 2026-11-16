import { h } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import JimuUI from 'jimu-ui'

import DemoBlock from './components/DemoBlock.vue'
import PhoneFrame from './components/PhoneFrame.vue'
import NavTools from './components/NavTools.vue'

import './styles/custom.css'
import './styles/demo.css'

export default {
  extends: DefaultTheme,

  Layout() {
    return h(DefaultTheme.Layout, null, {
      'nav-bar-content-after': () => h(NavTools),
    })
  },

  enhanceApp({ app }) {
    app.use(JimuUI)
    app.component('DemoBlock', DemoBlock)
    app.component('PhoneFrame', PhoneFrame)
  },
} satisfies Theme
