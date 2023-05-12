import machine, neopixel

band_lenght_m = 10
leds_per_meter = 30

number_of_leds = band_lenght_m * leds_per_meter
pin = 5

np = neopixel.NeoPixel(machine.Pin(pin), number_of_leds)

np[0] = (255, 0, 0)
np[3] = (125, 204, 223)
np[7] = (120, 153, 23)
np[10] = (255, 0, 153)
np.write()