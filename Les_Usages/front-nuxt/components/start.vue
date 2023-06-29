<template>
  <div class="backfish">
    <div class="text">
        <h1 style="font-size:4rem; font-family:bast">Pourquoi utiliser la bioluminescence ?</h1>
        <p style="font-size:2rem; font-family: 'Red Hat Display', sans-serif;">À ton tour de relier l'être vivant<br> à l'usage qui lui correspond.</p>
    </div>
    <button class="bStart" @click="startG">Commencer</button>
  </div>
</template>

<script>
export default {
    name:"StartGame",
    methods: {
        startG() {
            this.$emit('startGame')
        }
    }

}
</script>

<style>
.backfish {
    background-image: url('/back/backgroundS.png');
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    background-size: 100%;
    background-position: center;
    background-color: #02295F; 
    z-index: 2;
}

.text {
    width: 1000px;
    margin-left: 5rem;
    margin-top: 5rem;
    color: #FEFCF8;
}

.bStart {
    background-color: #B0D0E1;
    position: absolute;
    bottom: 3rem;
    right: 3rem;
    border:none;
    padding: 10px;
    padding-left: 25px;
    padding-right: 25px;
    border-radius: 25px;
    font-size: 1.5rem;
    font-style: bold;
    color:white;
    font-family: 'Red Hat Display', sans-serif;
    font-weight: bold;
}

@font-face {
  font-family: bast;
  src: url('/font/Basteleur-Bold.woff');
}
</style>

<style scoped>
body {
    z-index: 2;
}
</style>