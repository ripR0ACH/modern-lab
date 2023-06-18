import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from decimal import *

data = ["data061523_highbw_lowsens.txt", "data061523_lowbw_highsens.txt"]
calibration_data = ["calibration1.txt", "calibration2.txt"]
wavelength_calibration = "wavelength_calibration.txt"
sens_cal = "sens_calibration.txt"

T_guess = 5777

def blackbody(w, T, c1):
    from scipy.constants import h, k, c
    a = 2 * h * np.power(c, 2)
    b = h * c / (w * k * T)
    return c1 * a / (np.power(w, 5) * np.expm1(b))
class Run:
    def __init__(self, title):
        self.title = title
        self.w = [] # array of wavelengths
        self.i = [] # array of intensities
    def __add_wavelength(self, w):
        self.w.append(float(w) * 1e-9)
    def __add_intensity(self, i):
        self.i.append(float(i))
    def add_data(self, w, i):
        self.__add_wavelength(w)
        self.__add_intensity(i)
with open(sens_cal, "r") as f:
    lines = f.readlines()
    sens_factor = Run("Sensitivity Factor Calibration")
    for line in lines:
        sens_factor.add_data(float(line.split()[0].replace(',', '')), float(line.split()[1]))
true_vals = [369.67, 408.99, 412.17, 440.06, 550.91, 581.97, 584.20]
expected_vals = [365.015, 404.656, 407.783, 435.833, 546.074, 576.960, 579.066]
vals_diff = []
for i in range(len(expected_vals)-1):
    x = true_vals[i] - expected_vals[i]
    vals_diff.append(x)
err = np.mean(vals_diff) * 1e-9
sens_i = 0
sensors = []
for d in data:
    with open(d, "r") as f:
        lines = f.readlines()
        runs = []
        i = -1
        for line in lines:
            if len(line.split()) != 2:
                runs.append(Run(line.replace('\n', '')))
                i += 1
            else:
                runs[i].add_data(*line.split())
    sensors.append(runs)
for sensor in range(len(sensors)):
    for j in range(len(sensors[sensor])):
        for k in range(len(sensors[sensor][j].w)):
            if sensor == 0:
                sensors[sensor][j].w[k] -= err
            if sensors[sensor][j].w[k] <= sens_factor.w[sens_i]:
                sensors[sensor][j].i[k] *= sens_factor.i[sens_i] / 100
            else:
                while sensors[sensor][j].w[k] > sens_factor.w[sens_i]:
                    sens_i += 1
                sensors[sensor][j].i[k] *= sens_factor.i[sens_i] / 100
        sens_i = 0
fig, ax = plt.subplots(2, 1)
for s in sensors[0]:
    ax[0].plot(np.array(s.w) * 1e9, s.i, label = s.title)
for s in sensors[1]:
    ax[1].plot(np.array(s.w) * 1e9, s.i, label = s.title)
T_guess = 0.0029 / sensors[0][0].w[sensors[0][0].i.index(max(sensors[0][0].i))]
popt, pcov = curve_fit(blackbody, sensors[0][0].w, sensors[0][0].i, p0 = [T_guess, 0], maxfev = 5000)
print(popt[0], popt[1])
ax[0].plot(np.linspace(1e-9, 1e-6, 1000) * 1e9, blackbody(np.linspace(1e-9, 1e-6, 1000), popt[0], popt[1]), c="k")
plt.show()