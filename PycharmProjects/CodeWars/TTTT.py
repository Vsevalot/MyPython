names=["DeviceLock DLP","Forcepoint DLP","Infowatch Traffic Monitor DLP","McAfee DLP","SecureTower DLP",
   "Solar Dozor DLP","Trend Micro DLP","Zecurion DLP"]
links=["https://www.devicelock.com/", "https://www.forcepoint.com/",
       "https://infowatch.com/", "https://www.mcafee.com/us/index.html", "https://falcongaze.com/",
       "https://solarsecurity.ru/", "http://www.trendmicro.com.ru/", "http://zecurion.com/"]


path = "e:\\Users\\sevamunger\\Desktop\\DPL.csv"

with open(path, 'w') as file:
    for i in range(len(names)):
        file.write(';'.join([names[i], links[i]]) + '\n')
    file.close()