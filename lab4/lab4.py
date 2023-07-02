import numpy as np
import matplotlib.pyplot as plt
files = ["249-259nmFilter", "365-375nmFilter", "431-440nmFilter", "538-548nmFilter"]
ODs = ["point1OD", "point3OD", "point5OD", "point9OD"]
data = ["data/" + i for i in files]

h = 6.6261e-34
c = 2.9979e8
e = 1.6022e-19

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
def linear(x, a, b):
    return a * x + b
def piecewise(x, a, b, c, d, e, transition):
    linear = a * x + b
    exp = c * np.exp(d * (x - transition)) + e
    return np.where(x <= transition, linear, exp)
filters = []
for d in data:
    filters.append(Filter(d))

plt.xlim([-1, 0.5])
plt.ylim([-1e9, 3e9])
end = [650, 650, 598, 620]
guesses = [[1, 1, 1e7, 35, 1.1e7, -2], [1, 1, 1e7, 2, -4e6, -1.2], [1, 1, 9e6, 3, -6e6, -1], [1, 1, 1e6, 2, -5e6, -0.4]]
v_s = np.array([])
waveslengths = np.array([254, 369, 435.5, 543]) * 1e-9
freq = 1 / waveslengths
for f in range(len(filters[:1])):
    f = 1
    from scipy.optimize import curve_fit
    x = filters[f].get_voltages()
    y = filters[f].get_currents()
    popt, pcov = curve_fit(piecewise, x[:end[f]], y[:end[f]], p0=guesses[f], maxfev = 10000)
    print(popt[-1])
    plt.plot(x, piecewise(x, *popt))
    v_s = np.append(v_s, popt[-1])
    plt.plot(x, y, label = filters[f].get_title())
plt.legend()
plt.show()
# plt.plot(freq, v_s)
# popt, pcov = curve_fit(linear, freq, v_s)
# plt.plot(1 / np.linspace(250 * 1e-9, 600 * 1e-9, 1000), linear(1 / np.linspace(250 * 1e-9, 600 * 1e-9, 1000), *popt))
# print(popt)
# plt.show()
