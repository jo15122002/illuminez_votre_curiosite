import machine
import time

class ProximitySensor:
    def __init__(self, trigger_pin, echo_pin, led_pin):
        self.trigger_pin = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin, machine.Pin.IN)
        self.led_pin = machine.Pin(led_pin, machine.Pin.OUT)
        
    def measure_distance():
        self.trigger_pin.value(1)
        time.sleep(0.1)
        self.trigger_pin.value(0)
        
        pulse_time = machine.time_pulse_us(self.echo_pin, 1, 30000)
        distance = (pulse_time / 2) / 29.1
        return distance
    
    def isSomethingDetected():
        distance = self.measure_distance()
        if distance < 50:
            return True
        else:
            return False
    
    def handle():
        if self.isSomethingDetected():
            self.led_pin.value(1)
        else:
            self.led_pin.value(0)

sensor = ProximitySensor(4, 5, 2)

while True:
    sensor.handle()
    time.sleep(0.1)