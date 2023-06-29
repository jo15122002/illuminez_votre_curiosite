<template>
    <div>
        <video id="background-video" autoPlay loop playsInline @click="startV">
            <source src="~/assets/video/background-video.mp4" type="video/mp4">
        </video>

        <template v-if="fish === 6">
           <div id=love><img id="loveImg" src="fishImg/6/love.png"></div> 
        </template>

        <template v-if="fish === 4 || fish === 3">
           <div id=proie><img id="proieImg" src="fishImg/5/food.png"></div>
        </template>

        <template v-if="fish === 1 || fish === 5">
           <div id=pre><img id="preImg" src="fishImg/4/ex.png"></div>
        </template>

        <div class="backFishiesContain">
            <div v-for="(last, index) in lastFive" :key="last.fish" style="position:relative">
                <div :class="'backFishiesDiv small'+last.fish" :id="'backFish'+index" :fish="last.fish" :index="index" style="z-index:0">
                <template v-if="lastFishParts(last.fish)">
                    <img :src="last.data" :class="'head_'+last.fish+' masked hB backFishies small'+last.fish" :style="lastFishParts(last.fish).smallStyle">
                </template>
                    <template v-if="lastFishParts(last.fish) && lastFishParts(last.fish).eyes">
                        <img :src="last.data" :class="'eyes_'+last.fish+' masked backFishies small'+last.fish" :style="lastFishParts(last.fish).smallStyle">
                    </template>
                    <div v-for="part in lastFishParts(last.fish) ? lastFishParts(last.fish).parts : 0" :key="part">
                        <img :src="last.data" :class="'part'+part+'_'+last.fish+' backFishies small'+last.fish" :id="part+'background'+index" style="position:absolute">
                    </div>
                </div>
            </div>
        </div>
        
        <img :src="dataA">
        <div id="fish">
            <div>
                <template v-if="fishParts && fishParts.head">
                    <img :src="dataA" :class="'head_'+fish+' masked head'" :style="fishParts.style">
                </template>
                <template v-if="fishParts && fishParts.eyes">
                    <img :src="dataA" :class="'eyes_'+fish+' masked'" :style="fishParts.style">
                </template>
                <div v-for="part in fishParts ? fishParts.parts : 0" :key="part">
                    <img :src="dataA" :class="'part'+part+'_'+fish+' masked part'" :id="part" :style="fishParts.style">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import gsap from 'gsap'
