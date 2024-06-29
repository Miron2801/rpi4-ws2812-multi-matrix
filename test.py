import time
from rpi_ws281x import PixelStrip, Color
import math
LED_COUNT = 1024
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 10
LED_INVERT = False

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

# for i in range(LED_COUNT):
#     strip.setPixelColor(i, Color(255, 0, 0))  # Включение светодиода (красный цвет)
#     strip.show()
#     # time.sleep(0.01)

#     strip.setPixelColor(i, Color(0, 0, 0))  # Выключение светодиода
#     strip.show()

# for i in range(LED_COUNT):
#     strip.setPixelColor(i, Color(0, 0, 0))  # Выключение всех светодиодов
    
MATRIX_HEIGHT = 8
MATRIX_WIDTH = 32
MATRIX_COUNT = 4
num_pixels = MATRIX_HEIGHT * MATRIX_WIDTH
def snake_led_number(x, y):
        # delimeter = 
        if x < 0 or x >= MATRIX_WIDTH:
            return

        if y < 0 or y >= MATRIX_HEIGHT:
            return

        led_number: int = x * MATRIX_HEIGHT + y
        if (math.floor(led_number / MATRIX_HEIGHT) % 2) == 1:
          return (x + 1) * MATRIX_HEIGHT - y - 1
        else:
          return led_number
for i in range(8):
    strip.setPixelColor(snake_led_number(i, 0), Color(0, 0, 255))  # Выключение всех светодиодов
    time.sleep(0.1)
    strip.show()