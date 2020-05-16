"""
as of 16/05/2020 pystray does not support icon updates,
that's why i'm not using it in autotheme.
There's also the issue with PIL dependency

Too bad since infi.systray has its own issues
"""

import pystray
from PIL import Image
from pystray import MenuItem as item
import time
import sys
import threading

#print(dir(Image))
print(dir(pystray.Icon))

makemestop=False
icon_img="16/002-moon.png"

# the function to quit the program
def make_me_stop():
    print("I'm trying to stop")
    global makemestop
    makemestop=True
    print(makemestop)
    print("did i stop?")
    my_x.join()
    print("I STOPPED!")
    icon.stop()
    #sys.exit()

# This must go into another thread
def myloop():
    try:
        global icon_img
        icon_img="16/001-sun.png"
        while makemestop==False:
            print("I won't stop - ", makemestop)
            time.sleep(2)

    except SystemExit:
        pass
    finally:
        print("yass... I really stopped")

# this is the main thread
if __name__=="__main__":
    my_x=threading.Thread(target=myloop)
    my_x.start()

    image=Image.open(icon_img)

    menu=(
            item("Options", lambda: print("Call options")),
            item("Exit", lambda: make_me_stop())
    )

    icon=pystray.Icon("AutoTheme-19", image, "AutoTheme-19", menu)
    icon.run()
