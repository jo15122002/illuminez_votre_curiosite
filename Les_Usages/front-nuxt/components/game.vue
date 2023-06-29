<template>
  <div class="container border test">
    <div class="backgroundColor">
        <div class="pairsDiv" v-if="randomDone">
            <div v-for="(animalU, index) in animals" :key="index" class="pair">
                <div class="nameDiv">
                    <div :id="animalU.animal" class="animal"><p>{{animalU.animal}}</p></div>
                </div>

                <div class="nameDiv">
                    <div :id="random[index].use" class="use"><p style="opacity:1">{{random[index].use}}</p></div>
                </div>
            </div>
        </div>
        <template v-if="clue && !painting">
            <div class="backgroundClue">
                <div class="backClue"></div>
                <div class="clue" :style="'background-image:url('+animalClue.img+')'">
                    <div class="T">
                        <div class="clueT">
                            <div class="clueIB" :style="'background-color:'+animalClue.color">
                                </div>
                            <p class="animalName" :style="'color:'+animalClue.color">
                                {{animalClue.animal}}
                            </p>
                        </div>
                        <p class="clueText"> <span v-html="animalClue.clue"></span></p>
                    </div>
                     <div class="clueCloseDiv">
                        <button @click="closeClue" class="clueClose" :style="'background:' + animalClue.color"></button>
                    </div>
                </div>
            </div>
        </template>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Game',
    data() {
        return {
            paths : [],
            painting : false,
            animalsT: [],
            animal: null,
            clue: false,
            animalClue: '',
            clueText: '',
            random: [],
            randomDone: false,
            clues: [
                {
                    animal: 'Le poisson lanterne',
                    id: 1,
                    clue: 'Les petites lumières attirent les petites proies !',
                    color: '#3AA098',
                    img: '/fish/poisson-l.png',
                    animalId: 1
                },
                {
                    animal: 'Le calamar',
                    id: 2,
                    clue: 'Le calamar adore se déguiser ! <br>Le calamar adore passer inaperçu !',
                    color: '#B0D0E1',
                    img: '/fish/calamar.png',
                    animalId: 3
                }
            ],
            currentClue: 1,
            timerCount: 30
        }
    },
    props: {
        animals: {
            type:Array
        },
        finish: {
            type:Boolean
        }
    },
    watch: {
        timerCount: {
            handler(value) {
                if (value > 0 && !this.painting) {
                    setTimeout(() => {
                        this.timerCount--;
                    }, 1000)
                } else if (!this.painting) {
                    this.clueToggle(this.currentClue)
                }

            },
            immediate: true // This ensures the watcher is triggered upon creation
        }
    },
    created() {
        this.randomS()
    },
    async mounted () {
        const { default: P5 } = await import('p5')

        const sketch = (s) => {
            s.setup = () => {
                s.createCanvas(window.innerWidth, window.innerHeight);
                s.stroke(s.color('FFFFFF'))
                s.strokeWeight(3)
            }
            s.draw = () => {
                if (this.painting)  {
                    const useP = this.getUsePositionFromAnimal(this.animal)
                    const animalP = this.getAnimalPosition(this.animal)
                    const distance = s.dist(useP.x, useP.y, animalP.x, animalP.y)
                    const dist2 = s.dist(useP.x, useP.y, s.mouseX, s.mouseY)
                    const force = ((distance / 2) - dist2)/(distance / 2)
                    s.line(s.mouseX, s.mouseY, s.pmouseX, s.pmouseY)
                    const currentAnim = this.animals.find((anim) => anim.animal === this.animal)
                    this.$emit('sendForce', {id: currentAnim.id, distance: force})
                }
                this.animals.forEach((animal) => {
                    if (animal.led) {
                        const p = this.getLineXY(animal.animal)
                        s.line(p.lines.x1, p.lines.y1, p.lines.x2, p.lines.y2)
                    }
                })
            }
            s.mousePressed = () => {
                const allAnimals = window.document.getElementsByClassName("animal")
                allAnimals.forEach(animal => {
                    const dim = animal.getBoundingClientRect()
                    if (s.mouseX > dim.left && s.mouseX < dim.right && s.mouseY > dim.top && s.mouseY < dim.bottom) {
                        const currentAnim = this.animals.find((anim) => anim.animal === animal.id)
                        if (!currentAnim.led) {
                            this.animal = animal.id
                            this.painting = true
                        } else {
                            this.animal = null
                        }
                    }
                })
            }
            s.mouseReleased = () => {
                if (this.animal !== null) {
                    const p = this.getLineXY(this.animal)
                    if (s.mouseX > p.useP.left && s.mouseX < p.useP.right && s.mouseY > p.useP.top && s.mouseY < p.useP.bottom) {
                        s.clear()
                        s.line(p.lines.x1, p.lines.y1, p.lines.x2, p.lines.y2)
                        const currentAnim = this.animals.find((anim) => anim.animal === this.animal)
                        currentAnim.led = true
                        this.$emit('sendLight', currentAnim.id)
                        this.animal = null
                    } else {
                        const currentAnim = this.animals.find((anim) => anim.animal === this.animal)
                        this.$emit('sendForce', {id: currentAnim.id, distance: 0})
                        s.clear()
                        this.animal = null
                    }
                }
                this.timerCount--
                this.painting = false;
            }
        }
        // eslint-disable-next-line no-unused-vars
        const canvas = new P5(sketch, 'p5Canvas')
    },
    methods: {
        getLineXY(animal) {
            const currentAnim = this.animals.find((anim) => anim.animal === animal)
            const curUse = window.document.getElementById(currentAnim.use)
            const animalD = window.document.getElementById(currentAnim.animal)
            const animalP = animalD.getBoundingClientRect()
            const useP = curUse.getBoundingClientRect()
            return {animalP :animalP, useP: useP, lines: {x1:(animalP.right - 20), y1:animalP.y + animalP.height/2 , x2:useP.x, y2:useP.y + useP.height/2}}
        },
        getUsePositionFromAnimal(animal) {
            const currentAnim = this.animals.find((anim) => anim.animal === animal)
            const curUse = window.document.getElementById(currentAnim.use)
            const useP = curUse.getBoundingClientRect()
            return useP
        },
        getAnimalPosition(animal) {
            const animalD = window.document.getElementById(animal)
            const animalP = animalD.getBoundingClientRect()
            return animalP
        },
        clueToggle(animal) {
            let clue = animal
            let clueText = this.clues.find((el) => el.id === animal)
            let validate = this.animals.find((anim) => anim.id === clueText.animalId)
            if (validate.led === true) {
                this.currentClue += 1
                return this.clueToggle(this.currentClue)
            }

            if (clue < 3) {
                const currentC = this.clues.find((el) => el.id === animal)
                this.animalClue = currentC
                this.clue = true
            }
        },
        closeClue() {
            this.clue = false
            this.timerCount = 30
            this.currentClue += 1
        },
        randomS() {
            this.random = [...this.animals]
            this.random.sort(()=> Math.random() - 0.5)
            this.randomDone = true
        }
    }

}
</script>

