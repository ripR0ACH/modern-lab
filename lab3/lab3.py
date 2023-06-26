import numpy as np
import matplotlib.pyplot as plt
element_files = ["Cd109.Txt", "Co57.Txt", "Co60.Txt", "Cs137.Txt", "K40.Txt","Mn54.Txt", "Na22.Txt", "Zn65.Txt"]
data = ["data/" + i for i in element_files]

E_CONST = 1.972973

class Element():
    def __init__(self, file) -> None:
        self.__name = self.__set_name(file)
        self.__e = self.__set_energy(file) # energy array in keV
        self.__counts = self.__set_counts(file) # array of counts (usually 5 columns)
        self.__avg_counts = self.__set_avg_counts(self.get_counts()) # average of the columns in the counts
        self.fits = np.array([])
        self.peaks = np.array([])
        self.err_peaks = np.array([])
        self.edges = np.array([])
        self.err_edges = np.array([])
    def __set_name(self, file) -> str:
        with open(file, "r") as f:
            lines = f.readlines()
            for l in range(len(lines)):
                if lines[l] == "Sample description:\n":
                    n = lines[l + 1]
                    break
        return n.strip()
    def get_name(self) -> str:
        return self.__name
    def __set_energy(self, file) -> np.array(list()):
        e = np.array([])
        with open(file, "r") as f:
            lines = f.readlines()
        d_start = 0
        for l in range(len(lines)):
            if lines[l] == "SPECTRUM\n":
                d_start = l + 1
                break
        for l in lines[d_start:]:
            e = np.append(e, float(l.split()[0][:-1]) * E_CONST)
        return e
    def get_energy(self) -> np.array(list()):
        return self.__e
    def __set_counts(self, file) -> np.array(list()):
        with open(file, "r") as f:
            lines = f.readlines()
            for l in range(len(lines)):
                if lines[l] == "SPECTRUM\n":
                    d_start = l + 1
                    break
            col_counts = []
            for l in lines[d_start:]:
                l = l.split()[1:]
                line_len = len(l)
                col_val = []
                for i in range(line_len):
                    col_val.append(int(l[i]))
                col_counts.append(col_val)
        return col_counts
    def get_counts(self) -> np.array(list()):
        return self.__counts               
    def __set_avg_counts(self, counts) -> np.array(list()):
        avg_counts = np.array([])
        for c in counts:
            avg_counts = np.append(avg_counts, np.sum(c))
        return avg_counts
    def get_avg_counts(self) -> np.array(list()):
        return self.__avg_counts
    def __str__(self) -> str:
        return self.get_name()
def set_elements(d, e = np.array([])) -> np.array([]):
    for i in d:
        e = np.append(e, Element(i))
    return e
def plot_elements(e) -> None:
    for i in e:
        fits = i.fits
        fig, ax = plt.subplots(1, 1)
        ax.plot(i.get_energy(), i.get_avg_counts())
        # ax.set_xlim([0e3, 0.2e3])
        # ax.set_ylim([0, 500])
        ax.set_title(i.get_name())
        for fit in fits:
            if fit.type == "gaussian":
                ax.plot(np.linspace(min(fit.x), max(fit.x), 100), gaussian(np.linspace(min(fit.x), max(fit.x), 100), *fit.popt), c = "k")
            else:
                ax.plot(np.linspace(min(fit.x), max(fit.x), 100), logistic(np.linspace(min(fit.x), max(fit.x), 100), *fit.popt), c = "k")
        fig.show()
    plt.show()
    return None
def gaussian(x, height, center, stdev) -> float:
    return height * np.exp(-1 * np.power(x - center, 2) / (2 * stdev ** 2))
def logistic(x, max, growth, x0, c):
    return  -max / (1 + np.exp(-growth * (x - x0))) + c
class Fit():
        def __init__(self, x = np.array([]), y = np.array([]), guess = [], kind = ""):
            self.x = x
            self.y = y
            self.guess = guess
            if kind == "g":
                self.type = "gaussian"
                self.popt, self.pcov = self.fit_gaussian()
            else:
                self.type = "logistic"
                self.popt, self.pcov = self.fit_logistic()
        def fit_gaussian(self) -> tuple[list, list]:
            from scipy.optimize import curve_fit
            if len(self.guess) != 0:
                return curve_fit(gaussian, self.x, self.y, p0=self.guess, maxfev = 5000)
            return curve_fit(gaussian, self.x, self.y, maxfev = 5000)
        def fit_logistic(self) -> tuple[list, list]:
            from scipy.optimize import curve_fit
            if len(self.guess) != 0:
                return curve_fit(logistic, self.x, self.y, p0=self.guess, maxfev = 100000)
            return curve_fit(logistic, self.x, self.y, maxfev = 100000)
