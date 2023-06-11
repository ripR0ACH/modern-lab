import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from decimal import *

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
wavelength_second_peak = Decimal((popt2[1] + np.sqrt(np.log(1) * -1 * (2 * popt2[2] ** 2))) * 10 ** -9)
wavelength_first_peak = Decimal((popt1[1] + np.sqrt(np.log(1) * -1 * (2 * popt1[2] ** 2))) * 10 ** -9)
freq_diff = (1 / wavelength_first_peak) - (1 / wavelength_second_peak)
m_pro = Decimal(1.67262192e-27)
m_e = Decimal(9.1093837e-31)
e_charge = Decimal(1.60217663e-19)
h = Decimal(6.62607015e-34)
e0 = Decimal(8.85418781e-12)
k = (5 * (e_charge ** 4)) / (288 * (h ** 2) * (e0 ** 2))
zeta = (m_pro / (m_pro + m_e)) + (freq_diff / (k * m_e))
m_neu = (zeta * (m_pro + m_e) - m_pro) / (1 - zeta)

print(np.sqrt(pcov1[1][1]) / popt1[1])
print(np.sqrt(Decimal(655.565e-9 ** 2) * Decimal(np.sqrt(pcov1[1][1]) ** 2)))
err_1 = np.sqrt(Decimal(655.565e-9 ** 2) * Decimal(np.sqrt(pcov1[1][1]) ** 2) + wavelength_first_peak * Decimal(0.025e-9 ** 2))
err_2 = np.sqrt(Decimal(655.734e-9 ** 2) * Decimal(np.sqrt(pcov2[1][1]) ** 2) + wavelength_second_peak * Decimal(0.025e-9 ** 2))
print(err_1, err_2)
err_freq_diff = np.sqrt(err_1 ** 2 + err_2 ** 2)
err_zeta = (1 / (k * m_e)) * np.sqrt(err_freq_diff ** 2)
err_m_neu = (err_zeta * (m_pro + m_e) - m_pro) / (1 - err_zeta)
c = Decimal(3 * 10**8)
eVh = Decimal(4.135667516 * 10 ** -15)
e1 = eVh * c / wavelength_first_peak
e2 = eVh * c / wavelength_second_peak
E_diff = (e1 - e2) * Decimal(1.602e-19)
M_neu = ((((m_e * m_pro) / (m_e + m_pro)) - (E_diff / (m_e * c ** 2))) * (m_pro + m_e) - m_pro) / (1 - (((m_e * m_pro) / (m_e + m_pro)) - (E_diff / (Decimal(1.602e-19) * m_e * c ** 2))))
err_M_neu = eVh * err_freq_diff
# print(M_neu)
# print(err_M_neu)
plt.legend()
# plt.show()
# first peak starts at 1565 to 1587 and second peak is 1589 to 1607
