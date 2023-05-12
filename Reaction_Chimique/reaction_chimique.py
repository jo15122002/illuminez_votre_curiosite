import machine, neopixel
import math
import time

print("test")

class LedStrip():
    def __init__(self, pin, band_length_in_meters, leds_per_meter):
        self.pin = pin
        self.number_of_leds = math.floor(band_length_in_meters * leds_per_meter)
        self.np = neopixel.NeoPixel(machine.Pin(pin), self.number_of_leds)

    def set_pixel_color(self, index, color, intensity=1):
        self.np[index] = color * intensity
    
    def set_strip_color(self, color, intensity=1):
        self.np.fill(color*intensity)
    
    def show(self):
        self.np.write()
    
    def gradually_turn_on(self, color, delay, intensity = 1):
        for i in range(self.number_of_leds):
            self.set_pixel_color(i, color)
            self.show()
            time.sleep_ms(delay)

    def gradually_turn_off(self, delay):
        for i in range(self.number_of_leds):    
            self.set_pixel_color(self.number_of_leds - i, (0,0,0))
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
        while(ledsToRefresh[self.number_of_leds]["intensity"] < 1):
            for led in ledsToRefresh:
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
                led["intensity"] += intensityStep
                if(led["intensity"] > 1):
                    led["intensity"] = 1
            self.show()
            time.sleep_ms(delay)

    def gradually_turn_off_with_gradual_intensity(self, delay, color, intensityStep):
        ledsToRefresh = []
        index = 0
        for i in range(self.number_of_leds):
            ledsToRefresh.append({
                "id": i,
                "intensity": 1 - i*intensityStep,
                "color": color
            })
        while(ledsToRefresh[self.number_of_leds]["intensity"] > 0):
            for led in ledsToRefresh:
                self.set_pixel_color(led["id"], led["color"], led["intensity"])
                led["intensity"] -= intensityStep
                if(led["intensity"] < 0):
                    led["intensity"] = 0
            self.show()
            time.sleep_ms(delay)

    def wrong_answer_animation(self, color, delay):
        for i in range(self.number_of_leds/2):
            self.set_pixel_color(i, color)
            self.show()
            time.sleep_ms(delay)
        self.gradually_turn_off(delay)

