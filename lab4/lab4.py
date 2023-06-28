import numpy as np
import matplotlib.pyplot as plt
files = ["249-259nmFilter", "365-375nmFilter", "431-440nmFilter", "538-548nmFilter"]
ODs = ["point1OD", "point3OD", "point5OD", "point9OD"]
data = ["data/" + i for i in files]

class Filter():
    def __init__(self, data):
        self.__v = np.array([])
        self.__c = np.array([])
        self.__title = ""
        self.__set_data(data)
    def __set_data(self, data) -> None:
        self.__set_title(data)
        with open(data, "r") as f:
            lines = f.readlines()[1:]
        for l in lines:
            l = l.split()
            self.__add_voltage(l[0])
            self.__add_current(l[1])
        return None
    def __add_voltage(self, volt) -> None:
        self.__v = np.append(self.__v, float(volt))
        return None
    def __add_current(self, current):
        self.__c = np.append(self.__c, float(current) * 1e3)
        return None
    def __set_title(self, data) -> None:
        self.__title = data[5:]
        return None
    def get_title(self) -> str:
        return self.__title
    def get_voltages(self) -> np.array([]):
        return self.__v
    def get_currents(self) -> np.array([]):
        return self.__c
    def __str__(self):
        return self.get_title()
def logistic(x, max, growth, x0, c):
    return max / (1 + np.exp(-growth * (x - x0))) + c
def linear(x, a, b):
    return a * x + b
def e(x, a, b, c, d):
    return a * np.exp(b * (x - c)) + d
def e1(x, a, b):
    return a * np.exp(b * x)
filters = []
for d in data:
    filters.append(Filter(d))

plt.xlim([-3, 5])
plt.ylim([0, 5.5e9])
guesses = [[1e7, 35, -5e-1, 1.1e7], [6e6, 10, -5e-1, 6e6]]
# for f in range(len(filters[1:2])):
f = 0
from scipy.optimize import curve_fit
popt, pcov = curve_fit(linear, filters[f].get_voltages()[:400], filters[f].get_currents()[:400], p0 = [0, 0])
x = filters[f].get_voltages()
y = filters[f].get_currents()
y_linear = linear(x, *popt)
popt, pcov = curve_fit(e, filters[f].get_voltages()[400:550], filters[f].get_currents()[400:550], p0 = guesses[f], maxfev = 5000)
y_e = e(filters[f].get_voltages(), *popt)
i = np.abs(y_linear - y_e).argmin()
print(x[i])
plt.plot(x, y_linear, label = str(filters[f].get_title() + " linear fit"))
plt.plot(x, y_e, label = str(filters[f].get_title() + " e fit"))
plt.plot(x, y, label = filters[f].get_title())
plt.legend()
plt.show()
