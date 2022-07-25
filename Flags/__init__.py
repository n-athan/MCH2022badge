import display
import math
import buttons
import mch22
from machine import Pin
from neopixel import NeoPixel
import time

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
        createMenu(True,flags)

buttons.attach(buttons.BTN_MENU,on_menu_btn)

def on_A_btn(pressed):
    if (pressed):
        # change flag to selected
        main(flag,np)

buttons.attach(buttons.BTN_A,on_A_btn)

def on_B_btn(pressed):
    if (pressed):
        # dont change flag
        main(flag,np)
        
buttons.attach(buttons.BTN_B,on_B_btn)

def createMenu(selected,flags):
    display.drawFill(0)
    for i in range(1,len(flag)+1):
        display.drawText(10,10+i*20,flags[i-1])
    display.flush()

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
flag = ["0xFF0000","0xFF8800","0xFFFF00","0x00FF00","0x0000FF","0xFF00FF"]
flags = ["rainbow","bi"]
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

main(flag,np)