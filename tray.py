import pystray
from PIL import Image
from pystray import MenuItem as item


#print(dir(Image))
print(dir(pystray.Icon))

image=Image.open("16/001-sun.png")

menu=(
        item("Options", lambda: quit()),
        item("Exit", lambda: icon.stop())
)

icon=pystray.Icon("AutoTheme-19", image, "AutoTheme-19", menu)
icon.run()

