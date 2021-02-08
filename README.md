# Raspberry Pi Pico StreamDeck

## About this Project

This is a work in progress progress to create an OBS StreamDeck using a Raspberry Pi and CircuitPython.

Some of this work is based on a nice blog post by Hriday which shows how to get the Pico working as a HID device, emulating a keyboard;

https://hridaybarot.home.blog/2021/01/31/using-raspberry-pi-pico-has-hid-device-to-control-mouse-and-keyboard/

I'll be updating this README very soon to show how it all works...

![Pico StreamDeck Build 1](images/build1.jpg "Raspberry Pi Pico StreamDeck Build 1")

# In Action

![Pico StreamDeck In Action](images/animation.gif "Raspberry Pi Pico StreamDeck In Action")

## Basic Circuit

![Pico StreamDeck Circuit](images/circuit.png "Raspberry Pi Pico StreamDeck Circuit")

# Case

My good friend Clifford Agius and his son are working on a case for this project.

It'll be based on this;

https://www.thingiverse.com/thing:4186055

# CircuitPython HID

You can find some more info about the CircuitPython KeyMappings here;

https://circuitpython.readthedocs.io/projects/hid/en/latest/_modules/adafruit_hid/keycode.html

## Instructions

- Plug in the Raspberry Pi Pico while holding the onboard button.
- Your PC will mount the Pico as a drive
- Copy the `adafruit-circuitpython-raspberry_pi_pico-en_US-6.2.0-beta.1.uf2` file to the Pico
- The Pico will reboot once it's done with CircuitPython onboard.
- Copy the `adafruit_hid` folder and the `code.py` file to the Pico
- In OBS setup Hotkeys for the different scenes by putting your cursor in the Hotkey Box and pressing a button...

```
Scene 1 =  ctrl + KeyPad 1
Scene 2 =  ctrl + KeyPad 2
Scene 3 =  ctrl + KeyPad 3
Scene 4 =  ctrl + KeyPad 4
Scene 5 =  ctrl + KeyPad 5
Scene 6 =  ctrl + KeyPad 6
Scene 7 =  ctrl + KeyPad 7
Scene 8 =  ctrl + KeyPad 8
Scene 9 =  ctrl + KeyPad 9
Scene 10 =  ctrl + KeyPad 0
```

- Press the buttons to change scenes in OBS!
- Each button will light a corresponding LED to show which Scene is currently active.

## Future Planning

- 3D print a case and keycaps
- Look at Bluetooth / WebSockets (Will need add on circuitary!)