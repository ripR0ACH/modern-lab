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
            avg_counts = np.append(avg_counts, np.mean(c))
        return avg_counts
    def get_avg_counts(self) -> np.array(list()):
        return self.__avg_counts
    def __str__(self) -> str:
        return self.get_name()
def set_elements(d, e = np.array([])) -> np.array([]):
    for i in d:
        e = np.append(e, Element(i))
    return e
def gaussian(x, height, center, stdev) -> float:
    return height * np.exp(-1 * np.power(x - center, 2) / (2 * stdev ** 2))
def plot_elements(e, fit) -> None:
    for i in e:
        fig, ax = plt.subplots(1, 1)
        ax.plot(i.get_energy(), i.get_avg_counts())
        ax.set_xlim([0.55e3, 0.75e3])
        ax.set_ylim([0, 500])
        ax.set_title(i.get_name())
        ax.plot(np.linspace(500, 1000, 1000), gaussian(np.linspace(500, 1000, 1000), *fit), c = "k")
        fig.show()
    plt.show()
    return
def fit_gaussian(x, y) -> tuple[list, list]:
    from scipy.optimize import curve_fit
    return curve_fit(gaussian, x, y, p0=[400, 665, 1])
def main():
    elements = set_elements(data)
    popt, pcov = fit_gaussian(elements[0].get_energy()[30:100], elements[0].get_avg_counts()[30:100])
    print(max(elements[0].get_avg_counts()[30:100]))
    print(popt, "\n", pcov)
    plot_elements(elements[:1], popt)
if __name__ == "__main__":
    main()
# 2nd derivative to find concavity
