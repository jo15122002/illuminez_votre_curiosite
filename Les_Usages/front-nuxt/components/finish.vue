<template>
    <div class="backfish">
      <div class="text">
          <h1 class="finishTitle">Quel expert !</h1>
          <p class="finsihText">Tu as terminé l’activité, tu peux ajouter la lettre dans ton carnet.</p>
          <div class="lettreU"><p>U</p></div>
      </div>
      <button class="bStart" @click="startG">Recommencer</button>
  </div>
</template>

<script>
export default {
    name:'Finish',
    methods: {
      startG() {
        this.$emit('startGame')
      }
    }

}
</script>

<style>

.title {
    font-size: 3rem;
}

.lettreU {
  background: #3AA098;
  width: 70px;
  height: 70px;
  text-align: center;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Red Hat Display', sans-serif;
  font-weight: bold;
  font-size: 1.5rem;
}

.finsihText {
  font-size:2rem;
  font-family: 'Red Hat Display', sans-serif;
  width: 500px;
}

.finishTitle {
  font-size:3rem;
  font-family:bast
}
</style>

<style scoped>
body {
    z-index: 2;
}

</style>