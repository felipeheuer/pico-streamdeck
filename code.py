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
import pwmio
import usb_hid
import sys
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull


botao = [
    {
        "name": "Botao 1",
        "held": False,
        "keycode": [[Keycode.KEYPAD_SEVEN], [Keycode.CONTROL, Keycode.F9]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 2",
        "held": False,
        "keycode": [[Keycode.KEYPAD_EIGHT], [Keycode.CONTROL, Keycode.F10]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 3",
        "held": False,
        "keycode": [[Keycode.KEYPAD_NINE], [Keycode.CONTROL, Keycode.F11]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 4",
        "held": False,
        "keycode": [[], []],
        "button": None,
        "led": {
            "driver": None,
            "type": "toggle",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 5",
        "held": False,
        "keycode": [[Keycode.KEYPAD_FOUR], [Keycode.CONTROL, Keycode.F12]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 6",
        "held": False,
        "keycode": [[Keycode.KEYPAD_FIVE], [Keycode.CONTROL, Keycode.F13]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 7",
        "held": False,
        "keycode": [[Keycode.KEYPAD_SIX], [Keycode.CONTROL, Keycode.F14]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 8",
        "held": False,
        "keycode": [[Keycode.COMMA], [Keycode.CONTROL, Keycode.F15]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 9",
        "held": False,
        "keycode": [[Keycode.KEYPAD_ONE], [Keycode.CONTROL, Keycode.F16]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 10",
        "held": False,
        "keycode": [[Keycode.KEYPAD_TWO], [Keycode.CONTROL, Keycode.F17]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 11",
        "held": False,
        "keycode": [[Keycode.KEYPAD_THREE], [Keycode.CONTROL, Keycode.F18]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
    {
        "name": "Botao 12",
        "held": False,
        "keycode": [[Keycode.KEYPAD_ZERO], [Keycode.CONTROL, Keycode.F19]],
        "button": None,
        "led": {
            "driver": None,
            "type": "switch",
            "blink": False,
            "pending_off": False
        }
    },
]

# Define button pins
btn_pins = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
]

# Define led pins
led_pins = [
    board.GP13,
    board.GP14,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
    board.GP26,
    board.GP27,
    board.GP28,
]

fadding_status = False
fadding_counter = 0
fadding_step = int(65000/100)
fadding_dir = 1

# for i in range(len(botao)):
#     button = DigitalInOut(btn_pins[i])
#     button.direction = Direction.INPUT
#     button.pull = Pull.UP
#     botao[i]["button"] = button

#     if i == 0:
#         led = pwmio.PWMOut(board.GP13, frequency=1000)
#         led.duty_cycle = 0
#     else:
#         led = DigitalInOut(led_pins[i])
#         led.direction = Direction.OUTPUT
#     botao[i]["led"]["driver"] = led

# Initialize Keybaord
keyboard = Keyboard(usb_hid.devices)

blinking_interval = 1000
fading_interval = 100
fade_speed = 50

# Loop around and check for key presses
counter = 0
fade_dir = 1
level = 0


class Brightness:
    def __init__(self, min = 0, max = 50000):
        self.min = min
        self.max = max
        self.curr = self.min

    def update(self, value):
        if value > self.max:
            value = self.max
        elif value < self.min:
            value = self.min
        self.curr = value
        return self.curr

    def set_min(self):
        self.curr = self.min

    def set_max(self):
        self.curr = self.max

    def is_max(self):
        return self.curr >= self.max

    def is_min(self):
        return self.curr <= self.min

class Fade:
    def __init__(self, brt: Brightness, interval, step):
        self.brightness = brt
        self.interval = interval
        self.fade_step = step
        self.fade_on = False
        self.fade_styles = ["up", "up-down", "down-up", "down"]
        self.fade_current = ""
        self.fade_curr_dir_up = False

    def step_up(self):
        new_brt = self.brightness.curr + self.fade_step
        return self.brightness.update(new_brt)

    def step_down(self):
        new_brt = self.brightness.curr - self.fade_step
        return self.brightness.update(new_brt)

    def start(self, style):
        if style not in self.fade_styles:
            return
        self.fade_current = style
        self.fade_curr_dir_up = (style in self.fade_styles[:2])
        if style in self.fade_styles[:2]:
            self.brightness.set_min()
        else:
            self.brightness.set_max()

    def stop(self):
        self.fade_current = ""

    def handler(self):
        ret = False
        if self.fade_current == "up" or (self.fade_curr_dir_up and self.fade_current in self.fade_styles[1:3]):
            self.step_up()
            if self.brightness.is_max():
                if self.fade_current == "up-down" and self.fade_curr_dir_up:
                    self.fade_curr_dir_up = False
                else:
                    self.stop()
                    ret = True
        elif self.fade_current == "down" or (not self.fade_curr_dir_up and self.fade_current in self.fade_styles[1:3]):
            self.step_down()
            if self.brightness.is_min():
                if self.fade_current == "down-up" and not self.fade_curr_dir_up:
                    self.fade_curr_dir_up = True
                else:
                    self.stop()
                    ret = True
        return ret

class Led:
    def __init__(self, gpio, pwm_freq = 2000, fade_interval = 0.001, fade_step = 10000):
        self.brightness = Brightness()
        self.fade = Fade(self.brightness, interval=fade_interval, step=fade_step)
        self.driver = pwmio.PWMOut(led_pins[gpio], frequency=pwm_freq)
        self.driver.duty_cycle = 0
        self.curr_time = 0

    def fade_start(self, style):
        self.curr_time = time.monotonic()
        self.fade.start(style)

    def fade_stop(self):
        self.curr_time = 0
        self.fade.stop()

    def off(self):
        self.driver.duty_cycle = 0
        self.brightness.update(0)

    def update(self):
        self.driver.duty_cycle = self.brightness.curr

    def fade_handler(self):
        if time.monotonic() - self.curr_time > self.fade.interval:
            self.curr_time = time.monotonic()
            ret = self.fade.handler()
            self.driver.duty_cycle = self.brightness.curr
            if ret:
                self.fade_stop()
                return ret
        return False

class Button:
    def __init__(self, name, gpio, keycodes: list, type = "press", led = None):
        self.driver = DigitalInOut(btn_pins[gpio])
        self.driver.direction = Direction.INPUT
        self.driver.pull = Pull.UP
        self.keys = keycodes
        self.name = name
        self.held = False
        self.led = led
        self.types = ["press", "hold"]
        self.type = type
        self.level = 0
        self.changes_level = (type == "hold")

    def is_pressed(self):
        return self.driver.value

    def press(self, level):
        self.held = True
        if level <= len(self.keys):
            print(self.name, *self.keys[level])
            #keyboard.send(*self.keys[level])

        self.led.fade_start("up")
        print(self.changes_level)
        return self.changes_level

    def release(self, level):
        self.held = False
        if not (level == 0 and self.type == "hold"):
            self.led.fade_start("down")


led = []
button = []
for i in range(len(led_pins)):
    new_led = Led(i)
    led.append(new_led)
    if i == 3:
        type = "hold"
    else:
        type = "press"
    new_button = Button(botao[i]["name"], i, botao[i]["keycode"], led=led[i], type=type)
    button.append(new_button)

while True:
    for i in range(len(botao)):
        led[i].fade_handler()

        if not button[i].is_pressed() and not button[i].held:
            # send the keyboard commands
            if button[i].press(level):
                level = not level
                print("Level:", level)
                if level == 1:
                    min_brt = 0
                else:
                    min_brt = 500

                for j in range(len(button)):
                    led[j].brightness.min = min_brt

                    if j == i and level == 0:
                        print("A")
                        led[j].brightness.set_max()
                    else:
                        led[j].brightness.set_min()
            led[i].update()

            # update blink led
            # led[i].fade_start("up")

        # remove the held indication if it is no longer held
        elif button[i].is_pressed() and button[i].held:
            button[i].release(level)


while True:
    time_to_blink = counter >= blinking_interval
    time_to_fade = counter >= fading_interval
    if time.monotonic() - curr_time > 0.05:
        curr_time = time.monotonic()
        if fadding_status == True:
            if fadding_counter >= 20000:
                fadding_counter = 0
                curr_led += 1
            else:
                fadding_counter += fadding_step
            if curr_led not in range (12):
                curr_led = 0
            led[curr_led].duty_cycle = fadding_counter
exit()

while True:
    # x=sys.stdin.read(1)
    # print("You pressed", x)

    # time to blink?
    time_to_blink = counter >= blinking_interval
    time_to_fade = counter >= fading_interval

    # if time_to_fade:
    #     hid_actions[0]["led"].duty_cycle = hid_actions[0]["led"].duty_cycle + (fade_dir * fade_speed)
    #     if hid_actions[0]["led"].duty_cycle == 0 or hid_actions[0]["led"].duty_cycle == 65000:
    #         fade_dir = fade_dir * -1

    if time.monotonic() - curr_time > 0.001:
        curr_time = time.monotonic()
        # led_fade_handler(0)

    for i in range(len(botao)):
    # for i in range(12):
        # check if button is pressed but make sure it is not held down
        if not botao[i]["button"].value and not botao[i]["held"]:

            # print the name of the command for debug purposes
            print(botao[i]["name"], *botao[i]["keycode"][level])

            # send the keyboard commands
            #keyboard.send(*hid_actions[i]["keycode"])

            # update blink led
            # botao[i]["led"]["blink"] = not botao[i]["led"]["blink"]
            # botao[i]["led"]["driver"].value = 0
            # print("Update blink for", i, ":", botao[i]["led"]["blink"])

            # light up the associated LED
            # hid_actions[i]["led"].value = not hid_actions[i]["led"].value

            # turn off other LEDs that may be on
            # for j in range(12):
            #     if i != j:
            #         hid_actions[j]["led"].value = False

            # set the held to True for debounce
            botao[i]["held"] = True
            if i == 0:
                fadding_status = True
                fadding_dir = 1
            else:
                if i == 3:
                    level = not level
                    change_led(i, not level),
                else:
                    invert_led(i)

            # keyboard.send(*botao[i]["keycode"][level])

        # if time_to_blink:
        #     blink_led(i)

        # remove the held indication if it is no longer held
        elif botao[i]["button"].value and botao[i]["held"]:
            botao[i]["held"] = False
            if botao[i]["led"]["type"] == "switch":
                if i == 0:
                    fadding_status = True
                    # fadding_dir = -1
                    botao[i]["led"]["pending_off"] = True
                else:
                    change_led(i, False)


    if time_to_blink:
        counter = 0
    else:
        counter += 1