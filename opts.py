from tkinter import *
from tkinter import ttk
import tkinter as tk

# call this when needed
def opts_diag():


    # event handlers
    def cancelButton():
        winOptions.destroy()

    def okButton():
        # here we assign the values from the spinboxes to the dictionary variables
        prog_options={}

        #store the options from the widgets into the dictionary

        # store the sunrise hour
        prog_options["light_hour"]=int(spb_sun_hour.get())

        # store the sunrise minute
        prog_options["light_minute"]=int(spb_sun_min.get())

        # store the sunset hour
        prog_options["dark_hour"]=int(spb_moon_hour.get())

        # store the sunset minute
        prog_options["dark_minute"]=int(spb_moon_min.get())

        # store the use location boolean
        prog_options["use_location"]=bool(use_location.get())

        # store the work at night boolean
        prog_options["work_night"]=bool(work_night.get())
        
        #save the dictionary to a file
        openconf=open("conf.conf", "w")
        openconf.write(str(prog_options))
        openconf.close()
        
        winOptions.destroy()

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
    spb_sun_hour=ttk.Spinbox(master=frm_sunrise, from_=0, to=23, width=5)
    spb_sun_hour.grid(row=1, column=1, padx=10, pady=5)

    # the label with the : separator
    lbl_sep_sun=ttk.Label(text=" : ", master=frm_sunrise)
    lbl_sep_sun.grid(row=1, column=2)

    # the spinbox for the sunrise minute
    spb_sun_min=ttk.Spinbox(master=frm_sunrise, from_=0, to=59, width=5)
    spb_sun_min.grid(row=1, column=3, padx=10, pady=5)


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

    # the spinbox for the sunset hour
    spb_moon_hour=ttk.Spinbox(master=frm_sunset, from_=0, to=23, width=5)
    spb_moon_hour.grid(row=1, column=1, padx=10, pady=5)

    # the label with the : separator
    lbl_sep_moon=ttk.Label(text=" : ", master=frm_sunset)
    lbl_sep_moon.grid(row=1, column=2)

    # the spinbox for the sunrise minute
    spb_moon_min=ttk.Spinbox(master=frm_sunset, from_=0, to=59, width=5)
    spb_moon_min.grid(row=1, column=3, padx=10, pady=5)


    # FRAME: Option checkboxes
    frm_checkboxes=ttk.Frame(master=winOptions, borderwidth=0)
    frm_checkboxes.pack(fill=tk.X, padx=5, pady=5)

    # Checkbox options
    # checkbox for "I work at night"
    chkb_work_night=ttk.Checkbutton(master=frm_checkboxes, onvalue=True, offvalue=False, text="I work at night", variable=work_night)
    chkb_work_night.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # checkbox for "use my location"
    chkb_use_location=ttk.Checkbutton(master=frm_checkboxes, onvalue=True, offvalue=False, text="Use my location to calculate sunrise/sunset hours", variable=use_location)
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
    btn_cancel=ttk.Button(master=frm_buttons, text="Cancel", command=cancelButton)
    #btn_cancel.grid(row=0, column=3, padx=10, pady=5, sticky="we")
    btn_cancel.pack(side=tk.RIGHT, padx=10, pady=10)

    winOptions.mainloop()

# this must go when we are done
# opts_diag()
