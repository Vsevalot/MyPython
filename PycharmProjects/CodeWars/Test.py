import datetime

t="92656"
a=datetime.time(int(t[:-4]), int(t[-4:-2]), int(t[-2:]))
print(a.hour)