<template>
    <main>
        {{animal}}
        <div class="black" :style="'opacity: ' + opacity"></div>
    </main>
</template>

<script>
import {useCounterStore} from '../../store/index'
export default {
    setup() {
        const store = useCounterStore()
        const animals = computed(() => store.animals)
        return { animals }
    },
    computed: {
        id() {
            const route = useRoute()
            const {id} = route.params
            return id
        },
        animalsFull() {
            console.log(this.animals)
            return JSON.parse(JSON.stringify(this.animals))
        },
        animal() {
            if (Array.isArray(this.animalsFull)) {
                return this.animalsFull.find((a) => a.id === parseInt(this.id))
            }
            return this.animals
        },
        opacity() {
            return 1 - this.animal.guide
        }
    }

}
</script>

<style>
.black {
    background-color: black;
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
}
</style>