def get_fits(elements) -> None:
    elements[0].fits = np.append(elements[0].fits, Fit(elements[0].get_energy()[58:100], elements[0].get_avg_counts()[58:100], [430, 662, 1], "g"))
    elements[0].fits = np.append(elements[0].fits, Fit(elements[0].get_energy()[24:58], elements[0].get_avg_counts()[24:58], [100, 0, 480, 100]))
    elements[1].fits = np.append(elements[1].fits, Fit(elements[1].get_energy()[53:81], elements[1].get_avg_counts()[53:81], [612, 643, 1], "g")) # 101 start 121 end
    elements[1].fits = np.append(elements[1].fits, Fit(elements[1].get_energy()[17:53], elements[1].get_avg_counts()[17:53], [156, 0, 307, 1]))
    elements[2].fits = np.append(elements[2].fits, Fit(elements[2].get_energy()[103:124], elements[2].get_avg_counts()[103:124], [12000, 1132, 1], "g")) # 101 start 121 end
    elements[2].fits = np.append(elements[2].fits, Fit(elements[2].get_energy()[85:103], elements[2].get_avg_counts()[85:103], [1000, 0, 900, 1]))
    elements[3].fits = np.append(elements[3].fits, Fit(elements[3].get_energy()[57:103], elements[3].get_avg_counts()[57:103], [1100, 650, 1], "g"))
    elements[3].fits = np.append(elements[3].fits, Fit(elements[3].get_energy()[36:57], elements[3].get_avg_counts()[36:57], [125, 0, 500, 100]))
    elements[4].fits = np.append(elements[4].fits, Fit(elements[4].get_energy()[57:76], elements[4].get_avg_counts()[57:76], [35000, 700, 1], "g"))
    elements[4].fits = np.append(elements[4].fits, Fit(elements[4].get_energy()[42:57], elements[4].get_avg_counts()[42:57], [30000, 0, 400, 20000]))
    elements[4].fits = np.append(elements[4].fits, Fit(elements[4].get_energy()[132:155], elements[4].get_avg_counts()[132:155], [3100, 1400, 100], "g"))
    elements[4].fits = np.append(elements[4].fits, Fit(elements[4].get_energy()[84:132], elements[4].get_avg_counts()[84:132], [1200, 0, 1100, 1260]))
    elements[5].fits = np.append(elements[5].fits, Fit(elements[5].get_energy()[74:93], elements[5].get_avg_counts()[74:93], [464, 815, 1], "g")) # 101 start 121 end
    elements[5].fits = np.append(elements[5].fits, Fit(elements[5].get_energy()[13:55], elements[5].get_avg_counts()[13:55], [300, 0, 334, 1]))
    elements[6].fits = np.append(elements[6].fits, Fit(elements[6].get_energy()[40:65], elements[6].get_avg_counts()[40:65], [48200, 511, 1], "g")) # 101 start 121 end
    elements[6].fits = np.append(elements[6].fits, Fit(elements[6].get_energy()[25:40], elements[6].get_avg_counts()[25:40], [7070, 0, 246, 1]))
    elements[6].fits = np.append(elements[6].fits, Fit(elements[6].get_energy()[110:140], elements[6].get_avg_counts()[110:140], [5590, 1224, 2], "g")) # 101 start 121 end
    elements[6].fits = np.append(elements[6].fits, Fit(elements[6].get_energy()[96:110], elements[6].get_avg_counts()[96:110], [1050, 0, 1000, 1]))
    elements[7].fits = np.append(elements[7].fits, Fit(elements[7].get_energy()[60:80], elements[7].get_avg_counts()[60:80], [2000, 660, 100], "g"))
    elements[7].fits = np.append(elements[7].fits, Fit(elements[7].get_energy()[22:60], elements[7].get_avg_counts()[22:60], [400, 0, 300, 1]))
    return None
def compton(elements) -> np.array([]):
    for e in elements:
        for fit in range(len(e.fits)):
            if fit % 2 == 0:
                e.peaks = np.append(e.peaks, e.fits[fit].popt[1])
                e.err_peaks = np.append(e.err_peaks, np.sqrt(e.fits[fit].pcov[1][1]))
            else:
                e.edges = np.append(e.edges, e.fits[fit].popt[2])
                e.err_edges = np.append(e.err_edges, np.sqrt(e.fits[fit].pcov[2][2]))
def main():
    elements = set_elements(data)
    get_fits(elements)
    compton(elements)
    for e in elements:
        print(e.get_name())
        print(e.peaks, "+/-", str(e.err_peaks) + "\n" + str(e.edges), "+/-", str(e.err_edges) + "\n")
    # plot_elements(elements)
if __name__ == "__main__":
    main()