import {useCounterStore} from '@/store/index'
import { mapState } from 'pinia'
export default {
    watch: {
        animation(newAnimation, oldAnimation) {
            if (newAnimation === 'start') {
                this.startAnimation()
            } else if (newAnimation === 'hide') {
                this.hideAnim()
            } else if(newAnimation === 'repro') {
                this.repro()
            } else if(newAnimation === 'defence') {
                this.defence()
            } else if(newAnimation === 'chase') {
                this.chase()
            } else if (newAnimation === '') {
                gsap.killTweensOf('.part')
                this.timeline = this.animationLife()
            } else if (newAnimation === 'stop') {
                gsap.killTweensOf('.part')
                this.timeline = null
                this.sayGoodBye()
            } else if (newAnimation === 's') {
                this.setOpacity()
                console.log('hey')
            }
        },
        dataA(newFish) {
            if (!newFish) {
                this.timeline = null
            }
            this.setOpacity()
        }
    },
    data() {
        return {
            time: 0.2,
            timeline: null
        }
    },
    computed: {
        ...mapState(useCounterStore, ['currentA', 'newA', 'current', 'newAnim', 'fishPart', 'all']),
        dataA() {
            return this.currentA.data
        },
        fish() {
            return this.currentA.fish
        },
        fishParts() {
            return this.fishPart(this.fish)
        },
        animation() {
            return this.currentA.animation
        },
        allAnimal() {
            return this.all
        },
        lastFive() {
            return this.all.slice(-6)
        }
    },
    mounted() {
        /* let video = document.getElementById('background-video')
        video.muted = false
        video.autoplay = true */
        
    },
    methods: {
        startV() {
            let video = document.getElementById('background-video')
            video.play()
            video.style["z-index"] = -1
        },
        lastFishParts(fish) {
            return this.fishPart(fish)
        },
        startAnimation() {
            const tl = gsap.timeline().addLabel('start', 0)
            const fish = document.getElementById('fish')
            if (fish) {
                tl.set(fish, {
                    opacity:0,
                    x:0,
                    y:0
                }, "start")
                tl.to(fish, {
                    opacity:1,
                    duration: 2
                })
                this.newAnim('')
            }
        },
        sayGoodBye() {
            const newFish = document.getElementById('backFish'+(this.lastFive.length - 1).toString())
            if (this.lastFive.length < 6) {
                gsap.set(newFish, {
                    opacity: 0
                })
            }
            gsap.to(newFish, {
                x:"+=1500",
                overwrite: true
            })

            const tl = gsap.timeline().addLabel('start', 0)
            const fish = document.getElementById('fish')
            if (fish) {
                tl.to(fish, {
                    x:0,
                    y:0,
                    rotate:0
                })
                tl.to(fish, {
                    rotate: -10,
                    y:"+=50",
                    duration: 2
                })
                tl.to(fish, {
                    rotate: 0,
                    y:0,
                    duration:2
                })
                tl.to(fish, {
                    x: "-=1500",
                    duration:5
                })
                tl.set(fish, {
                    opacity: 0,
                    x:0,
                    onComplete: () => {
                        this.apparate(newFish)
                    }
                })
                gsap.killTweensOf('.part')
                this.timeline = null

                if (this.lastFive.length === 6) {
                    const oldFish = document.getElementById('backFish0')
                    
                    oldFish.innerHTML = ''
                }
                
            }
        },
        apparate(newFish) {
            gsap.set(newFish, {
                opacity: 1
            })
            gsap.to(newFish, {
                x: 0,
                duration:5,
                rotate:0,
                overwrite: true,
                onStart: () => {
                    const fishAttribute = newFish.getAttribute('fish')
                    const fishIndex = newFish.getAttribute('index')
                    if (fishAttribute == 5) {
                        this.simpleFish(fishIndex)
                    } if (fishAttribute == 2) {
                        this.calamarLife(fishIndex)
                    } if (fishAttribute == 3) {
                        this.poulpeLife(fishIndex)
                    } if (fishAttribute == 1) {
                        this.jellyFishLife(fishIndex)
                    } if (fishAttribute == 6) {
                        this.crevetteLife(fishIndex)
                    } if (fishAttribute == 4) {
                        this.lenterneLife(fishIndex)
                    }
                },
                onComplete: () => {
                    this.cycleBackground(newFish)
                }
            })
        },
        setOpacity() {
            const tl = gsap.timeline()
            const fish = document.getElementById('fish')
            tl.set(fish, {
                opacity:0
            })
        },
        animationLife() {
            gsap.killTweensOf('.part')
            if (this.fish === 5) {
                return this.simpleFish()
            } if (this.fish === 2) {
                return this.calamarLife()
            } if (this.fish === 3) {
                return this.poulpeLife()
            } if (this.fish === 1) {
                return this.jellyFishLife()
            } if (this.fish === 6) {
                return this.crevetteLife()
            } if (this.fish === 4) {
                this.lenterneLife()
            }
        },
        simpleFish(back = null) {
            if (!back && this.fish !== 5) {
                return this.animationLife()
            }
            const fin = document.getElementById(back ? '1background'+back : '1')
            const tlFin = gsap.timeline()
            
            tlFin.from(fin,{
                rotate: 0,
                y:0,
                overwrite: true
            })
            tlFin.to(fin, {
                rotate: 10,
                y: back ? "-=8" :"-=13"
            })
            tlFin.to(fin,{
                rotate: -10,
                y:back ? "+=15" :"+=27"
            })
            tlFin.to(fin,{
                rotate: 0,
                y:0, 
                ease:"none"
            })
            return tlFin
        },
        calamarLife(back=null) {
            gsap.killTweensOf('.part')
            if (!back && this.fish !== 2) {
                return this.animationLife()
            }
            const tlTotalTentacles = gsap.timeline()
            const tlTentacle1 = gsap.timeline({repeat:-1})
            const tlTentacle2 = gsap.timeline({repeat:-1})
            const tlTentacle3 = gsap.timeline({repeat:-1})
            const tlTentacle4 = gsap.timeline({repeat:-1})
            const p1 = document.getElementById(back ? '1background'+back : '1')
            const p2 = document.getElementById(back ? '2background'+back : '2')
            const p3 = document.getElementById(back ? '3background'+back : '3')
            const p4 = document.getElementById(back ? '4background'+back : '4')
            
            tlTentacle1.set(p1,{
                rotate: 0,
                y:0,
                x:0,
                overwrite: true
            })
            tlTentacle1.to(p1, {
                rotate: 5,
                x: back ? "+=4" : "+=0",
                y: back ? "+=2" : "+=15",
                duration: 2
            })
            tlTentacle1.to(p1,{
                rotate: 0,
                y:0,
                x:0,
                duration:2
            })

            tlTentacle2.set(p2,{
                rotate: 0,
                y:0,
                x:0,
                overwrite:true
            })
            tlTentacle2.to(p2, {
                rotate: 5,
                x: back ? "+=3" : "+=5",
                duration:3
            })
            tlTentacle2.to(p2,{
                rotate: 0,
                y:0,
                x:0,
                duration:1
            })

            tlTentacle3.set(p3,{
                rotate: 0,
                y:0,
                x:0,
                overwrite: true
            })
            tlTentacle3.to(p3, {
                rotate: -7,
                x: back ? "-=2" : "-=10",
                duration:1
            })
            tlTentacle3.to(p3,{
                rotate: 0,
                y:0,
                x:0,
                duration:3
            })

            tlTentacle4.set(p4,{
                rotate: 0,
                y:0,
                x:0,
                overwrite:true
            })
            tlTentacle4.to(p4, {
                rotate: -10,
                x: back ? "-=5" : "-=15",
                y: back ? "+=5" :"+=15",
                duration: 2
            })
            tlTentacle4.to(p4,{
                rotate: 0,
                y:0,
                x:0,
                duration:4
            })

            tlTotalTentacles.addLabel('start',0)
            tlTotalTentacles.add(tlTentacle1, 'start')
            tlTotalTentacles.add(tlTentacle2, 'start')
            tlTotalTentacles.add(tlTentacle3, 'start')
            tlTotalTentacles.add(tlTentacle4, 'start')
            return tlTotalTentacles
        },
        poulpeLife(back=null) {
            if (!back && this.fish !== 3) {
                return this.animationLife()
            }
            const tlTotalTentacles = gsap.timeline()
            const tlTentacle1 = gsap.timeline({repeat:-1})
            const tlTentacle2 = gsap.timeline({repeat:-1})
            const tlTentacle3 = gsap.timeline({repeat:-1})
            const p1 = document.getElementById(back ? '1background'+back : '1')
            const p2 = document.getElementById(back ? '2background'+back : '2')
            const p3 = document.getElementById(back ? '3background'+back : '3')

            tlTentacle1.set(p1,{
                rotate: 0,
                y:0,
                x:0,
                overwrite: true
            })

            let x = back ? "+=5" : "-=15"
            let y =  back ? "-=0" : "-=5"
            tlTentacle1.to(p1, {
                rotate: 5,
                x: x,
                y: y,
                duration: 2
            })
            tlTentacle1.to(p1,{
                rotate: 0,
                y:0,
                x:0,
                duration:2
            })

            tlTentacle2.set(p2,{
                rotate: 0,
                y:0,
                x:0,
                overwrite:true
            })
            tlTentacle2.to(p2, {
                rotate: -5,
                x: "+=5",
                y: "+=0",
                duration:3
            })
            tlTentacle2.to(p2, {
                rotate: 3,
                x: "+=5",
                y: "+=0",
                duration:3
            })
            tlTentacle2.to(p2,{
                rotate: 0,
                y:0,
                x:0,
                duration:1
            })

            tlTentacle3.set(p3,{
                rotate: 0,
                y:0,
                x:0,
                overwrite:true
            })
            x = back ? "+=5" : "-=5"
            y =  back ? "-=5" : "-=5"
            tlTentacle3.to(p3, {
                rotate: -7,
                x: x,
                y:y,
                duration:1
            })
            tlTentacle3.to(p3,{
                rotate: 0,
                y:0,
                x:0,
                duration:3
            })

            tlTotalTentacles.addLabel('start',0)
            tlTotalTentacles.add(tlTentacle1, 'start')
            tlTotalTentacles.add(tlTentacle2, 'start')
            tlTotalTentacles.add(tlTentacle3, 'start')
            return tlTotalTentacles
        },
        jellyFishLife(back=null) {
            if (!back && this.fish !== 1) {
                return this.animationLife()
            }
            const tlParts = gsap.timeline()
            const tl1 = gsap.timeline({repeat:-1})
            const tl2 = gsap.timeline({repeat:-1})
            const tl3 = gsap.timeline({repeat:-1})
            const p1 = document.getElementById(back ? '1background'+back : '1')
            const p2 = document.getElementById(back ? '2background'+back : '2')
            const p3 = document.getElementById(back ? '3background'+back : '3')

            tl1.set(p1,{
                rotate:0,
                y:0,
                overwrite: true
            })
            tl1.to(p1,{
                rotate:5,
                y:"-=15",
                duration:2
            })
            tl1.to(p1,{
                rotate:-4,
                y:"-=15",
                x:"+=10",
                duration:2
            })
            tl1.to(p1, {
                rotate:0,
                y:0,
                x:0,
                duration:3
            })

            tl2.set(p2,{
                rotate:0,
                y:0,
                overwrite:true
            })
            tl2.to(p2,{
                rotate:-5,
                y:"-=10",
                duration:2
            })
            tl2.to(p2,{
                rotate:5,
                y:"-=10",
                duration:3
            })
            tl2.to(p2, {
                rotate:0,
                y:0,
                duration:4
            })

            tl3.from(p3,{
                rotate:0,
                y:0,
                x:0,
                overwrite:true
            })
            tl3.to(p3,{
                rotate:5,
                y:"-=15",
                x:"-=15",
                duration:2
            })
            tl3.to(p3,{
                rotate:-5,
                y:"-=15",
                x:"+=15",
                duration:1
            })
            tl3.to(p3, {
                rotate:0,
                y:0,
                x:0,
                duration:2
            })
            tlParts.addLabel('start',0)
            tlParts.add(tl1, 'start')
            tlParts.add(tl2, 'start')
            tlParts.add(tl3, 'start')
            return tlParts
        },
        hideAnim() {
            const fish = document.getElementById('fish')
            const tl = gsap.timeline({onComplete: () => {this.newAnim('')}})
            if (fish) {
                tl.to(fish, {
                    opacity:0.2,
                    duration: 5,
                })
                tl.to(fish, {
                    opacity:0.8,
                    duration: 3
                })
                tl.to(fish, {
                    opacity:1
                })
            }
        },
        repro() {
            const fish = document.getElementById('fish')
            const love = document.getElementById('love')
            const tl = gsap.timeline({})
            tl.addLabel('start')
            if (fish) {
                tl.to(fish, {
                    x: "-=50",
                    duration: 5,
                },'start')
                tl.to(love, {
                    x:"+=623",
                    duration: 3
                }, 'start')

                tl.addLabel('next')
                tl.to(fish, {
                    x:0,
                    duration:2
                }, 'next')
                tl.to(love, {
                    x:0,
                    duration: 3,
                    onComplete: () => {this.newAnim('')}
                }, 'next')
            }
        },
        crevetteLife(back=null) {
            if (!back && this.fish !== 6) {
                return this.animationLife()
            }
            const fin = document.getElementById(back ? '1background'+back : '1')
            const tlFin = gsap.timeline({repeat:-1})
            tlFin.set(fin,{
                rotate: 0,
                y:0,
                x:0,
            })
            tlFin.to(fin, {
                rotate: 3,
                y: back ? "-=2" :"-=5"
            })
            tlFin.to(fin,{
                rotate: -8,
                y:back ? "+=10" : "+=15",
                x:"-=4"
            })
            tlFin.to(fin,{
                rotate: 0,
                y:0,
                x:0
            })
            return tlFin
        },
        lenterneLife(back=null) {
            if (!back && this.fish !== 4) {
                return this.animationLife()
            }
            const tlA = gsap.timeline({overwrite:true})
            const lent = document.getElementById(back ? '1background'+back : '1')
            const fin = document.getElementById(back ? '2background'+back : '2')

            const tlFin = gsap.timeline({repeat:-1})
            const tlL = gsap.timeline({repeat:-1})
            tlL.set(lent, {
                rotate:0,
                y:0,
                x:0,
                overwrite: true
            })
            let x = back ? "-=8" : "-=5"
            let y = back ? "+=8" : "+=15"
            tlL.to(lent, {
                rotate: 5,
                y:y,
                x: x,
                duration: 1
            })
            y = back ? "-=17" : "-=20"
            tlL.to(lent, {
                rotate:-5,
                y: y,
                x:"+=18",
                duration:2
            })

            tlL.to(lent, {
                rotate:0,
                y:0,
                x:0,
                duration: 1
            })

            tlFin.set(fin,{
                rotate: 0,
                y:0,
                overwrite: true
            })
            y = back ? "-=8" : "-=23"
            tlFin.to(fin, {
                rotate: 8,
                y: y,
                duration: 3
            })

            y = back ? "+=17" : "+=50"
            tlFin.to(fin,{
                rotate: -10,
                y:  y,
                duration: 2
            })

            tlFin.to(fin,{
                rotate: 0,
                y:0, 
                ease:"none",
                duration: 2
            })
            tlA.addLabel('s')
            tlA.add(tlFin, 's')
            tlA.add(tlL, 's')
            return tlA
        },
        chase() {
            const fish = document.getElementById('fish')
            const proie = document.getElementById('proie')
            const tl = gsap.timeline({onComplete: () => {this.newAnim('')}})
            tl.addLabel('start')
            if (fish) {
                tl.to(fish, {
                    x: "-=50",
                    duration: 5,
                },'start')
                let x = this.fish === 3 ? '+=580' : "+=490"
                tl.to(proie, {
                    x: x,
                    duration: 3
                }, 'start')

                tl.addLabel('next')
                x = this.fish === 3 ? '-=205' : "-=225"
                let y = this.fish === 3 ? '-=210' : "-=200"
                tl.to(fish, {
                    x:x,
                    rotate: 10,
                    y:y,
                    duration:2
                }, 'next')
                tl.addLabel('end')
                tl.to(proie, {
                    opacity:0,
                    duration: 1
                }, 'end')
                tl.set(proie, {
                    x:0,
                    y:0,
                    opacity: 1
                })
                tl.to(fish, {
                    x:0,
                    y: 0,
                    rotate:0,
                    duration:3
                })
            }
        },
        defence() {
            const tlAll = gsap.timeline()
            const fish = document.getElementById('fish')
            const pre = document.getElementById('pre')
            const tl = gsap.timeline({onComplete: () => {
                this.time = 2
                this.newAnim('')
            }})
            tl.addLabel('start')
            tl.to(fish, {
                x: "-=50",
                duration: 5
            },'start')
            tl.to(pre, {
                x:"-=500",
                duration: 3,
            }, 'start')

            tl.addLabel('next')
            tl.to(fish, {
                x:"-=1000",
                duration:1,
                delay:0.25
            }, 'next')
            tl.to(pre, {
                x:"-=2500",
                duration: 3
            }, 'next')
            tl.addLabel('end')
            tl.set(fish, {
                x:0,
                y: "-=1200"
            }, 'end')

            tl.to(fish, {
                x:0,
                y: 0,
                duration:3
            })

            tl.set(pre, {
                x:0
            })

            tlAll.addLabel('start')
            tlAll.add(tl, 'start')
        },
        cycleBackground(fish) {
            const tl = gsap.timeline()
            const x = this.randomIntFromInterval(-800, 800)
            const y = this.randomIntFromInterval(-600, 500)

            let deltaX = x - fish.getBoundingClientRect().x
            let deltaY = y - fish.getBoundingClientRect().y

            let angleInRadians = (Math.atan2(-deltaY, -deltaX))
            let angleInDegrees = angleInRadians * (180 / Math.PI)
            let rotate = (x < 0 || y < 0) ? -angleInDegrees : angleInDegrees

            tl.to(fish, {
                    x: x,
                    y: y,
                    ease: "power1.inOut",
                    rotate: rotate,
                    duration: gsap.utils.random(5, 10),
                    overwrite: true
            }, 'start')

            tl.to(fish, {
                x:0,
                y:0,
                rotate: 0,
                duration: gsap.utils.random(5,10),
                onComplete: () => {this.cycleBackground(fish)}

            })
        },
        randomIntFromInterval(min, max) {
            return Math.floor(Math.random() * (max - min + 1) + min)
        }
    }
}

