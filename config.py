import board

from adafruit_hid.keycode import Keycode

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