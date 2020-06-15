# Since we are all confined I decided to learn python during the lockdown.
# This script changes the windows theme according to a specific hour/minute

# import what we need first.
import winreg as wr
import time
import threading
from infi.systray import SysTrayIcon
import os.path, sys
import winshell
# this is just for logging and debugging
#import sys 
#sys.stdout = open('auto.log', 'w')

#---opts
from tkinter import *
import tkinter as tk
from tkinter import ttk
import ast

# set to save the program options
prog_options={}

# get the path of the program and save it to mypath
# getpath=os.path.dirname(os.path.abspath(__file__))
mypath= "\"" + sys.executable + "\""
print(mypath)

# get the path of the startup programs in windows. save it to startpath
startpath=winshell.startup()
print(startpath)

# check for internet. Source: https://stackoverflow.com/questions/3764291/checking-network-connection/#answer-33117579 
def is_internet(host="8.8.8.8", port=53, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

# save the configuration as a dictionary to a file
def write_conf():
    openconf=open("conf.conf", "w")
    openconf.write(str(prog_options))
    openconf.close()

# This function calculates the sunrise/sunset hours using geocoder and suntime
def calc_location():
    import geocoder
    from suntime import Sun, SunTimeException
    
    mygeo=geocoder.ip("me") 

    print("lat:", mygeo.latlng[0])
    print("lng:", mygeo.latlng[1])

    sun=Sun(mygeo.latlng[0],mygeo.latlng[1])

    # calculate the local sunrise and sunset
    c_sunrise = sun.get_local_sunrise_time()
    c_sunset = sun.get_local_sunset_time()

    print(c_sunrise.strftime("%H"), ":", c_sunrise.strftime("%M"))
    print(c_sunset.strftime("%H"), ":", c_sunset.strftime("%M"))
    
    #store the options from the calculation into the dictionary
    # the prog_options is already loaded. We call this from load_conf
    global prog_options

    # store the sunrise hour
    prog_options["light_hour"]=int(c_sunrise.strftime("%H"))

    # store the sunrise minute
    prog_options["light_minute"]=int(c_sunrise.strftime("%M"))

    # store the sunset hour
    prog_options["dark_hour"]=int(c_sunset.strftime("%H"))

    # store the sunset minute
    prog_options["dark_minute"]=int(c_sunset.strftime("%M"))


# function to load the config file 
def load_conf():
    import ast
    
    openconf=open("conf.conf", "r")
    contentconf=openconf.read()
    
    # prog_options will contain the dictionary with the variables
    global prog_options
    prog_options=ast.literal_eval(contentconf)
    
    # close the file
    openconf.close()
    
    # if user set location, perform the calculation
    if prog_options["use_location"]==True:
        calc_location()
        #write_conf()

    # what do we have in prog_options?
    print("light_hour: ", prog_options["light_hour"], " - ", type(prog_options["light_hour"]))
    print("light_minute: ", prog_options["light_minute"], " - ", type(prog_options["light_minute"]))
    print("dark_hour: ", prog_options["dark_hour"], " - ", type(prog_options["dark_hour"]))
    print("dark_minute: ", prog_options["dark_minute"], " - ", type(prog_options["dark_minute"]))
    print("use_location: ", prog_options["use_location"], " - ", type(prog_options["use_location"]))
    print("work_night: ", prog_options["work_night"], " - ", type(prog_options["work_night"]))
    print("run_startup: ", prog_options["run_startup"], " - ", type(prog_options["run_startup"]))


# THE OPTIONS DIALOG. GETS CALLED IF THERE'S NO CONFIGURATION OR FROM THE TRAY MENU
def opts_diag():

    # event handlers
    def cancelKey(event):
        winOptions.destroy()

    def okKey(event):
        okButton()

    def cancelButton():
        winOptions.destroy()

    def okButton():
        # here we assign the values from the comboboxes to the dictionary variables
        global prog_options

        #store the options from the widgets into the dictionary
        # store the sunrise hour
        prog_options["light_hour"]=int(cbx_sun_hour.get())

        # store the sunrise minute
        prog_options["light_minute"]=int(cbx_sun_min.get())

        # store the sunset hour
        prog_options["dark_hour"]=int(cbx_moon_hour.get())

        # store the sunset minute
        prog_options["dark_minute"]=int(cbx_moon_min.get())

        # store the use location boolean
        prog_options["use_location"]=bool(use_location.get())

        # store the work at night boolean
        prog_options["work_night"]=bool(work_night.get())
        
        # store the run at startup boolean
        prog_options["run_startup"]=bool(run_startup.get())

        # invoke the save conf function
        write_conf()

        # finally close the window
        winOptions.destroy()


    # set the widgets to the values in prog_options
    def set_widgets():
        cbx_sun_hour.set(str(prog_options["light_hour"]))
        cbx_sun_min.set(str(prog_options["light_minute"]).zfill(2))

        cbx_moon_hour.set(str(prog_options["dark_hour"]))
        cbx_moon_min.set(str(prog_options["dark_minute"]).zfill(2))

        use_location.set(prog_options["use_location"])
        work_night.set(prog_options["work_night"])
        run_startup.set(prog_options["run_startup"])

    def set_hours():
        cbx_sun_hour.set(str(prog_options["light_hour"]))
        cbx_sun_min.set(str(prog_options["light_minute"]).zfill(2))

        cbx_moon_hour.set(str(prog_options["dark_hour"]))
        cbx_moon_min.set(str(prog_options["dark_minute"]).zfill(2))
        
    # show a message when the user selects the location checkbox and we are offline
    def ticked_location():
        from tkinter import messagebox
        
        if use_location.get()==True and is_internet()==False:
            rt=Tk()
            rt.withdraw()
            messagebox.showinfo("Location not available", "Internet connection is needed to calculate the sunrise and sunset hours.")
            rt.destroy()
        elif use_location.get()==True:
            calc_location()
            set_hours()
        else:
            print("deactivating location")
    
    # event handler to the run on startup checkbox
    def ticked_runStartup():
        if run_startup.get()==True:
            # based on https://winshell.readthedocs.io/en/latest/shortcuts.html
            startup_lnk=os.path.join(winshell.startup(), "AutoTheme-19.lnk")
            with winshell.shortcut(startup_lnk) as link:
                link.path=sys.executable
                link.description="AutoTheme-19, a windows desktop time-based theme switcher"
                link.icon=sys.executable, 0
                link.working_directory=os.path.dirname(os.path.abspath(__file__))
            print("setting a shortcut in the startup folder to run at startup")
        elif run_startup.get()==False:
            try:
                winshell.delete_file(os.path.join(winshell.startup(), "AutoTheme-19.lnk"), allow_undo=False, no_confirm=True, silent=True)
                print("deleting the shortcut in the startup folder so I don't run at startup")
            except winshell.x_winshell:
                print("shortcut not found, shrugs")

    # options window creation
    winOptions=Tk()
    winOptions.title("AutoTheme-19 Options")
    winOptions.resizable(width=False, height=False)
    winOptions.focus_force()
    winOptions.bind("<Escape>", cancelKey)
    winOptions.bind("<Return>", okKey)

    #BUILD THE CONTROL VARIABLES FOR THE CHECKBOXES: They must be after the window creation "Tk()" and at the same indentation. Otherwise they won't work
    use_location=BooleanVar()
    work_night=BooleanVar()
    run_startup=BooleanVar()

    # FRAME: Sunrise Hour
    frm_sunrise=ttk.LabelFrame(master=winOptions, text="Sunrise Hour") # tk.Frame admits bg="#hex"
    frm_sunrise.pack(fill=tk.X, padx=10, pady=10)

    # the image for the sun (clear ui version)
    img_sunclear32=tk.PhotoImage(file="icons/32/B32sun.png")
    lbl_imgsun=tk.Label(image=img_sunclear32, master=frm_sunrise)
    lbl_imgsun.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

    # Create lists of numbers to be shown in the combo boxes
    hourlist=[]
    for x in range(24):
        hourlist.append(str(x))

    minlist=[]
    for x in range(60):
        minlist.append(str(x).zfill(2)) # zfill appends trailing zeroes for the minutes

    # combobox for the sunrise hour
    cbx_sun_hour=ttk.Combobox(master=frm_sunrise, height=8, width=5, state="readonly", values=hourlist)
    cbx_sun_hour.grid(row=1, column=1, padx=10, pady=5)

    # the label with the : separator
    lbl_sep_sun=ttk.Label(text=" : ", master=frm_sunrise)
    lbl_sep_sun.grid(row=1, column=2)

    # the combobox for the sunrise minute
    cbx_sun_min=ttk.Combobox(master=frm_sunrise, height=8, width=5, state="readonly", values=minlist)
    cbx_sun_min.grid(row=1, column=3, padx=10, pady=5)


    # FRAME: Sunset Hour
    frm_sunset=ttk.LabelFrame(master=winOptions, text="Sunset Hour")
    frm_sunset.pack(fill=tk.X, padx=10, pady=10)

    # the image for the moon (clear ui version)
    img_moonclear32=tk.PhotoImage(file="icons/32/B32moon.png")
    lbl_imgmoon=tk.Label(image=img_moonclear32, master=frm_sunset)
    lbl_imgmoon.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

    # the combobox for the sunset hour
    cbx_moon_hour=ttk.Combobox(master=frm_sunset, height=8, width=5, state="readonly", values=hourlist)
    cbx_moon_hour.grid(row=1, column=1, padx=10, pady=5)

    # the label with the : separator
    lbl_sep_moon=ttk.Label(text=" : ", master=frm_sunset)
    lbl_sep_moon.grid(row=1, column=2)

    # the combobox for the sunrise minute
    cbx_moon_min=ttk.Combobox(master=frm_sunset, height=8, width=5, state="readonly", values=minlist)
    cbx_moon_min.grid(row=1, column=3, padx=10, pady=5)


    # FRAME: Option checkboxes
    frm_checkboxes=ttk.Frame(master=winOptions, borderwidth=0)
    frm_checkboxes.pack(fill=tk.X, padx=5, pady=5)

    # Checkbox options
    # checkbox for "I work at night"
    chkb_work_night=ttk.Checkbutton(master=frm_checkboxes, onvalue=True, offvalue=False, text="I work at night", variable=work_night)
    chkb_work_night.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # checkbox for "use my location"
    chkb_use_location=ttk.Checkbutton(master=frm_checkboxes, onvalue=True, offvalue=False, text="Use my location to calculate sunrise/sunset hours", variable=use_location, command=ticked_location)
    chkb_use_location.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # checkbox for "run on startup"
    chkb_run_startup=ttk.Checkbutton(master=frm_checkboxes, onvalue=True, offvalue=False, text="Run on startup", variable=run_startup, command=ticked_runStartup)
    chkb_run_startup.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    # FRAME: Buttons
    frm_buttons=ttk.Frame(master=winOptions, borderwidth=0)
    frm_buttons.columnconfigure([0], minsize=200)
    frm_buttons.pack(fill=tk.X, padx=5, pady=5)

    # Button OK
    btn_ok=ttk.Button(master=frm_buttons, text="Ok", command=okButton)
    #btn_ok.grid(row=0, column=2, padx=10, pady=5, sticky="we")
    btn_ok.pack(side=tk.RIGHT, padx=10, pady=10)

    #set the widgets to the options in the conf file or if it's not made, set defaults
    try:
        # load the conf when we invoke the dialog, it can be modified. CANCEL button is enabled
        load_conf()

        # then set each widget to the values we got
        set_widgets()

        # Button Cancel
        btn_cancel=ttk.Button(master=frm_buttons, text="Cancel", command=cancelButton)
        
    except:
        # default values when no conf file is present. CANCEL button is disabled
        cbx_sun_hour.set(hourlist[5])
        cbx_sun_min.set(minlist[55])

        cbx_moon_hour.set(hourlist[18])
        cbx_moon_min.set(minlist[15])

        use_location.set(False)
        work_night.set(False)
        
        # DISABLED Button Cancel
        btn_cancel=ttk.Button(master=frm_buttons, text="Cancel", default=tk.DISABLED, state=tk.DISABLED)
    
    finally:
        btn_cancel.pack(side=tk.RIGHT, padx=10, pady=10)

    winOptions.iconbitmap("icons/16.ico")
    winOptions.mainloop()

# THE ABOUT BOX
def aboutBox():
    # import stuff that we need
    import tkinter.scrolledtext as scrolledtext
    import webbrowser

    # event handler for the donate button
    def donatebutton():
        webbrowser.open_new(r"https://www.paypal.me/juandaesarias")
        winAbout.destroy()

    winAbout=Tk()
    winAbout.title("About AutoTheme-19")
    winAbout.resizable(width=False, height=False)
    winAbout.focus_force()

    # frame for the app and license info
    frm_app=tk.Frame(master=winAbout)
    frm_app.pack()

    # frame for the title and the app icon
    frm_title=tk.Frame(master=frm_app)
    frm_title.pack(fill=tk.X, padx=10, pady=10)

    # 32*32 color icon
    img_app=tk.PhotoImage(file="icons/32.png")
    lbl_imgapp=tk.Label(image=img_app, master=frm_title)
    lbl_imgapp.grid(column=0, row=0, rowspan=2, sticky="w", padx=10)

    # the title of the app
    lbl_title=ttk.Label(text="AutoTheme-19", font=(None, 15, "bold"), master=frm_title)
    lbl_title.grid(column=1, row=0, sticky="w", padx=10)

    # version
    lbl_version=ttk.Label(text="Version 1 \"Let\'s just use a good\'ol integer\"", font=(None, 10, "bold"), master=frm_title)
    lbl_version.grid(column=1, row=1, sticky="w", padx=10)

    # info about the program
    aboutstring="AutoTheme-19 changes the theme on Windows 10 according to sunrise and sunset hours. I worked on this project during the covid-19 lockdown.\n\nCopyright \N{COPYRIGHT SIGN} 2020 Juan Escobar Arias.\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\nYou should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.\n\nProgramming and Artwork: Juan Escobar Arias."
    licstring=open("About.md", "r")

    # Text widget with all of that
    txt_mylic=tk.Message(master=frm_app, text=aboutstring) 
    txt_mylic.pack(padx=10, pady=10) 

    # Text area with the license infos for all the rest
    txa_liblic=scrolledtext.ScrolledText(master=frm_app, wrap=WORD, width=10, height=8, font=("Sans", "10"))
    txa_liblic.insert(tk.END, licstring.read())
    txa_liblic.pack(fill=tk.X, padx=10, pady=10)

    # frame with the donate and ok buttons
    frm_donate=tk.Frame(master=frm_app)
    frm_donate.pack(fill=tk.X, padx=10, pady=10)

    # image and button for donations
    img_donate=tk.PhotoImage(file="icons/btn/PP_logo.png")
    btn_donate=tk.Button(master=frm_donate, text="  Donate  ", image=img_donate, compound=tk.LEFT, command=donatebutton)
    btn_donate.pack(side=tk.RIGHT)

    winAbout.iconbitmap("icons/16.ico")
    winAbout.mainloop()
#---/opts


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

# OPTIONS FILE LOAD #
try:
    load_conf()

except IOError:
    # open the options dialog to get the variables
    opts_diag()
    
    # Then we read the file
    load_conf()
    
finally:
    # So far no need for stuff here
    pass


# AUXILIARY CODE FOR THE TRAY ICON

# control variable for the tray icon    
makemestop=False

# call the options
def call_opts_tray(icon):
    opts_diag()

# call the About Box
def call_about_tray(icon):
    aboutBox()

# function that will end the program
def make_me_stop(icon):
    global makemestop
    makemestop=True

    # Closing sequence
    mylogic.join()
    print("I'M STOPPING!")


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


    #       To activate the light theme we check for 3 scenarios:
    #       1) currenthour is the same as prog_options["light_hour"] AND currentmin is equal or later than prog_options["light_minute"]
    #       2) currenthour is later than prog_options["light_hour"] AND earlier than prog_options["dark_hour"]
    #       3) currenthour is same as prog_options["dark_hour"] AND currentmin is earlier than prog_options["dark_minute"]
    #       if one of them is true, it means we are on light theme time

            if (currenthour == prog_options["light_hour"] and currentmin >= prog_options["light_minute"]) or (currenthour > prog_options["light_hour"] and currenthour < prog_options["dark_hour"]) or (currenthour == prog_options["dark_hour"] and currentmin < prog_options["dark_minute"]):
                # we are in the light theme hour range, we do here the registry change.

                # Get the values of what we need to manipulate. we will use them in further conditions to check what theme is active across system and apps
                apps_theme = wr.QueryValueEx(openkey, "AppsUseLightTheme")
                system_theme = wr.QueryValueEx(openkey, "SystemUsesLightTheme")
                # remember if apps_theme[0] == 0 and system_theme[0] == 0 it means we are using the dark theme

                # Set the theme for the apps.
                # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
                # Then if we work at night we set the dark theme
                # And last, we set the light theme
                
                if apps_theme[0] == 0 and not prog_options["work_night"]: # using dark theme and not working at night? Set light theme
                    mod_setting("AppsUseLightTheme", 1)
                    update_icon("icons/16/B16sun.ico", "AutoTheme-19: Clear theme, day worker")

                elif apps_theme[0] == 1 and prog_options["work_night"]: # using light theme and working at night? set dark theme
                    mod_setting("AppsUseLightTheme", 0)
                    update_icon("icons/16/W16sun.ico", "AutoTheme-19: Dark theme, night worker")
                    
                elif apps_theme[0] == 0 and prog_options["work_night"]: # using dark theme (during daytime) and working at night? all is ok, do nothing
                    update_icon("icons/16/W16sun.ico", "AutoTheme-19: Dark theme, night worker")
                    #print("day case 1: dark theme, working at night")
                else: # light theme is already set, do nothing
                    update_icon("icons/16/B16sun.ico", "AutoTheme-19: Clear theme, day worker")
                    #print("day case 2: clear theme, working by day")

                # Set the theme for the system. 
                # First we check if the theme is dark and if we are not working at night. If this is the case, we set the light theme
                # Then if we work at night we set the dark theme
                # And last, we set the light theme

                if system_theme[0] == 0 and not prog_options["work_night"]: # using dark theme and not working at night? Set light theme
                    mod_setting("SystemUsesLightTheme", 1)
                elif system_theme[0] == 1 and prog_options["work_night"]: # using light theme and working at night? set dark theme
                    mod_setting("SystemUsesLightTheme", 0)
                elif system_theme[0] == 0 and prog_options["work_night"]: # using dark theme and working at night? all is ok, do nothing
                    pass
                else: # light theme is already set, do nothing
                    pass

    #       If none of that is true we check for other 3 cases:
    #       1) currenthour is the same as prog_options["dark_hour"] AND currentmin is equal or later than prog_options["dark_minute"] 
    #       2) currenthour is later than prog_options["dark_hour"] OR currenthour is earlier than prog_options["light_hour"]
    #       3) currenthour is same as prog_options["light_hour"] AND currentmin is earlier than prog_options["light_minute"]
    #       if one of these is true, it means we are on dark theme time

            elif (currenthour == prog_options["dark_hour"] and currentmin >= prog_options["dark_minute"]) or (currenthour > prog_options["dark_hour"] or currenthour < prog_options["light_hour"]) or (currenthour == prog_options["light_hour"] and currentmin < prog_options["light_minute"]):
                # we are in the dark theme hour range, we do here the registry change.
                
                # Get the values of what we need to manipulate. we will use them in further conditions to check what theme is active across system and apps
                apps_theme = wr.QueryValueEx(openkey, "AppsUseLightTheme")
                system_theme = wr.QueryValueEx(openkey, "SystemUsesLightTheme")
                # remember if apps_theme[0] == 0 and system_theme[0] == 0 it means we are using the dark theme

                # Set the theme for the apps. 
                # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
                # Then if the theme is dark and we work at night we set the light theme
                # Then if we use light theme and we work at night we do nothing, it's the way we want
                # For all else we leave it like it is
                
                if apps_theme[0] == 1 and not prog_options["work_night"]: # using light theme and not working at night? Set dark theme
                    mod_setting("AppsUseLightTheme", 0)
                    update_icon("icons/16/W16moon.ico", "AutoTheme-19: Dark theme, day worker")

                elif apps_theme[0] == 0 and prog_options["work_night"]: # using dark theme and working at night? set light theme
                    mod_setting("AppsUseLightTheme", 1)
                    update_icon("icons/16/B16moon.ico", "AutoTheme-19: Clear theme, night worker")

                elif apps_theme[0] == 1 and prog_options["work_night"]: # using clear theme (at nighttime) and working at night? all is ok, do nothing
                    update_icon("icons/16/B16moon.ico", "AutoTheme-19: Clear theme, night worker")
                    #print("night case 1: clear theme at night")
                else: # dark theme is already set, do nothing
                    update_icon("icons/16/W16moon.ico", "AutoTheme-19: Dark theme, day worker")
                    #print("night case 2: dark theme at night")

                # Set the theme for the system. 
                # First we check if the theme is light and if we are not working at night. If this is the case, we set the dark theme
                # Then if the theme is dark and we work at night we set the light theme
                # Then if we use light theme and we work at night we do nothing, it's the way we want
                # For all else we leave it like it is

                if system_theme[0] == 1 and not prog_options["work_night"]: # using light theme and not working at night? Set dark theme
                    mod_setting("SystemUsesLightTheme", 0)
                elif system_theme[0] == 0 and prog_options["work_night"]: # using dark theme and working at night? set light theme
                    mod_setting("SystemUsesLightTheme", 1)
                elif system_theme[0] == 1 and prog_options["work_night"]: # using light theme and working at night? all is ok, do nothing
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
            ("Options...", None, call_opts_tray),
            ("About AutoTheme-19", None, call_about_tray),
    )

    icon=SysTrayIcon("icons/16/B16sun.ico", "AutoTheme-19", menu_options, on_quit=make_me_stop)
    
    # Start the logic thread after defining the icon, because the logic thread needs to update the icon.
    mylogic=threading.Thread(target=logic_thread)
    mylogic.start()
    
    # now we start the tray icon
    icon.start()
