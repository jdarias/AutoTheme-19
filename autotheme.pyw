# Since we are all confined I decided to learn python during the zombie apocalypse.
# This script changes the windows theme according to a specific hour/minute

# import what we need first.
import winreg as wr
import time
import ast
import opts

# This is the time when the light theme will be activated (AKA. Sunrise). WARNING: no trailing zeroes!
light_active_hour = 6 # integer between 0-23
light_active_minute = 30 # integer between 0-59

# This is the time when the dark theme will be activated (AKA. Sunset). WARNING: Idem!
dark_active_hour = 18 # integer between 0-23
dark_active_minute = 30 # integer between 0-59

# do you work at night? If True we will set the light theme at night and dark theme during the day. We gotcha Nosferatu! 
work_night = False

### OPTIONS FILE ###
try:
    openconf=open("conf.conf", "r")
    contentconf=openconf.read()
    
    # prog_options will contain the dictionary with the variables
    prog_options=ast.literal_eval(contentconf)
    
    # what do we have?
    #print(prog_options["light_hour"], " - ", type(prog_options["light_hour"]))
    #print(prog_options["light_minute"], " - ", type(prog_options["light_minute"]))
    #print(prog_options["dark_hour"], " - ", type(prog_options["dark_hour"]))
    #print(prog_options["dark_minute"], " - ", type(prog_options["dark_minute"]))
    #print(prog_options["use_location"], " - ", type(prog_options["use_location"]))
    #print(prog_options["work_night"], " - ", type(prog_options["work_night"]))

except IOError:
    # open the options dialog to get the variables
    opts.opts_diag()
    # Then we read the file
    
finally:
    #opts.close()
    pass

# Create the access point to modify the registry
myregistry = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
openkey = wr.OpenKeyEx(myregistry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, wr.KEY_ALL_ACCESS) 

# try-except to be able to ctrl-c the program if launched from cmd
try:
    while True:
        # getting the current time
        mytime = time.localtime()

        # get the current hour and minute from the mytime tuple we just created
        currenthour = mytime[3] # note to myself: self, remember we can also use mytime.tm_hour
        currentmin = mytime[4]  # and mytime.tm_min here

        # Get the values of what we need to manipulate. we will use them in further conditions to check what theme is active across system and apps
        apps_theme = wr.QueryValueEx(openkey, "AppsUseLightTheme")
        system_theme = wr.QueryValueEx(openkey, "SystemUsesLightTheme")
        # remember if apps_theme[0] == 0 and system_theme[0] == 0 it means we are using the dark theme

#       To activate the light theme we check for 3 scenarios:
#       1) currenthour is the same as light_active_hour AND currentmin is equal or later than light_active_minute
#       2) currenthour is later than light_active_hour AND earlier than dark_active_hour
#       3) currenthour is same as dark_active_hour AND currentmin is earlier than dark_active_minute
#       if one of them is true, it means we are on light theme time

        if (currenthour == light_active_hour and currentmin >= light_active_minute) or (currenthour > light_active_hour and currenthour < dark_active_hour) or (currenthour == dark_active_hour and currentmin < dark_active_minute):
            # we are in the light theme hour range, we do here the registry change.

            # Set the theme for the apps. 
            # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
            # Then if we work at night we set the dark theme
            # And last, we set the light theme
            
            if apps_theme[0] == 0 and not work_night: # using dark theme and not working at night? Set light theme
                wr.SetValueEx(openkey, "AppsUseLightTheme", 0, wr.REG_DWORD, 1)
            elif apps_theme[0] == 1 and work_night: # using light theme and working at night? set dark theme
                wr.SetValueEx(openkey, "AppsUseLightTheme", 0, wr.REG_DWORD, 0)
            elif apps_theme[0] == 0 and work_night: # using dark theme and working at night? all is ok, do nothing
                pass
            else: # light theme is already set, do nothing
                pass

            # Set the theme for the system. 
            # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
            # Then if we work at night we set the dark theme
            # And last, we set the light theme

            if system_theme[0] == 0 and not work_night: # using dark theme and not working at night? Set light theme
                wr.SetValueEx(openkey, "SystemUsesLightTheme", 0, wr.REG_DWORD, 1)
            elif system_theme[0] == 1 and work_night: # using light theme and working at night? set dark theme
                wr.SetValueEx(openkey, "SystemUsesLightTheme", 0, wr.REG_DWORD, 0)
            elif system_theme[0] == 0 and work_night: # using dark theme and working at night? all is ok, do nothing
                pass
            else: # light theme is already set, do nothing
                pass

#       If none of that is true we check for other 3 cases:
#       1) currenthour is the same as dark_active_hour AND currentmin is equal or later than dark_active_minute 
#       2) currenthour is later than dark_active_hour OR currenthour is earlier than light_active_hour
#       3) currenthour is same as light_active_hour AND currentmin is earlier than light_active_minute
#       if one of these is true, it means we are on dark theme time

        elif (currenthour == dark_active_hour and currentmin >= dark_active_minute) or (currenthour > dark_active_hour or currenthour < light_active_hour) or (currenthour == light_active_hour and currentmin < light_active_minute):
            # we are in the dark theme hour range, we do here the registry change.

            # Set the theme for the apps. 
            # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
            # Then if the theme is dark and we work at night we set the light theme
            # Then if we use light theme and we work at night we do nothing, it's the way we want
            # For all else we leave it like it is
            
            if apps_theme[0] == 1 and not work_night: # using light theme and not working at night? Set dark theme
                wr.SetValueEx(openkey, "AppsUseLightTheme", 0, wr.REG_DWORD, 0)
            elif apps_theme[0] == 0 and work_night: # using dark theme and working at night? set light theme
                wr.SetValueEx(openkey, "AppsUseLightTheme", 0, wr.REG_DWORD, 1)
            elif apps_theme[0] == 1 and work_night: # using dark theme and working at night? all is ok, do nothing
                pass
            else: # light theme is already set, do nothing
                pass

            # Set the theme for the system. 
            # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
            # Then if the theme is dark and we work at night we set the light theme
            # Then if we use light theme and we work at night we do nothing, it's the way we want
            # For all else we leave it like it is

            if system_theme[0] == 1 and not work_night: # using light theme and not working at night? Set dark theme
                wr.SetValueEx(openkey, "SystemUsesLightTheme", 0, wr.REG_DWORD, 0)
            elif system_theme[0] == 0 and work_night: # using dark theme and working at night? set light theme
                wr.SetValueEx(openkey, "SystemUsesLightTheme", 0, wr.REG_DWORD, 1)
            elif system_theme[0] == 1 and work_night: # using light theme and working at night? all is ok, do nothing
                pass
            else: # dark theme is already set, do nothing
                pass

        else: # This should not be seen
            print("Something is wrong")
        
        # sleep the process to lower cpu usage. 
        time.sleep(5)

# yeah this is not that useful if you're using pyw extension to hide the console
except KeyboardInterrupt:
    print("Program finished")
