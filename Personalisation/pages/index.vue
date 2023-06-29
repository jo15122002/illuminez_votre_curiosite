<template>
    <main>
        <template v-if="game">
            <client-only>
                <Game :fish="fish" :name="name" @saved="saved" @back="returnCode"></Game>
            </client-only>
        </template>
        <template v-if="start">
            <Passcode @fish="newFish"></Passcode>
        </template>
        <template v-if="card">
            <Card @read="cardRead" :fish="fish"></Card>
        </template>
        <template v-if="nameCreate">
            <NameGive @named="nameGive" :fish="fish"></NameGive>
        </template>
        <template v-if="anims">
            <SendAnim :fish="fish" :send-a="anims" @back="returnCode" :name="name"></SendAnim>
        </template>
    </main>
</template>

<script>
import Passcode from '@/components/passcode.vue'
import Card from '@/components/card.vue'
import SendAnim from '@/components/sendAnim.vue'

export default {
    components: {
        Game: () => {
        if (process.client) {
          return import("../components/game.vue");
        }
      },
      Passcode,
      Card,
      SendAnim
    },
    data() {
        return {
            fish:1,
            start: true,
            card: false,
            name: '',
            nameCreate: false,
            game: false,
            anims: false
        }
    },
    methods: {
        newFish(fish) {
            this.fish = fish
            this.start = false
            this.card = true
        },
        cardRead(stay) {
            this.card = false
            if (stay) {
                this.game = true
            } else {
                this.start = true
            }
        },
        nameGive(stay) {
            this.nameCreate = false
            if (stay.stay) {
                this.name = stay.name
                this.anims = true
            } else {
                this.returnCode()
            }
        },
        saved() {
            this.game = false
            let oldcanv = document.getElementsByClassName('p5Canvas')[0]
            oldcanv.remove()
            this.nameCreate = true
        },
        returnCode() {
            window.location.reload(true)
        }
    }

}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;600;700&display=swap');

body {
    overflow: hidden;
    overscroll-behavior: none;
}

@font-face {
  font-family: bast;
  src: url('/font/Basteleur-Bold.woff');
}

html {
    overscroll-behavior-x: none;
}

</style>