import { resolve } from 'node:path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dts from 'vite-plugin-dts'

export default defineConfig({
  plugins: [
    vue(),
    dts({
      tsconfigPath: resolve(__dirname, 'tsconfig.json'),
      include: ['src/**/*.ts', 'src/**/*.vue'],
      outDir: 'dist',
      insertTypesEntry: false,
    }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'JimuUI',
      formats: ['es'],
      fileName: () => 'index.mjs',
      cssFileName: 'style',
    },
    cssCodeSplit: false,
    minify: 'esbuild',
    rollupOptions: {
      external: ['vue'],
      output: {
        preserveModules: true,
        preserveModulesRoot: 'src',
        entryFileNames: '[name].mjs',
      },
    },
  },
})
