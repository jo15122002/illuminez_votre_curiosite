import machine, neopixel
import math
import time
import random
import time

class LedStrip():
    def __init__(self, pin, number_of_leds, button_pin, extraLeds=0, extraLedBand = None, lastLedsBand = None, fishPart = None):
        self.pin = pin
        # self.number_of_leds = math.floor(band_length_in_meters * leds_per_meter)
        self.number_of_leds = number_of_leds
        self.np = neopixel.NeoPixel(machine.Pin(pin), self.number_of_leds)
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.lastTick = time.ticks_ms()
        self.is_right_answer = False
        self.extraLedBand = extraLedBand
        self.extraLeds = extraLeds
        self.lastLedsBand = lastLedsBand
        self.fishPart = fishPart
        self.stripColor = (255,255,255)
        self.isLit = False

        if(self.extraLedBand != None):
            self.offset = self.extraLedBand.number_of_leds - self.extraLeds
            if(extraLedBand == lastLedsBand):
                self.offset -= 4
        else:
            self.offset = 6
            self.extraLedBand = self
            self.extraLeds = self.number_of_leds - self.offset
            
            self.ledsOn = []
            self.ledsOff = []
            for i in range(self.number_of_leds):
                self.ledsOff.append({
                    "id": i,
                    "intensity": 0,
                    "color": (0,0,0)
                })
        
        self.set_strip_color((0,0,0), 1)
        self.show()

    def set_pixel_color(self, index, color, intensity=1.0):
        if(intensity > 1.0):
            intensity = 1.0
        if(intensity < 0.0):
            intensity = 0.0
        self.np[index] = (int(color[0]*intensity), int(color[1]*intensity), int(color[2]*intensity))
    
    def set_strip_color(self, color, intensity=1.0):
        if(intensity > 1.0):
            intensity = 1.0
        if(intensity < 0.0):
            intensity = 0.0
        self.np.fill((int(color[0]*intensity), int(color[1]*intensity), int(color[2]*intensity)))
    
    def show(self):
        self.np.write()
    
    def progressive_gradually_turn_on(self, color, delay, intensityStep):
        maxIntensity = 1
        if(time.ticks_ms() - self.lastTick > 10):
            if(self.button.value() == 0):
                if(len(self.ledsOff) > 0 ):
                    led = self.ledsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.show()

                    if(led not in self.ledsOn):
                        self.ledsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.ledsOff.pop(0)

                elif(len(self.extraLedsOff) > 0 and self.is_right_answer):
                    led = self.extraLedsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.extraLedBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.extraLedBand.show()

                    if(led not in self.extraLedsOn):
                        self.extraLedsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.extraLedsOff.pop(0)

                elif(len(self.lastLedsOff) > 0 and self.is_right_answer):
                    led = self.lastLedsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.lastLedsBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.lastLedsBand.show()

                    if(led not in self.extraLedsOn):
                        self.lastLedsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.lastLedsOff.pop(0)
                elif(self.is_right_answer and self.fishPart.isLit == False):
                    self.fishPart.stripColor = color
                    self.fishPart.gradually_turn_on_with_gradual_intensity(color, 7, intensityStep)
                    
                time.sleep_ms(delay)
            else:
                if(len(self.lastLedsOn) > 0 ):
                    led = self.lastLedsOn[len(self.lastLedsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.lastLedsBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.lastLedsBand.show()
                    if(led["intensity"] <= 0):
                        self.lastLedsOff.insert(0, led)
                        self.lastLedsOn.pop()
                elif(len(self.extraLedsOn) > 0 ):
                    led = self.extraLedsOn[len(self.extraLedsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.extraLedBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.extraLedBand.show()
                    if(led["intensity"] <= 0):
                        self.extraLedsOff.insert(0, led)
                        self.extraLedsOn.pop()
                elif(len(self.ledsOn) > 0 ):
                    led = self.ledsOn[len(self.ledsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.show()
                    if(led["intensity"] <= 0):
                        self.ledsOff.insert(0, led)
                        self.ledsOn.pop()
                time.sleep_ms(delay)
            self.lastTick = time.ticks_ms()

    def adaptive_gradually_turn_on(self, color, delay, intensityStep):
        maxIntensity = 1
        if(time.ticks_ms() - self.lastTick > 10):
            if(self.button.value() == 0):
                if(len(self.ledsOff) > 0 ):
                    led = self.ledsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.show()

                    if(led not in self.ledsOn):
                        self.ledsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.ledsOff.pop(0)

                elif(len(self.extraLedsOff) > 0 and self.is_right_answer):
                    led = self.extraLedsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.extraLedBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.extraLedBand.show()

                    if(led not in self.extraLedsOn):
                        self.extraLedsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.extraLedsOff.pop(0)

                elif(len(self.lastLedsOff) > 0 and self.is_right_answer):
                    led = self.lastLedsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.lastLedsBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.lastLedsBand.show()

                    if(led not in self.extraLedsOn):
                        self.lastLedsOn.append(led)

                    if(led["intensity"] >= maxIntensity):
                        self.lastLedsOff.pop(0)
                elif(self.is_right_answer and self.fishPart.isLit == False):
                    self.fishPart.stripColor = color
                    self.fishPart.gradually_turn_on_with_gradual_intensity(color, 7, intensityStep)
                    
                time.sleep_ms(delay)
            else:
                if(len(self.lastLedsOn) > 0 ):
                    led = self.lastLedsOn[len(self.lastLedsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.lastLedsBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.lastLedsBand.show()
                    if(led["intensity"] <= 0):
                        self.lastLedsOff.insert(0, led)
                        self.lastLedsOn.pop()
                elif(len(self.extraLedsOn) > 0 ):
                    led = self.extraLedsOn[len(self.extraLedsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.extraLedBand.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.extraLedBand.show()
                    if(led["intensity"] <= 0):
                        self.extraLedsOff.insert(0, led)
                        self.extraLedsOn.pop()
                elif(len(self.ledsOn) > 0 ):
                    led = self.ledsOn[len(self.ledsOn)-1]
                    led["intensity"] -= intensityStep
                    led["color"] = color
                    self.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.show()
                    if(led["intensity"] <= 0):
                        self.ledsOff.insert(0, led)
                        self.ledsOn.pop()
                time.sleep_ms(delay)
            self.lastTick = time.ticks_ms()

class ProximitySensor:
    def __init__(self, trigger_pin, echo_pin, leds):
        self.trigger_pin = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin, machine.Pin.IN)
        self.leds = leds
        self.state = False
        # self.led = neopixel.NeoPixel(machine.Pin(led_pin), 1)

        
    def measure_distance(self):
        self.trigger_pin.value(1)
        time.sleep(0.1)
        self.trigger_pin.value(0)
        
        pulse_time = machine.time_pulse_us(self.echo_pin, 1, 80000)
        distance = (pulse_time / 2) / 29.1
        return distance
    
    def isSomethingDetected(self):
        distance = self.measure_distance()
        print(distance)
        if distance > 0 :
            if distance < 150:
                return True
            else:
                return False
        else:
            return self.state
    
    def handle(self):
        max_intensity = 0.2
        self.state = self.isSomethingDetected()
        if self.state:
            for ledstrip in self.leds:
                if(len(ledstrip.ledsOff) > 0 ):
                    led = ledstrip.ledsOff[0]
                    led["intensity"] += max_intensity
                    led["color"] = ledstrip.stripColor
                    ledstrip.set_pixel_color(led["id"], led["color"], led["intensity"])
                    ledstrip.show()

                    if(led not in ledstrip.ledsOn):
                        ledstrip.ledsOn.append(led)

                    if(led["intensity"] >= max_intensity):
                        ledstrip.ledsOff.pop(0)

        else:
            for ledstrip in self.leds:
                if(len(ledstrip.ledsOn) > 0 ):
                    led = ledstrip.ledsOn[len(ledstrip.ledsOn)-1]
                    led["intensity"] -= max_intensity
                    led["color"] = ledstrip.stripColor
                    ledstrip.set_pixel_color(led["id"], led["color"], led["intensity"])
                    ledstrip.show()
                    if(led["intensity"] <= 0):
                        ledstrip.ledsOff.insert(0, led)
                        ledstrip.ledsOn.pop()



led1 = LedStrip(12, 50, 0, 0)
led2 = LedStrip(14, 48, 0, 0)
led3 = LedStrip(27, 45, 0, 0)

leds = [led1, led2, led3]

for led in leds:
    led.stripColor = (90,255,60)
    # led.set_strip_color((0, 0, 255), 0.1)
    # led.show()


sensor = ProximitySensor(18, 5, [led1, led2, led3])

# for led in sensor.leds:
#     led.stripColor = (0, 0, 255)

while True:
    sensor.handle()
    

