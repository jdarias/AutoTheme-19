import pystray
from PIL import Image
from pystray import MenuItem as item
import time
import sys

#print(dir(Image))
#print(dir(pystray.Icon))


def make_me_stop():
    icon.stop()
    sys.exit()
    
image=Image.open("16/001-sun.png")

menu=(
        item("Options", lambda: print("nope")),
        item("Exit", lambda: make_me_stop())
)

icon=pystray.Icon("AutoTheme-19", image, "AutoTheme-19", menu)
icon.run()

#while True:
#    print("I won't stop")
#    time.sleep(2)
