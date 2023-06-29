<template>
    <main id="fullScreen">
        <button @click="lightOn()" id="boutonOn"></button>
        <template v-if="startG">
            <StartGame @startGame="getData"></StartGame>
        </template>
        <template v-if="!startG && !finishS">
            <client-only>
                <template v-if="start">
                    <Game :animals="animals" @sendLight="sendWebsocket" @sendForce="sendForce"></Game>
                </template>
            </client-only>
        </template>
        
        <template v-if="finishS && !startG">
            <Finish @startGame="restart"></Finish>
        </template>
    </main>
</template>

<script>
import {useCounterStore} from '../store/index'
import StartGame from '../components/start.vue'
import Finish from '../components/finish.vue'

export default {
    setup() {
        const store = useCounterStore()
        const { leds, distance } = store
        const animalsStore = computed(() => store.animals)
        return { animalsStore, leds, distance }
    },
    components: {
        Game: () => {
        if (process.client) {
          return import("../components/game.vue");
        }
      },
      StartGame,
      Finish
    },
    data() {
        return {
            api: 'http://192.168.43.108:5000',
            websocket: null,
            animals: [],
            start : false,
            totalAnimals: 0,
            animalSucces: 0,
            currentForce: 0,
            startG: true,
            timeFinish: null,
            finishS: false,
            ledOn:false
        }
    },
    computed: {
        finish() {
            return this.animalSucces === this.totalAnimals
        }
    },
    watch: {
        startG: {
            handler(value) {
                if (value) {
                    clearTimeout(this.timeFinish)
                    this.timeFinish = null
                }
            }
        }
    },
    created() {
        if (process.client) {
            this.initializeSocket()
        }
        /* this.start = true
        this.animals = [
            {
                "id": 1,
                "animal": "poisson",
                "use": "chase",
                "led": false,
                "guide": 0,
                "pin" : 23,
                "clue": "1 fekozfjerifhriudezfh fruezfhue rfhe fhrd hefre"
            },
            {
                "id": 2,
                "animal": "luciolle",
                "use": "see",
                "led": false,
                "guide": 0,
                "pin": 22,
                "clue": "2 frejiofgre uf ruig reuyghr edhuf euf r ughre"
            }
        ]
        this.leds(this.animals)
        this.totalAnimals = this.animals.length */
    },
    methods: {
        initializeSocket() {
            this.websocket = new WebSocket('ws://192.168.43.108:5000/ws')
            this.websocket.onmessage = (event) => {
                console.log(this.start)
                if (!this.start) {
                    this.animals = JSON.parse(event.data)
                    this.start = true
                    this.leds(this.animals)
                    this.totalAnimals = this.animals.length
                    this.animalSucces = 0

                }
            }
            this.websocket.onopen = (event) => {
                console.log(event)
                console.log("Starting connection to WebSocket server..");
            }
            
            this.websocket.onerror = (event) => {
                console.log(event)
            }

            this.websocket.onclose = (event) => {
                console.log(event)
            } 
        },
        sendWebsocket(led) {
            this.websocket.send('succes:' + led)
            console.log('succes:' + led)
            this.distance(led, 1)
            this.animalSucces += 1
            if (this.finish) {
                setTimeout(() => {this.finishS = true}, 2000)
                this.timeFinish = setTimeout(() => {this.restart()}, 20000)
            }
        },
        sendForce(led) {
            const force = led.distance - this.currentForce
            if (force < -0.1 || force > 0.1) {
                this.websocket.send('led:' + led.id + ':' + led.distance)
                this.distance(led.id, led.distance)
                this.currentForce = led.distance
            }
        },
        getData() {
            this.startG = false
            this.start = false
            this.animalSucces = -1
            this.websocket.send("start")
        },
        restart() {
            this.startG = true
            this.start = false
            this.finishS = false
            this.animalSucces = 0
            this.websocket.send("start")
            let oldcanv = document.getElementsByClassName('p5Canvas')[0]
            console.log(oldcanv)
            oldcanv.remove()
            this.websocket.send("start")
        },
        lightOn() {
            if (!this.ledOn) {
                for(let i=1; i < 5; i++) {
                    console.log(i)
                    this.websocket.send('succes:' + i)
                    this.ledOn = true
                }
            } else {
                this.websocket.send("start")
                this.ledOn = false
            }
            
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;700&display=swap');

body {
    overflow: hidden;
    background-color: #02295F;
}

#boutonOn {
    height: 30px;
    width: 30px;
    background-color:#02295F;
    z-index: 3;
    position: absolute;
    border: #022c66 1px solid;
}
</style>