# this one uses infi.systray instead of pystray

from infi.systray import SysTrayIcon
import time
import sys
import threading


makemestop=False

# dummy functions
# functions that will be trigered by infi.systray need the variable that contains the SysTrayIcon object as a parameter
def my_dummy(icon):
    print("Call Options")


# the function to quit the program
def make_me_stop(icon):
    print("I'm trying to stop")
    global makemestop
    makemestop=True
    my_x.join()
    #icon.shutdown()
    print("I STOPPED!")

# This must go into another thread
def myloop():
    try:
        #while makemestop==False:
        while True:
            print("I won't stop - ", makemestop)
            time.sleep(3)
            icon.update(icon="16/001-sun.ico")
            icon.update(hover_text="Sun Icon, day version")
            time.sleep(3)

            icon.update(icon="16/001-sun2.ico")
            icon.update(hover_text="Sun Icon, night version")
            time.sleep(3)

            icon.update(icon="16/002-moon.ico")
            icon.update(hover_text="Moon Icon, day version")
            time.sleep(3)
            
            icon.update(icon="16/002-moon2.ico")
            icon.update(hover_text="Moon Icon, night version")
            time.sleep(3)
            
            if makemestop==True:
                break
    except:
        pass

    finally:
        print("FINALLY... I really stopped")
        sys.exit()


# this is the main thread
if __name__=="__main__":
    my_x=threading.Thread(target=myloop)
    my_x.start()

    menu_options=(
            ("Options", None, my_dummy),
    )

    icon=SysTrayIcon("16/001-sun.ico", "My icon title", menu_options, on_quit=make_me_stop)
    icon.start()