<style>
.animal {
    position: relative;
    background-color: rgba(58, 160, 152, 0.8);
    margin: 10px;
    z-index: 3;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 10px;
    font-family: 'Red Hat Display', sans-serif;
    font-weight: 900;
    text-transform: uppercase;
    width: 200px;
    text-align: center;
}

.use {
    position: relative;
    margin: 10px;
    background-color: #3AA098;
    opacity: 0.8;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 10px;
    font-family: 'Red Hat Display', sans-serif;
    font-weight:bolder;
    text-transform: uppercase;
    width: 200px;
    text-align: center;
}

.pair {
    display: flex;
    justify-content: space-between;
    width: 100%;
}
.test {
    position: fixed;
    display: contents;
    overscroll-behavior: none;
    overflow : hidden;
    background-color: #02295F;
    color:#EFE8D8;
}

#defaultCanvas0 {
    position: fixed;
    overscroll-behavior: none;
    overflow : hidden;
    top:0;
    z-index: 1;
}

.backgroundClue {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items:center;
    justify-content: center;
    z-index: 3;
}

.clue {
    background-color: #FEFCF8;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-direction: column;
    padding: 3rem;
    padding-top: 1rem;
    color:#02295F;
    width: 600px;
    height: 550px;
    opacity: 1;
    border-radius: 20px;
    background-size: 70%;
    background-position: bottom;
    background-position-x: left;
    background-repeat: no-repeat;
    z-index: 3;
}

.animalName {
    font-size: 2.5rem;
    font-family: bast;
}

.clueClose {
    border: none;
    position: relative;
    mask-image: url("/icons/arrow.svg");
    mask-repeat: no-repeat;
    mask-size: 100%;
    width: 70px;
    height: 50px;
    z-index: 3;
    
}

.clueCloseDiv {
    display: flex;
    justify-content: flex-end;
    width: 100%;
    height: inherit;
    align-items: flex-end;
}


.title {
    font-size: 2.5rem;
    font-family: bast;
}

.backgroundColor {
    background-image: url('/back/backgroundG.png');
    position: absolute;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-position:bottom;
    background-size: 100%;
    background-repeat: no-repeat;
}

.pairsDiv {
    width: 90%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    height: 100%;
}

.nameDiv {
    display: flex;
    align-items: center;
}

.clueIB {
    border-radius: 20px;
    width: 70px;
    height: 70px;
    margin-right: 2rem;
    background-image: url('/icons/clue.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 60%;
}

.clueIBI {
    width: 40px;
    height: 40px;
    margin: 10px;
}

.T {
    display: flex;
    flex-direction: column;
}

.clueT {
    display: flex;
    align-items: center;
}

.clueImg {
    width: inherit;
    position: fixed;
    margin: 0;
    left: 325px;
}

.clueText {
    font-family: 'Red Hat Display', sans-serif;
    font-size: 1.75rem;
    margin-top: -1rem;
    margin-left: 7rem;
}

.backClue {
    background-color: black;
    opacity: 0.7;
    width: 100%;
    height: 100%;
    position: absolute;
    z-index: -1;
}
</style>