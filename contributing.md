## Contributing
Thank you again for the time you invest in making this project better.
In order to contribute and make changes to the project, you need to install python from python.org. Then download the required libraries:
´´´
pip install infi.systray geocoder suntime winshell
´´´
I'm using pyinstaller to create the exe package, so you need to install that as well.
´´´
pip install pyinstaller
´´´
Clone or download the repo, and you will find an autotheme.spec file beside the main autotheme.py script. That's the file I'm using with pyinstaller to create the package.
In order to debug you need to activate the console output, to do this change the console=False line in autotheme.spec to console=True and then compile the exe:
´´´
pyinstaller autotheme.spec
´´´
Alternatively you can make changes to the autotheme.py script and run it directly.
