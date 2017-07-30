from PIL import Image

path2Indexes="C:\\Users\Dante\AppData\Local\GitHubDesktop\\app-0.6.2\MyPython\PycharmProjects\Heat Maps\Images\All.png"
Indexes=Image.open(path2Indexes)
path2Form="C:\\Users\Dante\AppData\Local\GitHubDesktop\\app-0.6.2\MyPython\PycharmProjects\Heat Maps\Images\Form.png"
headShape=Image.open(path2Form)
Indexes.paste(headShape,mask=headShape)
Indexes.show()
Indexes.save("headIndexes.png", format="png")