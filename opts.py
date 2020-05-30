from tkinter import *
import tkinter as tk
from tkinter import ttk
import ast

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
    
    if is_internet()==True:
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


# THE OPTIONS DIALOG. GETS CALLED IF THERE'S NO CONFIGURATION OR FROM THE TRAY MENU
def opts_diag():

    # event handlers
    def cancelKey(event):
        winOptions.destroy()

    def cancelButton():
        winOptions.destroy()

    def okButton():
        # here we assign the values from the comboboxes to the dictionary variables
        global prog_options
        prog_options={}

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

    def set_hours():
        cbx_sun_hour.set(str(prog_options["light_hour"]))
        cbx_sun_min.set(str(prog_options["light_minute"]).zfill(2))

        cbx_moon_hour.set(str(prog_options["dark_hour"]))
        cbx_moon_min.set(str(prog_options["dark_minute"]).zfill(2))
        
    # show a message when the user selects the location checkbox and we are offline
    def ticked_location():
        from tkinter import messagebox
        
        if prog_options["use_location"]==False and is_internet()==False:
            rt=Tk()
            rt.withdraw()
            messagebox.showinfo("Location not available", "Internet connection is needed to calculate the sunrise and sunset hours.")
            rt.destroy()
        elif prog_options["use_location"]==False:
            calc_location()
            set_hours()
    
    winOptions=Tk()
    winOptions.title("AutoTheme-19 Options")
    winOptions.resizable(width=False, height=False)
    winOptions.focus_force()
    winOptions.bind("<Escape>", cancelKey)

    #BUILD THE CONTROL VARIABLES FOR THE CHECKBOXES: They must be after the window creation "Tk()" and at the same indentation. Otherwise they won't work
    use_location=BooleanVar()
    work_night=BooleanVar()

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
