from tkinter import *
import tkinter as tk
from tkinter import ttk
import webbrowser

def weatherpack(event):
    webbrowser.open_new(r"https://www.flaticon.com/packs/weather-78")

def goodware(event):
    webbrowser.open_new(r"https://www.flaticon.com/authors/good-ware")

def iconsite(event):
    webbrowser.open_new(r"https://www.flaticon.com")

winAbout=Tk()
winAbout.title("About AutoTheme-19")
winAbout.resizable(width=False, height=True)

# frame for the app and license info
frm_app=tk.Frame(master=winAbout)
frm_app.pack()

# the title of the app
lbl_title=ttk.Label(text="AutoTheme-19", font=(None, 15, "bold"), master=frm_app)
lbl_title.pack()

# version
lbl_version=ttk.Label(text="Version 1 \"Let\'s just use a good\'ol integer\"", font=(None, 10, "bold"), master=frm_app)
lbl_version.pack()

# info about the program
aboutstring="AutoTheme-19 changes the theme on Windows 10 according to sunrise and sunset hours. I worked on this project during the covid-19 lockdown.\n\nCopyright \N{COPYRIGHT SIGN} 2020 Juan Escobar Arias.\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\nYou should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.\n\nArtwork:\nMonochrome icons: Weather icon pack made by Good Ware from Flaticon."

# Text with all of that
txt_mylic=tk.Text(frm_app, wrap=WORD, font=("sans", 9), relief=FLAT) 
txt_mylic.insert(INSERT, aboutstring) 
txt_mylic.config(state=DISABLED)
txt_mylic.pack(padx=10, pady=10) 

# tags 
txt_mylic.tag_add("goodware", "10.44", "10.53") 
txt_mylic.tag_add("flaticon", "10.59", "10.67") 
txt_mylic.tag_config("goodware", foreground="blue", underline=1) 
txt_mylic.tag_config("flaticon", foreground="blue", underline=1) 
txt_mylic.tag_bind("goodware", "<Button-1>", goodware) 
txt_mylic.tag_bind("flaticon", "<Button-1>", iconsite) 

winAbout.mainloop()
