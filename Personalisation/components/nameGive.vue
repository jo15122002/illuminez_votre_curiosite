<template>
    <div class="background" :style="'background:'+colorCode">
        <div class="back" >
            <button @click="stay(false)" class="return" :style="'background:'+colorCode"></button>
            <div class="nameDiv">
                <div class="textName">
                    <p class="title">Prénom</p>
                    <p class="text">Donne le prénom de ton choix à l’être vivant que tu as choisi.</p>
                </div>
                <input v-model="input" class="nameInput" :style="'background-color:rgba('+colors.join()+',0.2)'" @focus="keyboardOpen = true">
                <div class="line" :style="'background:'+colorCode"></div>

                <button @click="stay(true)" class="nextN" :style="'background:'+colorCode">Valider</button>
            </div>
            <div class="simple-keyboard" :style="keyboardOpen ? '': 'display:none'"></div>
        </div>
    </div>
</template>

<script>
import Keyboard from "simple-keyboard";
import "simple-keyboard/build/css/index.css";
import {useCounterStore} from '@/store/index'
import { mapState } from 'pinia'

export default {
    name: 'NameGive',
    props: {
        fish: {
            type:Number
        }
    },
    data() {
        return {
            keyboard: null,
            input: null,
            keyboardOpen: false
        }
    },
    computed: {
    ...mapState(useCounterStore, ['color']),
        colors() {
            return this.color(this.fish)
        },
        colorCode() {
            return 'rgb('+this.colors.join(',')+')'
        }
    },
    mounted() {
        this.keyboard = new Keyboard('simple-keyboard', {
            onChange: this.onChange,
            onKeyPress: this.onKeyPress,
            theme: "hg-theme-default hg-theme-ios key",
            layout: {
                default: [
                "a z e r t y u i o p {bksp}",
                "q s d f g h j k l m {enter}",
                "{shift} w x c v b n , . {shift}",
                "{alt} {smileys} {space} {altright} {downkeyboard}"
                ],
                shift: [
                "A Z E R T Y U I O P {bksp}",
                "Q S D F G H J K L M {enter}",
                "{shiftactivated} W X C V B N , . {shiftactivated}",
                "{alt} {smileys} {space} {altright} {downkeyboard}"
                ],
                alt: [
                "1 2 3 4 5 6 7 8 9 0 {bksp}",
                `@ # $ & * ( ) ' " {enter}`,
                "{shift} % - + = / ; : ! ? {shift}",
                "{default} {smileys} {space} {back} {downkeyboard}"
                ],
                smileys: [
                "😀 😊 😅 😂 🙂 😉 😍 😛 😠 😎 {bksp}",
                `😏 😬 😭 😓 😱 😪 😬 😴 😯 {enter}`,
                "😐 😇 🤣 😘 😚 😆 😡 😥 😓 🙄 {shift}",
                "{default} {smileys} {space} {altright} {downkeyboard}"
                ]
            },
            display: {
                "{alt}": ".?123",
                "{smileys}": "\uD83D\uDE03",
                "{shift}": "⇧",
                "{shiftactivated}": "⇧",
                "{enter}": "↲",
                "{bksp}": "⌫",
                "{altright}": ".?123",
                "{downkeyboard}": "🞃",
                "{space}": " ",
                "{default}": "ABC",
                "{back}": "⇦"
            }
        })
    },
    methods: {
        stay(stay) {
            this.$emit('named', {stay: stay, name:this.input})
        },
        onChange(input) {
            this.input = input
        },
        onKeyPress(button) {
            if (button.includes("{") && button.includes("}")) {
                this.handleLayoutChange(button);
            }
        },
        handleLayoutChange(button) {
            let currentLayout = this.keyboard.options.layoutName;
            let layoutName;

            switch (button) {
                case "{shift}":
                case "{shiftactivated}":
                case "{default}":
                    layoutName = currentLayout === "default" ? "shift" : "default";
                    break;

                case "{alt}":
                case "{altright}":
                    layoutName = currentLayout === "alt" ? "default" : "alt";
                    break;

                case "{smileys}":
                    layoutName = currentLayout === "smileys" ? "default" : "smileys";
                    break;
                case "{downkeyboard}":
                    this.keyboardOpen = false

                default:
                break;
            }

            if (layoutName) {
                this.keyboard.setOptions({
                    layoutName: layoutName
                });
            }
        }
    },
    watch: {
        input(input) {
            this.keyboard.setInput(input)
        }
    }
}
</script>

<style>
.nextN {
    border: none;
    border-radius: 40px;
    color: white;
    font-size: 48px;
    font-weight: bold;
    width: 261px;
    height: 104px;
    font-family: 'Red Hat Display', sans-serif;
    position: absolute;
    top: 611px;
}

.background {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.nameDiv {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    align-items: center;
    position: absolute;
    top: 348px;
    left: 445px;
    text-align: center;
}

.nameInput {
    border: none;
    border-radius: 20px;
    height: 191px;
    width: 835px;
    font-size: 34px;
    font-family: 'Red Hat Display', sans-serif;
    position: absolute;
    top: 362px;
    text-align: center;
}
.title {
    font-size: 90px;
    font-family: bast;
    margin: 0;
}

.text {
    font-family: 'Red Hat Display', sans-serif;
    font-size: 34px;
    margin: 0;
}

.line {
    position: absolute;
    top: 519.5px;
    height: 5px;
    width: 746px;
}

.textName {
    width: 1019px;
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.key {
    position: absolute;
    bottom: 0;
    height: 26.5vh;
    font-size: 2rem;
}

 .hg-theme-default .hg-button {
    height: 6vh;
}

.simple-keyboard {
    width: 100vw;
    height: 26vh;
    position: absolute;
    bottom: -62px;
}
</style>

<style scoped>
.return {
    mask-image: url('/icon/returnPage.png');
    mask-size: 50%;
    mask-position: center;
    mask-repeat: no-repeat;
}
</style>