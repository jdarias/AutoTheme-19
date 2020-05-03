import pystray
from PIL import Image
from pystray import MenuItem as item
import time
import sys

#print(dir(Image))
#print(dir(pystray.Icon))


def make_me_stop():
    print("I'm trying to stop")
    icon.stop()
    sys.exit()

icon="16/002-moon.png"
image=Image.open(icon)

menu=(
        item("Options", lambda: print("Call options")),
        item("Exit", lambda: make_me_stop())
)

icon=pystray.Icon("AutoTheme-19", image, "AutoTheme-19", menu)
icon.run()

try:
    icon="16/001-sun.png"
    while True:
        print("I won't stop")
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    print("I stopped!")
