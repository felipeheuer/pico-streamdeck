import board
import pwmio
import usb_hid
import sys
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull

class Brightness:
    def __init__(self, min = 0, max = 50000):
        self.min = min
        self.max = max
        self._curr = self.min
        self.needs_refresh = False

    @property
    def curr(self):
        return self._curr

    @curr.setter
    def curr(self, value):
        if self._curr != value:
            self.needs_refresh = True
            if value > self.max:
                self._curr = self.max
            elif value < self.min:
                self._curr = self.min
            else:
                self._curr = value

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
        self.brightness.curr = new_brt
        return self.brightness.curr

    def step_down(self):
        new_brt = self.brightness.curr - self.fade_step
        self.brightness.curr = new_brt
        return self.brightness.curr

    def start(self, style):
        if style not in self.fade_styles:
            return
        self.fade_on = True
        self.fade_current = style
        self.fade_curr_dir_up = (style in self.fade_styles[:2])
        if style in self.fade_styles[:2]:
            self.brightness.set_min()
        else:
            self.brightness.set_max()

    def stop(self):
        self.fade_on = False
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
    def __init__(self, gpio, pwm_freq = 1000, fade_interval = 0.001, fade_step = 2750):
        self.brightness = Brightness()
        self.fade = Fade(self.brightness, interval=fade_interval, step=fade_step)
        self.driver = pwmio.PWMOut(gpio, frequency=pwm_freq)
        self.driver.duty_cycle = 0
        self.curr_time = 0

    def fade_start(self, style):
        self.curr_time = time.monotonic()
        self.fade.start(style)

    def fade_stop(self):
        self.curr_time = 0
        self.fade.stop()

    def refresh(self):
        if self.brightness.needs_refresh:
            self.driver.duty_cycle = self.brightness.curr

    def off(self):
        self.brightness.curr = 0
        self.refresh()

    def fade_handler(self):
        if time.monotonic() - self.curr_time > self.fade.interval:
            self.curr_time = time.monotonic()
            ret = self.fade.handler()
            self.refresh()
            if ret:
                self.fade_stop()
                return ret
        return False

    def update(self):
        if self.fade.fade_on:
            self.fade_handler()
        else:
            self.refresh()

class Button:
    def __init__(self, name, gpio, keycodes: list, type = "press", led = None):
        self.driver = DigitalInOut(gpio)
        self.driver.direction = Direction.INPUT
        self.driver.pull = Pull.UP
        self.keys = keycodes
        self.name = name
        self.held = False
        self.led = led
        self.types = ["press", "hold"]
        self.type = type
        self.keyboard = Keyboard(usb_hid.devices)

    @property
    def is_hold(self):
        return self.type == "hold"

    @property
    def changes_layer(self):
        return self.type == "hold"

    def was_pressed(self):
        return not self.driver.value and not self.held

    def was_released(self):
        return self.driver.value and self.held

    def press(self, layer):
        self.held = True
        if layer <= len(self.keys):
            print(self.name, *self.keys[layer])
            #self.keyboard.send(*self.keys[layer])

        self.led.fade_start("up")
        print(self.changes_layer)
        return self.changes_layer

    def release(self, layer):
        self.held = False
        if not (layer == 0 and self.is_hold):
            self.led.fade_start("down")
