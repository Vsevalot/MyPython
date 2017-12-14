import os
import mypyfunctions as myPy

path_to_reports = "Z:\\Tetervak\\Reports\\complete"
REPORTS = [os.path.join(path_to_reports, f) for f in os.listdir(path_to_reports)
           if os.path.isfile(os.path.join(path_to_reports, f))]
REPORTS = [myPy.Report(report, myPy.readCSV(report)) for report in REPORTS]

if __name__ == "__main__":

    path_to_result_folder = "Z:\\Tetervak\\Data"

    data_path = [os.path.join(path_to_result_folder, f) for f in os.listdir(path_to_result_folder)
                      if os.path.isfile(os.path.join(path_to_result_folder, f)) and "5min" in f][0]

    path_to_save = "Z:\\Tetervak\\File-stage.csv"

    results = 0

    if  data_path[-4:] == "xlsx":
        results = myPy.matfiles2eegFragments(myPy.results2Dict(myPy.readXLSX(data_path)), REPORTS)
    elif data_path[-3:] == "csv":
        results = myPy.matfiles2eegFragments(myPy.results2Dict(myPy.readCSV(data_path)), REPORTS)

    with open(path_to_save, 'w') as file:
        for group in results:
            for fragment in results[group]:
                if (fragment.stage is not None) and (fragment.stage!=-1) and (fragment.stage<4):
                    rec = fragment.report_name.split('_')[0].split(')')[-1]
                    line  = "{}_{};{}\n".format(rec,fragment.name[7:-7], fragment.stage)
                    file.write(line)
    print("complete")




