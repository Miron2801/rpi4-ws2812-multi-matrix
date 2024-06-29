import os
import time
from ws281xMatrix import WS281xMatrix

path = os.path.dirname(__file__)
im = os.path.join(path, 'sample.png')
ani = os.path.join(path, 'sample.gif')
pica = os.path.join(path, 'pikacy.gif')
fire = os.path.join(path, 'fire2.gif')
moon = os.path.join(path, 'moon.gif')
pt = os.path.join(path, 'pt.png')
vmws = os.path.join(path, 'vmware2.png')
vsfi = os.path.join(path, 'apple.png')
raspberrypi = os.path.join(path, 'raspberrypi.png')

screen = WS281xMatrix()

def change_color(color):
    screen.next_frame(screen.blank_frame(color))

try:
    while True:
        # print('Red')
        # time.sleep(2)
        # print('Green')
        # change_color((0,255,0))
        # time.sleep(2)
        # print('Blue')
        # change_color((0,0,255))
        # time.sleep(2)
        # screen.render_image(im)
        # time.sleep(2)

        screen.render_animation(ani)
        screen.render_animation(pica)
        screen.render_animation(fire)
        screen.render_animation(moon)
        time.sleep(2)
        screen.render_image(raspberrypi)
        time.sleep(10)

except KeyboardInterrupt:
    screen.kill()
