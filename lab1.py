import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

data = pd.read_csv("data060523.csv")
df = data.iloc[:, 30:]
df = df.drop(df.columns[[2, 5]], axis = 1)
def fit_func(x, a, b, c):
	return a * np.exp(-1 * (((x - b) ** 2) / (2 * c ** 2)))
fig, ax = plt.subplots(1, 1)

x = np.linspace(655, 656, 100)

peaks = [pd.to_numeric(df.iloc[1550:1630, 0]), pd.to_numeric(df.iloc[1550:1630, 1]).abs()]
x_first_peak = pd.to_numeric(df.iloc[1560:1585, 0].to_numpy())
y_first_peak = pd.to_numeric(df.iloc[1560:1585, 1]).abs()
popt1, pcov1 = curve_fit(fit_func, x_first_peak, y_first_peak, p0 = [7000, 655, 1], maxfev = 5000)
ax.plot(peaks[0], peaks[1], 'o', label = "data")
ax.plot(x, fit_func(x, popt1[0], popt1[1], popt1[2]), '-', label = "fit 1st")
x_second_peak = pd.to_numeric(df.iloc[1589:1620, 0])
y_second_peak = pd.to_numeric(df.iloc[1589:1620, 1])
popt2, pcov2 = curve_fit(fit_func, x_second_peak, y_second_peak, p0 = [9000, 655, 1], maxfev = 5000)
ax.plot(x, fit_func(x, popt2[0], popt2[1], popt2[2]), '-', label = "fit 2nd")
plt.legend()
print(popt2[1] + np.sqrt(np.log(1) * -1 * (2 * popt2[2] ** 2)))
print(popt1[1] + np.sqrt(np.log(1) * -1 * (2 * popt1[2] ** 2)))   
plt.show()

# first peak starts at 1565 to 1587 and second peak is 1589 to 1607
