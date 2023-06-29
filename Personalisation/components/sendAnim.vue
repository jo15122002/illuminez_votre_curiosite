<template>
  <div class="background" :style="'background:'+colorCode">
        <div class="back" >
            <div class="arrows">
                <div class="arrow a1" :style="'background:'+colorCode"></div>
                <div class="arrow a2" :style="'background:'+colorCode"></div>
                <div class="arrow a3" :style="'background:'+colorCode"></div>
            </div>
            <div class="center">
                <img @click="anim" class="button" :src="'/fishImg/'+fish+'/buttonA.png'">
            </div>
            <div class="wait" :style="'background-color:rgba('+colors.join()+',0.2)'">
                <div class="progress" :style="'width:'+untilEnd+'%;background:'+colorCode"></div>
            </div>
            <div class="arrows2">
                <div class="arrow a1" :style="'background:'+colorCode"></div>
                <div class="arrow a2" :style="'background:'+colorCode"></div>
                <div class="arrow a3" :style="'background:'+colorCode"></div>
            </div>
        </div>
    </div>
</template>

<script>
import {useCounterStore} from '@/store/index'
import { mapState } from 'pinia'
import { collection, addDoc } from "firebase/firestore";
import gsap from 'gsap'

export default {
    name: 'SendAnim',
    props: {
        fish: {
            type:Number
        },
        sendA: {
            type:Boolean
        },
        name: {
            type:String
        }
    },
    data() {
        return {
            animF: {
                1: {func: 'defence', name: 'Se protéger', color:'#FEFCF8'},
                2: {func: 'hide', name: 'Se camoufler', color:'#02295F'},
                3: {func: 'chase', name: 'Chasser', color:'#02295F'},
                4: {func: 'chase', name: 'Chasser', color:'#FEFCF8'},
                5: {func: 'defence', name: 'Se protéger', color:'#02295F'},
                6: {func: 'repro', name: "se reproduire", color:'#FEFCF8'}
            },
            timer: 45,
            totalTimer: 45,
            animLaunch: false
        }
    },
    watch: {
        timer: {
            handler(value) {
                if (value > 0) {
                    setTimeout(() => {
                        this.timer--;
                    }, 1000);
                } else {
                    this.returnCode()
                }

            },
            immediate: true // This ensures the watcher is triggered upon creation
        }
    },
    computed: {
        ...mapState(useCounterStore, ['newAnim', 'color', 'newA', 'currentA', 'removeAll']),
        colors() {
            return this.color(this.fish)
        },
        colorCode() {
            return 'rgb('+this.colors.join(',')+')'
        },
        untilEnd() {
            return 100 - (100 - ((this.totalTimer-this.timer)/this.totalTimer * 100))
        }
    },
    created() {
        this.newAnim('start')
    },
    mounted() {
        this.animArrow()
    },
    methods: {
        animArrow () {
            let arrow1 = document.getElementsByClassName('a1')
            let arrow2 = document.getElementsByClassName('a2')
            let arrow3 = document.getElementsByClassName('a3')
            let tl = gsap.timeline({repeat:-1})
            tl.to(arrow3, {
                opacity:0.2
            })
            tl.to(arrow2, {
                opacity:0.5
            })
            tl.to(arrow1, {
                opacity:1
            })
            tl.to(arrow3, {
                opacity:0
            })
            tl.to(arrow2, {
                opacity:0
            })
            tl.to(arrow1, {
                opacity:0
            })
        },
        anim() {
            if (!this.animLaunch) {
                this.animLaunch = true
                let button = document.getElementsByClassName('button')[0]
                let tl = gsap.timeline()
                tl.addLabel('start')
                tl.to(button, {
                    width:"-=200",
                    height: "-=200",
                    duration:0.5
                }, 'start')
                tl.addLabel('next', 0.5)
                tl.to(button, {
                    width:"+=200",
                    height: "+=200",
                    duration:0.5,
                    onComplete: () => {
                        this.animLaunch = false
                    }
                }, 'next')
                this.newAnim(this.animF[this.fish].func)
            }
            
        },
        async returnCode() {
            await this.updateAnimal()
            this.newA({data: this.currentA.data, fish: this.fish, name: this.currentA.name})
            this.newAnim('stop')
            this.$emit('back')
        },
        async updateAnimal() {
            const { firestore } = useFirebase()
            try {
                console.log('send')
                await addDoc(collection(firestore, "fish"), {
                    data: this.currentA.data,
                    name: this.name,
                    fish: this.fish
                })
            } catch(err) {
                console.error("writeToDB failed. reason :", err)
            }
        }
    }
}
</script>

<style>
.animTxt {
    position: absolute;
    font-family: bast;
    font-size: 70px;
    text-transform: capitalize;
    z-index: 2;
}

.button {
    position: absolute;
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    z-index: 0;
}

.center {
    height: 1411px;
    width: 1910px;
    justify-content: center;
    display: flex;
    align-items: center;
}

.wait {
    height: 28px;
    width: 1846px;
    position: absolute;
    top: 1332px;
    left: 35px;
    border-radius: 50px;
}

.progress {
    height: 100%;
    transition: all 2s;
    border-radius: 50px;
    max-width: 100%;
}

.arrow {
    mask-image: url('/icon/arrow_up.svg');
    mask-position: center;
    mask-repeat: no-repeat;
    mask-size: 100%;
    height: 33px;
    width: 66px;
}

.arrows {
    height: 100px;
    width: 66px;
    position: absolute;
    top: 51px;
    left: 51px;
}

.arrows2 {
    height: 100px;
    width: 66px;
    position: absolute;
    top: 51px;
    right: 51px;
}

.a1 {
    opacity: 0;
}

.a2 {
    opacity: 0;
}

.a3 {
    opacity: 0;
}

.look {
    opacity: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.txtLook {
    font-family: bast;
    font-size: 3rem;
}


</style>

<style scoped>
.return {
    mask-image: url('/icon/returnPage.png');
    mask-position: center;
    mask-repeat: no-repeat;
    width: 218px;
    height: 223px;
    z-index: 2;
}
</style>