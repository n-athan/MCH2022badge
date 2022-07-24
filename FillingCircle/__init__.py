import display
import random
from machine import Pin
from neopixel import NeoPixel
import buttons
import mch22

def on_home_btn(pressed):
    if pressed:
        mch22.exit_python()

buttons.attach(buttons.BTN_HOME,on_home_btn)

def fillingCircle(color):
    x = 0
    while x <= 360:
        display.drawFill(0x000000)
        display.drawCircle(160,120,100,0,x,1,color)
        display.flush()
        x = x + 2

def hex2RGB(color):
	color = hex(color)
	color = color.lstrip('0').lstrip('x')
	return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

def neoPixelFill(color,np):
    for x in range(0,5):
         np[x] = color
    np.write()

powerPin = Pin(19, Pin.OUT)
dataPin = Pin(5, Pin.OUT)
np = NeoPixel(dataPin, 5)
powerPin.on()

while True:
    clr = random.randrange(0x000000,0xFFFFFF)
    rgb = hex2RGB(clr)
    neoPixelFill(rgb,np)
    fillingCircle(clr)