## Autotheme-19
Switching between dark and clear themes according to times of the day. 
Written during the COVID-19 pandemic.

Copyright © 2020 Juan Escobar Arias. Licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007.
## How does it work?
You set a sunrise hour to set the clear theme and a sunset hour to activate the dark theme. Then the app sits on your system tray and waits for the specified time to change the theme.

If you work during nighttime you can set the app to activate the clear theme at night and the dark theme during the day.

You can also set the app to calculate the sunrise and sunset times according to your location. For this internet access is needed.

The tray icon will show a sun after sunrise hour until the sunset. At that time a moon icon will be displayed. 
## About location and privacy
The app uses the geocoder library to obtain your location from the Google Maps service. If you have concerns about Google knowing your location/IP please do not use this option.

This app does not "call home" nor collects data from you.

I am not responsible for the development or the funcionality of the libraries linked in this project. Please check the respective documentation and direct inquiries to the relevant project.

You can also check the source code of the app and suggest improvements.

## Third party python libraries used

- [infi.systray](https://github.com/Infinidat/infi.systray)
- [geocoder](https://geocoder.readthedocs.io/)
- [suntime](https://github.com/SatAgro/suntime)

## Python libraries used in this project 
See [the Python Documentation](https://docs.python.org) for information on them)


- tkinter
- ast
- socket
- winreg
- time
- threading

## Icons
[Weather icon pack](https://www.flaticon.com/packs/weather-78) made by [Good Ware](https://www.flaticon.com/authors/good-ware) from [Flaticon](https://www.flaticon.com)