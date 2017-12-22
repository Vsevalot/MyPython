import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

if __name__ == "__main__":
    fig = plt.figure(figsize=(13.92, 8.83), dpi=100)
    plot1 = fig.add_subplot(2, 2, 1)
    plot1.axis([-5, 5, -5, 5])
    plot1.plot([-10,10],[0,0],'k')
    plot1.plot([0,0],[-10, 10], 'k')
    plot1.plot([4,0,-3],[3,1,4], 'o')

    plot2 = fig.add_subplot(2, 2, 2)
    plot2.axis([-10, 10, -10, 10])
    plot2.plot([-10,10],[0,0],'k')
    plot2.plot([0,0],[-10, 10], 'k')
    plot2.plot([4,0,-6],[3,2,8], 'o')

    plot3 = fig.add_subplot(2, 2, 3)
    plot3.axis([-25, 25, -25, 25])
    plot3.plot([-25,25],[0,0],'k')
    plot3.plot([0,0],[-25, 25], 'k')
    plot3.plot([4,4,7],[3,3,24], 'o')

    plot4 = fig.add_subplot(2, 2, 4)
    plot4.axis([-6, 6, -6, 6])
    plot4.plot([-10,10],[0,0],'k')
    plot4.plot([0,0],[-10, 10], 'k')
    plot4.plot([2, 1,0],[1,2,5], 'o')
    plt.show()
