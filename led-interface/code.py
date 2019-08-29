import time

from analogio import AnalogIn
import board
from digitalio import DigitalInOut, Direction, Pull
from neopixel import NeoPixel
import touchio

touch = touchio.TouchIn(board.A1)

leds = NeoPixel(board.NEOPIXEL, 10)
ok_led = DigitalInOut(board.D13)
ok_led.direction = Direction.OUTPUT

# The `scroll_button` is responsible for moving the cursor
scroll_button = DigitalInOut(board.BUTTON_A)
scroll_button.direction = Direction.INPUT
scroll_button.pull = Pull.DOWN

# The `confirm_button` is reasponsible for confirming a choice
confirm_button = DigitalInOut(board.BUTTON_B)
confirm_button.direction = Direction.INPUT
confirm_button.pull = Pull.DOWN

light_sensor = AnalogIn(board.LIGHT)

def ok():
    ok_led.value = True

def wheel(pos):
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))

def select_program():
    index = 0
    while True:
        if scroll_button.value:
            index = (index + 1) % 10
        if confirm_button.value:
            leds.fill((0, 0, 0))
            return index

        color = wheel(index * 28)

        leds.fill((0, 0, 0))
        leds[index] = color
        time.sleep(0.2)

def touch_light():
    print('Starting touch_light() function')
    ok()
    i = 0
    while True:
        i = (i + 1) % 256
        if touch.value:
            leds.fill(wheel(i))
        else:
            leds.fill((0, 0, 0))
        time.sleep(0.01)

def sense_light():
    """The brighter it is, the more LEDs light up"""
    print('Starting sense_light() function')
    ok()
    while True:
        light_level = light_sensor.value / 256
        up_to = int(light_level / 256 * 10)
        for i in range(up_to+2):
            print((i,))
            if i > 9:
                break
            leds[i] = wheel(i * 25)
        for i in range(up_to+2, 10):
            if i > 9:
                break
            leds[i] = (0, 0, 0)
        leds.show()
        time.sleep(0.1)

def sense_light_dark():
    """The darker it is, the more LEDs light up"""
    print('Starting sense_light() function')
    ok()
    while True:
        light_level = light_sensor.value / 256
        light_level = 256 - light_level
        up_to = int(light_level / 256 * 10)
        for i in range(up_to):
            leds[i] = wheel(i * 25)
        for i in range(up_to, 10):
            leds[i] = (0, 0, 0)
        leds.show()
        time.sleep(0.1)


def function_not_found():
    leds.fill((255, 0, 0))
    ok()
    while True:
        for i in range(0, 101, ):
            leds.brightness = i / 100
            time.sleep(0.01)
        for i in range(100, -1,  -1):
            leds.brightness = i / 100
            time.sleep(0.01)

functions = {
    0: touch_light,
    1: sense_light,
    2: sense_light_dark
}

index = select_program()
print('You selected program #{}'.format(index))

if index in functions.keys():
    functions[index]()
else:
    print('There is no function {}'.format(index))
    function_not_found()
