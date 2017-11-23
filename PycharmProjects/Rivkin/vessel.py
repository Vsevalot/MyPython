import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib import style

style.use("ggplot")

P0 = 120
alpha = 0.5
viscosity = 5
diameter_w = 0.2
I = 120*math.pi * (diameter_w**4) * (alpha**4)/(viscosity*(2**8)*(2*(alpha**4)+1)) # amperage (flow)

def pressure_calc(d_w, v, a ): # d_b - diameter of the wide part of the vessel, v - viscosity,
    y = [P0]                    # a - diameter of the narrow part / diameter of the wide part of the vessel
    wide_w = 8 * v * 4 / (math.pi * (d_w/2) ** 4)
    y.append(y[-1] - wide_w * I)
    narrow_w = 8 * v * 2 / (math.pi * ((d_w/2)*a) ** 4)
    y.append(y[-1] - narrow_w * I)
    y.append(y[-1] - wide_w * I)
    return y

def vessel_calc(a):
    y_high = [0.95]*2
    y_low = [0.05]*2
    y_high.append(0.5 + 0.45 * a)
    y_high.append(y_high[-1])
    y_low.append(0.5 - 0.45 * a)
    y_low.append(y_low[-1])
    y_high.append(0.95)
    y_high.append(0.95)
    y_low.append(0.05)
    y_low.append(0.05)
    return y_low, y_high


x = [0, 4, 6, 10]
fig = plt.figure()
ax = fig.add_subplot(211)


[pressure] = ax.plot(x, pressure_calc(diameter_w, viscosity, alpha), linewidth=2, color='red')
ax.set_xlim([0, 10])
ax.set_ylabel("Pressure")
ax.set_title("Vessel pressure")
plt.setp(ax.get_xticklabels(), visible=False)


vessel_model = fig.add_subplot(212)
x_vessel = [0,4,4,6,6,10]
[vessel_l] = vessel_model.plot(x_vessel, vessel_calc(alpha)[0], linewidth=2, color='red')
[vessel_h] = vessel_model.plot(x_vessel, vessel_calc(alpha)[1], linewidth=2, color='red')
vessel_model.set_xlim([0, 10])
vessel_model.axis(visible = False)
vessel_model.set_ylim([0, 1])
vessel_model.set_title("Vessel view")
vessel_model.arrow(0, 0.5, 3, 0, head_width=0.15, head_length=0.15, linewidth=1,  fc='red', ec='red')
vessel_model.text(1, 0.55 ,"Blood flow")
vessel_model.grid(False)
vessel_model.axis('off')
plt.setp(vessel_model.get_xticklabels(), visible=False)
plt.setp(vessel_model.get_yticklabels(), visible=False)


diameter_slider_ax  = fig.add_axes([0.25, 0.05, 0.65, 0.03])
diameter_slider = Slider(diameter_slider_ax, 'Vessel diameter ', 0.01, 0.5, valinit=diameter_w)

viscosity_slider_ax  = fig.add_axes([0.25, 0.10, 0.65, 0.03])
viscosity_slider = Slider(viscosity_slider_ax, 'Viscosity ', 0.5, 10, valinit=viscosity)

alpha_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03])
alpha_slider = Slider(alpha_slider_ax, 'Alpha ', 0.05, 1, valinit=alpha)


def sliders_on_changed(val):
    new_pressure = pressure_calc(diameter_slider.val, viscosity_slider.val, alpha_slider.val)
    pressure.set_ydata(new_pressure)
    ax.relim()
    ax.autoscale_view()

    vessel_l.set_ydata(vessel_calc(alpha_slider.val)[0])
    vessel_h.set_ydata(vessel_calc(alpha_slider.val)[1])

    fig.canvas.draw_idle()

diameter_slider.on_changed(sliders_on_changed)
viscosity_slider.on_changed(sliders_on_changed)
alpha_slider.on_changed(sliders_on_changed)

fig.subplots_adjust(bottom=0.25, hspace=0.6)
plt.show()

