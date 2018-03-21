import matplotlib.pyplot as plt


def report_to_ai(report) -> list:
    return []


def draw_bar(figure, axis, position, value):
    xy = figure.ginput(n=1, timeout=0)
    x = round(xy[0][0])
    y = xy[0][1]
    value[position.index(x)] = y
    axis.clear()
    axis.bar(position, value)
    axis.figure.canvas.draw()
    draw_bar(figure, axis, position, value)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
test_data = [i for i in range(5)]
test_time = [i for i in range(len(test_data))]
ax.bar(test_time, test_data)
draw_bar(fig, ax, test_time, test_data)