</script>

<style>

.head_1 {
    mask-image: url('/fishImg/1/head.png');
}

.part1_1 {
    mask-image: url('/fishImg/1/leg1.png');
}

.part2_1 {
    mask-image: url('/fishImg/1/leg2.png');
}

.part3_1 {
    mask-image: url('/fishImg/1/leg3.png');
}

.head_2 {
    mask-image: url('/fishImg/2/head.png');
}

.eyes_2 {
    mask-image: url('/fishImg/2/eyes.png');
}

.part1_2 {
    mask-image: url('/fishImg/2/part1.png');
}

.part2_2 {
    mask-image: url('/fishImg/2/part2.png');
}

.part3_2 {
    mask-image: url('/fishImg/2/part3.png');
}

.part4_2 {
    mask-image: url('/fishImg/2/part4.png');
}

.head_3 {
    mask-image: url('/fishImg/3/head.png');
}

.eyes_3 {
    mask-image: url('/fishImg/3/eyes.png');
}

.part1_3 {
    mask-image: url('/fishImg/3/part1.png');
}

.part2_3 {
    mask-image: url('/fishImg/3/part2.png');
}

.part3_3 {
    mask-image: url('/fishImg/3/part3.png');
}

.head_4 {
    mask-image: url('/fishImg/4/head.png');
}

