import pystray
from PIL import Image
from pystray import MenuItem as item
import time
import sys
import threading


makemestop=False
icon="16/002-moon.png"

# the function to quit the program
def make_me_stop():
    print("I'm trying to stop")
    global makemestop
    makemestop=True
    my_x.join()
    icon.stop()
    print("I STOPPED!")
    sys.exit()

# This must go into another thread
def myloop():
    try:
        global icon
        icon="16/001-sun.png"
        while makemestop==False:
            print("I won't stop - ", makemestop)
            time.sleep(1)
    except:
        print("yass... I really stopped")

# this is the main thread
if __name__=="__main__":
    my_x=threading.Thread(target=myloop)
    my_x.start()

    image=Image.open(icon)

    menu=(
            item("Options", lambda: print("Call options")),
            item("Exit", lambda: make_me_stop())
    )

    icon=pystray.Icon("My icon title", image, "My icon title", menu)
    icon.run()
