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
        for i in range(6):
            self.ledsOff.append({
                "id": i,
                "intensity": 0,
                "color": (0,0,0)
            })

        self.extraLedsOn = []
        self.extraLedsOff = []
        for i in range(self.extraLeds):
            self.extraLedsOff.append({
                "id": i + self.offset,
                "intensity": 0,
                "color": (0,0,0)
            })

        self.lastLedsOn = []
        self.lastLedsOff = []
        if(self.lastLedsBand != None):
            for i in range(4):
                self.lastLedsOff.append({
                    "id": i + self.lastLedsBand.number_of_leds - 4, # 4 is the number of leds in the last band
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
    
    def gradually_turn_on(self, color, delay, intensity = 1.0):
        self.set_strip_color((0,0,0))
        for i in range(self.number_of_leds):
            self.set_pixel_color(i, color, intensity)
            self.show()
            time.sleep_ms(delay)

    def gradually_turn_off(self, delay):
        for i in range(self.number_of_leds):
            self.set_pixel_color(self.number_of_leds - (i+1), (0,0,0))
            self.show()
            time.sleep_ms(delay)

    def gradually_turn_on_with_gradual_intensity(self, color, delay, intensityStep):
        ledsToRefresh = []
        index = 0
        for i in range(self.number_of_leds):
            ledsToRefresh.append({
                "id": i,
                "intensity": 0 - i*intensityStep,
                "color": color
            })
        while(ledsToRefresh[self.number_of_leds-1]["intensity"] < 1):
            for led in ledsToRefresh:
                led["intensity"] += intensityStep
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
            self.show()
            self.isLit = True
            time.sleep_ms(delay)

    def gradually_turn_off_with_gradual_intensity(self, delay, color, intensityStep):
        ledsToRefresh = []
        for i in range(self.number_of_leds):
            ledsToRefresh.append({
                "id": i,
                "intensity": 1.0 - i*intensityStep,
                "color": color
            })
        while(ledsToRefresh[0]["intensity"] > 0):
            for led in ledsToRefresh:
                led["intensity"] -= intensityStep
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
            self.show()
            time.sleep_ms(delay)

    def wrong_answer_animation(self, color, intensityStep, delay):
        ledsToRefresh = []
        index = 0
        for i in range(math.floor(self.number_of_leds/2)):
            ledsToRefresh.append({
                "id": i,
                "intensity": 0 - i*intensityStep,
                "color": color
            })
        while(ledsToRefresh[math.floor(self.number_of_leds/2)-1]["intensity"] < 1):
            for led in ledsToRefresh:
                led["intensity"] += intensityStep
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
            self.show()
            time.sleep_ms(delay)
        
        time.sleep_ms(1000)
        
        ledsToRefresh = []
        for i in range(math.floor(self.number_of_leds/2)):
            ledsToRefresh.append({
                "id": i,
                "intensity": 1.0 - i*intensityStep,
                "color": color
            })
        while(ledsToRefresh[0]["intensity"] > 0):
            for led in ledsToRefresh:
                led["intensity"] -= intensityStep
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
            self.show()
            time.sleep_ms(delay)
    
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


ledStrips = []
upperFish = LedStrip(22, 20, 0)
lowerFish = LedStrip(23, 19, 0)

led6 = LedStrip(33, 29, 19, 0)
ledStrips.append(led6)

led1 = LedStrip(12, 26, 4, 0, None, led6)
ledStrips.append(led1)

led2 = LedStrip(14, 6, 16, 12, led1, led6)
ledStrips.append(led2)

led3 = LedStrip(27, 6, 17, 4, led1, led6)
ledStrips.append(led3)

led4 = LedStrip(26, 6, 18, 11, led6, led6)
ledStrips.append(led4)

led5 = LedStrip(25, 6, 5, 3, led6, led6)
ledStrips.append(led5)

def shuffle_array(arr):
    length = len(arr)
    shuffled_arr = arr.copy()
    
    for i in range(length):
        j = random.randint(i, length - 1)
        shuffled_arr[i], shuffled_arr[j] = shuffled_arr[j], shuffled_arr[i]
    
    return shuffled_arr

def randomiseAnswers(ledStrips, upperFish, lowerFish):
    ledStripsDone = []
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]
    colors = shuffle_array(colors)
    fishPartsAffected = [upperFish,lowerFish]
    for i in range(2):
        index = random.randint(0, len(ledStrips)-1)
        print(index)
        ledStrips[index].is_right_answer = True
        ledStrips[index].stripColor = colors[index]
        ledStrips[index].fishPart = fishPartsAffected[i]

        #show responses
        ledStrips[index].set_pixel_color(0, ledStrips[index].stripColor, 1)
        ledStrips[index].show()


        ledStripsDone.append(ledStrips[index])

        ledStrips.pop(index)
        colors.pop(index)
    
    for led in ledStrips:
        index = random.randint(0, len(colors)-1)
        led.stripColor = colors[index]
        led.set_pixel_color(0, led.stripColor, 1)
        led.show()
        ledStripsDone.append(led)
        colors.pop(index)

    return ledStripsDone

ledStrips = randomiseAnswers(ledStrips, upperFish, lowerFish)

while True:
    for led in ledStrips:
        led.adaptive_gradually_turn_on(led.stripColor, 5, 0.33)

        if(upperFish.isLit and lowerFish.isLit):
            print("both lit")
            ur, ug, ub = upperFish.stripColor
            lr, lg, lb = lowerFish.stripColor
            while ur < 255 or ug < 255 or ub < 255 or lr < 255 or lg < 255 or lb < 255:
                for led in ledStrips:
                    led.adaptive_gradually_turn_on(led.stripColor, 5, 0.33)
                ur += 1
                ug += 1
                ub += 1
                lr += 1
                lg += 1
                lb += 1

                if(ur > 255):
                    ur = 255
                if(ug > 255):
                    ug = 255
                if(ub > 255):
                    ub = 255
                if(lr > 255):
                    lr = 255
                if(lg > 255):
                    lg = 255
                if(lb > 255):
                    lb = 255

                upperFish.set_strip_color((ur,ug,ub))
                lowerFish.set_strip_color((lr,lg,lb))
                upperFish.show()
                lowerFish.show()
                time.sleep(0.005)

            timeStart = time.ticks_ms()

            while time.ticks_ms() - timeStart < 5000:
                for led in ledStrips:
                    led.adaptive_gradually_turn_on(led.stripColor, 5, 0.33)
            
            for led in ledStrips:
                led.is_right_answer = False
                led.set_strip_color((0,0,0))
                led.show()
            upperFish.set_strip_color((0,0,0))
            lowerFish.set_strip_color((0,0,0))
            upperFish.show()
            lowerFish.show()
            upperFish.isLit = False
            lowerFish.isLit = False

            ledStrips = []
            upperFish = LedStrip(22, 20, 0)
            lowerFish = LedStrip(23, 19, 0)

            led6 = LedStrip(33, 29, 19, 0)
            ledStrips.append(led6)

            led1 = LedStrip(12, 26, 4, 0, None, led6)
            ledStrips.append(led1)

            led2 = LedStrip(14, 6, 16, 12, led1, led6)
            ledStrips.append(led2)

            led3 = LedStrip(27, 6, 17, 4, led1, led6)
            ledStrips.append(led3)

            led4 = LedStrip(26, 6, 18, 11, led6, led6)
            ledStrips.append(led4)

            led5 = LedStrip(25, 6, 5, 3, led6, led6)
            ledStrips.append(led5)

            ledStrips = randomiseAnswers(ledStrips, upperFish, lowerFish)