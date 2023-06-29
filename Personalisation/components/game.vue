<template>
    <div class="background" :style="'background: '+colorCode">
        <div class="back">
            <button @click="back" class="return" :style="'background:'+colorCode"></button>
            <div class="button-right">
                <button @click="draw" class="buttonChange" :style="'background-color:'+colorOpacity(true)">
                    <img class="imgB" src="/icon/draw.svg">
                </button>
                <button @click="gommeToogle" class="buttonChange" :style="'background-color:'+colorOpacity(false)">
                    <img class="imgB" src="/icon/erase.svg">
                </button>
            </div>
            <div class="colors">
                <button
                    @click="colorChange('#02295F')" 
                    style="background-color: #02295F"
                    :class=" colorS == '#02295F' ? 'color colorChosen': 'color'"
                ></button>
                <button
                    :class=" colorS == '#3AA098' ? 'color colorChosen': 'color'"
                    @click="colorChange('#3AA098')"
                    style="background-color: #3AA098"
                ></button>
                <button
                    :class=" colorS == '#B0D0E1' ? 'color colorChosen': 'color'"
                    @click="colorChange('#B0D0E1')" 
                    style="background-color: #B0D0E1"
                ></button>
                <button 
                    :class=" colorS == '#C5E2A6' ? 'color colorChosen': 'color'"
                    @click="colorChange('#C5E2A6')"
                    style="background-color: #C5E2A6"
                ></button>
                <button
                    :class=" colorS == '#C3ABD8' ? 'color colorChosen': 'color'"
                    @click="colorChange('#C3ABD8')"
                    style="background-color: #C3ABD8"
                ></button>
                <button
                    :class=" colorS == '#EFE8D8' ? 'color colorChosen': 'color colorGlow'"
                    @click="colorChange('#EFE8D8')"
                    style="background-color: #EFE8D8"
                ></button>
            </div>
            <button class="next" @click="save" :style="'background: '+colorCode">Enregistrer</button>
        </div>
    </div>
</template>

<script>
import {useCounterStore} from '../store/index'

export default {
    setup() {
        const store = useCounterStore()
        const { newA, current, newAnim, color } = store
        return { newA, current, newAnim, color }
    },
    name:'Game',
    props: {
        fish: {
            default: 1
        },
        name: {
            type:String
        }
    },
    data() {
        return {
            colorS: '#C3ABD8',
            painting: false,
            image: null,
            width: 30,
            canvas: null,
            dataA: null,
            gomme: false,
            saved: false,
            animF: {
                1: 'defence',
                2: 'hide',
                3: 'chase',
                4: 'chase',
                5: 'defence',
                6: 'repro'
            },
            glow: false
        }
    },
    watch: {
        fish: {
            handle(val) {
                this.mounted()
            }
        }
    },
    computed: {
        colors() {
            return this.color(this.fish)
        },
        colorCode() {
            if (this.colors) {
                return 'rgb('+this.colors.join(',')+')'
            }
        }
    },
    async mounted () {
        console.log('mount')
        const { default: P5 } = await import('p5')

        const sketch = (s) => {
            s.setup = () => {
                this.canvas = s.createCanvas(1080, 1080)
                s.background(s.color('FFFFFF'))
                this.img = s.loadImage('/fishImg/'+this.fish+'/fish.png')
            }
            s.draw = () => {
                s.image(this.img, 0, 0, 1080, 1080);
                if (this.painting)  {
                    if (this.gomme) {
                        s.stroke(s.color('FFFFFF'))
                    } else {
                        s.stroke(s.color(this.colorS))
                    }
                    s.strokeWeight(this.width)

                    if (this.glow) {
                        s.drawingContext.filter = 'blur(20px)'
                        s.line(s.mouseX, s.mouseY, s.pmouseX, s.pmouseY)
                        s.strokeWeight(this.width - 5)
                        s.stroke(s.color('FFFFFF'))
                        s.drawingContext.filter = 'blur(5px)'
                        s.line(s.mouseX, s.mouseY, s.pmouseX, s.pmouseY)
                        s.drawingContext.filter = 'none'
                    } else {
                        s.line(s.mouseX, s.mouseY, s.pmouseX, s.pmouseY)
                    }
                    s.image(this.img, 0, 0, 1080, 1080);
                }
                s.saveFrames('out', 'png', 1, 1, data => {
                    this.dataA = data[0].imageData
                })
            }
            s.mousePressed = () => {
                this.painting = true
            }
            s.mouseReleased = () => {
                this.painting = false;
                s.saveFrames('out', 'png', 1, 1, data => {
                    this.dataA = data[0].imageData
                })
            }
        }
        // eslint-disable-next-line no-unused-vars
        const canvas = new P5(sketch, 'p5Canvas')
    },
    beforeDestroy() {
        console.log('destroy')
    },
    methods: {
        colorChange(color) {
            this.gomme = false
            this.colorS = color
            if (color === '#EFE8D8') {
                this.glow = true
            } else {
                this.glow = false
            }
        },
        draw() {
            this.gomme = false
        },
        gommeToogle() {
            this.gomme = true
        },
        save() {
            console.log(this.dataA, this.fish)
            this.current({data: this.dataA, fish: this.fish, animation: 's', name:this.name})
            this.saved = true
            this.$emit('saved')
        },
        back() {
            this.$emit('back')
        },
        colorOpacity(draw) {
            let opacity = this.gomme ? 0.5 : 0.2
            if (draw) {
                opacity = !this.gomme ? 0.5 : 0.2
            }
            console.log('rgba('+this.colors.join(',')+', '+ opacity +')')
            return 'rgba('+this.colors.join(',')+', '+ opacity +')'
        }
    }

}
</script>

<style>

.buttonChange {
    border:none;
    width: 200px;
    height: 200px;
    border-radius: 20px;
}

.button-right {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    top: 547px;
    left: 1582px;
    height: 427px;
    z-index: 3;
}

.p5Canvas {
    position: absolute;
    background-color: white;
    left: 420px;
    top: 245px;
    display: flex;
}

.color {
    width: 98px;
    height: 98px;
    border: none;
    border-radius: 50%;
    z-index: 3;
}

.colors {
    position: absolute;
    top: 387px;
    width: 650px;
    left: 100px;
    height: 788px;
    display:flex;
    justify-content: space-between;
    flex-direction: column-reverse;
}

.colorChosen {
    outline: #E3E3E3 14px solid;
}

.colorGlow {
    outline: rgba(239, 232, 216, 0.6) 14px solid;
}

.background {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
}
.imgB {
    width: 8vh;
}

.action {
    background-color: white;
    position: relative;
    border: none;
    border-radius: 100%;
    height: 70px;
    width: 70px;
}

</style>

<style scoped>
.return {
    mask-image: url('/icon/returnPage.png');
    mask-position: center;
    mask-repeat: no-repeat;
    width: 218px;
    height: 223px;
}
</style>