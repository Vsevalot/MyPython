import mypyfunctions as myPy

if __name__=="__main__":
    old = myPy.readCSV("Z:\\Tetervak\\File-stage_AI_old.csv")
    new = myPy.readCSV("Z:\\Tetervak\\File-stage_AI.csv")

    booleans = []
    for i in range(len(new[1])):
        if new[1][i] != old[1][old[0].index(new[0][i])]:
            string = "{0} AI={1}"
            booleans.append(string.format(new[0][i], old[1][old[0].index(new[0][i])], new[1][i]).split(' '))


    booleans = sorted(booleans)
    for i in booleans:
        print(i)
    # for i in booleans:
    #     print(i[0])
    #
    # for i in booleans:
    #     print(i[1])























