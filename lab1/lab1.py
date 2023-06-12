import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from decimal import *

data = pd.read_csv("data060523.csv")
df = data.iloc[:, 30:]
df = df.drop(df.columns[[2, 5]], axis = 1)
m_pro = Decimal(1.67262192e-27)
m_e = Decimal(9.1093837e-31)
e_charge = Decimal(1.60217663e-19)
h = Decimal(6.62607015e-34)
e0 = Decimal(8.85418781e-12)
def fit_func(x, a, b, c):
	return a * np.exp(-1 * (((x - b) ** 2) / (2 * c ** 2)))

x = np.linspace(655, 656, 100)
wavelength_first_peak = []
wavelength_second_peak = []
err_1 = []
err_2 = []
for trial in range(3):
	fig, ax = plt.subplots(1, 1)
	peaks = [pd.to_numeric(df.iloc[1550:1630, (trial * 2)]), pd.to_numeric(df.iloc[1550:1630, (trial * 2) + 1]).abs()]
	ax.plot(peaks[0], peaks[1], 'o', label = "data - run " + str(trial + 1))

	x_first_peak = list(pd.to_numeric(df.iloc[1560:1585, (trial * 2)]))
	y_first_peak = list(pd.to_numeric(df.iloc[1560:1585, (trial * 2) + 1]).abs())
	popt1, pcov1 = curve_fit(fit_func, x_first_peak, y_first_peak, p0=[max(y_first_peak), x_first_peak[y_first_peak.index(max(y_first_peak))], 1], maxfev=5000)
	ax.plot(x, fit_func(x, popt1[0], popt1[1], popt1[2]), '-', label = "1st peak fit - run " + str(trial + 1))

	x_second_peak = list(pd.to_numeric(df.iloc[1589:1620, (trial * 2)]))
	y_second_peak = list(pd.to_numeric(df.iloc[1589:1620, (trial * 2) + 1]).abs())
	popt2, pcov2 = curve_fit(fit_func, x_second_peak, y_second_peak, p0 = [max(y_second_peak), x_first_peak[y_second_peak.index(max(y_second_peak))], 1], maxfev = 5000)
	ax.plot(x, fit_func(x, popt2[0], popt2[1], popt2[2]), '-', label = "2nd peak fit - run " + str(trial + 1))
	ax.set_xlabel("wavelength (nm)")
	ax.set_ylabel("intensity (W / m^2)")
	ax.set_title("Wavelength vs Intensity Plot for run #" + str(trial + 1))
	fig.legend()
	fig.savefig('data_run' + str(trial + 1) + '.jpg')

	wavelength_first_peak.append(Decimal((popt1[1] + np.sqrt(np.log(1) * -1 * (2 * popt1[2] ** 2))) * 10 ** -9))
	wavelength_second_peak.append(Decimal((popt2[1] + np.sqrt(np.log(1) * -1 * (2 * popt2[2] ** 2))) * 10 ** -9))
	# error calculations
	err_1.append(np.sqrt(Decimal((pcov1[1][1] * 1e-9) ** 2) + Decimal(0.025e-9 ** 2)))
	err_2.append(np.sqrt(Decimal((pcov2[1][1] * 1e-9) ** 2) + Decimal(0.025e-9 ** 2)))
	# print(np.round(float(wavelength_first_peak[trial]) * 1e9, 4), "+/-", np.round(float(err_1[trial]) * 1e9, 4))
	# print(np.round(float(wavelength_second_peak[trial]) * 1e9, 4), "+/-", np.round(float(err_2[trial]) * 1e9, 4))]
freq_diff = (1 / np.mean(wavelength_first_peak)) - (1 / np.mean(wavelength_second_peak))
k = (5 * (e_charge ** 4)) / (288 * (h ** 2) * (e0 ** 2))
zeta = (m_pro / (m_pro + m_e)) + (freq_diff / (k * m_e))
m_neu = (- zeta * (m_pro + m_e) - m_pro) / (1 - zeta)
# print(m_neu)
mfp = np.mean(wavelength_first_peak)
msp = np.mean(wavelength_second_peak)
u_h = (-m_e * (mfp - (2 * msp)) / (msp ** 2)) / ((m_e / m_pro) - (msp - mfp) / msp) ** 2
u_d = -m_e / (msp * ((m_e / m_pro) - ((msp - mfp) / msp)) ** 2)
print(m_neu)
print(np.sqrt(float(m_neu) * ((float(u_h) ** 2) * ((0.025 / np.sqrt(3)) ** 2) + (float(u_d) ** 2) * ((0.025 / np.sqrt(3)) ** 2))))
# plt.legend()
# plt.show()
