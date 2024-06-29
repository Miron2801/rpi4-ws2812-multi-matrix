import time
from rpi_ws281x import PixelStrip, Color
import math
LED_COUNT = 1024
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 20
LED_INVERT = False

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()
    
MATRIX_HEIGHT = 8
MATRIX_WIDTH = 32
MATRIX_COUNT = 4
num_pixels = MATRIX_HEIGHT * MATRIX_WIDTH
color = (0, )
def snake_led_number(x, y):
        delimeter = (y // 8)             
        if delimeter % 2 == 1:
          if (y % 2 == 0):
            pixel = delimeter * 256 + (((MATRIX_WIDTH - x)  - delimeter - 1 ) * MATRIX_HEIGHT) + y

          else:
            pixel = delimeter * 256 + (MATRIX_WIDTH - x + delimeter -1) * MATRIX_HEIGHT + (MATRIX_HEIGHT - y - 1)
        else:
            if (y % 2 == 0):
              pixel = (x - delimeter) * MATRIX_HEIGHT + y + delimeter * 256 
            else:
              pixel = (x + delimeter) * MATRIX_HEIGHT + (MATRIX_HEIGHT - y - 1) + delimeter * 256 
        return pixel, color

def snake_led_number_rewrite(x, y):
        delimeter = (y // 8)             
        if delimeter % 2 == 1:
          if (x % 2 == 0):
            pixel = delimeter * 256 + (((MATRIX_WIDTH - x)  - delimeter - 1 ) * MATRIX_HEIGHT) + y

          else:
            pixel = delimeter * 256 + (MATRIX_WIDTH - x + delimeter -1) * MATRIX_HEIGHT + (MATRIX_HEIGHT - y - 1)
        else:
            if (x % 2 == 0):
              pixel = (x - delimeter) * MATRIX_HEIGHT + y + delimeter * 256 
            else:
              pixel = (x + delimeter) * MATRIX_HEIGHT + (MATRIX_HEIGHT - y - 1) + delimeter * 256 
        return pixel



def draw_circle(cx, cy, radius):
    for x in range(32):
            for y in range(32):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    led = snake_led_number_rewrite(x, y)    
                    # print("im here", led)

                    strip.setPixelColor(led, Color(0, 0,255))  # Выключение всех светодиодов
    strip.show()
def clean():
        for cx in range(1024):
                strip.setPixelColor(cx, Color(0,0,0))
        strip.show()
for cx in range(0, 32, 4):
  for cy in range(0, 32, 4):
      for r in range(0, 16):
        draw_circle(cx, cy, r)
      clean()
        
