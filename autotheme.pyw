# Since we are all confined I decided to learn python during the lockdown.
# This script changes the windows theme according to a specific hour/minute

# import what we need first.
import winreg as wr
import time
import threading
from infi.systray import SysTrayIcon
import opts



### OPTIONS FILE LOAD ###
try:
    opts.load_conf()

except IOError:
    # open the options dialog to get the variables
    opts.opts_diag()
    
    # Then we read the file
    opts.load_conf()
    
finally:
    # So far no need for stuff here
    pass


# AUXILIARY CODE FOR THE TRAY ICON

# control variable for the tray icon    
makemestop=False

# call the options
def call_opts_tray(icon):
    opts.opts_diag()
    
# function that will end the program
def make_me_stop(icon):
    global makemestop
    makemestop=True

    # Closing sequence
    mylogic.join()
    print("I'M STOPPING!")


# CREATE THE ACCESS POINTS TO MODIFY THE REGISTRY

# myregistry is the registry connection to read from and to modify
myregistry = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)

# openkey is used to read the theme settings as they are.
openkey = wr.OpenKeyEx(myregistry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, wr.KEY_QUERY_VALUE) 

# this function will modify the registry and uses the myregistry access point
# theme_setting is either "AppsUseLightTheme" or "SystemUsesLightTheme"
# theme_value is either 1 or 0
def mod_setting(theme_setting, theme_value):
    modkey = wr.OpenKeyEx(myregistry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, wr.KEY_WRITE) 
    wr.SetValueEx(modkey, theme_setting, 0, wr.REG_DWORD, theme_value)
    wr.CloseKey(modkey)

# This function updates the icon if it needs to be updated
# new_icon is string pointing to the file
# new_text is string 
def update_icon(new_icon, new_text):
    if icon._icon!=new_icon or icon._hover_text!=new_text:
        # update the icon
        icon.update(icon=new_icon, hover_text=new_text)


