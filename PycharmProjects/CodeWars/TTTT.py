from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim([0,10000])

x = np.linspace(6000.,7000., 5)
y = np.ones_like(x)

collection = plt.fill_between(x, y)

def animate(i):
    path = collection.get_paths()[0]
    path.vertices[:, 1] *= 0.9

animation.FuncAnimation(fig, animate,
                        frames=25, interval=30)