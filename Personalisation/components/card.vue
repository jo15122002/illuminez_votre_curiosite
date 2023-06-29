<template>
  <div class="background" :style="'background: '+colorCode">
    <div class="back">
        <button @click="stay(false)" class="return" :style="'background:'+colorCode"></button>
        <button @click="stay(true)" class="next" :style="'background:'+colorCode">Commencer</button>
        <div class="txtCard">
            <div class="names" :style="'background:rgba('+color.join()+',0.2);width:'+fishInfo.widthName">
                <h1 class="name">{{fishInfo.name}}</h1>
                <p class="latin">{{ fishInfo.latin }}</p>
            </div>

            <div class="cardInfo">
                <div class="identity" :style="'background-color:rgba('+color.join()+',0.2)'">
                    <div class="cardIcon"></div>
                    <p class="identityTitle">Carte d’identité</p>
                </div>

                <div class="datas">
                    <div v-for="(data, index) in fishCard" :key="index" class="cardData">
                        <p class="dataTitle">{{ data }}</p>
                        <p class="dataInfo">{{ fishInfo[data] }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="exemple">
            <img class="imgEx" :src="'fishImg/'+fish+'/ex.png'">
        </div>
    </div>
  </div>
</template>

<script>
import {useCounterStore} from '@/store/index'
import { mapState } from 'pinia'

export default {
    name: 'Card',
    props: {
        fish: {
            type: Number
        }
    },
    data() {
        return {
            fishies: {
                1: {
                    name: 'La méduse',
                    latin: 'Aequorea Victoria',
                    Usage: 'Se protèger',
                    Taille: '10 centimètres',
                    Repas: 'Micro Plancton',
                    Lieu: 'Côte Ouest - Amérique du Nord',
                    Prédateurs: 'Môle, Poisson lune',
                    widthName: '835px'
                },
                2: {
                    name: 'Le calamar',
                    latin: 'histioteuthis heteropsis',
                    Usage: 'Se camoufler',
                    Taille: '10 et 20 centimètres',
                    Repas: "Petits poissons et d'autres invertébrés",
                    Profondeur: '200 à 1 500 mètres',
                    Prédateurs: "Grands poissons ou d'autres céphalopodes",
                    widthName: '728px'
                },
                3 : {
                    name: 'La pieuvre',
                    latin: 'Stauroteuthis syrtensis',
                    Usage: 'Chasser',
                    Taille: '10 à 15 centimètres',
                    Repas: 'Petits poissons, crevettes, méduses',
                    Profondeur: '1 000 à 4 000 mètres',
                    Prédateurs: "Grands poissons ou d'autres céphalopodes",
                    widthName: '835px'
                },
                4: {
                    name: 'La baudroie abyssale',
                    latin: 'Melanocetus johnsonii',
                    Usage: 'Chasser',
                    Taille: '18 centimètres',
                    Repas: 'Crustacés et petits poisssons',
                    Profondeur: 'Entre 300 et 2500 mètres',
                    Prédateurs: 'Dragon des mers, Poisson ogre, Poisson vipère',
                    widthName: '1224px'
                },
                5: {
                    name: 'Le poisson pilote',
                    latin: 'Gymnoscopelus',
                    Usage: 'Se protèger',
                    Taille: '5 et 15 centimètres',
                    Repas: 'Plancton',
                    Profondeur: '200 et 1 000 mètres',
                    Prédateurs: 'Oiseaux marins et mammifères marins',
                    widthName: '1017px'
                }, 
                6: {
                    name: 'La crevette pélagique',
                    latin: 'Sergestidae',
                    Usage: 'Se reproduire',
                    Taille: '2 et 5 centimètres',
                    Repas: 'Zooplancton',
                    Profondeur: '200 mètres',
                    Prédateurs: 'Oiseaux marins et mammifères marins',
                    widthName: '1239px'
                }
            },
            cardData: ['Usage', 'Taille', 'Repas', 'Lieu', 'Profondeur', 'Prédateurs']
        }
    },
    computed: {
        ...mapState(useCounterStore, {colors:'color'}),
        fishInfo() {
            return this.fishies[this.fish]
        },
        color() {
            return this.colors(this.fish)
        },
        colorCode() {
            return 'rgb('+this.color.join(',')+')'
        },
        fishCard() {
            return this.cardData.filter((data) => Object.keys(this.fishInfo).includes(data))
        }
    },
    methods: {
        stay(stay) {
            this.$emit('read', stay)
        }
    }
}
</script>

<style>
.return {
    border: none;
    background-color: transparent;
    width: 337px;
    height: 200px;
    position: absolute;
    top: 12px;
    left: -7px;
    mask-image: url('/icon/return.svg');
    mask-size: cover;
}

.next {
    border: none;
    border-radius: 60px;
    color: white;
    width: 380px;
    height: 104px;
    position: absolute;
    top: 60px;
    left: 1475px;
    font-size: 48px;
    font-family: 'Red Hat Display', sans-serif;
    font-weight: bold;
    z-index: 4;
}

.background {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
}

.names {
    height: 266px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: absolute;
    left: 93px;
    top: 322px;
}

.name {
    font-family: bast;
    font-size: 90px;
    color: #02295F;
    position: absolute;
    left: 69px;
    top: 46px;
    margin: 0;
    width: max-content;
}

.latin {
    margin: 0;
    font-size: 32px;
    font-family: 'Red Hat Display', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    position: absolute;
    top: 172px;
    left: 69px;
}

.cardInfo {
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
}

.identity {
    display: flex;
    align-items: center;
    position: absolute;
    left: 93px;
    top: 634px;
    height: 111px;
    width: 114px;
    border-radius: 20px;

}

.cardIcon {
    background-image: url('/icon/card.png');
    height: 111px;
    width: 114px;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 20px;
    padding-top: 2rem;
}

.identityTitle {
    font-weight: bold;
    font-size: 44px;
    margin:0;
    text-transform: uppercase;
    position: absolute;
    left: 175px;
    width: 486px;
}

.cardData {
    display: flex;
    align-items: center;
}

.dataTitle {
    font-weight: bold;
    font-size: 32px;
    margin: 0;
}

.dataInfo {
    position: absolute;
    left: 237px;
    font-weight: 600;
    font-size: 32px;
    width: fit-content;
    margin: 0;
}

.datas {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 433px;
    width: fit-content;
    min-width: 1000px;
    position: absolute;
    left: 93px;
    top: 791px;
}

.exemple {
    position: absolute;
    top: 45px;
    right: 0vw;
}
</style>

<style scoped>
p {
    color: #02295F;
    font-family: 'Red Hat Display', sans-serif;
}
</style>