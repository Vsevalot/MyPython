import matplotlib.pyplot as plt
import os
import somefuncs as smf
import pickle

def reportUpdating(path_to_pickle = "Z:\\Tetervak\\Reports\\reports 2.0\\pickle_reports",
                   path_to_xlsx = "Z:\\Tetervak\\Reports\\reports 2.0\\complete"):
    # Grab all txt reports
    pickle_reports = [f[:-7] for f in os.listdir(path_to_pickle)
                   if os.path.isfile(os.path.join(path_to_pickle, f))]

    # Find all completed reports which don't have an txt version
    for f in os.listdir(path_to_xlsx):
        if f[:6] not in pickle_reports:
            smf.report2pickle(os.path.join(path_to_xlsx, f))

def drawBar(figure, axis, position, value):
    xy = figure.ginput(n=1, timeout=0)
    x = round(xy[0][0])
    y = xy[0][1]
    value[position.index(x)] = y
    axis.clear()
    axis.bar(position, value)
    axis.figure.canvas.draw()
    drawBar(figure, axis, position, value)

if __name__ == "__main__":
    # For all .xlsx report without a pickle add one
    reportUpdating()

    path_to_pickles = "Z:\\Tetervak\\Reports\\reports 2.0\\pickle_reports"

    reports = [pickle.load(open("{}\\{}".format(path_to_pickles, pck), 'rb')) for pck in os.listdir(path_to_pickles)]

    test = reports[0]
    print(test.record_number)
    exit(1)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    test_data = [i for i in range(5)]
    test_time = [i for i in range(len(test_data))]
    ax.bar(test_time, test_data)
    drawBar(fig, ax, test_time, test_data)
    print(1)