.eyes_4 {
    mask-image: url('/fishImg/4/eyes.png');
}

.part1_4 {
    mask-image: url('/fishImg/4/part1.png');
}

.part2_4 {
    mask-image: url('/fishImg/4/part2.png');
}

.head_5 {
    mask-image: url('/fishImg/5/head.png');
}

.part1_5 {
    mask-image: url('/fishImg/5/part1.png');
}

.head_6 {
    mask-image: url('/fishImg/6/head.png');
}

.part1_6 {
    mask-image: url('/fishImg/6/part1.png');
}

.masked {
    mask-repeat: no-repeat;
    position: absolute;
}

.head {
    z-index: 3;
}

#fish {
    position: absolute;
    top: 25vh;
    left: 25vw;
}

#love {
    transform: scaleX(-1);
    position: absolute;
    top: 25vh;
    left: -20vw;
    z-index: 2;
}

#loveImg {
    width: 20vw;
    height: 20vw;
}

#proie {
    transform: scaleX(-1);
    position: absolute;
    top: 35vh;
    left: -10vw;
}

#proieImg {
    width: 10vw;
    height: 10vw;
}

#pre {
    position: absolute;
    top: 10vh;
    right: -50vw;
    z-index: 2;
}

#preImg {
    width: 50vw;
}

#background-video {
    height: 100vh;
    width: 100vw;
    object-fit: cover;
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: -1;
}

.backFishies {
    mask-position: center;
    mask-size: 100%;
}

.backFishiesDiv {
    position: relative;
    width: 20vh;
    filter: blur(1px);
}

.backFishiesContain {
    display: flex;
    height:100vh;
    justify-content: center;
    align-items: center;
}

.hB {
    z-index: 1;
}

.small1 {
    width: 20vw;
}

.small2 {
    width: 20vw;
}

.small3 {
    width: 18vw;
}

.small4 {
    width: 18vw;
}

.small5 {
    width: 10vw;
}
.small6 {
    width: 10vw;
}
</style>

<style>
body {
    background-color:cornflowerblue;
    width: 100vw;
    height: 100vh;
}
</style>