## Autotheme-19
A Windows app that switches between dark and clear themes (on Windows 10) according to the times of the day you set. 

The app sets the clear theme at sunrise, and the dark theme at sunset.

You can set the sunrise and sunset hours yourself or let the app calculate these times for you.

The app can also run at startup so you basically set it and forget it. 

No matter when you turn on your computer, or if you haven't used it in a while, the app will change your theme according to its settings. It will also enforce the setting if the theme changes, i.e by another app.

If you work at night, you can set the app to set the clear theme at night and the dark theme during the day.

Written as a Python learning project during the COVID-19 pandemic.

Copyright © 2020 Juan Escobar Arias. Licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007.

## How does it work?
You set a sunrise hour to set the clear theme and a sunset hour to activate the dark theme. Then the app sits on your system tray and waits for the specified time to change the theme.

If you work during nighttime you can set the app to activate the clear theme at night and the dark theme during the day. Just check the "I work at night" option.

You can also set the app to calculate the sunrise and sunset times according to your location. For this internet access is needed.

The tray icon will show a sun from sunrise hour until sunset. After that a moon icon will be displayed.

## About location and privacy policy
The app uses the geocoder library to obtain your location from the Google Maps service. If you have concerns about Google knowing your location/IP please do not use this option. Also please check the privacy policy of geocoder.

This app does not "call home" nor collects data from you.

I am not responsible for the development or the funcionality of the libraries linked in this project. Please check the respective documentation and direct inquiries to the relevant project. Everything is open source. You can check the source code of the app and suggest improvements.

## Setup / Uninstall
Put the autotheme.exe file anywhere on your system and double clic it.

On your first run, it will show the options window and you can set the sunrise/sunset hours, if you work at night or if you want to calculate the hours using your location.

The run on startup option will create a shortcut on your startup folder, that is normally "C:\Users\[YOUR_USERNAME]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup".

Additionally, a text file called conf.conf will be created beside the autotheme.exe file, to save the program options.

To "uninstall" first deactivate the run on startup option. This will delete the shortcut in your startup folder. Then just delete the exe and the conf files. That's it.

## Contributing and donating
Thank you so much for considering a contribution, it means a lot! Please refer to the contributing file to set you up.

Check out the list of issues, I'll gladly accept patches for the issues I'm having trouble with!

If you like this project and it has brought you a smile, please consider making a small donation in my paypal link, It would really be appreciated in these hard times. I can't be thankful enough.

## Third party python libraries used
- [infi.systray](https://github.com/Infinidat/infi.systray)
- [geocoder](https://github.com/DenisCarriere/geocoder)
- [suntime](https://github.com/SatAgro/suntime)
- [winshell](http://github.com/tjguk/winshell>)

## Python libraries used in this project 
See [the Python Documentation](https://docs.python.org) for information on them)

- tkinter
- ast
- socket
- winreg
- time
- threading
- webbrowser