# All of this goes into a thread
def logic_thread():
    # try-except to be able to ctrl-c the program if launched from cmd
    try:
        while True:
            # getting the current time
            mytime = time.localtime()

            # get the current hour and minute from the mytime tuple we just created
            currenthour = mytime.tm_hour # note to myself: remember we can use mytime.tm_hour or mytime[3]
            currentmin = mytime.tm_min  # and mytime.tm_min or mytime[4] here

            # Get the values of what we need to manipulate. we will use them in further conditions to check what theme is active across system and apps
            apps_theme = wr.QueryValueEx(openkey, "AppsUseLightTheme")
            system_theme = wr.QueryValueEx(openkey, "SystemUsesLightTheme")
            # remember if apps_theme[0] == 0 and system_theme[0] == 0 it means we are using the dark theme

    #       To activate the light theme we check for 3 scenarios:
    #       1) currenthour is the same as opts.prog_options["light_hour"] AND currentmin is equal or later than opts.prog_options["light_minute"]
    #       2) currenthour is later than opts.prog_options["light_hour"] AND earlier than opts.prog_options["dark_hour"]
    #       3) currenthour is same as opts.prog_options["dark_hour"] AND currentmin is earlier than opts.prog_options["dark_minute"]
    #       if one of them is true, it means we are on light theme time

            if (currenthour == opts.prog_options["light_hour"] and currentmin >= opts.prog_options["light_minute"]) or (currenthour > opts.prog_options["light_hour"] and currenthour < opts.prog_options["dark_hour"]) or (currenthour == opts.prog_options["dark_hour"] and currentmin < opts.prog_options["dark_minute"]):
                # we are in the light theme hour range, we do here the registry change.

                # Set the theme for the apps.
                # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
                # Then if we work at night we set the dark theme
                # And last, we set the light theme
                
                if apps_theme[0] == 0 and not opts.prog_options["work_night"]: # using dark theme and not working at night? Set light theme
                    mod_setting("AppsUseLightTheme", 1)
                    update_icon("icons/16/B16sun.ico", "AutoTheme-19: Clear theme, day worker")

                elif apps_theme[0] == 1 and opts.prog_options["work_night"]: # using light theme and working at night? set dark theme
                    mod_setting("AppsUseLightTheme", 0)
                    update_icon("icons/16/W16sun.ico", "AutoTheme-19: Dark theme, night worker")
                    
                elif apps_theme[0] == 0 and opts.prog_options["work_night"]: # using dark theme (during daytime) and working at night? all is ok, do nothing
                    update_icon("icons/16/W16sun.ico", "AutoTheme-19: Dark theme, night worker")
                    print("day case 1: dark theme, working at night")
                else: # light theme is already set, do nothing
                    update_icon("icons/16/B16sun.ico", "AutoTheme-19: Clear theme, day worker")
                    print("day case 2: clear theme, working by day")

                # Set the theme for the system. 
                # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
                # Then if we work at night we set the dark theme
                # And last, we set the light theme

                if system_theme[0] == 0 and not opts.prog_options["work_night"]: # using dark theme and not working at night? Set light theme
                    mod_setting("SystemUsesLightTheme", 1)
                elif system_theme[0] == 1 and opts.prog_options["work_night"]: # using light theme and working at night? set dark theme
                    mod_setting("SystemUsesLightTheme", 0)
                elif system_theme[0] == 0 and opts.prog_options["work_night"]: # using dark theme and working at night? all is ok, do nothing
                    pass
                else: # light theme is already set, do nothing
                    pass

    #       If none of that is true we check for other 3 cases:
    #       1) currenthour is the same as opts.prog_options["dark_hour"] AND currentmin is equal or later than opts.prog_options["dark_minute"] 
    #       2) currenthour is later than opts.prog_options["dark_hour"] OR currenthour is earlier than opts.prog_options["light_hour"]
    #       3) currenthour is same as opts.prog_options["light_hour"] AND currentmin is earlier than opts.prog_options["light_minute"]
    #       if one of these is true, it means we are on dark theme time

            elif (currenthour == opts.prog_options["dark_hour"] and currentmin >= opts.prog_options["dark_minute"]) or (currenthour > opts.prog_options["dark_hour"] or currenthour < opts.prog_options["light_hour"]) or (currenthour == opts.prog_options["light_hour"] and currentmin < opts.prog_options["light_minute"]):
                # we are in the dark theme hour range, we do here the registry change.

                # Set the theme for the apps. 
                # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
                # Then if the theme is dark and we work at night we set the light theme
                # Then if we use light theme and we work at night we do nothing, it's the way we want
                # For all else we leave it like it is
                
                if apps_theme[0] == 1 and not opts.prog_options["work_night"]: # using light theme and not working at night? Set dark theme
                    mod_setting("AppsUseLightTheme", 0)
                    update_icon("icons/16/W16moon.ico", "AutoTheme-19: Dark theme, day worker")

                elif apps_theme[0] == 0 and opts.prog_options["work_night"]: # using dark theme and working at night? set light theme
                    mod_setting("AppsUseLightTheme", 1)
                    update_icon("icons/16/B16moon.ico", "AutoTheme-19: Clear theme, night worker")

                elif apps_theme[0] == 1 and opts.prog_options["work_night"]: # using clear theme (at nighttime) and working at night? all is ok, do nothing
                    update_icon("icons/16/B16moon.ico", "AutoTheme-19: Clear theme, night worker")
                    print("night case 1: clear theme at night")
                else: # dark theme is already set, do nothing
                    update_icon("icons/16/W16moon.ico", "AutoTheme-19: Dark theme, day worker")
                    print("night case 2: dark theme at night")

                # Set the theme for the system. 
                # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
                # Then if the theme is dark and we work at night we set the light theme
                # Then if we use light theme and we work at night we do nothing, it's the way we want
                # For all else we leave it like it is

                if system_theme[0] == 1 and not opts.prog_options["work_night"]: # using light theme and not working at night? Set dark theme
                    mod_setting("SystemUsesLightTheme", 0)
                elif system_theme[0] == 0 and opts.prog_options["work_night"]: # using dark theme and working at night? set light theme
                    mod_setting("SystemUsesLightTheme", 1)
                elif system_theme[0] == 1 and opts.prog_options["work_night"]: # using light theme and working at night? all is ok, do nothing
                    pass
                else: # dark theme is already set, do nothing
                    pass

            else: # This should not be seen
                print("Something is wrong")
            
            # control variable gets true? start exit sequence
            if makemestop==True:
                break

            # sleep the process to lower cpu usage. 
            time.sleep(5)

    # yeah this is not that useful if you're using pyw extension to hide the console
    except (KeyboardInterrupt, SystemExit):
        # Place here the code to close the reg object that reads the registry
        wr.CloseKey(openkey)
        print("Program finished")

    finally:
        # Place here the code to close the reg object that reads the registry
        wr.CloseKey(openkey)

        print("Logic thread finished")


# this is the main thread
if __name__=="__main__":

    menu_options=(
            ("Options", None, call_opts_tray),
    )

    icon=SysTrayIcon("icons/16/B16sun.ico", "AutoTheme-19", menu_options, on_quit=make_me_stop)
    
    # Start the logic thread after defining the icon, because the logic thread needs to update the icon.
    mylogic=threading.Thread(target=logic_thread)
    mylogic.start()
    
    # now we start the tray icon
    icon.start()
