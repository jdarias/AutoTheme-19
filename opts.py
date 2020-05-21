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
        
    # change the comboboxes to disabled when the user selects the location checkbox
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
    
    #BUILD THE CONTROL VARIABLES FOR THE CHECKBOXES: They must be after the window creation "Tk()" and at the same indentation. Otherwise they won't work
    use_location=BooleanVar()
    work_night=BooleanVar()

    # FRAME: Sunrise Hour
    frm_sunrise=tk.Frame(master=winOptions, borderwidth=0) # tk.Frame admits bg="#hex"
    frm_sunrise.pack(fill=tk.X, padx=5, pady=5)

    # the label "Sunrise Hour"
    lbl_sunrise=ttk.Label(master=frm_sunrise, text="Sunrise Hour")
    lbl_sunrise.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

    # the image for the sun (clear ui version)
    img_sunclear32=tk.PhotoImage(file="32/001-sun.png")
    lbl_imgsun=tk.Label(image=img_sunclear32, master=frm_sunrise)
    lbl_imgsun.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

    # the spinbox for the sunrise hour
    # spb_sun_hour=ttk.Spinbox(master=frm_sunrise, from_=0, to=23, width=5)
    # spb_sun_hour.grid(row=1, column=1, padx=10, pady=5)
    
    # Create lists of numbers to be shown in the combo boxes
    hourlist=[]
    for x in range(24):
        hourlist.append(str(x))

    minlist=[]
    for x in range(60):
        minlist.append(str(x).zfill(2))

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
    frm_sunset=ttk.Frame(master=winOptions, borderwidth=0)
    frm_sunset.pack(fill=tk.X, padx=5, pady=5)

    # the label "Sunset Hour"
    lbl_sunset=ttk.Label(master=frm_sunset, text="Sunset Hour")
    lbl_sunset.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

    # the image for the moon (clear ui version)
    img_moonclear32=tk.PhotoImage(file="32/002-moon.png")
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

    # Button Cancel
    #btn_cancel=ttk.Button(master=frm_buttons, text="Cancel", command=cancelButton)
    #btn_cancel.grid(row=0, column=3, padx=10, pady=5, sticky="we")
    #btn_cancel.pack(side=tk.RIGHT, padx=10, pady=10)

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

    winOptions.mainloop()
