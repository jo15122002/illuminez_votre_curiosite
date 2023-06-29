import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    animals: {}
  }),
  actions: {
    leds(animals) {
      this.animals = animals
    },
    distance(id, dist) {
      const anim = this.animals.find((a) => a.id === id)
      anim.guide = dist
    }
  },
})