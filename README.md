# Illuminez votre curiosité

Ce dépôt contient le code source pour le projet "Illuminez votre curiosité". Le projet est structuré en plusieurs dossiers et fichiers, chacun ayant un rôle spécifique dans le fonctionnement global du projet.


## Structure du projet

Voici une description de la structure du projet :

- **ESP32/Activite1** : Ce dossier contient les scripts Python pour le microcontrôleur ESP32. Il comprend les fichiers `boot.py`, `main.py`. `main.py` est le fichier qui sera envoyé à l'ESP32.

- **Proximity_sensor** : Ce dossier contient les scripts Python pour le capteur de proximité pour les éléments de scénographie. Il comprend les fichiers `meduse.py`, `poulpe.py` et `proximity_sensor.py`.

- **Reaction_Chimique** : Ce dossier contient les scripts Python pour l'activité 1. Il comprend le fichier `reaction_chimique.py`.


## Installation

Pour installer et exécuter ce projet, vous aurez besoin de Python et de certaines dépendances. Vous pouvez installer les dépendances en utilisant pip :

```
pip install -r requirements.txt
```

Il faudra également installer :
- l'extension VsCode [PyMakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr)
- le driver [CP210X](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=overview)
- [esptools](https://github.com/espressif/esptool/)

## Utilisation

Pour utiliser ce projet, vous devrez envoyer le programme dans l'ESP32 :

## 1. Flasher un ESP32 avec MicroPython

1. **Installation de esptool** : esptool est un utilitaire Python pour communiquer avec le bootloader ROM de l'ESP8266 et l'ESP32. Vous pouvez l'installer avec pip :

    ```
    pip install esptool
    ```

2. **Téléchargement du firmware MicroPython** : Vous pouvez télécharger le dernier firmware MicroPython pour l'ESP32 depuis le [site officiel de MicroPython](https://micropython.org/download/esp32/). Assurez-vous de choisir le bon firmware en fonction de la disponibilité de la puce SPIRAM sur votre module ESP32.

3. **Effacement du flash** : Avant de flasher le nouveau firmware, il est recommandé d'effacer le flash de l'ESP32. Connectez votre ESP32 à votre ordinateur via le câble micro USB, puis exécutez la commande suivante dans votre terminal :

    ```
    esptool.py --chip esp32 erase_flash
    ```

    Si vous rencontrez des problèmes pour identifier le port de l'ESP32, vous pouvez lister tous les ports disponibles avec la commande `python -m serial.tools.list_ports` sur Windows ou `ls /dev/tty.*` sur macOS et Linux.

4. **Flashing du firmware MicroPython** : Une fois le flash effacé, vous pouvez flasher le firmware MicroPython que vous avez téléchargé. Remplacez `firmware.bin` par le chemin vers le fichier de firmware que vous avez téléchargé :

    ```
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin
    ```

    Remplacez `/dev/ttyUSB0` par le port de votre ESP32.

5. **Vérification de l'installation (optionnel)** : Vous pouvez vérifier que MicroPython a été correctement installé en vous connectant à l'ESP32 via un terminal série. Vous pouvez utiliser le module pyserial de Python pour cela :

    ```
    pip install pyserial
    python -m serial.tools.miniterm /dev/ttyUSB0 115200
    ```

    Remplacez `/dev/ttyUSB0` par le port de votre ESP32. Une fois connecté, vous devriez voir un prompt `>>>`. Vous pouvez essayer de taper du code Python ici, par exemple `print("Hello, World!")`.

## 2. Mettre en place PyMakr

1. **Installation de l'extension PyMakr** : Ouvrez Visual Studio Code, cliquez sur l'icône des extensions dans la barre latérale, recherchez "PyMakr" et cliquez sur "Install".

2. **Configuration de l'extension PyMakr** : Après l'installation de l'extension, vous devrez peut-être configurer le port série de votre appareil. Ouvrez le fichier de configuration PyMakr en cliquant sur "File" > "Preferences" > "Settings", puis recherchez "PyMakr". Entrez le nom du port série de votre appareil dans le champ "autoconnect comport".

3. **Connexion à l'appareil** : Connectez votre appareil à votre ordinateur via le câble micro USB. Dans Visual Studio Code, ouvrez la vue du terminal (View > Terminal) et vous devriez voir un terminal PyMakr. Cliquez sur le bouton "Connect" dans le terminal PyMakr pour vous connecter à votre appareil.

4. **Écriture de code** : Vous pouvez maintenant écrire du code Python dans Visual Studio Code. Pour exécuter votre code sur l'appareil, cliquez sur le bouton "Run" dans le terminal PyMakr.

5. **Téléchargement de fichiers sur l'appareil** : Vous pouvez télécharger des fichiers sur votre appareil en cliquant sur le bouton "Upload" dans le terminal PyMakr. Sélectionnez les fichiers que vous souhaitez télécharger et ils seront transférés sur votre appareil.

6. **Récupération de fichiers depuis l'appareil** : Vous pouvez également récupérer des fichiers depuis votre appareil en cliquant sur le bouton "Download" dans le terminal PyMakr. Sélectionnez les fichiers que vous souhaitez télécharger et ils seront transférés sur votre ordinateur.


##3. Commencer à coder
Il ne vous reste plus qu'a coder en python dans le fichier main.py et l'envoyer sur l'ESP32 pour l'executer
