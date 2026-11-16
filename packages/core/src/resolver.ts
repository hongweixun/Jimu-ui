/**
 * 按需引入解析器，配合 unplugin-vue-components 使用：
 *
 * import Components from 'unplugin-vue-components/vite'
 * import { JimuResolver } from 'jimu-ui/resolver'
 *
 * Components({ resolvers: [JimuResolver()] })
 *
 * 模板里直接写 <jm-button /> 即可，JS 由 tree-shaking 保证只打进用到的组件。
 */
export interface ComponentResolverItem {
  name: string
  from: string
  sideEffects?: string | string[]
}

export function JimuResolver(): {
  type: 'component'
  resolve: (name: string) => ComponentResolverItem | undefined
} {
  return {
    type: 'component',
    resolve(name: string) {
      if (!name.startsWith('Jm')) return
      const partial = name.slice(2)
      if (!partial) return
      return {
        name: partial,
        from: 'jimu-ui',
        sideEffects: 'jimu-ui/style.css',
      }
    },
  }
}

export default JimuResolver
