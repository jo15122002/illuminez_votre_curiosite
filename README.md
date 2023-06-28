# Illuminez votre curiosité

This repository contains the source code for the "Illuminate Your Curiosity" project. The project is structured into several folders and files, each having a specific role in the overall functioning of the project.

## Project Structure

Here is a description of the project structure:

- **ESP32/Activite1**: This folder contains the Python scripts for the ESP32 microcontroller. It includes the `boot.py`, `main.py` files. `main.py` is the file that will be sent to the ESP32.

- **Proximity_sensor**: This folder contains the Python scripts for the proximity sensor for the scenographic elements. It includes the `meduse.py`, `poulpe.py`, and `proximity_sensor.py` files.

- **Reaction_Chimique**: This folder contains the Python scripts for Activity 1. It includes the `reaction_chimique.py` file.

## Installation

To install and run this project, you will need Python and some dependencies. You can install the dependencies using pip:

```
pip install -r requirements.txt
```

You will also need to install:
- The VsCode extension [PyMakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr)
- The driver [CP210X](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=overview)
- [esptools](https://github.com/espressif/esptool/)

## Usage

To use this project, you will need to send the program to the ESP32:

## 1. Flash an ESP32 with MicroPython

1. **Installation of esptool**: esptool is a Python utility to communicate with the ESP8266 and ESP32 ROM bootloader. You can install it with pip:

    ```
    pip install esptool
    ```

2. **Download the MicroPython firmware**: You can download the latest MicroPython firmware for the ESP32 from the [official MicroPython website](https://micropython.org/download/esp32/). Make sure to choose the right firmware based on the availability of the SPIRAM chip on your ESP32 module.

3. **Erase the flash**: Before flashing the new firmware, it is recommended to erase the ESP32's flash. Connect your ESP32 to your computer via the micro USB cable, then run the following command in your terminal:

    ```
    esptool.py --chip esp32 erase_flash
    ```

    If you encounter problems identifying the ESP32's port, you can list all available ports with the command `python -m serial.tools.list_ports` on Windows or `ls /dev/tty.*` on macOS and Linux.

4. **Flashing the MicroPython firmware**: Once the flash is erased, you can flash the MicroPython firmware you downloaded. Replace `firmware.bin` with the path to the firmware file you downloaded:

    ```
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin
    ```

    Replace `/dev/ttyUSB0` with your ESP32's port.

5. **Installation verification (optional)**: You can verify that MicroPython was installed correctly by connecting to the ESP32 via a serial terminal. You can use Python's pyserial module for this:

    ```
    pip install pyserial
    python -m serial.tools.miniterm /dev/ttyUSB0 115200
    ```

    Replace `/dev/ttyUSB0` with your ESP32's port. Once connected, you should see a `>>>` prompt. You can try typing Python code here, for example, `print("Hello, World!")`.

## 

## 2. Set Up PyMakr

1. **Install the PyMakr extension**: Open Visual Studio Code, click on the extensions icon in the sidebar, search for "PyMakr" and click "Install".

2. **Configure the PyMakr extension**: After installing the extension, you may need to configure your device's serial port. Open the PyMakr configuration file by clicking on "File" > "Preferences" > "Settings", then search for "PyMakr". Enter your device's serial port name in the "autoconnect comport" field.

3. **Connect to the device**: Connect your device to your computer via the micro USB cable. In Visual Studio Code, open the terminal view (View > Terminal) and you should see a PyMakr terminal. Click the "Connect" button in the PyMakr terminal to connect to your device.

4. **Write code**: You can now write Python code in Visual Studio Code. To run your code on the device, click the "Run" button in the PyMakr terminal.

5. **Upload files to the device**: You can upload files to your device by clicking the "Upload" button in the PyMakr terminal. Select the files you want to upload and they will be transferred to your device.

6. **Retrieve files from the device**: You can also retrieve files from your device by clicking the "Download" button in the PyMakr terminal. Select the files you want to download and they will be transferred to your computer.

## 3. Start Coding
All that's left is to code in Python in the main.py file and send it to the ESP32 for execution.
