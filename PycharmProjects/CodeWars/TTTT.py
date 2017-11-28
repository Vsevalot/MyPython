import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open("e:\\Users\\sevamunger\\Desktop\\testData.txt").read()
    lines = graph_data.split('\n')
    x = []
    y = []
    for line in lines:
        if len(line)<1:
            continue
        x.append(int(line.split(',')[0]))
        y.append(int(line.split(',')[1]))

    ax1.clear()
    ax1.plot(x,y)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
