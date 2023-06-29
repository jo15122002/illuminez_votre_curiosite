from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
import microdot_cors
from led_band import LedStrip
import time
import json
from machine import Pin

from animals import animals

pins = {}
color = {}
for animal in animals:
    pins[str(animal['id'])] = LedStrip(animal['pin'],3,21)

# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'
cors = microdot_cors.CORS(app=app, allowed_origins='*')

# root route
@app.route('/')
async def index(request):
    return 'hey1'

@app.route('/all')
async def all(request):
    return animals


@app.route('/ws')
@with_websocket
async def read_sensor(request, ws):
    while True:
        data = await ws.receive()
        light_led(data)
        time.sleep(.1)
        await ws.send(json.dumps(animals))

def light_led(string_led):
    new_string = string_led.split(':')
    if (len(new_string) > 1):
        if new_string[0] == 'succes':
            print('led', new_string[1])
            """ pins[str(new_string[1])].value(1) """
            print(new_string[1])
            color = animals[int(new_string[1]) - 1]
            pins[str(new_string[1])].set_strip_color(color['color'], 1)
            pins[str(new_string[1])].show()
        elif new_string[0] == 'led':
            print(new_string[1])
            color = animals[int(new_string[1]) - 1]
            pins[str(new_string[1])].set_strip_color(color['color'],float(new_string[2]))
            pins[str(new_string[1])].show()
    elif new_string[0] == 'start':
        """ led.gradually_turn_off(0) """
        for pin in pins.values():
            """pin.value(0)"""
            pin.gradually_turn_off(0)


# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        pass