from PIL import Image
from PIL import ImageFilter

im=Image.open("C:\\Users\Dante\AppData\Local\GitHubDesktop\\app-0.6.2\MyPython\PycharmProjects\Heat Maps\Images\Background_Theta.png")
imout = im.filter(ImageFilter.BLUR)
for i in range(10):
    imout=imout.filter(ImageFilter.SMOOTH)
im.show()
imout.show()