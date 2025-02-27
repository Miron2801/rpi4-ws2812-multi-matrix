"""WS281X Matrix Renderer Class.

Use Case:
  - If you have a NeoPixel (or similar LED panel from ADAFruit or others) or
    similar LED Matrix and would like to display frames, this will make your
    life easier. Adafruit offers a microcontroller library and complains RPi
    does not meet their timing requirements
Usage:
  - See demo.py
Prereq:
  - pip install pillow rpi_ws281x
Contents:
  - Matrix Setup Class.
"""

__author__ = "Nishant Arora"
__version__ = '0.0.2'
__maintainer__ = "Nishant Arora"
__email__ = "me@nishantarora.in"

from PIL import Image, ImageSequence
import queue
import rpi_ws281x as ws
from threading import Timer

MATRIX_HEIGHT = 8
MATRIX_WIDTH = 32
MATRIX_COUNT = 4

class WS281xMatrix(object):
    """Represents the LED Matrix."""

    def __init__(
        self,
        width = 32,          # Number of pixels in width
        height = 32,         # Number of pixels in height
        led_pin = 18,        # PWM pin
        freq = 800000,       # 800khz
        dma_channel = 10,
        invert = False,      # Invert Shifter, should not be needed
        brightness = 0.2,    # 1: 100%, 0: 0% everything in between.
        led_channel = 0,     # set to '1' for GPIOs 13, 19, 41, 45 or 53
        led_type = None,     # Read the documentation to get your strip type.
        fps = 20             # frames per second.
    ):
        if width < 1 or height < 1:
            raise Exception('Invalid Dimensions')
        if brightness < 0 or brightness > 1:
            raise Exception('Brightness can only be between 0 and 1')
        else:
            brightness = int(brightness * 255)    # Make this more relevant.
        self.width = width
        self.height = height
        self.fps = fps
        self.wh_ratio = float(width) / height
        self.pixels = width * height

        # Init the strip here.
        self.strip = ws.PixelStrip(self.pixels, led_pin, freq, dma_channel, invert,
                                   brightness, led_channel, led_type)
        self.strip.begin()

        # Maintaining the state of the strip.
        self.power = True
        self.buffer = queue.Queue()
        self.reset()

        # Init the loop so that we can start displaying the buffer.
        self.loop()

    def kill(self):
        """Kills the instance of the the matrix and wipes the display."""
        self.power = False
        self.reset()

    def reset(self):
        """Wipes the display."""
        self.buffer = queue.Queue()
        self.render(self.blank_frame((0,0,0)))

    def loop(self):
        """This method is called over and over again to render whatever we have
           available in the buffer.
        """
        if self.power:
            if not self.buffer.empty():
                frame = self.buffer.get()
                self.render(frame)
            # Non Blocking thread.
            Timer(float(1)/self.fps, self.loop).start()
        else:
            self.reset()

    def next_frame(self, frame, override = False):
        """Queues the next frame in the buffer. We can also override the current
           buffer and display this frame instead.

           Args:
             frame: RGB representation of the frame.
             override: optional
        """
        if override:
            self.buffer = Queue()

        self.buffer.put(frame)
    def snake_led_number_rewrite(self, x, y):
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
    def render(self, frame):
        """Renders the supplied frame on the matrix.
           Args:
             frame: RGB representation of the frame.
        """
        x = 0
        y = 0
        for y in range(len(frame)):
            for x in range(len(frame[y])):
                self.strip.setPixelColor(self.snake_led_number_rewrite(y, x), ws.Color(*frame[y][x]))
        self.strip.show()

    def blank_frame(self, color):
        """Generates a RGB representation of the frame of a given color.
           Args:
             color: RGB Tuple
           Returns:
             frame rgb values.
        """
        return [[color] * self.width] * self.height

    def __pad_size(self, size):
        """Calculates the padding required to render and center the image on
           the matrix
           Args:
             size: of the image to be displayed.
           Returns:
             calculated size.
        """
        (w,h) = size
        if float(w)/h != self.wh_ratio:
            if max(size) == w:
                return (w, int(w/self.wh_ratio))
            return (int(h*self.wh_ratio), h)
        return size

    def __rgb_translate(self, im):
        """Translates a given image object to corresponding RGB frame.
           Args:
             im: image object
           Returns:
             rgb translated values centered on the given matrix.
        """
        pad_size = self.__pad_size(im.size)
        pad = Image.new("RGB", pad_size, (0, 0, 0, 0))
        pad.paste(im, (int((pad_size[0]-im.size[0])*0.5),
                       int((pad_size[1]-im.size[1])*0.5)))
        new_size = (self.width, self.height)
        pad.thumbnail(new_size)

        pix = pad.load()

        frame = []
        for i in range(new_size[0]):
            row = []
            for j in range(new_size[1]):
                row.append(pix[i,j])
            frame.append(row)
        return frame

    def render_image(self, image_path):
        """Renders an actual png/jpg image on the LED matrix.
           Args:
             image_path: resolvable path to the image.
        """
        im = Image.open(image_path)
        frame = self.__rgb_translate(im)
        self.next_frame(frame)

    def render_animation(self, ani_path, loops = 5):
        """Renders animated images on the matrix.
           Args:
             ani_path: resolvable path to the animation
             loops: how many times to loop the image, 5 by default.
        """
        im = Image.open(ani_path)
        if not im.is_animated:
            raise Exception("Not an animation")
        ani = []

        # translate animation.
        for frame in ImageSequence.Iterator(im):
            ani.append(self.__rgb_translate(frame))

        # Queue the frames
        for loop in range(loops):
            for frame in ani:
                self.next_frame(frame)
