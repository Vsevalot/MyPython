# import os
path = "e:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\CodeWars\\file.wav"
# os.system("start {}".format(path))

import winsound

winsound.PlaySound(path, winsound.SND_FILENAME)