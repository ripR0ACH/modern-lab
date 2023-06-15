import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

data = ["data061323_highbw_lowsens.txt", "data061323_lowbw_highsens.txt"]
calibration_data = ["calibration1.txt", "calibration2.txt"]
wavelength_calibration = "wavelength_calibration.txt"
pixel_calibration = "pixel_calibration.txt"
sens_cal = "sens_calibration.txt"

def fit_func(pix, i, c1, c2, c3):
    return i + c1 * pix + c2 * pix**2 + c3 * pix**3

class Run:
    def __init__(self, title):
        self.title = title
        self.w = [] # array of wavelengths
        self.i = [] # array of intensities
    def __add_wavelength(self, w):
        self.w.append(float(w))
    def __add_intensity(self, i):
        self.i.append(float(i))
    def add_data(self, w, i):
        self.__add_wavelength(w)
        self.__add_intensity(i)
with open(pixel_calibration, "r") as f:
    lines = f.readlines()
    pix = Run(lines[0].replace('\n', ''))
    for line in lines[1:]:
        pix.add_data(*line.split())
with open(wavelength_calibration, "r") as f:
    lines = f.readlines()
    wave = Run(lines[0].replace('\n', ''))
    for line in lines:
        if len(line.split()) != 2:
            continue
        else:
            wave.add_data(line.split()[0], line.split()[1])
with open(sens_cal, "r") as f:
    lines = f.readlines()
    sens_factor = Run("Sensitivity Factor Calibration")
    for line in lines:
        sens_factor.add_data(float(line.split()[0].replace(',', '')), float(line.split()[1]))
popt, pcov = curve_fit(fit_func, pix.w[:len(wave.w)], wave.w)
intercept, c1, c2, c3 = enumerate(popt)
true_vals = [369.67, 408.99, 412.17, 440.06, 550.91, 581.97, 584.20]
expected_vals = [365.015, 404.656, 407.783, 435.833, 546.074, 576.960, 579.066]
vals_diff = []
for i in range(len(expected_vals)-1):
    x = true_vals[i] - expected_vals[i]
    vals_diff.append(x)
err = np.mean(vals_diff)
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
fig, ax = plt.subplots(2, 1)
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
for s in sensors[0]:
    ax[0].plot(s.w, s.i, label = s.title)
for s in sensors[1]:
    ax[1].plot(s.w, s.i, label = s.title)
plt.show()
# plt.show()
