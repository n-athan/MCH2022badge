import display
import math
import buttons
import mch22
from machine import Pin
from neopixel import NeoPixel
import time

## settings
selected = 0
choice = 0
flags = [
    ["rainbow",["0xFF0000","0xFF8800","0xFFFF00","0x00FF00","0x0000FF","0xFF00FF"]],
    ["trans",["0x63E2EB","0xEB63DF","0xFFFFFF","0xEB63DF","0x63E2EB"]],
    ["bi",["0xC70A62","0x46068F","0xC920B9","0x46068F","0xC70A62"]],
    ["nonbinary",["0xFFFF00","0xFFFFFF","0xAF07F7","0x00000"]],
    ["lesbian",["0xF71F07","0xF77707","0xFFFFFF","0xF7078F","0xD10420"]],
    ["gay",["0x269435","0x39C44C","0x49F560","0xFFFFFF","0x4949F5","0x2F2F9E","0x1F1F63"]]
    ]

## Buttons
display.drawFill(255)
menuh= display.height()-30
display.drawRect(0,menuh,display.width(),30,1,0)
display.drawText(30,menuh,'home')
display.drawText(115,menuh,'menu')
display.flush()

def on_home_btn(pressed):
    if pressed:
        mch22.exit_python()

buttons.attach(buttons.BTN_HOME,on_home_btn)

def on_menu_btn(pressed):
    if pressed:
        createMenu(flags)

buttons.attach(buttons.BTN_MENU,on_menu_btn)

def on_A_btn(pressed):
    global choice
    global selected
    if (pressed):
        selected = choice
        main(flags[selected][1],np)

buttons.attach(buttons.BTN_A,on_A_btn)

def on_B_btn(pressed):
    if (pressed):
        # dont change flag
        main(flags[selected][1],np)
        
buttons.attach(buttons.BTN_B,on_B_btn)

def createMenu(flags):
    display.drawFill(0)
    for i in range(0,len(flags)):
        display.drawText(10,10+i*20,flags[i][0])
    display.drawRect(0,5+choice*20,100,30,0,0xFF0000)
    display.flush()

def on_up_btn(pressed):
    global choice
    if (pressed):
        if choice > 0:
            choice = choice - 1
    createMenu(flags)
        
buttons.attach(buttons.BTN_UP,on_up_btn)

def on_down_btn(pressed):
    global choice
    if (pressed):
        if choice < 0:
            choice = choice + 1
    createMenu(flags)
        
buttons.attach(buttons.BTN_DOWN,on_down_btn)

## NEOPixels
def hex2RGB(color):
	color = color.lstrip('0').lstrip('x')
	return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


def neoPixelFill(color,np):
    for x in range(0,5):
         np[x] = color
    np.write()
    
def neoPixelCycle(flag,np):
    index = int(time.ticks_ms()/1000)%len(flag)
    for x in range(0,5):
        rgb = hex2RGB(flag[(index+x)%len(flag)])
        np[x] = rgb
    np.write()

powerPin = Pin(19, Pin.OUT)
dataPin = Pin(5, Pin.OUT)
np = NeoPixel(dataPin, 5)
powerPin.on()

## Flags
def pride(flag,xoff,diag,w,h): 
    display.drawFill(0x000000)
    stripe = int(h/(len(flag)-1))
    x = 0
    while x <= w:
        yprev = 0
	for index in range(1,len(flag)+1):
	    yoff = stripe*index-stripe/2
	    y = yoff+math.sin((x+xoff+diag*index)/20)*stripe/4
	    display.drawLine(x,yprev,x,y,int(flag[index-1]))
	    yprev = y
	display.drawLine(x,yprev,x,h,int(flag[index-1]))
	x = x + 1

## Main
def main(flag,np):
    w = display.width()
    h = display.height() - 30

    xoff = 0    
    while True:
        pride(flag,xoff,16,w,h)
        xoff = xoff + 1
        neoPixelCycle(flag,np)
        menuh= display.height()-30
        display.drawRect(0,menuh,display.width(),30,1,0)
        display.drawText(30,menuh,'home')
        display.drawText(115,menuh,'menu')
        display.flush()
        if buttons.value(1):
            break

main(flags[selected][1],np)