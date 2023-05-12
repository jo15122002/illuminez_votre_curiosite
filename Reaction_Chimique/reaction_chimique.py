import machine, neopixel
import math
import time

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
    
    def gradually_turn_on(self, color, delay):
        for i in range(self.number_of_leds):
            self.set_strip_color(color)
            for j in range(i+1):
                self.set_pixel_color(j, color)
            self.show()
            time.sleep_ms(delay)
