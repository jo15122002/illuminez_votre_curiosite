import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    animals: [],
    all: [],
    currentA: {},
    animation: '',
    animalsColor: {1: [195, 171, 216], 2:[176, 208, 225], 3:[197, 226, 166], 4:[58, 160, 152], 5:[176, 208, 225], 6:[241, 155, 168]},
    fishsParts: [
      {
        fish: 1,
        parts: 3,
        head: true,
        eyes: false,
        style: 'mask-size:30vw;width:30vw;-webkit-mask-size:30vw',
        smallsStyle: 'mask-size:20vw;width:20vw;-webkit-mask-size:20vw'
      },
      {
        fish: 2,
        parts: 4,
        head: true,
        eyes: true,
        style: 'mask-size:40vw;width:40vw;-webkit-mask-size:40vw',
        smallsStyle: 'mask-size:25vw;width:25vw;-webkit-mask-size:25vw'
      },
      {
        fish: 3,
        parts: 3,
        head: true,
        eyes: true,
        style: 'mask-size:30vw;width:30vw;-webkit-mask-size:30vw',
        smallsStyle: 'mask-size:20vw;width:20vw;-webkit-mask-size:20vw'
      },
      {
        fish: 4,
        parts: 2,
        head: true,
        eyes: true,
        style: 'mask-size:30vw;width:30vw;-webkit-mask-size:30vw',
        smallsStyle: 'mask-size:20vw;width:20vw;-webkit-mask-size:20vw'
      },
      {
        fish: 5,
        parts: 1,
        head: true,
        eyes: false,
        style: 'mask-size:20vw;width:20vw;-webkit-mask-size:20vw',
        smallsStyle: 'mask-size:15vw;width:15vw;-webkit-mask-size:15vw'
      },
      {
        fish: 6,
        parts: 1,
        head: true,
        eyes: false,
        style: 'mask-size:20vw;width:20vw;-webkit-mask-size:20vw',
        smallsStyle: 'mask-size:10vw;width:10vw;-webkit-mask-size:10vw'
      }
    ]
  }),
  actions: {
    newA(animal) {
      this.all.push(animal)
    },
    current(animal) {
      this.currentA = animal
    },
    newAnim(animation) {
      this.currentA.animation = animation
    },
    fishPart(fish) {
      return this.fishsParts.find((id) => id.fish === fish)
    },
    color(fish) {
      return this.animalsColor[fish]
    },
    removeAll() {
      this.all = []
    }
  },
})