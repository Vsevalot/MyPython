import os

def readCSV(path2csv:str)->list:
    with open(path2csv, 'r') as file:
        lines=[line.split(';') for line in file.readlines()] # reading all lines in the file with rows as elements of the list
        squareCSV=True
        for line in lines: # check for square form of the csv (the number of columns is constant in the file)
            if(len(line)!=len(lines[0])):
                squareCSV=False
                print("CSV file: "+path2csv+" does not have square form (the number of columns is changing through the file)")
                exit(1)
        if(squareCSV):
            data=[[value[i] for value in lines] for i in range(len(lines[0]))] # transpose the list to make columns elements of the list
            return data

def results2dict(results:list)->dict:
    for i in range(len(results)): # convert values from "'abc'\n" to "abc"
        for k in range(len(results[i])):
            if(results[i][k]!='' and results[i][k]!='\n'):
                if(results[i][k][0]=="'"):
                    results[i][k]=results[i][k][1:]
                if(results[i][k][-1]=='\n'):
                    results[i][k] = results[i][k][:-1]
                if(results[i][k][-1]=="'"):
                    results[i][k] = results[i][k][:-1]
            else:
                results[i]=results[i][:k]
                break
    return {"Column_"+str(i+1):results[i] for i in range(len(results))}

def stageDetector(matFile:str,reportList:list):
    dayReports=[report for report in reportsList if report[-12:-4]==matFile[:8]] # compare date in mat and csv files 20101105==20101105 (2010 year, 11 month, 05 number)
    matTime=int(''.join(matFile[9:-4].split('.')))
    for report in dayReports:
        csv=readCSV(report)
        if int(''.join(csv[0][1].split(':')))<matTime: # 1 because first element is a title
            continue # if first time is later than matFile - pass this report
        for i in range(1,len(csv[0])):
            if int(''.join(csv[0][i].split(':')))>=matTime:
                return csv[1][i-1]
    return None # if none report in reportList much return None


if __name__ == "__main__":
    path2results="E:\\test\\results.csv"
    data=readCSV(path2results)
    results=results2dict(data)

    path2reports="E:\\test\Repotrs"
    reportsList = [ os.path.join(path2reports, f) for f in os.listdir(path2reports) if os.path.isfile(os.path.join(path2reports, f))]

    print(stageDetector(results["Column_1"][0],reportsList))
