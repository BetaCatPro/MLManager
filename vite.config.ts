import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import { UserConfig } from 'vite'
import svgLoader from 'vite-svg-loader'
// import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'

export default () => {
    const config: UserConfig = {
        server: {
            proxy: {
                '/api': {
                    target: 'http://110.42.184.111',
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, '')
                }
            }
        },
        resolve: {
            alias: {
                '@': resolve(__dirname, 'src')
            }
        },
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `@use "@/assets/styles/index.scss" as *;`
                }
            }
        },
        plugins: [
            vue(),
            svgLoader(),
            // 自定义 svg 指令
            // createSvgIconsPlugin({
            //     iconDirs: [resolve(process.cwd(), '@/assets/icons')],
            //     symbolId: 'icon-[name]'
            // }),
            Components({
                dirs: ['src/views', 'src/components'],
                resolvers: [
                    ElementPlusResolver({ importStyle: 'sass' }),
                    IconsResolver({
                        prefix: 'icon',
                        enabledCollections: ['ep']
                    })
                ],
                dts: true
            }),
            Icons({
                autoInstall: true
            })
        ]
    }
    return config
}
