from PIL import Image

path2Indexes=".\Images\All.png"
Indexes=Image.open(path2Indexes)
path2Form=".\Images\HeadForms.png"
headShape=Image.open(path2Form)
Indexes.paste(headShape,mask=headShape)
Indexes.show()
Indexes.save("headIndexes.png", format="tif",dpi=(300,300))