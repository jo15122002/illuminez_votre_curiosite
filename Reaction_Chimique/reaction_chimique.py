import machine, neopixel
import math
import time

class LedStrip():
    def __init__(self, pin, number_of_leds, button_pin):
        self.pin = pin
        # self.number_of_leds = math.floor(band_length_in_meters * leds_per_meter)
        self.number_of_leds = number_of_leds
        self.np = neopixel.NeoPixel(machine.Pin(pin), self.number_of_leds)
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.lastTick = time.ticks_ms()

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
    
    def gradually_turn_on(self, color, delay, intensity = 1.0):
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
        if(time.ticks_ms() - self.lastTick > 10):
            if(self.button.value() == 0):
                # print("button pressed")
                # print(len(self.ledsOff))
                if(len(self.ledsOff) > 0):
                    led = self.ledsOff[0]
                    led["intensity"] += intensityStep
                    led["color"] = color
                    self.set_pixel_color(led["id"], led["color"], led["intensity"])
                    self.show()
                    # print(led["intensity"])

                    if(led not in self.ledsOn):
                        self.ledsOn.append(led)

                    if(led["intensity"] >= 1):
                        self.ledsOff.pop(0)
                time.sleep_ms(delay)
            else:
                if(len(self.ledsOn) > 0):
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

led = LedStrip(23, 6, 21)

while True:
    led.adaptive_gradually_turn_on((255,0,0), 10, 0.1)