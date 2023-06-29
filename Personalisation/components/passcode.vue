<template>
    <div class="background">
        <div class="back">
            {{ data }}
            <div class="txt">
                <p class="title">Code secret</p>
                <p class="sTitle">Trouve le code secret situé sur les cartes.</p>
            </div>
            <div class="code">
                <div v-for="touch in codesTouch" :key="touch.value">
                    <div :class="pass.includes(touch.value) ? 'touch used' : 'touch'" @click="add(touch.value)">
                        <img class="imgCode" :src="'/icon/code/'+touch.value+'.png'">
                    </div>
                </div>
            </div>
            <div class="saveRetryDiv">
                <div class="retry" @click="retry"></div>
                <div :class="isCode ? 'save codeTrue' : 'save'" @click="save"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Passcode',
    data() {
        return {
            pass: '',
            codes:[ 
                {
                    code: '254',
                    fish: 1
                },
                {
                    code: '642',
                    fish: 2
                },
                {
                    code: '645',
                    fish: 3
                },
                {
                    code: '625',
                    fish: 4
                },
                {
                    code: '541',
                    fish: 5
                },
                {
                    code: '362',
                    fish: 6
                }
            ],
            codesTouch: [
                {
                    value: 1
                },
                {
                    value: 2
                },
                {
                    value:3
                },
                {
                    value: 4
                },
                {
                    value: 5
                },
                {
                    value: 6
                }
            ]
        }
    },
    computed: {
        isCode() {
            let code = false
            this.codes.forEach((coded) => {
                if (coded.code === this.pass) {
                    code = true
                }
            })
            return code
        }
    },
    methods: {
        save() {
            let codeOk = false
            let fish = 0
            this.codes.forEach((code) => {
                if (code.code === this.pass) {
                    codeOk = true
                    fish = code.fish
                }
            })
            if (codeOk) {
                this.$emit('fish', fish)
            } else {
                this.pass = ''
            }
        },
        add(val) {
            if (!this.pass.includes(val)) {
                this.pass += val.toString()
            } else {
                this.pass = this.pass.replace(val, '')
            }
        },
        retry() {
            this.pass = ''
        }
    }
}
</script>

<style>
.nextN {
    z-index: 3;
}

.back{
    position: absolute;
    left: 69px;
    top: 62px;
    height: 1411px;
    width: 1910px;
    border-radius: 20px;
    background: #FEFCF8;
    z-index: 0;
    display: flex;
    justify-content: center;
}
</style>

<style scoped>
.background {
    background: #3AA098;
}

.code {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-content: space-between;
    align-items: center;
    width: 833px;
    height: 551px;
    position: absolute;
    top: 424px;
    z-index: 2;
}

.touch {
    background: #B0D0E1;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 263px;
    height: 263px;
}

.imgCode {
    overflow: auto;
}

.txt {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    align-items: center;
    position: absolute;
    top: 141px;
    height: 200px;
    width: 514px;
}

.saveRetryDiv {
    position: absolute;
    top: 1057px;
    left: 538px;
    width: 833px;
    height: 197px;
    display: flex;
    justify-content: space-between;
}

.save {
    background-image: url('/icon/check.png');
    background-position: center;
    background-size: 25%;
    background-repeat: no-repeat;
    width: 405.5px;
    height: 197px;
    background-color: rgba(58, 160, 152, 0.3);
    border-radius: 10px;
}

.retry {
    background-image: url('/icon/retry.png');
    background-position: center;
    background-size: 25%;
    background-repeat: no-repeat;
    width: 405.5px;
    height: 100%;
    background-color: #3AA098;
    border-radius: 10px;
}

.used {
    background: #02295F;
}

.title {
    font-family: bast;
    font-size: 90px;
    color: #02295F;
    width: 592px;
    margin: 0;
}

.sTitle {
    font-family: 'Red Hat Display', sans-serif;
    font-size: 34px;
    color: #02295F;
    font-weight: 600;
    width: 1019px;
    margin: 0;
}

.codeTrue {
    background-color: #3AA098;
}
</style>