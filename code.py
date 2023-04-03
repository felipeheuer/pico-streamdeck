# Author:   Felipe Heuer
# Version:  1.0
# Date:     11th February 2021
# Website:  https://www.cpu.eng.br
# Git:      https://github.com/felipeheuer

#################################################
# Heuer Strem-Deck
# ----------------
# This code takes a Raspberry Pi Pico connected
#  to 12 button and leds, mock keyboard key press
#  for each button
# This code is a for of the original
#  pico-streamdeck, written by Pete Gallagher
#
# * CircuitPython updated to 8.0.4
#
#################################################

# Imports
import board

from adafruit_hid.keycode import Keycode
from lib.led_button import Button, Led


botao = [
    {
        "name": "Botao 1",
        "keycode": [[Keycode.KEYPAD_SEVEN], [Keycode.CONTROL, Keycode.F9]],
        "gpio": board.GP0,
        "led_gpio": board.GP13
    },
    {
        "name": "Botao 2",
        "keycode": [[Keycode.KEYPAD_EIGHT], [Keycode.CONTROL, Keycode.F10]],
        "gpio": board.GP1,
        "led_gpio": board.GP14
    },
    {
        "name": "Botao 3",
        "keycode": [[Keycode.KEYPAD_NINE], [Keycode.CONTROL, Keycode.F11]],
        "gpio": board.GP2,
        "led_gpio": board.GP16
    },
    {
        "name": "Botao 4",
        "keycode": [[], []],
        "gpio": board.GP3,
        "led_gpio": board.GP17
    },
    {
        "name": "Botao 5",
        "keycode": [[Keycode.KEYPAD_FOUR], [Keycode.CONTROL, Keycode.F12]],
        "gpio": board.GP4,
        "led_gpio": board.GP18
    },
    {
        "name": "Botao 6",
        "keycode": [[Keycode.KEYPAD_FIVE], [Keycode.CONTROL, Keycode.F13]],
        "gpio": board.GP5,
        "led_gpio": board.GP19
    },
    {
        "name": "Botao 7",
        "keycode": [[Keycode.KEYPAD_SIX], [Keycode.CONTROL, Keycode.F14]],
        "gpio": board.GP6,
        "led_gpio": board.GP20
    },
    {
        "name": "Botao 8",
        "keycode": [[Keycode.COMMA], [Keycode.CONTROL, Keycode.F15]],
        "gpio": board.GP7,
        "led_gpio": board.GP21
    },
    {
        "name": "Botao 9",
        "keycode": [[Keycode.KEYPAD_ONE], [Keycode.CONTROL, Keycode.F16]],
        "gpio": board.GP8,
        "led_gpio": board.GP22
    },
    {
        "name": "Botao 10",
        "keycode": [[Keycode.KEYPAD_TWO], [Keycode.CONTROL, Keycode.F17]],
        "gpio": board.GP9,
        "led_gpio": board.GP26
    },
    {
        "name": "Botao 11",
        "keycode": [[Keycode.KEYPAD_THREE], [Keycode.CONTROL, Keycode.F18]],
        "gpio": board.GP10,
        "led_gpio": board.GP27
    },
    {
        "name": "Botao 12",
        "keycode": [[Keycode.KEYPAD_ZERO], [Keycode.CONTROL, Keycode.F19]],
        "gpio": board.GP11,
        "led_gpio": board.GP28
    },
]


layer = 0
def change_layer(layer, last_press, led, button):
    _layer = not layer
    print("layer:", _layer)
    if _layer == 1:
        min_brt = 0
    else:
        min_brt = 500

    for j in range(len(button)):
        led[j].brightness.min = min_brt

        if j == last_press and _layer == 0:
            print("A")
            led[j].brightness.set_max()
        else:
            led[j].brightness.set_min()
    return _layer

led = []
button = []
for i in range(len(botao)):
    new_led = Led(botao[i]["led_gpio"])
    led.append(new_led)
    if i == 3:
        type = "hold"
    else:
        type = "press"
    new_button = Button(botao[i]["name"], botao[i]["gpio"], botao[i]["keycode"], led=led[i], type=type)
    button.append(new_button)

layer = change_layer(1, 3, led, button)

while True:
    for i in range(len(botao)):
        led[i].update()

        if button[i].was_pressed():
            # send the keyboard commands
            if button[i].press(layer):
                layer = change_layer(layer, i, led, button)

        # remove the held indication if it is no longer held
        elif button[i].was_released():
            button[i].release(layer)
