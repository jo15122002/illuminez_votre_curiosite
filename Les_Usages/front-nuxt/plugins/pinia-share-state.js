import { PiniaSharedState  } from 'pinia-shared-state'
import { useCookie } from '#app' // optional import as Nuxt will auto-import it

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.$pinia.use(PiniaSharedState({enable: true}))
})