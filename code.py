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
from adafruit_hid.keycode import Keycode
from config import botao
from lib.led_button import Button, Led

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
