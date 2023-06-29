# Les Usages de la reaction chimique

Une activité pour apprendre pourquoi la bioluminescence est utilisée.

## Esp 32

1. boot.py connect Esp 32 to Internet

```py
# change to connect to chosen wifi

SSID = "Your Wifi"
SSI_PASSWORD = "Your Wifi Password"

```
2. main.py create websocket server

3. animals.py contains animals, uses, pins for the leds, color of leds


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