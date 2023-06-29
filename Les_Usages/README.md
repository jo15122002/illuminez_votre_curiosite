# Les Usages de la reaction chimique

Une activité pour apprendre pourquoi la bioluminescence est utilisée.

## Esp 32

1. boot.py connecte l'Esp 32 à internet

```py
# change pour connecter au bon wifi

SSID = "Your Wifi"
SSI_PASSWORD = "Your Wifi Password"

```

2. main.py crée un server websocket

3. animals.py reference les animaux, les usage reliés, les pin associé au leds, la couleur des leds, et si la led est alumée et à quelle intencité


## Front

1. Interface pour relier

2. Connection au websocket

```js
// installation
cd /front_nuxt

npm i

npm start
```

Attention !
L'appareil sur le quel est le front doit être connecter au même wifi que l'Esp 32.

Le petit jeu ne demare pas si le websocket n'est pas connecté