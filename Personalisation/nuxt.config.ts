// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: [
        '@pinia/nuxt'
    ],
    plugins: [{src: './plugins/pinia-share-state.js'}]
})
