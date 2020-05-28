from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import webbrowser

def donatebutton(event):
    webbrowser.open_new(r"https://www.paypal.com")

winAbout=Tk()
winAbout.title("About AutoTheme-19")
winAbout.resizable(width=False, height=True)

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
winAbout.mainloop()
